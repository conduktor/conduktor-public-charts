"""
Kubernetes operations wrapper using kubectl.
"""

import json
import time
from typing import Optional

from test.utils import (
    KubernetesError,
    log_debug,
    log_info,
    log_warning,
    run_command,
)


def create_namespace(namespace: str, verbose: bool = False) -> None:
    """Create a Kubernetes namespace if it doesn't exist.

    Args:
        namespace: Namespace name
        verbose: Enable verbose output
    """
    # Check if namespace exists
    result = run_command(
        ["kubectl", "get", "namespace", namespace],
        verbose=verbose,
    )

    if result.success:
        log_debug(f"Namespace {namespace} already exists", verbose)
        return

    # Create namespace
    result = run_command(
        ["kubectl", "create", "namespace", namespace],
        verbose=verbose,
    )

    if not result.success:
        raise KubernetesError(f"Failed to create namespace {namespace}: {result.stderr}")

    log_info(f"Created namespace: {namespace}")


def delete_namespace(
    namespace: str,
    wait: bool = True,
    timeout: int = 120,
    verbose: bool = False,
) -> None:
    """Delete a Kubernetes namespace.

    Args:
        namespace: Namespace name
        wait: Wait for deletion to complete
        timeout: Timeout in seconds
        verbose: Enable verbose output
    """
    cmd = ["kubectl", "delete", "namespace", namespace, "--ignore-not-found"]

    if wait:
        cmd.extend(["--wait=true", f"--timeout={timeout}s"])

    log_info(f"Deleting namespace: {namespace}")
    result = run_command(cmd, timeout=timeout + 30, verbose=verbose)

    if not result.success:
        log_warning(f"Namespace deletion warning: {result.stderr}")


def wait_for_resource(
    resource: str,
    namespace: str,
    condition: str = "Available",
    timeout: str = "300s",
    verbose: bool = False,
) -> None:
    """Wait for a Kubernetes resource to meet a condition.

    Args:
        resource: Resource reference (e.g., deployment/my-app, statefulset/db)
        namespace: Kubernetes namespace
        condition: Condition to wait for
        timeout: Timeout string (e.g., "300s")
        verbose: Enable verbose output

    Raises:
        KubernetesError: If wait times out or fails
    """
    log_info(f"Waiting for {resource} to be {condition}")

    # Parse timeout to seconds for subprocess
    timeout_seconds = int(timeout.rstrip("s"))

    result = run_command(
        [
            "kubectl",
            "wait",
            resource,
            "--namespace",
            namespace,
            f"--for=condition={condition}",
            f"--timeout={timeout}",
        ],
        timeout=timeout_seconds + 30,
        verbose=verbose,
    )

    if not result.success:
        raise KubernetesError(f"Wait for {resource} failed: {result.stderr}")


def wait_for_rollout(
    resource: str,
    namespace: str,
    timeout: str = "300s",
    verbose: bool = False,
) -> None:
    """Wait for a rollout to complete.

    Args:
        resource: Resource reference (e.g., deployment/my-app, statefulset/db)
        namespace: Kubernetes namespace
        timeout: Timeout string
        verbose: Enable verbose output

    Raises:
        KubernetesError: If rollout times out or fails
    """
    log_info(f"Waiting for rollout: {resource}")

    timeout_seconds = int(timeout.rstrip("s"))

    result = run_command(
        [
            "kubectl",
            "rollout",
            "status",
            resource,
            "--namespace",
            namespace,
            f"--timeout={timeout}",
        ],
        timeout=timeout_seconds + 30,
        verbose=verbose,
    )

    if not result.success:
        raise KubernetesError(f"Rollout status for {resource} failed: {result.stderr}")


def get_pods(namespace: str, verbose: bool = False) -> list[dict]:
    """Get pods in a namespace.

    Args:
        namespace: Kubernetes namespace
        verbose: Enable verbose output

    Returns:
        List of pod info dictionaries
    """
    result = run_command(
        [
            "kubectl",
            "get",
            "pods",
            "--namespace",
            namespace,
            "-o",
            "json",
        ],
        verbose=verbose,
    )

    if not result.success:
        return []

    try:
        data = json.loads(result.stdout)
        return data.get("items", [])
    except json.JSONDecodeError:
        return []


def get_pod_logs(
    pod_name: str,
    namespace: str,
    container: Optional[str] = None,
    tail: int = 100,
    verbose: bool = False,
) -> str:
    """Get logs from a pod.

    Args:
        pod_name: Pod name
        namespace: Kubernetes namespace
        container: Container name (optional)
        tail: Number of lines to tail
        verbose: Enable verbose output

    Returns:
        Pod logs
    """
    cmd = [
        "kubectl",
        "logs",
        pod_name,
        "--namespace",
        namespace,
        f"--tail={tail}",
    ]

    if container:
        cmd.extend(["--container", container])

    result = run_command(cmd, verbose=verbose)
    return result.stdout


def get_events(namespace: str, verbose: bool = False) -> str:
    """Get events in a namespace, sorted by time.

    Args:
        namespace: Kubernetes namespace
        verbose: Enable verbose output

    Returns:
        Events output
    """
    result = run_command(
        [
            "kubectl",
            "get",
            "events",
            "--namespace",
            namespace,
            "--sort-by=.lastTimestamp",
        ],
        verbose=verbose,
    )
    return result.stdout


def exec_in_pod(
    pod_name: str,
    namespace: str,
    command: list[str],
    container: Optional[str] = None,
    verbose: bool = False,
) -> str:
    """Execute a command in a pod.

    Args:
        pod_name: Pod name
        namespace: Kubernetes namespace
        command: Command to execute
        container: Container name (optional)
        verbose: Enable verbose output

    Returns:
        Command output

    Raises:
        KubernetesError: If command fails
    """
    cmd = [
        "kubectl",
        "exec",
        pod_name,
        "--namespace",
        namespace,
        "--",
    ]

    if container:
        cmd.insert(3, "-c")
        cmd.insert(4, container)

    cmd.extend(command)

    result = run_command(cmd, verbose=verbose)

    if not result.success:
        raise KubernetesError(f"exec in {pod_name} failed: {result.stderr}")

    return result.stdout


def create_database(
    pod_name: str,
    namespace: str,
    database: str,
    user: str = "postgres",
    verbose: bool = False,
) -> None:
    """Create a PostgreSQL database.

    Args:
        pod_name: PostgreSQL pod name
        namespace: Kubernetes namespace
        database: Database name to create
        user: Database user
        verbose: Enable verbose output
    """
    log_info(f"Creating database: {database}")

    # Check if database exists
    check_cmd = [
        "psql",
        "-U",
        user,
        "-tc",
        f"SELECT 1 FROM pg_database WHERE datname = '{database}'",
    ]

    try:
        result = exec_in_pod(pod_name, namespace, check_cmd, verbose=verbose)
        if "1" in result:
            log_debug(f"Database {database} already exists", verbose)
            return
    except KubernetesError:
        pass  # Database check failed, try to create

    # Create database
    create_cmd = ["createdb", "-U", user, database]

    try:
        exec_in_pod(pod_name, namespace, create_cmd, verbose=verbose)
        log_info(f"Created database: {database}")
    except KubernetesError as e:
        log_warning(f"Database creation warning: {e}")


def drop_database(
    pod_name: str,
    namespace: str,
    database: str,
    user: str = "postgres",
    verbose: bool = False,
) -> None:
    """Drop a PostgreSQL database.

    Args:
        pod_name: PostgreSQL pod name
        namespace: Kubernetes namespace
        database: Database name to drop
        user: Database user
        verbose: Enable verbose output
    """
    log_info(f"Dropping database: {database}")

    # Force disconnect connections
    disconnect_cmd = [
        "psql",
        "-U",
        user,
        "-c",
        f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{database}'",
    ]

    try:
        exec_in_pod(pod_name, namespace, disconnect_cmd, verbose=verbose)
    except KubernetesError:
        pass  # Ignore errors

    # Drop database
    drop_cmd = ["dropdb", "-U", user, "--if-exists", database]

    try:
        exec_in_pod(pod_name, namespace, drop_cmd, verbose=verbose)
    except KubernetesError as e:
        log_warning(f"Database drop warning: {e}")


def check_current_context(expected_context: str = "k3d-conduktor-platform") -> bool:
    """Check if the current kubectl context matches expected.

    Args:
        expected_context: Expected context name

    Returns:
        True if context matches
    """
    result = run_command(["kubectl", "config", "current-context"])

    if not result.success:
        return False

    current = result.stdout.strip()
    return current == expected_context


def get_current_context() -> Optional[str]:
    """Get the current kubectl context name.

    Returns:
        Context name or None
    """
    result = run_command(["kubectl", "config", "current-context"])

    if result.success:
        return result.stdout.strip()
    return None
