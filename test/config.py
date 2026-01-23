"""
Configuration loading and management for test dependencies.
"""

from pathlib import Path
from typing import Optional

import yaml

from test.models import ChartDependenciesConfig, DependencySpec, ScenarioConfig
from test.utils import CHARTS_DIR, ROOT_DIR, ConfigError, log_debug


def load_yaml(path: Path) -> dict:
    """Load a YAML file and return its contents as a dict.

    Args:
        path: Path to the YAML file

    Returns:
        Parsed YAML content

    Raises:
        ConfigError: If file doesn't exist or is invalid YAML
    """
    if not path.exists():
        raise ConfigError(f"Configuration file not found: {path}")

    try:
        with open(path) as f:
            return yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        raise ConfigError(f"Invalid YAML in {path}: {e}")


def load_chart_dependencies(chart: str) -> ChartDependenciesConfig:
    """Load the test dependencies configuration for a chart.

    Args:
        chart: Name of the chart (e.g., 'console')

    Returns:
        Parsed ChartDependenciesConfig

    Raises:
        ConfigError: If configuration is invalid
    """
    deps_file = CHARTS_DIR / chart / "test-deps" / "dependencies.yaml"

    if not deps_file.exists():
        log_debug(f"No test-deps/dependencies.yaml for {chart}, using defaults")
        return ChartDependenciesConfig()

    data = load_yaml(deps_file)

    try:
        return ChartDependenciesConfig(**data)
    except Exception as e:
        raise ConfigError(f"Invalid dependencies config for {chart}: {e}")


def get_scenario_dependencies(
    chart: str,
    scenario: str,
    config: Optional[ChartDependenciesConfig] = None,
) -> list[DependencySpec]:
    """Get the list of dependencies required for a scenario.

    Args:
        chart: Chart name
        scenario: Scenario name
        config: Optional pre-loaded config (will load if not provided)

    Returns:
        List of DependencySpec for the scenario
    """
    if config is None:
        config = load_chart_dependencies(chart)

    # Check if scenario has specific dependencies configured
    if scenario in config.scenarios:
        dep_names = config.scenarios[scenario].dependencies
    else:
        # Use default dependencies
        dep_names = config.default_dependencies

    # If no dependencies specified, use all shared dependencies
    if not dep_names:
        dep_names = list(config.shared_dependencies.keys())

    # Resolve dependency names to specs
    deps = []
    for name in dep_names:
        if name not in config.shared_dependencies:
            raise ConfigError(
                f"Unknown dependency '{name}' in scenario '{scenario}' for chart '{chart}'"
            )
        deps.append(config.shared_dependencies[name])

    return deps


def get_scenario_config(
    chart: str,
    scenario: str,
    config: Optional[ChartDependenciesConfig] = None,
) -> ScenarioConfig:
    """Get the configuration for a specific scenario.

    Args:
        chart: Chart name
        scenario: Scenario name
        config: Optional pre-loaded config

    Returns:
        ScenarioConfig for the scenario
    """
    if config is None:
        config = load_chart_dependencies(chart)

    if scenario in config.scenarios:
        return config.scenarios[scenario]

    return ScenarioConfig()


def get_ci_values_file(chart: str, scenario: str) -> Path:
    """Get the path to the CI values file for a scenario.

    Args:
        chart: Chart name
        scenario: Scenario name (e.g., '01-basic')

    Returns:
        Path to the values file

    Raises:
        ConfigError: If values file doesn't exist
    """
    values_file = CHARTS_DIR / chart / "ci" / f"{scenario}-values.yaml"

    if not values_file.exists():
        raise ConfigError(f"CI values file not found: {values_file}")

    return values_file


def get_old_ci_values(chart: str, scenario: str, ref: str = "main") -> Optional[str]:
    """Get the old CI values file content from a git ref.

    Args:
        chart: Chart name
        scenario: Scenario name
        ref: Git ref (branch, tag, commit) to get values from

    Returns:
        Content of the old values file, or None if not found
    """
    import subprocess

    values_path = f"charts/{chart}/ci/{scenario}-values.yaml"

    try:
        result = subprocess.run(
            ["git", "show", f"{ref}:{values_path}"],
            capture_output=True,
            text=True,
            cwd=ROOT_DIR,
        )
        if result.returncode == 0:
            return result.stdout
        return None
    except Exception:
        return None


def merge_values_files(*paths: Path) -> dict:
    """Merge multiple values files, later files override earlier ones.

    Args:
        paths: Paths to values files to merge

    Returns:
        Merged values dictionary
    """
    result = {}
    for path in paths:
        if path.exists():
            data = load_yaml(path)
            result = _deep_merge(result, data)
    return result


def _deep_merge(base: dict, override: dict) -> dict:
    """Deep merge two dictionaries.

    Args:
        base: Base dictionary
        override: Dictionary to merge on top

    Returns:
        Merged dictionary
    """
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def get_dependency_values_files(
    chart: str,
    dep_spec: DependencySpec,
) -> list[Path]:
    """Get the list of values files for a dependency.

    Args:
        chart: Chart name
        dep_spec: Dependency specification

    Returns:
        List of paths to values files (base + chart-specific overrides)
    """
    files = []

    # Add base values file from shared-deps
    if dep_spec.values_file:
        base_path = ROOT_DIR / dep_spec.values_file
        if base_path.exists():
            files.append(base_path)

    # Add chart-specific values override
    if dep_spec.chart_values_file:
        chart_path = CHARTS_DIR / chart / dep_spec.chart_values_file
        if chart_path.exists():
            files.append(chart_path)

    return files
