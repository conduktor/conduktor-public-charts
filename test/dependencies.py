"""Dependency lifecycle management."""

import tempfile
from pathlib import Path
from typing import Optional
import yaml

from test.config import get_shared_values_file, load_chart_config
from test.helm import helm_install, helm_uninstall
from test.kubernetes import kubectl_exec, wait_for_rollout
from test.models import Dependency
from test.utils import log_info, log_success, log_warning, log_error


class DependencyManager:
    """Manages dependency lifecycle for chart tests."""

    def __init__(self, chart: str, namespace: str, verbose: bool = False):
        self.chart = chart
        self.namespace = namespace
        self.verbose = verbose
        self.config = load_chart_config(chart)
        self.installed: list[str] = []

    def setup_all(self) -> None:
        """Install all dependencies.

        Dependencies are installed once in a shared namespace
        before running scenarios.
        """
        deps = self.config.get_all_dependencies()
        self._install_deps(deps)

    def init_scenario_resources(self, scenario_id: str) -> None:
        """Initialize resources (database, bucket) for a single scenario.

        This should be called at the beginning of each scenario test.
        """
        init_config = self.config.get_init_config_for_scenario(scenario_id)

        # Create PostgreSQL database if needed
        if 'database' in init_config and "postgresql" in self.installed:
            self._create_postgresql_database(init_config['database'])

        # Create Minio bucket if needed
        if 'bucket' in init_config and "minio" in self.installed:
            self._create_minio_bucket(init_config['bucket'])

    def _get_pod_name(self, label_selector: str) -> Optional[str]:
        """Get pod name by label selector."""
        from test.utils import run_command
        result = run_command([
            "kubectl", "get", "pods", "-n", self.namespace,
            "-l", label_selector,
            "-o", "jsonpath={.items[0].metadata.name}"
        ], verbose=self.verbose)
        return result.stdout.strip() if result.success and result.stdout.strip() else None

    def _create_postgresql_database(self, config: dict) -> None:
        """Create a single database in PostgreSQL.

        Args:
            config: Dict with 'name', 'user', 'password' keys
        """
        db_name = config['name']
        user = config.get('user', 'postgres')
        password = config.get('password', '')

        log_info(f"Creating PostgreSQL database: {db_name}")

        # Use psql with PGPASSWORD env var to create database if not exists
        sql = f"SELECT 'CREATE DATABASE {db_name}' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '{db_name}')\\gexec"
        success, stdout, stderr = kubectl_exec(
            pod="postgresql-0",
            namespace=self.namespace,
            command=[
                "sh", "-c",
                f"echo \"{sql}\" | PGPASSWORD='{password}' psql -U {user}"
            ],
            verbose=self.verbose,
        )

        if success:
            log_success(f"PostgreSQL database ready: {db_name}")
        else:
            log_warning(f"Failed to create database {db_name}: {stderr}")

    def _create_minio_bucket(self, config: dict) -> None:
        """Create a single bucket in Minio using mc (minio client).

        Args:
            config: Dict with 'name', 'user', 'password' keys
        """
        bucket_name = config['name']
        user = config.get('user', 'admin')
        password = config.get('password', '')

        log_info(f"Creating Minio bucket: {bucket_name}")

        # Find minio pod - it's a deployment so name is minio-xxxxx
        pod_name = self._get_pod_name("app.kubernetes.io/name=minio")
        if not pod_name:
            log_warning("Could not find minio pod, skipping bucket creation")
            return

        # Use mc to create bucket - mc is included in bitnami minio image
        # First configure mc alias, then create bucket
        success, stdout, stderr = kubectl_exec(
            pod=pod_name,
            namespace=self.namespace,
            command=[
                "sh", "-c",
                f"mc alias set local http://localhost:9000 {user} {password} && "
                f"mc mb --ignore-existing local/{bucket_name}"
            ],
            verbose=self.verbose,
        )

        if success:
            log_success(f"Minio bucket ready: {bucket_name}")
        else:
            log_warning(f"Failed to create bucket {bucket_name}: {stderr}")

    def _install_deps(self, deps: list[Dependency]) -> None:
        """Install a list of dependencies with parallel install."""
        if not deps:
            return

        log_info(f"Setting up {len(deps)} dependencies (parallel install)")

        # Phase 1: Install all dependencies without waiting
        deps_to_wait = []
        for dep in deps:
            if dep.name in self.installed:
                continue
            self._install(dep, wait=False)
            self.installed.append(dep.name)
            deps_to_wait.append(dep)

        # Phase 2: Wait for all dependencies to be ready
        if deps_to_wait:
            log_info(f"Waiting for {len(deps_to_wait)} dependencies to be ready")
            for dep in deps_to_wait:
                wait_for_rollout(dep.wait, self.namespace, dep.timeout, self.verbose)

        log_success("Dependencies ready")

    def teardown(self) -> None:
        """Uninstall all dependencies."""
        for name in reversed(self.installed):
            try:
                helm_uninstall(name, self.namespace, verbose=self.verbose)
            except Exception as e:
                log_warning(f"Failed to uninstall {name}: {e}")

        self.installed.clear()

    def _install(self, dep: Dependency, wait: bool = True) -> None:
        """Install a single dependency."""
        # Collect values files
        values_files = []

        # Add shared values if exists
        shared = get_shared_values_file(dep.name)
        if shared:
            values_files.append(shared)

        # Handle inline values
        inline_values_file = None
        if dep.values:
            f = tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False)
            yaml.dump(dep.values, f)
            f.close()
            inline_values_file = Path(f.name)
            values_files.append(inline_values_file)

        try:
            helm_install(
                release_name=dep.name,
                chart=dep.chart,
                namespace=self.namespace,
                values_files=values_files,
                version=dep.version,
                timeout=dep.timeout,
                wait=wait,
                verbose=self.verbose,
            )

            # Wait for resource only if wait=True
            if wait:
                wait_for_rollout(dep.wait, self.namespace, dep.timeout, self.verbose)

        finally:
            if inline_values_file:
                inline_values_file.unlink(missing_ok=True)


def setup_helm_repos(verbose: bool = False) -> None:
    """Add required Helm repositories."""
    from test.helm import helm_repo_add, helm_repo_update

    repos = [
        ("bitnami", "https://charts.bitnami.com/bitnami"),
        ("conduktor", "https://helm.conduktor.io"),
    ]

    for name, url in repos:
        helm_repo_add(name, url, verbose)

    helm_repo_update(verbose)
