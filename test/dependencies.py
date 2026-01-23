"""
Dependency lifecycle management for chart testing.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from test.config import (
    get_dependency_values_files,
    get_scenario_dependencies,
    load_chart_dependencies,
)
from test.helm import helm_install, helm_uninstall
from test.kubernetes import (
    create_database,
    create_namespace,
    delete_namespace,
    drop_database,
    wait_for_rollout,
)
from test.models import (
    ChartDependenciesConfig,
    DependencySpec,
    IsolationType,
    TestContext,
)
from test.utils import (
    DependencyError,
    log_debug,
    log_info,
    log_success,
    log_warning,
)


@dataclass
class InstalledDependency:
    """Tracks an installed dependency."""

    name: str
    release_name: str
    namespace: str
    spec: DependencySpec


@dataclass
class DependencyManager:
    """Manages dependency lifecycle for chart tests.

    This class handles installing, waiting for, and tearing down
    dependencies like PostgreSQL, Kafka, and Minio.
    """

    chart: str
    namespace: str
    verbose: bool = False
    config: Optional[ChartDependenciesConfig] = None
    installed: dict[str, InstalledDependency] = field(default_factory=dict)

    def __post_init__(self):
        if self.config is None:
            self.config = load_chart_dependencies(self.chart)

    def setup_dependencies(
        self,
        scenario: str,
        context: TestContext,
    ) -> None:
        """Set up all dependencies required for a scenario.

        Args:
            scenario: Scenario name
            context: Test context

        Raises:
            DependencyError: If setup fails
        """
        deps = get_scenario_dependencies(self.chart, scenario, self.config)

        if not deps:
            log_debug(f"No dependencies for scenario {scenario}", self.verbose)
            return

        log_info(f"Setting up {len(deps)} dependencies for {self.chart}/{scenario}")

        # Create namespace if needed
        create_namespace(self.namespace, verbose=self.verbose)

        for dep_spec in deps:
            dep_name = self._get_dep_name(dep_spec)

            # Skip if already installed
            if dep_name in self.installed:
                log_debug(f"Dependency {dep_name} already installed", self.verbose)
                continue

            self._install_dependency(dep_name, dep_spec)

        # Wait for all dependencies to be ready
        self._wait_for_dependencies()

        # Create scenario-specific isolation resources
        self._setup_isolation(scenario, context, deps)

        log_success(f"Dependencies ready for {self.chart}/{scenario}")

    def teardown_scenario(
        self,
        scenario: str,
        context: TestContext,
    ) -> None:
        """Clean up scenario-specific resources without removing shared deps.

        Args:
            scenario: Scenario name
            context: Test context
        """
        deps = get_scenario_dependencies(self.chart, scenario, self.config)

        for dep_spec in deps:
            if dep_spec.isolation:
                self._cleanup_isolation(scenario, context, dep_spec)

    def teardown_all(self) -> None:
        """Tear down all installed dependencies."""
        log_info("Tearing down all dependencies")

        for dep_name, installed in list(self.installed.items()):
            try:
                helm_uninstall(
                    installed.release_name,
                    installed.namespace,
                    verbose=self.verbose,
                )
                del self.installed[dep_name]
            except Exception as e:
                log_warning(f"Failed to uninstall {dep_name}: {e}")

    def _get_dep_name(self, dep_spec: DependencySpec) -> str:
        """Get a canonical name for a dependency."""
        # Use chart name as identifier (e.g., bitnami/postgresql -> postgresql)
        return dep_spec.chart.split("/")[-1]

    def _install_dependency(self, name: str, spec: DependencySpec) -> None:
        """Install a single dependency.

        Args:
            name: Dependency name
            spec: Dependency specification
        """
        release_name = spec.release_name or name
        namespace = spec.namespace or self.namespace

        log_info(f"Installing dependency: {name} ({spec.chart}@{spec.version})")

        # Get values files
        values_files = get_dependency_values_files(self.chart, spec)

        try:
            helm_install(
                release_name=release_name,
                chart=spec.chart,
                namespace=namespace,
                values_files=values_files,
                set_values={"image.repository": f"bitnamilegacy/{name}"}
                if "bitnami/" in spec.chart
                else None,
                wait=True,
                timeout=spec.timeout,
                verbose=self.verbose,
            )

            self.installed[name] = InstalledDependency(
                name=name,
                release_name=release_name,
                namespace=namespace,
                spec=spec,
            )

        except Exception as e:
            raise DependencyError(f"Failed to install {name}: {e}")

    def _wait_for_dependencies(self) -> None:
        """Wait for all installed dependencies to be ready."""
        for name, installed in self.installed.items():
            spec = installed.spec

            if not spec.wait_for:
                continue

            log_info(f"Waiting for {name} ({spec.wait_for})")

            try:
                wait_for_rollout(
                    spec.wait_for,
                    installed.namespace,
                    timeout=spec.timeout,
                    verbose=self.verbose,
                )
            except Exception as e:
                raise DependencyError(f"Dependency {name} not ready: {e}")

    def _setup_isolation(
        self,
        scenario: str,
        context: TestContext,
        deps: list[DependencySpec],
    ) -> None:
        """Set up scenario-specific isolation resources.

        Args:
            scenario: Scenario name
            context: Test context
            deps: List of dependencies
        """
        for dep_spec in deps:
            if not dep_spec.isolation:
                continue

            dep_name = self._get_dep_name(dep_spec)
            installed = self.installed.get(dep_name)

            if not installed:
                continue

            isolation_name = context.get_isolation_name(dep_spec.isolation.template)

            if dep_spec.isolation.type == IsolationType.DATABASE:
                self._create_database_isolation(installed, isolation_name)
            elif dep_spec.isolation.type == IsolationType.BUCKET:
                self._create_bucket_isolation(installed, isolation_name)
            elif dep_spec.isolation.type == IsolationType.TOPIC_PREFIX:
                # Topic prefixes don't need pre-creation
                log_debug(f"Using topic prefix: {isolation_name}", self.verbose)

    def _cleanup_isolation(
        self,
        scenario: str,
        context: TestContext,
        dep_spec: DependencySpec,
    ) -> None:
        """Clean up scenario-specific isolation resources.

        Args:
            scenario: Scenario name
            context: Test context
            dep_spec: Dependency specification
        """
        if not dep_spec.isolation:
            return

        dep_name = self._get_dep_name(dep_spec)
        installed = self.installed.get(dep_name)

        if not installed:
            return

        isolation_name = context.get_isolation_name(dep_spec.isolation.template)

        if dep_spec.isolation.type == IsolationType.DATABASE:
            self._drop_database_isolation(installed, isolation_name)
        elif dep_spec.isolation.type == IsolationType.BUCKET:
            self._drop_bucket_isolation(installed, isolation_name)

    def _create_database_isolation(
        self,
        installed: InstalledDependency,
        database: str,
    ) -> None:
        """Create an isolated PostgreSQL database.

        Args:
            installed: Installed dependency info
            database: Database name to create
        """
        pod_name = f"{installed.release_name}-0"

        try:
            create_database(
                pod_name=pod_name,
                namespace=installed.namespace,
                database=database,
                verbose=self.verbose,
            )
        except Exception as e:
            log_warning(f"Failed to create database {database}: {e}")

    def _drop_database_isolation(
        self,
        installed: InstalledDependency,
        database: str,
    ) -> None:
        """Drop an isolated PostgreSQL database.

        Args:
            installed: Installed dependency info
            database: Database name to drop
        """
        pod_name = f"{installed.release_name}-0"

        try:
            drop_database(
                pod_name=pod_name,
                namespace=installed.namespace,
                database=database,
                verbose=self.verbose,
            )
        except Exception as e:
            log_warning(f"Failed to drop database {database}: {e}")

    def _create_bucket_isolation(
        self,
        installed: InstalledDependency,
        bucket: str,
    ) -> None:
        """Create an isolated Minio bucket.

        Args:
            installed: Installed dependency info
            bucket: Bucket name to create
        """
        # Minio bucket creation via mc client
        log_debug(f"Bucket isolation not implemented: {bucket}", self.verbose)

    def _drop_bucket_isolation(
        self,
        installed: InstalledDependency,
        bucket: str,
    ) -> None:
        """Drop an isolated Minio bucket.

        Args:
            installed: Installed dependency info
            bucket: Bucket name to drop
        """
        log_debug(f"Bucket cleanup not implemented: {bucket}", self.verbose)


def setup_helm_repos(verbose: bool = False) -> None:
    """Ensure required Helm repositories are configured.

    Args:
        verbose: Enable verbose output
    """
    from test.helm import helm_repo_add, helm_repo_update

    log_info("Setting up Helm repositories")

    repos = [
        ("bitnami", "https://charts.bitnami.com/bitnami"),
        ("conduktor", "https://helm.conduktor.io"),
        ("ingress-nginx", "https://kubernetes.github.io/ingress-nginx"),
        ("redpanda", "https://charts.redpanda.com"),
    ]

    for name, url in repos:
        helm_repo_add(name, url, verbose=verbose)

    helm_repo_update(verbose=verbose)
