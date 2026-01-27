"""
Conduktor Helm Charts test runner CLI.

Usage:
    python -m test.runner run --chart console
    python -m test.runner run --changed
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

from test.config import get_ci_values_file, get_old_values_content, get_scenarios
from test.dependencies import DependencyManager, setup_helm_repos
from test.helm import get_released_version, helm_dependency_build, helm_install, helm_test, helm_uninstall, helm_upgrade
from test.kubernetes import create_namespace, delete_namespace, get_current_context, print_debug_info
from test.models import ScenarioResult
from test.utils import BOLD, RESET, BLUE, CHARTS_DIR, ROOT_DIR, _print, get_charts, gh_group_end, gh_group_start, log_error, log_info, log_step, log_success, print_summary


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
    namespace: str,
    upgrade: bool = True,
    verbose: bool = False,
) -> ScenarioResult:
    """Run a single test scenario."""
    start = time.time()
    release = f"{chart}-test"
    chart_path = str(CHARTS_DIR / chart)

    # Dependencies in same namespace as the test
    dep_manager = DependencyManager(chart, namespace, verbose)

    _print(f"\n{BOLD}{BLUE}>>> {chart}/{scenario}{RESET}")
    gh_group_start(f"{chart}/{scenario}")

    try:
        # Setup
        log_step("1", "Create namespace")
        create_namespace(namespace, verbose)

        log_step("2", "Setup dependencies")
        dep_manager.setup(scenario)

        log_step("3", "Build chart dependencies")
        helm_dependency_build(chart, verbose)

        ci_values = get_ci_values_file(chart, scenario)
        if not ci_values.exists():
            raise FileNotFoundError(f"CI values file not found: {ci_values}")

        if upgrade:
            old_version = get_released_version(chart)
            old_values = get_old_values_content(chart, scenario)

            if old_version and old_values:

                with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
                    f.write(old_values)
                    old_values_path = Path(f.name)

                # Install old version
                log_step("4", f"Install old version ({old_version})")
                helm_install(release, f"conduktor/{chart}", namespace, values_files=[old_values_path], version=old_version, verbose=verbose)

                log_step("4a", "Test old version")
                helm_test(release, namespace, verbose=verbose)

                # Upgrade with old values
                log_step("5", "Upgrade to current (old values)")

                try:
                    helm_upgrade(release, chart_path, namespace, values_files=[old_values_path], verbose=verbose)
                    log_step("5a", "Test upgrade")
                    helm_test(release, namespace, verbose=verbose)
                finally:
                    old_values_path.unlink(missing_ok=True)

                # Upgrade with current values
                log_step("6", "Upgrade with current values")
                helm_upgrade(release, chart_path, namespace, values_files=[ci_values], verbose=verbose)
            else:
                log_info("No old version found, fresh install")
                log_step("4", "Install current version")
                helm_install(release, chart_path, namespace, values_files=[ci_values], verbose=verbose)
        else:
            log_step("4", "Install current version")
            helm_install(release, chart_path, namespace, values_files=[ci_values], verbose=verbose)

        log_step("7", "Run helm test")
        helm_test(release, namespace, verbose=verbose)

        log_success(f"PASSED: {chart}/{scenario}")
        return ScenarioResult(chart=chart, scenario=scenario, success=True, duration=time.time() - start)

    except Exception as e:
        log_error(f"FAILED: {chart}/{scenario} - {e}")
        print_debug_info(namespace)
        return ScenarioResult(chart=chart, scenario=scenario, success=False, duration=time.time() - start, error=str(e))

    finally:
        try:
            dep_manager.teardown()
        except Exception:
            pass
        try:
            helm_uninstall(release, namespace, verbose)
        except Exception:
            pass
        try:
            delete_namespace(namespace, verbose)
        except Exception:
            pass
        gh_group_end()


def run_chart(chart: str, scenarios: Optional[list[str]] = None, upgrade: bool = True, verbose: bool = False) -> list[ScenarioResult]:
    """Run all scenarios for a chart."""
    _print(f"\n{BOLD}{BLUE}========== TESTING: {chart.upper()} =========={RESET}")

    scenario_list = scenarios or get_scenarios(chart)
    if not scenario_list:
        log_info(f"No scenarios found for {chart}")
        return []

    results = []
    for scenario in scenario_list:
        namespace = f"ct-{chart}-{scenario.replace('_', '-')}"
        result = run_scenario(chart, scenario, namespace, upgrade, verbose)
        results.append(result)

    return results


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
