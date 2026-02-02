"""Utility functions for the test framework."""

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# Paths
ROOT_DIR = Path(__file__).parent.parent.resolve()
CHARTS_DIR = ROOT_DIR / "charts"
SHARED_DEPS_DIR = ROOT_DIR / "test" / "shared-deps"

# Detect CI environment
IS_CI = os.environ.get("CI", "").lower() == "true"
IS_GITHUB_ACTIONS = os.environ.get("GITHUB_ACTIONS", "").lower() == "true"

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"


def _print(msg: str) -> None:
    """Print message and flush."""
    print(msg, flush=True)


# Exceptions
class TestError(Exception):
    pass


class HelmError(TestError):
    pass


class KubernetesError(TestError):
    pass


@dataclass
class CommandResult:
    returncode: int
    stdout: str
    stderr: str

    @property
    def success(self) -> bool:
        return self.returncode == 0


def log_command(cmd: list[str]) -> None:
    """Log a command that is about to be executed."""
    _print(f"{DIM}$ {' '.join(cmd)}{RESET}")


def run_command(
    cmd: list[str],
    verbose: bool = False,
    timeout: Optional[int] = None,
    log: bool = False,
) -> CommandResult:
    """Run a command and return the result."""
    if verbose or log:
        log_command(cmd)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return CommandResult(result.returncode, result.stdout, result.stderr)
    except subprocess.TimeoutExpired:
        return CommandResult(1, "", f"Command timed out after {timeout}s")
    except FileNotFoundError:
        return CommandResult(127, "", f"Command not found: {cmd[0]}")


def log_info(msg: str) -> None:
    _print(f"{BLUE}INFO{RESET} {msg}")


def log_success(msg: str) -> None:
    _print(f"{GREEN}OK{RESET} {msg}")


def log_warning(msg: str) -> None:
    prefix = "::warning::" if IS_GITHUB_ACTIONS else ""
    _print(f"{prefix}{YELLOW}WARN{RESET} {msg}")


def log_error(msg: str) -> None:
    prefix = "::error::" if IS_GITHUB_ACTIONS else ""
    _print(f"{prefix}{RED}ERROR{RESET} {msg}")


def log_step(step: str, msg: str) -> None:
    _print(f"{CYAN}STEP {step}{RESET} {msg}")


class timed_step:
    """Context manager that logs step execution time.

    Usage:
        with timed_step("1", "Create namespace"):
            create_namespace(namespace)
    """

    def __init__(self, step: str, msg: str):
        self.step = step
        self.msg = msg
        self.start = 0.0

    def __enter__(self):
        import time
        self.start = time.time()
        _print(f"{CYAN}STEP {self.step}{RESET} {self.msg}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        duration = time.time() - self.start
        if exc_type is None:
            _print(f"{DIM}  └─ done in {duration:.1f}s{RESET}")
        else:
            _print(f"{DIM}  └─ failed after {duration:.1f}s{RESET}")
        return False  # Don't suppress exceptions


# GitHub Actions grouping
def gh_group_start(title: str) -> None:
    """Start a collapsible group in GitHub Actions."""
    if IS_GITHUB_ACTIONS:
        _print(f"::group::{title}")


def gh_group_end() -> None:
    """End a collapsible group in GitHub Actions."""
    if IS_GITHUB_ACTIONS:
        _print("::endgroup::")


def print_summary(results: list[tuple[str, str, bool, Optional[str]]]) -> None:
    """Print test results summary."""
    _print(f"\n{BOLD}{'=' * 60}{RESET}")
    _print(f"{BOLD}Test Results{RESET}")
    _print(f"{BOLD}{'=' * 60}{RESET}")

    for chart, scenario, success, error in results:
        status = f"{GREEN}PASS{RESET}" if success else f"{RED}FAIL{RESET}"
        line = f"  {status} {chart}/{scenario}"
        if error:
            line += f" - {DIM}{error}{RESET}"
        _print(line)

    # Summary counts
    passed = sum(1 for _, _, s, _ in results if s)
    failed = len(results) - passed
    _print(f"{BOLD}{'=' * 60}{RESET}")
    _print(f"Total: {len(results)} | {GREEN}Passed: {passed}{RESET} | {RED}Failed: {failed}{RESET}")
    _print(f"{BOLD}{'=' * 60}{RESET}\n")


def get_charts() -> list[str]:
    """Get list of chart names."""
    return sorted([d.name for d in CHARTS_DIR.iterdir() if (d / "Chart.yaml").exists()])
