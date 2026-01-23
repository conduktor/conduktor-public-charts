"""
Main CLI entry point for the Conduktor Helm Charts test runner.

Usage:
    python -m test.runner run --chart console
    python -m test.runner run --chart console --scenario 01-basic
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

from test.config import (
    get_ci_values_file,
    get_old_ci_values,
    get_scenario_config,
    load_chart_dependencies,
)
from test.dependencies import DependencyManager, setup_helm_repos
from test.helm import (
    get_chart_path,
    get_current_chart_version,
    get_released_chart_version,
    helm_dependency_build,
    helm_install,
    helm_test,
    helm_uninstall,
    helm_upgrade,
)
from test.kubernetes import (
    check_current_context,
    create_namespace,
    delete_namespace,
    get_current_context,
    get_events,
    get_pod_logs,
    get_pods,
)
from test.models import ChartTestResult, ScenarioResult, TestContext
from test.utils import (
    CHARTS_DIR,
    ROOT_DIR,
    TestError,
    console,
    get_chart_names,
    get_scenario_names,
    log_chart,
    log_error,
    log_info,
    log_scenario,
    log_step,
    log_success,
    log_warning,
    print_summary,
)


def detect_changed_charts() -> list[str]:
    """Detect which charts have changed compared to main branch.

    Returns:
        List of chart names that have changes
    """
    import subprocess

    # Get list of changed files
    result = subprocess.run(
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        capture_output=True,
        text=True,
        cwd=ROOT_DIR,
    )

    if result.returncode != 0:
        # Fallback: diff against main
        result = subprocess.run(
            ["git", "diff", "--name-only", "main...HEAD"],
            capture_output=True,
            text=True,
            cwd=ROOT_DIR,
        )

    changed_files = result.stdout.strip().split("\n") if result.stdout else []

    # Extract chart names from changed paths
    charts = set()
    for f in changed_files:
        if f.startswith("charts/"):
            parts = f.split("/")
            if len(parts) >= 2:
                chart_name = parts[1]
                if (CHARTS_DIR / chart_name / "Chart.yaml").exists():
                    charts.add(chart_name)

    return sorted(charts)


def run_scenario(
    chart: str,
    scenario: str,
    dep_manager: DependencyManager,
    upgrade_enabled: bool = True,
    verbose: bool = False,
) -> ScenarioResult:
    """Run a single test scenario.

    Args:
        chart: Chart name
        scenario: Scenario name
        dep_manager: Dependency manager instance
        upgrade_enabled: Whether to run upgrade tests
        verbose: Enable verbose output

    Returns:
        ScenarioResult with test outcome
    """
    start_time = time.time()
    namespace = f"ct-{chart}-{scenario.replace('_', '-')}"
    release_name = f"{chart}-test"

    context = TestContext(
        chart=chart,
        scenario=scenario,
        namespace=namespace,
        upgrade_enabled=upgrade_enabled,
        verbose=verbose,
    )

    log_scenario(chart, scenario)

    try:
        # Create test namespace
        log_step("1", "Creating namespace")
        create_namespace(namespace, verbose=verbose)

        # Setup dependencies
        log_step("2", "Setting up dependencies")
        dep_manager.setup_dependencies(scenario, context)

        # Get scenario config
        scenario_config = get_scenario_config(chart, scenario)
        ci_values_file = get_ci_values_file(chart, scenario)
        chart_path = str(get_chart_path(chart))

        # Build chart dependencies
        log_step("3", "Building chart dependencies")
        helm_dependency_build(chart, verbose=verbose)

        # Determine if we should run upgrade test
        should_upgrade = upgrade_enabled and not scenario_config.skip_upgrade

        if should_upgrade:
            # Get old version info
            old_version = get_released_chart_version(chart, verbose=verbose)
            old_values = get_old_ci_values(chart, scenario)

            if old_version and old_values:
                # Step 4: Install OLD version with OLD values
                log_step("4", f"Installing old version ({old_version}) with old values")
                helm_install(
                    release_name=release_name,
                    chart=f"conduktor/{chart}",
                    namespace=namespace,
                    values_files=[],
                    set_values=None,
                    wait=True,
                    verbose=verbose,
                )

                # Write old values to temp file for upgrade
                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".yaml", delete=False
                ) as f:
                    f.write(old_values)
                    old_values_path = Path(f.name)

                try:
                    # Run helm test on old version
                    log_step("4a", "Testing old version")
                    helm_test(release_name, namespace, verbose=verbose)

                    # Step 5: Upgrade to CURRENT version with OLD values
                    log_step("5", "Upgrading to current version with old values")
                    helm_upgrade(
                        release_name=release_name,
                        chart=chart_path,
                        namespace=namespace,
                        values_files=[old_values_path],
                        wait=True,
                        verbose=verbose,
                    )

                    # Run helm test after upgrade with old values
                    log_step("5a", "Testing after upgrade (old values)")
                    helm_test(release_name, namespace, verbose=verbose)

                    # Step 6: Upgrade to CURRENT version with CURRENT values
                    log_step("6", "Upgrading with current values")
                    helm_upgrade(
                        release_name=release_name,
                        chart=chart_path,
                        namespace=namespace,
                        values_files=[ci_values_file],
                        wait=True,
                        verbose=verbose,
                    )

                finally:
                    old_values_path.unlink(missing_ok=True)

            else:
                log_warning(
                    f"No old version found for {chart}, skipping upgrade test"
                )
                # Fresh install with current values
                log_step("4", "Installing current version (no old version found)")
                helm_install(
                    release_name=release_name,
                    chart=chart_path,
                    namespace=namespace,
                    values_files=[ci_values_file],
                    wait=True,
                    verbose=verbose,
                )

        else:
            # No upgrade test, just install current version
            log_step("4", "Installing current version (upgrade skipped)")
            helm_install(
                release_name=release_name,
                chart=chart_path,
                namespace=namespace,
                values_files=[ci_values_file],
                wait=True,
                verbose=verbose,
            )

        # Run final helm test
        log_step("7", "Running helm test")
        helm_test(release_name, namespace, verbose=verbose)

        log_success(f"Scenario {chart}/{scenario} PASSED")

        duration = time.time() - start_time
        return ScenarioResult(
            chart=chart,
            scenario=scenario,
            success=True,
            duration_seconds=duration,
            upgrade_tested=should_upgrade,
        )

    except Exception as e:
        duration = time.time() - start_time
        log_error(f"Scenario {chart}/{scenario} FAILED: {e}")

        # Collect debug info
        if verbose:
            try:
                log_info("Pod status:")
                pods = get_pods(namespace, verbose=verbose)
                for pod in pods:
                    name = pod.get("metadata", {}).get("name", "unknown")
                    phase = pod.get("status", {}).get("phase", "unknown")
                    console.print(f"  {name}: {phase}")

                log_info("Events:")
                events = get_events(namespace, verbose=verbose)
                console.print(events)
            except Exception:
                pass

        return ScenarioResult(
            chart=chart,
            scenario=scenario,
            success=False,
            duration_seconds=duration,
            error_message=str(e),
            upgrade_tested=False,
        )

    finally:
        # Cleanup
        try:
            helm_uninstall(release_name, namespace, verbose=verbose)
        except Exception:
            pass

        try:
            dep_manager.teardown_scenario(scenario, context)
        except Exception:
            pass

        try:
            delete_namespace(namespace, wait=True, verbose=verbose)
        except Exception:
            pass


def run_chart_tests(
    chart: str,
    scenarios: Optional[list[str]] = None,
    upgrade_enabled: bool = True,
    verbose: bool = False,
) -> ChartTestResult:
    """Run all tests for a chart.

    Args:
        chart: Chart name
        scenarios: Optional list of specific scenarios to run
        upgrade_enabled: Whether to run upgrade tests
        verbose: Enable verbose output

    Returns:
        ChartTestResult with all scenario outcomes
    """
    start_time = time.time()
    log_chart(chart)

    # Get scenarios to run
    if scenarios:
        scenario_list = scenarios
    else:
        scenario_list = get_scenario_names(chart)

    if not scenario_list:
        log_warning(f"No scenarios found for chart {chart}")
        return ChartTestResult(
            chart=chart,
            scenarios=[],
            total_duration_seconds=0,
        )

    log_info(f"Running {len(scenario_list)} scenarios for {chart}")

    # Create dependency manager for shared deps
    deps_namespace = f"ct-{chart}-deps"
    dep_manager = DependencyManager(
        chart=chart,
        namespace=deps_namespace,
        verbose=verbose,
    )

    results = []

    try:
        # Run each scenario sequentially
        for scenario in scenario_list:
            result = run_scenario(
                chart=chart,
                scenario=scenario,
                dep_manager=dep_manager,
                upgrade_enabled=upgrade_enabled,
                verbose=verbose,
            )
            results.append(result)

    finally:
        # Teardown shared dependencies
        log_info("Cleaning up shared dependencies")
        dep_manager.teardown_all()

        try:
            delete_namespace(deps_namespace, wait=True, verbose=verbose)
        except Exception:
            pass

    duration = time.time() - start_time

    return ChartTestResult(
        chart=chart,
        scenarios=results,
        total_duration_seconds=duration,
    )


# CLI Commands
@click.group()
def cli():
    """Conduktor Helm Charts Test Runner."""
    pass


@cli.command()
@click.option("--chart", "-c", help="Chart to test (e.g., console)")
@click.option("--scenario", "-s", help="Specific scenario to run")
@click.option("--changed", is_flag=True, help="Test only changed charts")
@click.option("--all", "test_all", is_flag=True, help="Test all charts")
@click.option("--skip-upgrade", is_flag=True, help="Skip upgrade tests")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
def run(
    chart: Optional[str],
    scenario: Optional[str],
    changed: bool,
    test_all: bool,
    skip_upgrade: bool,
    verbose: bool,
):
    """Run chart tests."""
    # Validate context
    current_ctx = get_current_context()
    if not current_ctx or "k3d" not in current_ctx:
        log_error(f"Current context '{current_ctx}' doesn't look like a k3d cluster")
        log_error("Please run 'make k3d-up' first")
        sys.exit(1)

    # Setup helm repos
    setup_helm_repos(verbose=verbose)

    # Determine which charts to test
    if chart:
        charts_to_test = [chart]
    elif changed:
        charts_to_test = detect_changed_charts()
        if not charts_to_test:
            log_info("No charts have changed")
            sys.exit(0)
    elif test_all:
        charts_to_test = get_chart_names()
    else:
        log_error("Please specify --chart, --changed, or --all")
        sys.exit(1)

    log_info(f"Testing charts: {', '.join(charts_to_test)}")

    all_results = []
    upgrade_enabled = not skip_upgrade

    for chart_name in charts_to_test:
        scenarios_to_run = [scenario] if scenario else None
        result = run_chart_tests(
            chart=chart_name,
            scenarios=scenarios_to_run,
            upgrade_enabled=upgrade_enabled,
            verbose=verbose,
        )
        all_results.append(result)

    # Print summary
    summary_data = []
    for result in all_results:
        for scenario_result in result.scenarios:
            summary_data.append(
                (
                    scenario_result.chart,
                    scenario_result.scenario,
                    scenario_result.success,
                    scenario_result.error_message,
                )
            )

    print_summary(summary_data)

    # Exit with appropriate code
    all_passed = all(r.all_passed for r in all_results)
    sys.exit(0 if all_passed else 1)


@cli.command("detect-changed")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON array")
def detect_changed(as_json: bool):
    """Detect charts that have changed vs main branch."""
    charts = detect_changed_charts()

    if as_json:
        click.echo(json.dumps(charts))
    else:
        if charts:
            for chart in charts:
                click.echo(chart)
        else:
            click.echo("No charts have changed")


@cli.command("lint-manifests")
@click.option("--chart", "-c", help="Chart to lint (default: all)")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
def lint_manifests(chart: Optional[str], verbose: bool):
    """Validate helm template output with kubeconform."""
    from test.lint import lint_chart_manifests

    charts_to_lint = [chart] if chart else get_chart_names()

    all_passed = True
    for chart_name in charts_to_lint:
        passed = lint_chart_manifests(chart_name, verbose=verbose)
        if not passed:
            all_passed = False

    sys.exit(0 if all_passed else 1)


@cli.command("list-charts")
def list_charts():
    """List available charts."""
    for chart in get_chart_names():
        click.echo(chart)


@cli.command("list-scenarios")
@click.argument("chart")
def list_scenarios(chart: str):
    """List scenarios for a chart."""
    for scenario in get_scenario_names(chart):
        click.echo(scenario)


if __name__ == "__main__":
    cli()
