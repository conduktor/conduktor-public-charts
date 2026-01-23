"""
Utility functions for logging, output formatting, and common operations.
"""

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

# Global console for rich output
console = Console()

# Project root directory
ROOT_DIR = Path(__file__).parent.parent.resolve()
CHARTS_DIR = ROOT_DIR / "charts"
TEST_DIR = ROOT_DIR / "test"
SHARED_DEPS_DIR = TEST_DIR / "shared-deps"


@dataclass
class CommandResult:
    """Result of a subprocess command execution."""

    returncode: int
    stdout: str
    stderr: str
    command: str

    @property
    def success(self) -> bool:
        return self.returncode == 0


class TestError(Exception):
    """Base exception for test framework errors."""

    pass


class HelmError(TestError):
    """Error during Helm operations."""

    pass


class KubernetesError(TestError):
    """Error during Kubernetes operations."""

    pass


class DependencyError(TestError):
    """Error during dependency management."""

    pass


class ConfigError(TestError):
    """Error loading or parsing configuration."""

    pass


def log_info(message: str) -> None:
    """Log an info message."""
    console.print(f"[blue]INFO[/blue] {message}")


def log_success(message: str) -> None:
    """Log a success message."""
    console.print(f"[green]OK[/green] {message}")


def log_warning(message: str) -> None:
    """Log a warning message."""
    console.print(f"[yellow]WARN[/yellow] {message}")


def log_error(message: str) -> None:
    """Log an error message."""
    console.print(f"[red]ERROR[/red] {message}")


def log_debug(message: str, verbose: bool = False) -> None:
    """Log a debug message (only if verbose mode is enabled)."""
    if verbose:
        console.print(f"[dim]DEBUG[/dim] {message}")


def log_step(step: str, description: str) -> None:
    """Log a test step."""
    console.print(f"[cyan]STEP[/cyan] [{step}] {description}")


def log_scenario(chart: str, scenario: str) -> None:
    """Log the start of a test scenario."""
    console.print(
        Panel(
            f"[bold]{chart}[/bold] / [cyan]{scenario}[/cyan]",
            title="Running Scenario",
            border_style="blue",
        )
    )


def log_chart(chart: str) -> None:
    """Log the start of chart testing."""
    console.print(
        Panel(
            f"[bold white on blue] {chart.upper()} [/bold white on blue]",
            title="Testing Chart",
            border_style="bold blue",
        )
    )


def print_summary(results: list[tuple[str, str, bool, Optional[str]]]) -> None:
    """Print a summary table of test results.

    Args:
        results: List of (chart, scenario, success, error_message) tuples
    """
    table = Table(title="Test Results Summary")
    table.add_column("Chart", style="cyan")
    table.add_column("Scenario", style="magenta")
    table.add_column("Status")
    table.add_column("Details")

    for chart, scenario, success, error in results:
        status = "[green]PASSED[/green]" if success else "[red]FAILED[/red]"
        details = error or ""
        table.add_row(chart, scenario, status, details)

    console.print(table)


def run_command(
    command: list[str],
    capture_output: bool = True,
    check: bool = False,
    timeout: Optional[int] = None,
    cwd: Optional[Path] = None,
    env: Optional[dict] = None,
    verbose: bool = False,
) -> CommandResult:
    """Run a subprocess command and return the result.

    Args:
        command: Command and arguments as a list
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise an exception on non-zero exit
        timeout: Command timeout in seconds
        cwd: Working directory for the command
        env: Environment variables
        verbose: Whether to log debug output

    Returns:
        CommandResult with returncode, stdout, stderr

    Raises:
        TestError: If check=True and command fails
    """
    cmd_str = " ".join(command)
    log_debug(f"Running: {cmd_str}", verbose)

    try:
        result = subprocess.run(
            command,
            capture_output=capture_output,
            text=True,
            timeout=timeout,
            cwd=cwd,
            env=env,
        )

        cmd_result = CommandResult(
            returncode=result.returncode,
            stdout=result.stdout if capture_output else "",
            stderr=result.stderr if capture_output else "",
            command=cmd_str,
        )

        if check and not cmd_result.success:
            log_error(f"Command failed: {cmd_str}")
            if cmd_result.stderr:
                log_error(f"stderr: {cmd_result.stderr}")
            raise TestError(f"Command failed with exit code {cmd_result.returncode}")

        return cmd_result

    except subprocess.TimeoutExpired:
        raise TestError(f"Command timed out after {timeout}s: {cmd_str}")


def create_spinner(message: str) -> Progress:
    """Create a spinner progress indicator."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    )


def confirm(message: str, default: bool = False) -> bool:
    """Ask for user confirmation.

    Args:
        message: The confirmation message
        default: Default value if user just presses enter

    Returns:
        True if confirmed, False otherwise
    """
    suffix = " [Y/n]" if default else " [y/N]"
    response = console.input(f"{message}{suffix} ").strip().lower()

    if not response:
        return default
    return response in ("y", "yes")


def get_chart_names() -> list[str]:
    """Get list of available chart names."""
    charts = []
    for chart_dir in CHARTS_DIR.iterdir():
        if chart_dir.is_dir() and (chart_dir / "Chart.yaml").exists():
            charts.append(chart_dir.name)
    return sorted(charts)


def get_scenario_names(chart: str) -> list[str]:
    """Get list of scenario names for a chart."""
    ci_dir = CHARTS_DIR / chart / "ci"
    if not ci_dir.exists():
        return []

    scenarios = []
    for values_file in ci_dir.glob("*-values.yaml"):
        # Extract scenario name: "01-basic-values.yaml" -> "01-basic"
        name = values_file.stem.replace("-values", "")
        scenarios.append(name)

    return sorted(scenarios)
