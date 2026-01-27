"""Manifest linting with kubeconform."""

import tempfile
from pathlib import Path

from test.config import get_ci_values_file, get_scenarios
from test.helm import helm_dependency_build, helm_template
from test.utils import CHARTS_DIR, gh_group_end, gh_group_start, log_error, log_info, log_success, log_warning, run_command


def lint_chart(chart: str, verbose: bool = False) -> bool:
    """Lint all scenarios for a chart."""
    log_info(f"Linting {chart}")
    gh_group_start(f"Lint {chart}")

    try:
        # Build dependencies first
        try:
            helm_dependency_build(chart, verbose)
        except Exception as e:
            log_error(f"Failed to build dependencies for {chart}: {e}")
            return False

        scenarios = get_scenarios(chart)
        if not scenarios:
            log_warning(f"No scenarios for {chart}")
            return True

        all_ok = True
        for scenario in scenarios:
            ok = lint_scenario(chart, scenario, verbose)
            if not ok:
                all_ok = False

        return all_ok
    finally:
        gh_group_end()


def lint_scenario(chart: str, scenario: str, verbose: bool = False) -> bool:
    """Lint a single scenario."""
    chart_path = str(CHARTS_DIR / chart)
    values_file = get_ci_values_file(chart, scenario)

    # Check values file exists
    if not values_file.exists():
        log_error(f"Values file not found: {values_file}")
        return False

    # Render templates
    try:
        manifests = helm_template(chart_path, "lint", [values_file])
    except Exception as e:
        log_error(f"Template failed {chart}/{scenario}: {e}")
        if verbose:
            # Show more details
            result = run_command(["helm", "template", "test", chart_path, "--values", str(values_file), "--debug"])
            print(result.stderr)
        return False

    # Check if kubeconform is available
    result = run_command(["kubeconform", "-v"])
    if not result.success:
        log_warning("kubeconform not installed, skipping validation")
        log_success(f"Template OK: {chart}/{scenario}")
        return True

    # Run kubeconform
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(manifests)
        temp_path = Path(f.name)

    try:
        result = run_command(["kubeconform", "-strict", "-summary", str(temp_path)], verbose=verbose)
        if result.success:
            log_success(f"Lint OK: {chart}/{scenario}")
            return True
        else:
            log_error(f"Lint failed: {chart}/{scenario}")
            print(result.stdout + result.stderr)
            return False
    finally:
        temp_path.unlink(missing_ok=True)
