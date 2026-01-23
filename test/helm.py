"""Helm operations wrapper."""

import json
import tempfile
from pathlib import Path
from typing import Optional

from test.utils import CHARTS_DIR, HelmError, log_info, run_command


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
    version: Optional[str] = None,
    timeout: str = "600s",
    verbose: bool = False,
) -> None:
    """Install a Helm chart."""
    cmd = [
        "helm", "install", release_name, chart,
        "--namespace", namespace,
        "--create-namespace",
        "--wait",
        "--timeout", timeout,
    ]

    if version:
        cmd.extend(["--version", version])

    for vf in (values_files or []):
        if vf.exists():
            cmd.extend(["--values", str(vf)])

    log_info(f"Installing {release_name}")
    result = run_command(cmd, verbose=verbose, timeout=900, log=True)

    if not result.success:
        raise HelmError(f"Install failed: {result.stderr}")


def helm_upgrade(
    release_name: str,
    chart: str,
    namespace: str,
    values_files: Optional[list[Path]] = None,
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
        if vf.exists():
            cmd.extend(["--values", str(vf)])

    result = run_command(cmd)
    if not result.success:
        raise HelmError(f"Template failed: {result.stderr}")

    return result.stdout


def helm_dependency_build(chart: str, verbose: bool = False) -> None:
    """Build chart dependencies."""
    run_command(["helm", "dependency", "build", str(CHARTS_DIR / chart)], verbose=verbose)


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
