"""Kubernetes operations wrapper."""

import json
from typing import Optional

from test.utils import KubernetesError, log_info, run_command


def create_namespace(namespace: str, verbose: bool = False) -> None:
    """Create namespace if it doesn't exist."""
    result = run_command(["kubectl", "get", "namespace", namespace], verbose=verbose)
    if result.success:
        return

    result = run_command(["kubectl", "create", "namespace", namespace], verbose=verbose)
    if not result.success:
        raise KubernetesError(f"Failed to create namespace: {result.stderr}")

    log_info(f"Created namespace: {namespace}")


def delete_namespace(namespace: str, verbose: bool = False) -> None:
    """Delete namespace."""
    log_info(f"Deleting namespace: {namespace}")
    run_command(
        ["kubectl", "delete", "namespace", namespace, "--ignore-not-found", "--wait=true", "--timeout=120s"],
        verbose=verbose,
        timeout=150,
        log=True,
    )


def wait_for_rollout(resource: str, namespace: str, timeout: str = "300s", verbose: bool = False) -> None:
    """Wait for a rollout to complete."""
    log_info(f"Waiting for {resource}")
    timeout_sec = int(timeout.rstrip("s"))

    result = run_command(
        ["kubectl", "rollout", "status", resource, "--namespace", namespace, f"--timeout={timeout}"],
        verbose=verbose,
        timeout=timeout_sec + 30,
        log=True,
    )

    if not result.success:
        raise KubernetesError(f"Rollout failed: {result.stderr}")


def get_current_context() -> Optional[str]:
    """Get current kubectl context."""
    result = run_command(["kubectl", "config", "current-context"])
    return result.stdout.strip() if result.success else None


def get_pods(namespace: str) -> str:
    """Get pods in namespace."""
    result = run_command(["kubectl", "get", "pods", "-n", namespace])
    return result.stdout


def get_events(namespace: str) -> str:
    """Get events in namespace."""
    result = run_command(["kubectl", "get", "events", "-n", namespace, "--sort-by=.lastTimestamp"])
    return result.stdout


def get_pods_status(namespace: str) -> list[dict]:
    """Get pods with detailed status information."""
    result = run_command([
        "kubectl", "get", "pods", "-n", namespace,
        "-o", "json"
    ])
    if not result.success:
        return []

    try:
        data = json.loads(result.stdout)
        pods = []
        for item in data.get("items", []):
            name = item.get("metadata", {}).get("name", "unknown")
            status = item.get("status", {})
            phase = status.get("phase", "Unknown")

            # Get container statuses
            containers = []
            for cs in status.get("containerStatuses", []):
                container = {
                    "name": cs.get("name"),
                    "ready": cs.get("ready", False),
                    "restartCount": cs.get("restartCount", 0),
                }
                # Get state
                state = cs.get("state", {})
                if "running" in state:
                    container["state"] = "Running"
                elif "waiting" in state:
                    container["state"] = f"Waiting: {state['waiting'].get('reason', 'Unknown')}"
                    container["message"] = state["waiting"].get("message", "")
                elif "terminated" in state:
                    container["state"] = f"Terminated: {state['terminated'].get('reason', 'Unknown')}"
                    container["exitCode"] = state["terminated"].get("exitCode")
                containers.append(container)

            pods.append({
                "name": name,
                "phase": phase,
                "containers": containers,
                "ready": all(c.get("ready", False) for c in containers) if containers else False,
            })
        return pods
    except json.JSONDecodeError:
        return []


def get_unhealthy_pods(namespace: str) -> list[str]:
    """Get list of unhealthy pod names."""
    pods = get_pods_status(namespace)
    unhealthy = []
    for pod in pods:
        if pod["phase"] not in ("Running", "Succeeded") or not pod["ready"]:
            unhealthy.append(pod["name"])
    return unhealthy


def describe_pod(pod_name: str, namespace: str) -> str:
    """Get pod description."""
    result = run_command(["kubectl", "describe", "pod", pod_name, "-n", namespace])
    return result.stdout if result.success else result.stderr


def get_pod_logs(pod_name: str, namespace: str, container: Optional[str] = None, tail: int = 100) -> str:
    """Get pod logs."""
    cmd = ["kubectl", "logs", pod_name, "-n", namespace, f"--tail={tail}"]
    if container:
        cmd.extend(["-c", container])
    # Also get previous logs if container crashed
    result = run_command(cmd)
    output = result.stdout if result.success else result.stderr

    # Try to get previous logs too
    prev_cmd = cmd + ["--previous"]
    prev_result = run_command(prev_cmd)
    if prev_result.success and prev_result.stdout.strip():
        output += f"\n--- Previous logs ---\n{prev_result.stdout}"

    return output


def print_debug_info(namespace: str) -> None:
    """Print comprehensive debug information for a namespace."""
    from test.utils import BOLD, RESET, RED, YELLOW, GREEN, DIM, _print

    _print(f"\n{BOLD}{RED}━━━ DEBUG INFO ━━━{RESET}")

    # Pods status
    _print(f"\n{BOLD}{YELLOW}Pods:{RESET}")
    pods = get_pods_status(namespace)
    if not pods:
        _print("  No pods found")
    else:
        for pod in pods:
            status_icon = "✓" if pod["ready"] and pod["phase"] == "Running" else "✗"
            color = GREEN if pod["ready"] and pod["phase"] == "Running" else RED
            _print(f"  {color}{status_icon}{RESET} {pod['name']} - {pod['phase']}")
            for c in pod["containers"]:
                c_icon = "✓" if c.get("ready") else "✗"
                c_color = GREEN if c.get("ready") else RED
                restarts = f" (restarts: {c['restartCount']})" if c.get("restartCount", 0) > 0 else ""
                _print(f"      {c_color}{c_icon}{RESET} {c['name']}: {c.get('state', 'Unknown')}{restarts}")
                if c.get("message"):
                    _print(f"         {c['message']}")

    # Unhealthy pods details
    unhealthy = get_unhealthy_pods(namespace)
    if unhealthy:
        _print(f"\n{BOLD}{YELLOW}Unhealthy Pod Details:{RESET}")
        for pod_name in unhealthy[:3]:  # Limit to first 3 unhealthy pods
            _print(f"\n{BOLD}--- {pod_name} ---{RESET}")

            # Describe
            _print(f"\n{DIM}Description (last 50 lines):{RESET}")
            desc = describe_pod(pod_name, namespace)
            desc_lines = desc.strip().split("\n")
            _print("\n".join(desc_lines[-50:]))

            # Logs
            _print(f"\n{DIM}Logs (last 50 lines):{RESET}")
            logs = get_pod_logs(pod_name, namespace, tail=50)
            _print(logs if logs.strip() else "  No logs available")

    # Recent events
    _print(f"\n{BOLD}{YELLOW}Recent Events:{RESET}")
    events = get_events(namespace)
    if events.strip():
        event_lines = events.strip().split("\n")
        _print("\n".join(event_lines[-20:]))  # Last 20 events
    else:
        _print("  No events")

    _print(f"\n{BOLD}{RED}━━━━━━━━━━━━━━━━━{RESET}\n")
