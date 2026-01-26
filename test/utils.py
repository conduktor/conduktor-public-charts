"""Utility functions for the test framework."""

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.table import Table

# Paths
ROOT_DIR = Path(__file__).parent.parent.resolve()
CHARTS_DIR = ROOT_DIR / "charts"
SHARED_DEPS_DIR = ROOT_DIR / "test" / "shared-deps"

# Console for rich output
console = Console()


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
    console.print(f"[dim]$ {' '.join(cmd)}[/dim]")


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
    console.print(f"[blue]INFO[/blue] {msg}")


def log_success(msg: str) -> None:
    console.print(f"[green]OK[/green] {msg}")


def log_warning(msg: str) -> None:
    console.print(f"[yellow]WARN[/yellow] {msg}")


def log_error(msg: str) -> None:
    console.print(f"[red]ERROR[/red] {msg}")


def log_step(step: str, msg: str) -> None:
    console.print(f"[cyan]STEP {step}[/cyan] {msg}")


def print_summary(results: list[tuple[str, str, bool, Optional[str]]]) -> None:
    """Print test results summary."""
    table = Table(title="Test Results")
    table.add_column("Chart")
    table.add_column("Scenario")
    table.add_column("Status")
    table.add_column("Error")

    for chart, scenario, success, error in results:
        status = "[green]PASS[/green]" if success else "[red]FAIL[/red]"
        table.add_row(chart, scenario, status, error or "")

    console.print(table)


def get_charts() -> list[str]:
    """Get list of chart names."""
    return sorted([d.name for d in CHARTS_DIR.iterdir() if (d / "Chart.yaml").exists()])
