"""
Manifest linting with kubeconform and helm template validation.
"""

import tempfile
from pathlib import Path
from typing import Optional

from test.config import get_ci_values_file
from test.helm import get_chart_path, helm_template
from test.utils import (
    CHARTS_DIR,
    CommandResult,
    get_scenario_names,
    log_error,
    log_info,
    log_success,
    log_warning,
    run_command,
)


def check_kubeconform_installed() -> bool:
    """Check if kubeconform is installed.

    Returns:
        True if installed
    """
    result = run_command(["kubeconform", "-v"])
    return result.success


def run_kubeconform(
    manifests: str,
    verbose: bool = False,
) -> tuple[bool, str]:
    """Run kubeconform on rendered manifests.

    Args:
        manifests: YAML manifests content
        verbose: Enable verbose output

    Returns:
        Tuple of (passed, output)
    """
    # Write manifests to temp file
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".yaml", delete=False
    ) as f:
        f.write(manifests)
        temp_path = Path(f.name)

    try:
        cmd = [
            "kubeconform",
            "-strict",
            "-summary",
            "-output",
            "text",
            str(temp_path),
        ]

        if verbose:
            cmd.append("-verbose")

        result = run_command(cmd, verbose=verbose)
        return result.success, result.stdout + result.stderr

    finally:
        temp_path.unlink(missing_ok=True)


def lint_chart_scenario(
    chart: str,
    scenario: str,
    verbose: bool = False,
) -> bool:
    """Lint a single chart scenario.

    Args:
        chart: Chart name
        scenario: Scenario name
        verbose: Enable verbose output

    Returns:
        True if lint passed
    """
    log_info(f"Linting {chart}/{scenario}")

    chart_path = get_chart_path(chart)
    ci_values_file = get_ci_values_file(chart, scenario)

    # Render templates
    try:
        manifests = helm_template(
            release_name=f"{chart}-lint",
            chart=str(chart_path),
            namespace="lint",
            values_files=[ci_values_file],
            verbose=verbose,
        )
    except Exception as e:
        log_error(f"helm template failed for {chart}/{scenario}: {e}")
        return False

    # Skip kubeconform if not installed
    if not check_kubeconform_installed():
        log_warning("kubeconform not installed, skipping manifest validation")
        log_success(f"helm template OK: {chart}/{scenario}")
        return True

    # Run kubeconform
    passed, output = run_kubeconform(manifests, verbose=verbose)

    if passed:
        log_success(f"Lint passed: {chart}/{scenario}")
    else:
        log_error(f"Lint failed: {chart}/{scenario}")
        if output:
            print(output)

    return passed


def lint_chart_manifests(
    chart: str,
    scenarios: Optional[list[str]] = None,
    verbose: bool = False,
) -> bool:
    """Lint all scenarios for a chart.

    Args:
        chart: Chart name
        scenarios: Optional list of specific scenarios
        verbose: Enable verbose output

    Returns:
        True if all scenarios passed
    """
    log_info(f"Linting chart: {chart}")

    # Get scenarios
    if scenarios:
        scenario_list = scenarios
    else:
        scenario_list = get_scenario_names(chart)

    if not scenario_list:
        log_warning(f"No scenarios found for {chart}")
        return True

    all_passed = True

    for scenario in scenario_list:
        passed = lint_chart_scenario(chart, scenario, verbose=verbose)
        if not passed:
            all_passed = False

    return all_passed
