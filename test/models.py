"""Pydantic models for test configuration."""

from typing import Optional
from pydantic import BaseModel, Field


class DependencyInitConfig(BaseModel):
    """Initialization configuration for a dependency (database, bucket creation)."""
    database: Optional[str] = None  # PostgreSQL database name template
    bucket: Optional[str] = None  # Minio bucket name template
    user: Optional[str] = None
    password: Optional[str] = None


class Dependency(BaseModel):
    """A single dependency specification."""
    name: str
    chart: str
    version: Optional[str] = None
    wait: str  # Resource to wait for (e.g., statefulset/postgresql)
    timeout: str = "300s"
    values: Optional[dict] = None  # Inline values override
    init: Optional[DependencyInitConfig] = None  # Resource init config (database/bucket)


class ChartTestConfig(BaseModel):
    """Test configuration for a chart."""
    dependencies: list[Dependency] = Field(default_factory=list)

    def get_all_dependencies(self) -> list[Dependency]:
        """Get all dependencies."""
        return list(self.dependencies)

    def get_init_config_for_scenario(self, scenario_id: str) -> dict:
        """Get initialization config for a scenario.

        Returns dict with 'database' and 'bucket' keys if configured.
        """
        result = {}

        for dep in self.dependencies:
            if dep.init:
                if dep.init.database:
                    result['database'] = {
                        'name': dep.init.database.format(scenario_id=scenario_id),
                        'user': dep.init.user,
                        'password': dep.init.password,
                    }
                if dep.init.bucket:
                    result['bucket'] = {
                        'name': dep.init.bucket.format(scenario_id=scenario_id),
                        'user': dep.init.user,
                        'password': dep.init.password,
                    }

        return result


class ScenarioResult(BaseModel):
    """Result of a single scenario test."""
    chart: str
    scenario: str
    success: bool
    duration: float
    error: Optional[str] = None
