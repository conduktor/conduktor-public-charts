"""Helm operations wrapper."""

import json
import tempfile
from pathlib import Path
from typing import Optional

import yaml

from test.utils import CHARTS_DIR, HelmError, log_info, run_command


def _dependencies_satisfied(chart_path: Path) -> bool:
    """Check if chart dependencies are already downloaded."""
    chart_yaml = chart_path / "Chart.yaml"
    charts_dir = chart_path / "charts"

    if not chart_yaml.exists():
        return False

    # Parse Chart.yaml to get dependencies
    with open(chart_yaml) as f:
        chart_data = yaml.safe_load(f) or {}

    dependencies = chart_data.get("dependencies", [])
    if not dependencies:
        return True  # No dependencies needed

    if not charts_dir.exists():
        return False

    # Check each dependency has a matching .tgz file
    for dep in dependencies:
        name = dep.get("name", "")
        version = dep.get("version", "")
        if not name or not version:
            continue

        # Look for {name}-{version}.tgz
        expected_file = charts_dir / f"{name}-{version}.tgz"
        if not expected_file.exists():
            return False

    return True


def helm_repo_add(name: str, url: str, verbose: bool = False) -> None:
    """Add a Helm repository."""
    run_command(["helm", "repo", "add", name, url, "--force-update"], verbose=verbose)


def helm_repo_update(verbose: bool = False) -> None:
    """Update Helm repositories."""
    run_command(["helm", "repo", "update"], verbose=verbose)


def helm_install(
    release_name: str,
    chart: str,
    namespace: str,
    values_files: Optional[list[Path]] = None,
    set_overrides: Optional[list[str]] = None,
    version: Optional[str] = None,
    timeout: str = "600s",
    wait: bool = True,
    verbose: bool = False,
) -> None:
    """Install a Helm chart."""
    cmd = [
        "helm", "upgrade", "--install", release_name, chart,
        "--namespace", namespace,
        "--create-namespace",
    ]

    if wait:
        cmd.extend(["--wait", "--timeout", timeout])

    if version:
        cmd.extend(["--version", version])

    for vf in (values_files or []):
        if vf.exists():
            cmd.extend(["--values", str(vf)])

    for override in (set_overrides or []):
        cmd.extend(["--set", override])

    log_info(f"Installing {release_name}" + ("" if wait else " (no wait)"))
    result = run_command(cmd, verbose=verbose, timeout=900 if wait else 120, log=True)

    if not result.success:
        raise HelmError(f"Install failed: {result.stderr}")


def helm_upgrade(
    release_name: str,
    chart: str,
    namespace: str,
    values_files: Optional[list[Path]] = None,
    set_overrides: Optional[list[str]] = None,
    values_content: Optional[str] = None,
    timeout: str = "600s",
    verbose: bool = False,
) -> None:
    """Upgrade a Helm release."""
    cmd = [
        "helm", "upgrade", release_name, chart,
        "--namespace", namespace,
        "--wait",
        "--timeout", timeout,
    ]

    for vf in (values_files or []):
        if vf.exists():
            cmd.extend(["--values", str(vf)])

    for override in (set_overrides or []):
        cmd.extend(["--set", override])

    # Handle raw values content
    temp_file = None
    if values_content:
        temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False)
        temp_file.write(values_content)
        temp_file.close()
        cmd.extend(["--values", temp_file.name])

    log_info(f"Upgrading {release_name}")

    try:
        result = run_command(cmd, verbose=verbose, timeout=900, log=True)
        if not result.success:
            raise HelmError(f"Upgrade failed: {result.stderr}")
    finally:
        if temp_file:
            Path(temp_file.name).unlink(missing_ok=True)


def helm_uninstall(release_name: str, namespace: str, verbose: bool = False) -> None:
    """Uninstall a Helm release."""
    log_info(f"Uninstalling {release_name}")
    run_command(
        ["helm", "uninstall", release_name, "--namespace", namespace, "--wait"],
        verbose=verbose,
        timeout=300,
        log=True,
    )


def helm_test(release_name: str, namespace: str, timeout: str = "600s", verbose: bool = False) -> None:
    """Run Helm tests."""
    log_info(f"Running helm test for {release_name}")
    result = run_command(
        ["helm", "test", release_name, "--namespace", namespace, "--timeout", timeout],
        verbose=verbose,
        timeout=900,
        log=True,
    )
    if not result.success:
        raise HelmError(f"Helm test failed: {result.stderr}")


def helm_template(chart: str, namespace: str, values_files: Optional[list[Path]] = None) -> str:
    """Render Helm templates."""
    cmd = ["helm", "template", "test", chart, "--namespace", namespace]

    for vf in (values_files or []):
        if not vf.exists():
            raise HelmError(f"Values file not found: {vf}")
        cmd.extend(["--values", str(vf)])

    result = run_command(cmd)
    if not result.success:
        raise HelmError(f"Template failed: {result.stderr}")

    return result.stdout


def helm_dependency_build(chart: str, verbose: bool = False, force: bool = False) -> None:
    """Build chart dependencies if needed."""
    chart_path = CHARTS_DIR / chart

    # Skip if dependencies already satisfied
    if not force and _dependencies_satisfied(chart_path):
        log_info(f"Dependencies for {chart} already up to date")
        return

    log_info(f"Building dependencies for {chart}")
    result = run_command(["helm", "dependency", "build", str(chart_path)], verbose=verbose, log=True)
    if not result.success:
        raise HelmError(f"Dependency build failed: {result.stderr}")


def get_chart_name(chart_path: Path) -> Optional[str]:
    """Get the name of a chart from its Chart.yaml."""
    chart_yaml = chart_path / "Chart.yaml"
    if not chart_yaml.exists():
        return None

    with open(chart_yaml) as f:
        chart_data = yaml.safe_load(f) or {}

    return chart_data.get("name")

def get_released_version(chart: str) -> Optional[str]:
    """Get latest released version of a chart."""
    result = run_command(["helm", "search", "repo", f"conduktor/{chart}", "--versions", "-o", "json"])
    if result.success:
        try:
            data = json.loads(result.stdout)
            return data[0]["version"] if data else None
        except (json.JSONDecodeError, KeyError, IndexError):
            pass
    return None
