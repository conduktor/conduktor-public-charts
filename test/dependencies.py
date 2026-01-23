"""Dependency lifecycle management."""

import tempfile
from pathlib import Path
from typing import Optional
import yaml

from test.config import get_shared_values_file, load_chart_config
from test.helm import helm_install, helm_uninstall
from test.kubernetes import wait_for_rollout
from test.models import Dependency
from test.utils import log_info, log_success, log_warning


class DependencyManager:
    """Manages dependency lifecycle for chart tests."""

    def __init__(self, chart: str, namespace: str, verbose: bool = False):
        self.chart = chart
        self.namespace = namespace
        self.verbose = verbose
        self.config = load_chart_config(chart)
        self.installed: list[str] = []

    def setup(self, scenario: str) -> None:
        """Install dependencies for a scenario."""
        deps = self.config.get_dependencies_for_scenario(scenario)

        if not deps:
            return

        log_info(f"Setting up {len(deps)} dependencies")

        for dep in deps:
            if dep.name in self.installed:
                continue
            self._install(dep)
            self.installed.append(dep.name)

        log_success("Dependencies ready")

    def teardown(self) -> None:
        """Uninstall all dependencies."""
        for name in reversed(self.installed):
            try:
                helm_uninstall(name, self.namespace, verbose=self.verbose)
            except Exception as e:
                log_warning(f"Failed to uninstall {name}: {e}")

        self.installed.clear()

    def _install(self, dep: Dependency) -> None:
        """Install a single dependency."""
        log_info(f"Installing {dep.name} ({dep.chart})")

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
                verbose=self.verbose,
            )

            # Wait for resource
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
