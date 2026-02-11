"""Configuration loading for test dependencies."""

from pathlib import Path
from typing import Optional
import yaml

from test.models import ChartTestConfig
from test.utils import CHARTS_DIR, SHARED_DEPS_DIR


def load_chart_config(chart: str) -> ChartTestConfig:
    """Load test configuration for a chart."""
    config_file = CHARTS_DIR / chart / "ci" / "test-config.yaml"

    if not config_file.exists():
        return ChartTestConfig()

    with open(config_file) as f:
        data = yaml.safe_load(f) or {}

    return ChartTestConfig(**data)


def get_shared_values_file(dep_name: str) -> Optional[Path]:
    """Get the shared values file for a dependency."""
    values_file = SHARED_DEPS_DIR / dep_name / "values.yaml"
    return values_file if values_file.exists() else None


def get_ci_values_file(chart: str, scenario: str) -> Path:
    """Get the CI values file for a scenario."""
    return CHARTS_DIR / chart / "ci" / f"{scenario}-values.yaml"


def get_scenarios(chart: str) -> list[str]:
    """Get list of scenario names for a chart."""
    ci_dir = CHARTS_DIR / chart / "ci"
    if not ci_dir.exists():
        return []

    scenarios = []
    for f in sorted(ci_dir.glob("*-values.yaml")):
        # Extract: "01-basic-values.yaml" -> "01-basic"
        name = f.stem.replace("-values", "")
        scenarios.append(name)

    return scenarios


def get_old_values_content(chart: str, scenario: str, ref: str = "main") -> Optional[str]:
    """Get old CI values content from git ref.

    Tries origin/{ref} first (for CI environments), then {ref} (for local).
    """
    import subprocess

    path = f"charts/{chart}/ci/{scenario}-values.yaml"

    # Try origin/ref first (CI typically has origin/main but not local main)
    for git_ref in [f"origin/{ref}", ref]:
        result = subprocess.run(
            ["git", "show", f"{git_ref}:{path}"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout

    return None
