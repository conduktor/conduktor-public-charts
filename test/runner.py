"""
Conduktor Helm Charts test runner CLI.

Usage:
    python -m test.runner run --chart console
    python -m test.runner run --changed
    python -m test.runner install --chart console --scenario 01-basic
    python -m test.runner uninstall --chart console --scenario 01-basic
    python -m test.runner detect-changed --json
    python -m test.runner lint-manifests
"""

import json
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional

import click

from test.config import get_ci_values_file, get_old_values_content, get_scenarios, load_chart_config
from test.dependencies import DependencyManager, setup_helm_repos
from test.helm import get_chart_name, get_released_version, helm_dependency_build, helm_install, helm_test, helm_uninstall, helm_upgrade
from test.kubernetes import create_namespace, delete_namespace, delete_namespace_async, get_current_context, print_debug_info
from test.models import ScenarioResult
from test.utils import BOLD, RESET, BLUE, CHARTS_DIR, ROOT_DIR, _print, get_charts, gh_group_end, gh_group_start, log_error, log_info, log_step, log_success, log_warning, print_summary


def detect_changed_charts() -> list[str]:
    """Detect charts changed vs main branch."""
    import subprocess

    result = subprocess.run(
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        capture_output=True, text=True, cwd=ROOT_DIR,
    )

    if result.returncode != 0:
        result = subprocess.run(
            ["git", "diff", "--name-only", "main...HEAD"],
            capture_output=True, text=True, cwd=ROOT_DIR,
        )

    charts = set()
    for f in (result.stdout.strip().split("\n") if result.stdout else []):
        if f.startswith("charts/"):
            parts = f.split("/")
            if len(parts) >= 2 and (CHARTS_DIR / parts[1] / "Chart.yaml").exists():
                charts.add(parts[1])

    return sorted(charts)


def run_scenario(
    chart: str,
    scenario: str,
    scenario_id: str,
    namespace: str,
    dep_manager: Optional[DependencyManager] = None,
    upgrade: bool = True,
    verbose: bool = False,
) -> ScenarioResult:
    """Run a single test scenario.

    Args:
        chart: Chart name
        scenario: Scenario name
        scenario_id: Scenario identifier (e.g., s01, s02)
        namespace: Namespace for the test (chart release)
        dep_manager: Optional dependency manager for resource initialization
        upgrade: Whether to run upgrade test path
        verbose: Enable verbose output
    """
    start = time.time()
    release = f"{chart}-test"
    chart_path = str(CHARTS_DIR / chart)
    chart_name = get_chart_name(CHARTS_DIR / chart)

    _print(f"\n{BOLD}{BLUE}>>> {chart}/{scenario}{RESET}")
    gh_group_start(f"{chart}/{scenario}")

    try:
        # Setup
        log_step("1", "Create namespace")
        create_namespace(namespace, verbose)

        # Initialize isolation resources (database, bucket) for this scenario
        if dep_manager:
            log_step("2", "Initialize isolation resources")
            dep_manager.init_scenario_resources(scenario_id)

        log_step("3", "Build chart dependencies")
        helm_dependency_build(chart, verbose)

        ci_values = get_ci_values_file(chart, scenario)
        if not ci_values.exists():
            raise FileNotFoundError(f"CI values file not found: {ci_values}")

        if upgrade:
            old_version = get_released_version(chart_name, verbose)
            old_values = get_old_values_content(chart, scenario, "main")

            if old_version and old_values:
                with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
                    f.write(old_values)
                    old_values_path = Path(f.name)

                try:
                    # Install old version
                    log_step("5", f"Install old version ({old_version})")
                    helm_install(release, f"conduktor/{chart_name}", namespace, values_files=[old_values_path], version=old_version, verbose=verbose)

                    log_step("5a", "Test old version")
                    helm_test(release, namespace, verbose=verbose)

                    # Upgrade with old values
                    log_step("6", "Upgrade to current (old values)")
                    helm_upgrade(release, chart_path, namespace, values_files=[old_values_path], verbose=verbose)

                    log_step("6a", "Test upgrade")
                    helm_test(release, namespace, verbose=verbose)

                    # Upgrade with current values
                    log_step("7", "Upgrade with current values")
                    helm_upgrade(release, chart_path, namespace, values_files=[ci_values], verbose=verbose)
                finally:
                    old_values_path.unlink(missing_ok=True)
            else:
                log_info("No old version found, fresh install")
                log_step("5", "Install current version")
                helm_install(release, chart_path, namespace, values_files=[ci_values], verbose=verbose)
        else:
            log_step("5", "Install current version")
            helm_install(release, chart_path, namespace, values_files=[ci_values], verbose=verbose)

        log_step("8", "Run helm test")
        helm_test(release, namespace, verbose=verbose)

        log_success(f"PASSED: {chart}/{scenario}")
        return ScenarioResult(chart=chart, scenario=scenario, success=True, duration=time.time() - start)

    except Exception as e:
        log_error(f"FAILED: {chart}/{scenario} - {e}")
        print_debug_info(namespace)
        return ScenarioResult(chart=chart, scenario=scenario, success=False, duration=time.time() - start, error=str(e))

    finally:
        try:
            helm_uninstall(release, namespace, verbose)
        except Exception:
            pass
        try:
            # Use async deletion - don't wait for namespace to fully delete
            delete_namespace_async(namespace, verbose)
        except Exception:
            pass
        gh_group_end()


def run_chart(chart: str, scenarios: Optional[list[str]] = None, upgrade: bool = True, verbose: bool = False) -> list[ScenarioResult]:
    """Run all scenarios for a chart.

    This function orchestrates shared dependencies across scenarios:
    1. Creates a shared deps namespace
    2. Installs all dependencies once
    3. Runs each scenario (isolation via convention-based resource naming)
    4. Tears down dependencies after all scenarios
    """
    _print(f"\n{BOLD}{BLUE}========== TESTING: {chart.upper()} =========={RESET}")

    scenario_list = scenarios or get_scenarios(chart)
    if not scenario_list:
        log_info(f"No scenarios found for {chart}")
        return []

    # Load chart config for dependencies
    config = load_chart_config(chart)
    deps_namespace = f"ct-{chart}-deps"

    # Setup shared dependencies
    dep_manager = None
    has_deps = len(config.get_all_dependencies()) > 0

    if has_deps:
        log_info(f"Setting up shared dependencies in {deps_namespace}")
        create_namespace(deps_namespace, verbose)
        dep_manager = DependencyManager(chart, deps_namespace, verbose)
        dep_manager.setup_all()

    try:
        results = []
        for i, scenario in enumerate(scenario_list):
            namespace = f"ct-{chart}-{scenario.replace('_', '-')}"
            scenario_id = f"{i+1:02d}"  # 01, 02, 03...

            result = run_scenario(
                chart, scenario, scenario_id, namespace,
                dep_manager=dep_manager,
                upgrade=upgrade,
                verbose=verbose
            )
            results.append(result)

        return results

    finally:
        # Teardown shared dependencies
        if dep_manager:
            try:
                log_info("Tearing down shared dependencies")
                dep_manager.teardown()
            except Exception as e:
                log_warning(f"Failed to teardown dependencies: {e}")
            try:
                delete_namespace(deps_namespace, verbose)
            except Exception:
                pass


def install_scenario(chart: str, scenario: str, verbose: bool = False) -> None:
    """Install a scenario for local development/debugging.

    This installs dependencies and the chart but does NOT cleanup afterward.
    Use uninstall_scenario to cleanup when done.
    """
    config = load_chart_config(chart)
    scenarios = get_scenarios(chart)

    # Find scenario index for isolation ID
    scenario_id = "01"
    for i, s in enumerate(scenarios):
        if s == scenario:
            scenario_id = f"{i+1:02d}"
            break

    deps_namespace = f"ct-{chart}-deps"
    namespace = f"ct-{chart}-{scenario.replace('_', '-')}"
    release = f"{chart}-test"
    chart_path = str(CHARTS_DIR / chart)

    _print(f"\n{BOLD}{BLUE}========== INSTALLING: {chart}/{scenario} =========={RESET}")

    # Setup dependencies
    dep_manager = None
    has_deps = len(config.get_all_dependencies()) > 0

    if has_deps:
        log_info(f"Setting up dependencies in {deps_namespace}")
        create_namespace(deps_namespace, verbose)
        dep_manager = DependencyManager(chart, deps_namespace, verbose)
        dep_manager.setup_all()

        # Initialize isolation resources
        log_step("1", "Initialize isolation resources")
        dep_manager.init_scenario_resources(scenario_id)

    # Create namespace and install chart
    log_step("2", "Create namespace")
    create_namespace(namespace, verbose)

    log_step("3", "Build chart dependencies")
    helm_dependency_build(chart, verbose)

    ci_values = get_ci_values_file(chart, scenario)
    if not ci_values.exists():
        raise FileNotFoundError(f"CI values file not found: {ci_values}")

    log_step("4", "Install chart")
    helm_install(release, chart_path, namespace, values_files=[ci_values], verbose=verbose)

    log_success(f"Installed {chart}/{scenario}")
    _print(f"\n{BOLD}Namespaces:{RESET}")
    _print(f"  Chart:        {namespace}")
    if has_deps:
        _print(f"  Dependencies: {deps_namespace}")
    _print(f"\n{BOLD}To access:{RESET}")
    _print(f"  kubectl get pods -n {namespace}")
    _print(f"  kubectl logs -n {namespace} -l app.kubernetes.io/name={chart} -f")
    _print(f"\n{BOLD}To cleanup:{RESET}")
    _print(f"  make test-uninstall CHART={chart} SCENARIO={scenario}")


def uninstall_scenario(chart: str, scenario: str, verbose: bool = False) -> None:
    """Uninstall a scenario and its dependencies."""
    deps_namespace = f"ct-{chart}-deps"
    namespace = f"ct-{chart}-{scenario.replace('_', '-')}"
    release = f"{chart}-test"

    _print(f"\n{BOLD}{BLUE}========== UNINSTALLING: {chart}/{scenario} =========={RESET}")

    # Uninstall chart
    try:
        log_step("1", "Uninstall chart")
        helm_uninstall(release, namespace, verbose)
    except Exception as e:
        log_warning(f"Failed to uninstall chart: {e}")

    # Delete chart namespace
    try:
        log_step("2", "Delete chart namespace")
        delete_namespace(namespace, verbose)
    except Exception as e:
        log_warning(f"Failed to delete namespace {namespace}: {e}")

    # Uninstall dependencies
    config = load_chart_config(chart)
    if config.get_all_dependencies():
        try:
            log_step("3", "Uninstall dependencies")
            dep_manager = DependencyManager(chart, deps_namespace, verbose)
            # Mark all deps as installed so teardown will uninstall them
            dep_manager.installed = [d.name for d in config.get_all_dependencies()]
            dep_manager.teardown()
        except Exception as e:
            log_warning(f"Failed to uninstall dependencies: {e}")

        try:
            log_step("4", "Delete dependencies namespace")
            delete_namespace(deps_namespace, verbose)
        except Exception as e:
            log_warning(f"Failed to delete namespace {deps_namespace}: {e}")

    log_success(f"Uninstalled {chart}/{scenario}")


# CLI
@click.group()
def cli():
    """Conduktor Helm Charts test runner."""
    pass


@cli.command()
@click.option("--chart", "-c", help="Chart to test")
@click.option("--scenario", "-s", help="Specific scenario")
@click.option("--changed", is_flag=True, help="Test changed charts only")
@click.option("--all", "test_all", is_flag=True, help="Test all charts")
@click.option("--skip-upgrade", is_flag=True, help="Skip upgrade tests")
@click.option("--verbose", "-v", is_flag=True)
def run(chart: Optional[str], scenario: Optional[str], changed: bool, test_all: bool, skip_upgrade: bool, verbose: bool):
    """Run chart tests."""
    ctx = get_current_context()
    if not ctx or "k3d" not in ctx:
        log_error(f"Not a k3d context: {ctx}")
        sys.exit(1)

    setup_helm_repos(verbose)

    if chart:
        charts = [chart]
    elif changed:
        charts = detect_changed_charts()
        if not charts:
            log_info("No charts changed")
            sys.exit(0)
    elif test_all:
        charts = get_charts()
    else:
        log_error("Specify --chart, --changed, or --all")
        sys.exit(1)

    all_results = []
    for c in charts:
        results = run_chart(c, [scenario] if scenario else None, not skip_upgrade, verbose)
        all_results.extend(results)

    print_summary([(r.chart, r.scenario, r.success, r.error) for r in all_results])
    sys.exit(0 if all(r.success for r in all_results) else 1)


@cli.command()
@click.option("--chart", "-c", required=True, help="Chart to install")
@click.option("--scenario", "-s", required=True, help="Scenario to install")
@click.option("--verbose", "-v", is_flag=True)
def install(chart: str, scenario: str, verbose: bool):
    """Install a scenario for local dev/debug (no cleanup)."""
    ctx = get_current_context()
    if not ctx or "k3d" not in ctx:
        log_error(f"Not a k3d context: {ctx}")
        sys.exit(1)

    setup_helm_repos(verbose)

    try:
        install_scenario(chart, scenario, verbose)
    except Exception as e:
        log_error(f"Install failed: {e}")
        sys.exit(1)


@cli.command()
@click.option("--chart", "-c", required=True, help="Chart to uninstall")
@click.option("--scenario", "-s", required=True, help="Scenario to uninstall")
@click.option("--verbose", "-v", is_flag=True)
def uninstall(chart: str, scenario: str, verbose: bool):
    """Uninstall a scenario and its dependencies."""
    ctx = get_current_context()
    if not ctx or "k3d" not in ctx:
        log_error(f"Not a k3d context: {ctx}")
        sys.exit(1)

    try:
        uninstall_scenario(chart, scenario, verbose)
    except Exception as e:
        log_error(f"Uninstall failed: {e}")
        sys.exit(1)


@cli.command("detect-changed")
@click.option("--json", "as_json", is_flag=True)
def detect_changed(as_json: bool):
    """Detect changed charts."""
    charts = detect_changed_charts()
    if as_json:
        click.echo(json.dumps(charts))
    else:
        for c in charts:
            click.echo(c)


@cli.command("lint-manifests")
@click.option("--chart", "-c")
@click.option("--verbose", "-v", is_flag=True)
def lint_manifests(chart: Optional[str], verbose: bool):
    """Lint chart manifests."""
    from test.lint import lint_chart

    charts = [chart] if chart else get_charts()
    ok = all(lint_chart(c, verbose) for c in charts)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    cli()
