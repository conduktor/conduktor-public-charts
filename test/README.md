# Helm Charts Test Framework

Python-based test framework for Conduktor Helm charts with shared dependencies, upgrade testing, and per-scenario isolation.

## Prerequisites

- Python 3.10+
- Kubernetes cluster (k3d recommended)
- Helm 3.6+
- kubectl
- kubeconform (for lint)

```bash
# Install Python dependencies
pip install -r test/requirements.txt

# Create local k3d cluster
make k3d-up
```

## How It Works

### Test Flow

For each chart, the framework:

1. **Setup shared dependencies** - Installs dependencies (PostgreSQL, Kafka, etc.) once in a dedicated namespace (`ct-{chart}-deps`)
2. **Run scenarios** - For each scenario in `charts/{chart}/ci/`:
   - Creates isolated namespace (`ct-{chart}-{scenario}`)
   - Initializes isolation resources (database, bucket)
   - Runs upgrade test path (if enabled)
   - Runs helm test
   - Cleans up namespace
3. **Teardown dependencies** - Removes shared dependencies

### Upgrade Testing

When upgrade testing is enabled (default), the framework:

1. Installs the **previous released version with previous values** from the Conduktor Helm repo
2. Runs `helm test` on old version
3. Upgrades to **current version with previous values**
4. Runs `helm test` after upgrade
5. Upgrades to **current version with current values**
6. Runs final `helm test`

This validates that upgrades from released versions work correctly.

### Isolation Model

Dependencies are shared across scenarios but isolation is achieved through:

- **PostgreSQL**: Separate database per scenario (`db_01`, `db_02`, etc.)
- **Minio**: Separate bucket per scenario (`bucket-01`, `bucket-02`, etc.)
- **Kafka/Gateway**: Scenario ID prefix in cluster/topic names

**Convention**: Scenario values files should use the scenario number (from filename) for isolation. For example, `01-basic-values.yaml` uses `db_01` database.

## CLI Commands

### Run Tests

```bash
# Test specific chart
python -m test.runner run --chart console

# Test specific scenario
python -m test.runner run --chart console --scenario 01-basic

# Test changed charts (vs main branch)
python -m test.runner run --changed

# Test all charts
python -m test.runner run --all
```

**Options:**
| Option | Description |
|--------|-------------|
| `--chart, -c` | Chart to test |
| `--scenario, -s` | Specific scenario to run |
| `--changed` | Test only charts with changes vs main |
| `--all` | Test all charts |
| `--skip-upgrade` | Skip upgrade path, fresh install only |
| `--pause-on-failure` | Pause before cleanup on failure for debugging |
| `--timeout, -t` | Helm timeout (overrides test-config.yaml) |
| `--verbose, -v` | Enable verbose output |

### Local Development

```bash
# Install scenario without cleanup (for debugging)
python -m test.runner install --chart console --scenario 01-basic

# Cleanup when done
python -m test.runner uninstall --chart console --scenario 01-basic
```

### Other Commands

```bash
# Detect changed charts
python -m test.runner detect-changed
python -m test.runner detect-changed --json

# Lint manifests with kubeconform
python -m test.runner lint-manifests
python -m test.runner lint-manifests --chart console
```

## Makefile Targets

| Target | Description |
|--------|-------------|
| `make test-run CHART=x` | Run tests for a chart |
| `make test-run CHART=x SCENARIO=y` | Run specific scenario |
| `make test-changed` | Test changed charts |
| `make test-charts` | Test all charts |
| `make test-install CHART=x SCENARIO=y` | Install for debugging |
| `make test-uninstall CHART=x SCENARIO=y` | Cleanup after debugging |
| `make test-deps` | Install Python dependencies |
| `make lint-manifests` | Validate manifests |
| `make detect-changed` | List changed charts |

**Makefile Options:** `SKIP_UPGRADE=1`, `PAUSE_ON_FAILURE=1`, `TIMEOUT=900s`, `VERBOSE=1`

## Adding Test Scenarios

### 1. Create Test Configuration

Create `charts/{chart}/ci/test-config.yaml`:

```yaml
# Helm install/upgrade/test timeout
timeout: "600s"

# Dependencies installed before tests
dependencies:
  - name: postgresql
    chart: bitnami/postgresql
    version: "12.5.8"
    wait: statefulset/postgresql  # Resource to wait for
    timeout: "300s"               # Dependency install timeout
    init:                         # Isolation resources
      database: "db_{scenario_id}"
      user: postgres
      password: conduktor123

  - name: minio
    chart: bitnami/minio
    version: "12.8.0"
    wait: deployment/minio
    init:
      bucket: "bucket-{scenario_id}"
      user: admin
      password: conduktor123
```

**Dependency fields:**
| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Release name |
| `chart` | Yes | Helm chart reference |
| `version` | No | Chart version |
| `wait` | Yes | Resource to wait for (e.g., `statefulset/name`) |
| `timeout` | No | Install timeout (default: 300s) |
| `values` | No | Inline values override (dict) |
| `init.database` | No | PostgreSQL database to create |
| `init.bucket` | No | Minio bucket to create |
| `init.user` | No | Username for init |
| `init.password` | No | Password for init |

### 2. Create Scenario Values Files

Create `charts/{chart}/ci/{number}-{name}-values.yaml`:

```
charts/console/ci/
├── test-config.yaml
├── 01-basic-values.yaml
├── 02-with-tls-values.yaml
├── 03-external-secret-values.yaml
└── ...
```

**Naming convention:**
- Files must end with `-values.yaml`
- Prefix with number for ordering (`01-`, `02-`, etc.)
- Number is used as `scenario_id` for isolation (`db_01`, `bucket-01`)

### 3. Configure Isolation in Values

Use the scenario number in your values file to connect to isolated resources:

```yaml
# 01-basic-values.yaml
config:
  database:
    name: db_01  # Matches init.database template with scenario_id=01
    host: postgresql.ct-console-deps.svc.cluster.local
    username: postgres
    password: conduktor123
```

**Dependency service URLs:**
- PostgreSQL: `postgresql.ct-{chart}-deps.svc.cluster.local:5432`
- Minio: `minio.ct-{chart}-deps.svc.cluster.local:9000`
- Kafka: `kafka.ct-{chart}-deps.svc.cluster.local:9092`

### 4. Add Helm Tests

Create test pods in `charts/{chart}/templates/tests/`:

```yaml
# charts/console/templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ .Release.Name }}-test-connection"
  annotations:
    "helm.sh/hook": test
spec:
  containers:
    - name: test
      image: curlimages/curl:latest
      command: ['curl', '--fail', 'http://{{ .Release.Name }}:{{ .Values.service.port }}/health']
  restartPolicy: Never
```

## File Structure

```
test/
├── README.md           # This file
├── requirements.txt    # Python dependencies
├── runner.py          # Main CLI entry point
├── config.py          # Config loading
├── models.py          # Pydantic models
├── dependencies.py    # Dependency lifecycle
├── helm.py            # Helm operations
├── kubernetes.py      # kubectl operations
├── lint.py            # Manifest validation
├── utils.py           # Logging, utilities
└── shared-deps/       # Shared dependency values
    ├── postgresql/values.yaml
    ├── kafka/values.yaml
    └── minio/values.yaml

charts/{chart}/ci/
├── test-config.yaml       # Test configuration
├── 01-basic-values.yaml   # Scenario 1
├── 02-xxx-values.yaml     # Scenario 2
└── ...
```

## Troubleshooting

### Debug Failed Tests

```bash
# Run with pause on failure
make test-run CHART=console SCENARIO=01-basic PAUSE_ON_FAILURE=1

# Or install without cleanup
make test-install CHART=console SCENARIO=01-basic

# Then inspect
kubectl get pods -n ct-console-01-basic
kubectl logs -n ct-console-01-basic -l app.kubernetes.io/name=console
kubectl describe pod -n ct-console-01-basic <pod-name>

# Cleanup when done
make test-uninstall CHART=console SCENARIO=01-basic
```

### Upgrade Tests Not Running

If you see "No old version found, fresh install":

1. Ensure Helm repos are updated: `helm repo update`
2. On CI, ensure main branch is fetched: `git fetch origin main --depth=1`
3. Run with verbose to debug: `make test-run CHART=console VERBOSE=1`

### Timeout Issues

Increase timeout in `test-config.yaml` or via CLI:

```bash
make test-run CHART=console TIMEOUT=900s
```
