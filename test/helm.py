"""
Helm operations wrapper for chart testing.
"""

import json
import tempfile
from pathlib import Path
from typing import Optional

import yaml

from test.utils import (
    CHARTS_DIR,
    ROOT_DIR,
    CommandResult,
    HelmError,
    log_debug,
    log_error,
    log_info,
    run_command,
)


def helm_repo_add(name: str, url: str, verbose: bool = False) -> None:
    """Add a Helm repository.

    Args:
        name: Repository name
        url: Repository URL
        verbose: Enable verbose output
    """
    result = run_command(
        ["helm", "repo", "add", name, url, "--force-update"],
        verbose=verbose,
    )
    if not result.success:
        log_debug(f"helm repo add warning: {result.stderr}", verbose)


def helm_repo_update(verbose: bool = False) -> None:
    """Update Helm repositories."""
    result = run_command(["helm", "repo", "update"], verbose=verbose)
    if not result.success:
        raise HelmError(f"helm repo update failed: {result.stderr}")


def helm_dependency_build(chart: str, verbose: bool = False) -> None:
    """Build Helm dependencies for a chart.

    Args:
        chart: Chart name
        verbose: Enable verbose output
    """
    chart_path = CHARTS_DIR / chart
    result = run_command(
        ["helm", "dependency", "build", str(chart_path)],
        verbose=verbose,
    )
    if not result.success:
        raise HelmError(f"helm dependency build failed: {result.stderr}")


def helm_install(
    release_name: str,
    chart: str,
    namespace: str,
    values_files: Optional[list[Path]] = None,
    set_values: Optional[dict] = None,
    wait: bool = True,
    timeout: str = "600s",
    verbose: bool = False,
) -> CommandResult:
    """Install a Helm chart.

    Args:
        release_name: Helm release name
        chart: Chart reference (path or repo/chart)
        namespace: Kubernetes namespace
        values_files: List of values files to use
        set_values: Dictionary of values to set via --set
        wait: Wait for resources to be ready
        timeout: Timeout for the operation
        verbose: Enable verbose output

    Returns:
        CommandResult from helm install

    Raises:
        HelmError: If installation fails
    """
    cmd = [
        "helm",
        "install",
        release_name,
        chart,
        "--namespace",
        namespace,
        "--create-namespace",
        "--timeout",
        timeout,
    ]

    if wait:
        cmd.append("--wait")

    if values_files:
        for vf in values_files:
            if vf.exists():
                cmd.extend(["--values", str(vf)])

    if set_values:
        for key, value in set_values.items():
            cmd.extend(["--set", f"{key}={value}"])

    log_info(f"Installing {release_name} in {namespace}")
    result = run_command(cmd, verbose=verbose, timeout=900)

    if not result.success:
        raise HelmError(f"helm install failed: {result.stderr}")

    return result


def helm_upgrade(
    release_name: str,
    chart: str,
    namespace: str,
    values_files: Optional[list[Path]] = None,
    values_content: Optional[str] = None,
    set_values: Optional[dict] = None,
    wait: bool = True,
    timeout: str = "600s",
    verbose: bool = False,
) -> CommandResult:
    """Upgrade a Helm release.

    Args:
        release_name: Helm release name
        chart: Chart reference (path or repo/chart)
        namespace: Kubernetes namespace
        values_files: List of values files to use
        values_content: Raw values content (will be written to temp file)
        set_values: Dictionary of values to set via --set
        wait: Wait for resources to be ready
        timeout: Timeout for the operation
        verbose: Enable verbose output

    Returns:
        CommandResult from helm upgrade

    Raises:
        HelmError: If upgrade fails
    """
    cmd = [
        "helm",
        "upgrade",
        release_name,
        chart,
        "--namespace",
        namespace,
        "--timeout",
        timeout,
    ]

    if wait:
        cmd.append("--wait")

    if values_files:
        for vf in values_files:
            if vf.exists():
                cmd.extend(["--values", str(vf)])

    # Handle raw values content by writing to temp file
    temp_file = None
    if values_content:
        temp_file = tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        )
        temp_file.write(values_content)
        temp_file.close()
        cmd.extend(["--values", temp_file.name])

    if set_values:
        for key, value in set_values.items():
            cmd.extend(["--set", f"{key}={value}"])

    log_info(f"Upgrading {release_name} in {namespace}")

    try:
        result = run_command(cmd, verbose=verbose, timeout=900)

        if not result.success:
            raise HelmError(f"helm upgrade failed: {result.stderr}")

        return result
    finally:
        if temp_file:
            Path(temp_file.name).unlink(missing_ok=True)


def helm_uninstall(
    release_name: str,
    namespace: str,
    wait: bool = True,
    verbose: bool = False,
) -> CommandResult:
    """Uninstall a Helm release.

    Args:
        release_name: Helm release name
        namespace: Kubernetes namespace
        wait: Wait for uninstallation to complete
        verbose: Enable verbose output

    Returns:
        CommandResult from helm uninstall
    """
    cmd = ["helm", "uninstall", release_name, "--namespace", namespace]

    if wait:
        cmd.append("--wait")

    log_info(f"Uninstalling {release_name} from {namespace}")
    result = run_command(cmd, verbose=verbose, timeout=300)

    if not result.success:
        log_debug(f"helm uninstall warning: {result.stderr}", verbose)

    return result


def helm_test(
    release_name: str,
    namespace: str,
    timeout: str = "600s",
    verbose: bool = False,
) -> CommandResult:
    """Run Helm tests for a release.

    Args:
        release_name: Helm release name
        namespace: Kubernetes namespace
        timeout: Timeout for tests
        verbose: Enable verbose output

    Returns:
        CommandResult from helm test

    Raises:
        HelmError: If tests fail
    """
    cmd = [
        "helm",
        "test",
        release_name,
        "--namespace",
        namespace,
        "--timeout",
        timeout,
    ]

    log_info(f"Running helm test for {release_name}")
    result = run_command(cmd, verbose=verbose, timeout=900)

    if not result.success:
        raise HelmError(f"helm test failed: {result.stderr}")

    return result


def helm_template(
    release_name: str,
    chart: str,
    namespace: str,
    values_files: Optional[list[Path]] = None,
    set_values: Optional[dict] = None,
    verbose: bool = False,
) -> str:
    """Render Helm templates without installing.

    Args:
        release_name: Helm release name
        chart: Chart reference
        namespace: Kubernetes namespace
        values_files: List of values files
        set_values: Dictionary of values to set
        verbose: Enable verbose output

    Returns:
        Rendered YAML manifests

    Raises:
        HelmError: If template rendering fails
    """
    cmd = [
        "helm",
        "template",
        release_name,
        chart,
        "--namespace",
        namespace,
    ]

    if values_files:
        for vf in values_files:
            if vf.exists():
                cmd.extend(["--values", str(vf)])

    if set_values:
        for key, value in set_values.items():
            cmd.extend(["--set", f"{key}={value}"])

    result = run_command(cmd, verbose=verbose)

    if not result.success:
        raise HelmError(f"helm template failed: {result.stderr}")

    return result.stdout


def helm_search_versions(
    chart: str,
    verbose: bool = False,
) -> list[str]:
    """Search for available chart versions.

    Args:
        chart: Chart reference (e.g., conduktor/console)
        verbose: Enable verbose output

    Returns:
        List of available versions (sorted descending)
    """
    result = run_command(
        ["helm", "search", "repo", chart, "--versions", "-o", "json"],
        verbose=verbose,
    )

    if not result.success:
        log_debug(f"helm search warning: {result.stderr}", verbose)
        return []

    try:
        data = json.loads(result.stdout)
        return [item["version"] for item in data]
    except (json.JSONDecodeError, KeyError):
        return []


def helm_show_chart(chart: str, verbose: bool = False) -> dict:
    """Get chart metadata.

    Args:
        chart: Chart reference or path
        verbose: Enable verbose output

    Returns:
        Chart.yaml contents as dict
    """
    result = run_command(
        ["helm", "show", "chart", chart],
        verbose=verbose,
    )

    if not result.success:
        raise HelmError(f"helm show chart failed: {result.stderr}")

    return yaml.safe_load(result.stdout)


def get_chart_path(chart: str) -> Path:
    """Get the local path for a chart.

    Args:
        chart: Chart name

    Returns:
        Path to the chart directory
    """
    return CHARTS_DIR / chart


def get_current_chart_version(chart: str) -> str:
    """Get the current version from local Chart.yaml.

    Args:
        chart: Chart name

    Returns:
        Version string
    """
    chart_yaml = CHARTS_DIR / chart / "Chart.yaml"
    data = yaml.safe_load(chart_yaml.read_text())
    return data["version"]


def get_released_chart_version(chart: str, verbose: bool = False) -> Optional[str]:
    """Get the latest released version of a chart from the repo.

    Args:
        chart: Chart name (e.g., 'console')
        verbose: Enable verbose output

    Returns:
        Latest released version, or None if not found
    """
    versions = helm_search_versions(f"conduktor/{chart}", verbose)
    return versions[0] if versions else None
