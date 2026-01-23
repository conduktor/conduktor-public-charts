"""
Pydantic models for test configuration validation.
"""

from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class IsolationType(str, Enum):
    """Type of isolation for shared dependencies."""

    DATABASE = "database"  # PostgreSQL: separate database per scenario
    TOPIC_PREFIX = "topic_prefix"  # Kafka: topic prefix per scenario
    BUCKET = "bucket"  # Minio: separate bucket per scenario
    NAMESPACE = "namespace"  # Full namespace isolation


class IsolationConfig(BaseModel):
    """Configuration for dependency isolation."""

    type: IsolationType
    template: str = Field(
        default="{chart}_{scenario}",
        description="Template for isolation resource name. Supports {chart} and {scenario} placeholders.",
    )


class DependencySpec(BaseModel):
    """Specification for a single dependency."""

    chart: str = Field(..., description="Helm chart reference (e.g., bitnami/postgresql)")
    version: str = Field(..., description="Chart version")
    values_file: Optional[str] = Field(
        default=None,
        description="Path to base values file (relative to repo root)",
    )
    chart_values_file: Optional[str] = Field(
        default=None,
        description="Path to chart-specific values override (relative to chart dir)",
    )
    release_name: Optional[str] = Field(
        default=None,
        description="Helm release name (defaults to dependency name)",
    )
    namespace: Optional[str] = Field(
        default=None,
        description="Kubernetes namespace (defaults to test namespace)",
    )
    wait_for: str = Field(
        ...,
        description="Kubernetes resource to wait for (e.g., statefulset/postgresql)",
    )
    timeout: str = Field(
        default="300s",
        description="Timeout for dependency to be ready",
    )
    isolation: Optional[IsolationConfig] = Field(
        default=None,
        description="Isolation configuration for shared dependencies",
    )


class ScenarioConfig(BaseModel):
    """Configuration for a specific test scenario."""

    dependencies: list[str] = Field(
        default_factory=list,
        description="List of dependency names required for this scenario",
    )
    skip_upgrade: bool = Field(
        default=False,
        description="Skip upgrade test for this scenario",
    )
    extra_values: Optional[dict] = Field(
        default=None,
        description="Extra Helm values to merge for this scenario",
    )


class ChartDependenciesConfig(BaseModel):
    """Root configuration for a chart's test dependencies."""

    shared_dependencies: dict[str, DependencySpec] = Field(
        default_factory=dict,
        description="Shared dependencies that can be reused across scenarios",
    )
    scenarios: dict[str, ScenarioConfig] = Field(
        default_factory=dict,
        description="Per-scenario configuration overrides",
    )
    default_dependencies: list[str] = Field(
        default_factory=list,
        description="Default dependencies if scenario doesn't specify any",
    )


class TestContext(BaseModel):
    """Runtime context for a test execution."""

    chart: str
    scenario: str
    namespace: str
    upgrade_enabled: bool = True
    verbose: bool = False

    @property
    def release_name(self) -> str:
        """Generate Helm release name for this test."""
        return f"{self.chart}-test"

    def get_isolation_name(self, template: str) -> str:
        """Generate an isolation resource name from template."""
        return (
            template.replace("{chart}", self.chart)
            .replace("{scenario}", self.scenario.replace("-", "_"))
        )


class ScenarioResult(BaseModel):
    """Result of a single scenario test."""

    chart: str
    scenario: str
    success: bool
    duration_seconds: float
    error_message: Optional[str] = None
    upgrade_tested: bool = False

    class Config:
        frozen = True


class ChartTestResult(BaseModel):
    """Result of testing all scenarios for a chart."""

    chart: str
    scenarios: list[ScenarioResult]
    total_duration_seconds: float

    @property
    def all_passed(self) -> bool:
        return all(s.success for s in self.scenarios)

    @property
    def passed_count(self) -> int:
        return sum(1 for s in self.scenarios if s.success)

    @property
    def failed_count(self) -> int:
        return sum(1 for s in self.scenarios if not s.success)
