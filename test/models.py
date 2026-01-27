"""Pydantic models for test configuration."""

from typing import Optional
from pydantic import BaseModel, Field


class Dependency(BaseModel):
    """A single dependency specification."""
    name: str
    chart: str
    version: Optional[str] = None
    wait: str  # Resource to wait for (e.g., statefulset/postgresql)
    timeout: str = "300s"
    optional: bool = False
    values: Optional[dict] = None  # Inline values override


class ScenarioConfig(BaseModel):
    """Per-scenario configuration."""
    include: list[str] = Field(default_factory=list)  # Optional deps to include
    skip_upgrade: bool = False


class ChartTestConfig(BaseModel):
    """Test configuration for a chart."""
    dependencies: list[Dependency] = Field(default_factory=list)
    scenarios: dict[str, ScenarioConfig] = Field(default_factory=dict)

    def get_dependencies_for_scenario(self, scenario: str) -> list[Dependency]:
        """Get list of dependencies needed for a scenario."""
        # Start with required dependencies
        deps = [d for d in self.dependencies if not d.optional]

        # Add optional dependencies if scenario includes them
        if scenario in self.scenarios:
            include = self.scenarios[scenario].include
            deps.extend([d for d in self.dependencies if d.optional and d.name in include])

        return deps


class ScenarioResult(BaseModel):
    """Result of a single scenario test."""
    chart: str
    scenario: str
    success: bool
    duration: float
    error: Optional[str] = None
