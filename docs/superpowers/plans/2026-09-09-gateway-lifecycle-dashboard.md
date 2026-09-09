# Gateway Request Lifecycle Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a new Grafana dashboard (`gateway-lifecycle.json`) to the gateway Helm chart that visualizes the eleven per-stage request-lifecycle metrics from ADR-0015.

**Architecture:** A static Grafana dashboard JSON export is added under `charts/gateway/grafana-dashboards/` and wired into the existing `grafana-dashboards.yaml` (ConfigMap + v5/v4 GrafanaDashboard CRs), gated by the existing `metrics.grafana.enable`. To build the ~15 near-identical panels reliably and DRY, we author a **throwaway Python generator script in the scratchpad** that emits the JSON; only the generated JSON is committed (matching the repo convention of hand-exported static dashboards). Each task extends the generator, regenerates, validates, and commits the JSON diff.

**Tech Stack:** Grafana dashboard JSON (schemaVersion 37, Grafana 9.3.2 baseline), Prometheus/PromQL, Helm/Go templates, Python 3 (build-time only), `helm`, `jq`/`python3 -m json.tool`.

**Spec:** `docs/superpowers/specs/2026-09-09-gateway-lifecycle-dashboard-design.md`

## Global Constraints

- **Dashboard file:** `charts/gateway/grafana-dashboards/gateway-lifecycle.json` — a static JSON export mirroring `gateway.json`'s envelope.
- **Envelope must match existing dashboards** so `patchGrafanaDashboardInputs` works unchanged: `__inputs` = `INPUT_DS_PROMETHEUS` (datasource) + `INPUT_GATEWAY_JOB_NAME` (constant); variable names `datasource` and `job` reused verbatim; `schemaVersion: 37`.
- **Metric series are `_seconds`** histograms: each prefix exposes `_seconds_bucket`, `_seconds_sum`, `_seconds_count`, `_seconds_max`.
- **Tags:** per-stage metrics carry `api_key` (snake_case — NOT the old `apiKeys`); the two interceptor metrics additionally carry `interceptor`.
- **Bucket ladder (ADR §4):** `1ms, 10ms, 50ms, 100ms, 500ms, 1s, 5s, 30s` (+`+Inf`). `le="0.1"` (100ms) is a real bound → exact fraction, no interpolation.
- **All latency fields use `unit: "s"`** (Grafana auto-scales to ms/µs; no `*1000`).
- **Every Prometheus target** uses `datasource: {type: prometheus, uid: "${datasource}"}`, `editorMode: "code"`, `range: true`, `$__rate_interval`, and the filter `{job="$job", pod=~"$pod", api_key=~"$api_key"}` (interceptor panels add `, interceptor=~"$interceptor"`).
- **No new Helm values** — deployment gated only by existing `metrics.grafana.enable`.
- **Do not modify** `gateway.json`, `gateway-logs.json`, or `_helpers.tpl`.
- **Metric prefixes** (referred to throughout by these names):

  | Ref | Prometheus prefix | Stage label used in overview panels |
  |---|---|---|
  | PRE | `gateway_request_preprocess_duration_seconds` | preprocess |
  | AUTH | `gateway_request_authorization_duration_seconds` | authorization |
  | RINT | `gateway_request_interceptor_duration_seconds` | request.interceptor |
  | RREB | `gateway_request_rebuilder_duration_seconds` | request.rebuilder |
  | UQ | `gateway_request_upstreamqueue_duration_seconds` | upstreamqueue |
  | UW | `gateway_request_upstreamwait_duration_seconds` | upstreamwait |
  | SREB | `gateway_response_rebuilder_duration_seconds` | response.rebuilder |
  | SINT | `gateway_response_interceptor_duration_seconds` | response.interceptor |
  | SAUTH | `gateway_response_authorization_duration_seconds` | response.authorization |
  | SEND | `gateway_response_send_duration_seconds` | response.send |
  | TOTAL | `gateway_request_total_duration_seconds` | total |

---

## File Structure

- **Create (committed):** `charts/gateway/grafana-dashboards/gateway-lifecycle.json` — the dashboard.
- **Create (throwaway, scratchpad only, NOT committed):** `<scratchpad>/build_lifecycle_dashboard.py` — generator that writes the JSON.
- **Modify (committed):** `charts/gateway/templates/grafana-dashboards.yaml` — load/patch the new file, add ConfigMap key + v5 + v4 CRs.
- **Untouched:** `_helpers.tpl`, `values.yaml`, existing dashboards.

`<scratchpad>` refers to the session scratchpad directory:
`/private/tmp/claude-501/-Users-badaiaqrandista-Sources-conduktor-conduktor-public-charts/f8b0f2fb-39bb-495c-a33f-95cf7f2abc4f/scratchpad`

---

## Task 1: Dashboard skeleton (envelope, variables, notes panel) via generator

**Files:**
- Create: `<scratchpad>/build_lifecycle_dashboard.py`
- Create: `charts/gateway/grafana-dashboards/gateway-lifecycle.json` (generator output)

**Interfaces:**
- Produces: the generator module with helpers `ds()`, `target(expr, legend, refid)`, `ts_panel(pid, title, description, gridpos, targets, unit="s", stack="none")`, `row(pid, title, y)`, `text_panel(pid, title, y, h, content)`, a global `PANELS` list, and an emit block writing `OUTPUT`. Later tasks append to `PANELS` immediately above the `# ---- emit ----` marker.

- [ ] **Step 1: Write the generator with envelope, variables, and the notes text panel**

Create `<scratchpad>/build_lifecycle_dashboard.py` with exactly this content:

```python
#!/usr/bin/env python3
"""Throwaway generator for gateway-lifecycle.json (ADR-0015 Stage 6 / YSH-869)."""
import json, os

OUTPUT = os.path.join(os.path.dirname(__file__),
    "../../Sources/conduktor/conduktor-public-charts/charts/gateway/grafana-dashboards/gateway-lifecycle.json")
# NOTE: replace OUTPUT with the absolute repo path if the relative path does not resolve:
OUTPUT = "/Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts/charts/gateway/grafana-dashboards/gateway-lifecycle.json"

# ---- metric prefixes ----
PRE   = "gateway_request_preprocess_duration_seconds"
AUTH  = "gateway_request_authorization_duration_seconds"
RINT  = "gateway_request_interceptor_duration_seconds"
RREB  = "gateway_request_rebuilder_duration_seconds"
UQ    = "gateway_request_upstreamqueue_duration_seconds"
UW    = "gateway_request_upstreamwait_duration_seconds"
SREB  = "gateway_response_rebuilder_duration_seconds"
SINT  = "gateway_response_interceptor_duration_seconds"
SAUTH = "gateway_response_authorization_duration_seconds"
SEND  = "gateway_response_send_duration_seconds"
TOTAL = "gateway_request_total_duration_seconds"

F  = 'job="$job", pod=~"$pod", api_key=~"$api_key"'          # per-stage filter
FI = 'job="$job", pod=~"$pod", api_key=~"$api_key", interceptor=~"$interceptor"'  # interceptor filter

def ds():
    return {"type": "prometheus", "uid": "${datasource}"}

def target(expr, legend, refid):
    return {"datasource": ds(), "editorMode": "code", "expr": expr,
            "legendFormat": legend, "range": True, "refId": refid}

def ts_panel(pid, title, description, gridpos, targets, unit="s", stack="none"):
    refids = "ABCDEFGHIJKLMNOP"
    tgts = [target(e, l, refids[i]) for i, (e, l) in enumerate(targets)]
    return {
        "datasource": ds(),
        "description": description,
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "palette-classic"},
                "custom": {
                    "axisBorderShow": False, "axisCenteredZero": False, "axisColorMode": "text",
                    "axisLabel": "", "axisPlacement": "auto", "barAlignment": 0, "drawStyle": "line",
                    "fillOpacity": 60 if stack != "none" else 10, "gradientMode": "none",
                    "hideFrom": {"legend": False, "tooltip": False, "viz": False},
                    "insertNulls": False, "lineInterpolation": "linear", "lineWidth": 1, "pointSize": 1,
                    "scaleDistribution": {"type": "linear"}, "showPoints": "auto", "spanNulls": False,
                    "stacking": {"group": "A", "mode": stack},
                    "thresholdsStyle": {"mode": "off"},
                },
                "mappings": [],
                "thresholds": {"mode": "absolute", "steps": [{"color": "green", "value": None}]},
                "unit": unit,
            },
            "overrides": [],
        },
        "gridPos": gridpos,
        "id": pid,
        "options": {
            "legend": {"calcs": [], "displayMode": "table", "placement": "right", "showLegend": True},
            "tooltip": {"mode": "single", "sort": "none"},
        },
        "targets": tgts,
        "title": title,
        "type": "timeseries",
    }

def row(pid, title, y):
    return {"type": "row", "title": title, "collapsed": False,
            "gridPos": {"h": 1, "w": 24, "x": 0, "y": y}, "id": pid, "panels": []}

def text_panel(pid, title, y, h, content):
    return {"type": "text", "title": title, "id": pid,
            "gridPos": {"h": h, "w": 24, "x": 0, "y": y},
            "options": {"mode": "markdown", "content": content},
            "datasource": None}

NOTES = (
    "**Request lifecycle latency** — one panel per T0→T10 stage from ADR-0015. "
    "Requires the gateway feature flag `GATEWAY_FEATURE_FLAGS_LIFECYCLE_METRICS=true`; "
    "with it off, panels are empty.\\n\\n"
    "**Reading gaps (ADR §7):** a missing/zero series means traffic didn't reach that stage, "
    "not that instrumentation is broken. Cache hits skip `upstreamwait`/rebuilder (healthy); "
    "`acks=0` produce skips `total`; a ~30s `total` spike with no `upstreamwait` is an upstream timeout.\\n\\n"
    "**Percentiles (ADR §4):** buckets start at 1ms, so P99 reads flat for the sub-ms stages until "
    "they degrade; use mean and max for those, P99 for `upstreamwait`."
)

PANELS = []
PANELS.append(text_panel(1, "About this dashboard", 0, 4, NOTES))

# ---- emit ----
dashboard = {
    "__inputs": [
        {"name": "INPUT_DS_PROMETHEUS", "label": "prometheus", "description": "",
         "type": "datasource", "pluginId": "prometheus", "pluginName": "Prometheus", "value": "prometheus"},
        {"name": "INPUT_GATEWAY_JOB_NAME",
         "label": "Gateway job name (app.kubernetes.io/instance by default)",
         "description": "The name of the gateway to monitor", "type": "constant", "value": "conduktor-gateway"},
    ],
    "__elements": {},
    "__requires": [
        {"type": "grafana", "id": "grafana", "name": "Grafana", "version": "9.3.2"},
        {"type": "datasource", "id": "prometheus", "name": "Prometheus", "version": "1.0.0"},
        {"type": "panel", "id": "timeseries", "name": "Time series", "version": ""},
        {"type": "panel", "id": "text", "name": "Text", "version": ""},
    ],
    "annotations": {"list": [{"builtIn": 1, "datasource": {"type": "datasource", "uid": "grafana"},
        "enable": True, "hide": True, "iconColor": "rgba(0, 211, 255, 1)", "limit": 100,
        "name": "Annotations & Alerts",
        "target": {"limit": 100, "matchAny": False, "tags": [], "type": "dashboard"}, "type": "dashboard"}]},
    "description": "Per-stage request lifecycle latency for Conduktor Gateway (ADR-0015).",
    "editable": True, "fiscalYearStartMonth": 0, "gnetId": None, "graphTooltip": 1, "id": None,
    "links": [], "liveNow": False,
    "panels": PANELS,
    "refresh": "30s", "schemaVersion": 37, "style": "dark",
    "tags": ["Conduktor", "conduktor-gateway", "lifecycle", "latency"],
    "templating": {"list": [
        {"current": {"selected": False, "text": "Prometheus", "value": "default"},
         "hide": 2, "includeAll": False, "label": "Datasource", "multi": False, "name": "datasource",
         "options": [], "query": "${INPUT_DS_PROMETHEUS}", "refresh": 1, "regex": "", "type": "datasource"},
        {"hide": 2, "label": "job", "name": "job", "query": "${INPUT_GATEWAY_JOB_NAME}",
         "skipUrlSync": False, "type": "constant"},
        {"allFormat": "glob", "current": {}, "datasource": {"type": "prometheus", "uid": "${datasource}"},
         "definition": 'label_values(up{job="$job"}, pod)', "hide": 0, "includeAll": True, "label": "Pod",
         "multi": True, "multiFormat": "glob", "name": "pod", "options": [],
         "query": {"query": 'label_values(up{job="$job"}, pod)', "refId": "StandardVariableQuery"},
         "refresh": 2, "regex": "", "skipUrlSync": False, "sort": 0, "type": "query"},
        {"current": {}, "datasource": {"type": "prometheus", "uid": "${datasource}"},
         "definition": 'label_values(gateway_request_total_duration_seconds_count{job="$job"}, api_key)',
         "hide": 0, "includeAll": True, "label": "API key", "multi": True, "name": "api_key", "options": [],
         "query": {"query": 'label_values(gateway_request_total_duration_seconds_count{job="$job"}, api_key)',
                   "refId": "StandardVariableQuery"},
         "refresh": 2, "regex": "", "skipUrlSync": False, "sort": 1, "type": "query"},
        {"current": {}, "datasource": {"type": "prometheus", "uid": "${datasource}"},
         "definition": 'label_values(gateway_request_interceptor_duration_seconds_count{job="$job"}, interceptor)',
         "hide": 0, "includeAll": True, "label": "Interceptor", "multi": True, "name": "interceptor", "options": [],
         "query": {"query": 'label_values(gateway_request_interceptor_duration_seconds_count{job="$job"}, interceptor)',
                   "refId": "StandardVariableQuery"},
         "refresh": 2, "regex": "", "skipUrlSync": False, "sort": 1, "type": "query"},
    ]},
    "time": {"from": "now-30m", "to": "now"},
    "timepicker": {}, "timezone": "browser", "title": "Conduktor Gateway Lifecycle", "version": 1, "weekStart": "",
}

with open(OUTPUT, "w") as fh:
    json.dump(dashboard, fh, indent=2)
    fh.write("\\n")
print("wrote", OUTPUT, "with", len(PANELS), "panels")
```

- [ ] **Step 2: Run the generator; verify it fails/succeeds to produce valid JSON**

Run:
```bash
python3 <scratchpad>/build_lifecycle_dashboard.py
python3 -m json.tool /Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts/charts/gateway/grafana-dashboards/gateway-lifecycle.json > /dev/null && echo JSON_OK
```
Expected: prints `wrote ... with 1 panels` then `JSON_OK`. If the relative `OUTPUT` path errored, the second `OUTPUT =` absolute assignment (already in the script) is authoritative — no action needed.

- [ ] **Step 3: Verify envelope invariants**

Run:
```bash
python3 - <<'PY'
import json
d=json.load(open("/Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts/charts/gateway/grafana-dashboards/gateway-lifecycle.json"))
assert [i["name"] for i in d["__inputs"]]==["INPUT_DS_PROMETHEUS","INPUT_GATEWAY_JOB_NAME"], d["__inputs"]
assert d["schemaVersion"]==37
names=[v["name"] for v in d["templating"]["list"]]
assert names==["datasource","job","pod","api_key","interceptor"], names
apikey=[v for v in d["templating"]["list"] if v["name"]=="api_key"][0]
assert "api_key" in apikey["definition"] and "apiKeys" not in apikey["definition"]
print("ENVELOPE_OK")
PY
```
Expected: `ENVELOPE_OK`.

- [ ] **Step 4: Commit**

```bash
cd /Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts
git add charts/gateway/grafana-dashboards/gateway-lifecycle.json
git commit -m "feat(gateway): add lifecycle dashboard skeleton (YSH-869)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: Wire the dashboard into the chart

**Files:**
- Modify: `charts/gateway/templates/grafana-dashboards.yaml`

**Interfaces:**
- Consumes: `gateway-lifecycle.json` (Task 1); the existing `patchGrafanaDashboardInputs` helper and `$gatewayNsRelease` / `$configMapName` locals already defined at the top of the template.
- Produces: a ConfigMap `data` key `gateway-lifecycle.json` and two `GrafanaDashboard` CRs (v1beta1 + v1alpha1) referencing it.

- [ ] **Step 1: Add the load-and-patch block**

In `charts/gateway/templates/grafana-dashboards.yaml`, after the existing `gateway-logs.json` patch line (`$_3 := ...`, around line 9), add:

```gotemplate
{{- $lifecycleDashboard :=  .Files.Get "grafana-dashboards/gateway-lifecycle.json" | fromJson }}
{{- $lifecycleDashboardTitle := printf "Conduktor Gateway Lifecycle [%s]" $gatewayNsRelease -}}
{{- $_5 := (include "conduktor-gateway.patchGrafanaDashboardInputs" (dict "dashboard" $lifecycleDashboard "title" $lifecycleDashboardTitle "context" $)) -}}
```

- [ ] **Step 2: Add the ConfigMap data key**

In the same file, in the ConfigMap `data:` block (after the `gateway-logs.json: >` entry, around line 23), add:

```gotemplate
  gateway-lifecycle.json: >
{{ toPrettyJson $lifecycleDashboard | indent 4 }}
```

- [ ] **Step 3: Add the v5 (v1beta1) GrafanaDashboard CR**

Inside the `{{- if .Capabilities.APIVersions.Has "grafana.integreatly.org/v1beta1/GrafanaDashboard" }}` block, after the `-log-dashboard` CR (before the `{{- end }}` that closes the v1beta1 block, around line 80), add:

```gotemplate
---
apiVersion: grafana.integreatly.org/v1beta1
kind: GrafanaDashboard
metadata:
  name: {{ include "conduktor-gateway.fullname" . | trunc 42 }}-lifecycle-dashboard
  namespace: {{ include "conduktor-gateway.dashboard.namespace" . | quote }}
  labels: {{ include "conduktor-gateway.labels" . | nindent 4 }}
    "conduktor.io/dashboard": "true"
    {{- if .Values.metrics.grafana.labels }}
    {{- include "common.tplvalues.render" ( dict "value" .Values.metrics.grafana.labels "context" $ ) | nindent 4 }}
    {{- end }}
spec:
  instanceSelector:
    matchLabels:
    {{- include "common.tplvalues.render" ( dict "value" .Values.metrics.grafana.matchLabels "context" $ ) | nindent 6 }}
  {{- if .Values.metrics.grafana.folder }}
  folder: {{ .Values.metrics.grafana.folder | quote }}
  {{- end }}
  configMapRef:
    name:  {{ $configMapName | quote }}
    key: gateway-lifecycle.json
  datasources:
    - inputName: "DS_PROMETHEUS"
      datasourceName: {{ .Values.metrics.grafana.datasources.prometheus | quote }}
    - inputName: "GATEWAY_NAME"
      datasourceName: {{ .Release.Name | quote }}
```

- [ ] **Step 4: Add the v4 (v1alpha1) GrafanaDashboard CR**

Inside the `{{- if .Capabilities.APIVersions.Has "integreatly.org/v1alpha1/GrafanaDashboard" }}` block, after the `-log-dashboard` CR (before the `{{- end }}` closing that block, around line 131), add:

```gotemplate
---
apiVersion: integreatly.org/v1alpha1
kind: GrafanaDashboard
metadata:
  name: {{ include "conduktor-gateway.fullname" . | trunc 44 }}-lifecycle-dashboard
  namespace: {{ include "conduktor-gateway.dashboard.namespace" . | quote }}
  labels: {{ include "conduktor-gateway.labels" . | nindent 4 }}
    conduktor.io/dashboard: "true"
    {{- if .Values.metrics.grafana.labels }}
    {{- include "common.tplvalues.render" ( dict "value" .Values.metrics.grafana.labels "context" $ ) | nindent 4 }}
    {{- end }}
spec:
  {{- if .Values.metrics.grafana.folder }}
  customFolderName: {{ .Values.metrics.grafana.folder | quote }}
  {{- end }}
  configMapRef:
    name:  {{ $configMapName | quote }}
    key: gateway-lifecycle.json
  datasources:
    - inputName: "INPUT_DS_PROMETHEUS"
      datasourceName: {{ .Values.metrics.grafana.datasources.prometheus | quote }}
    - inputName: "INPUT_GATEWAY_JOB_NAME"
      datasourceName: {{ .Release.Name | quote }}
```

- [ ] **Step 5: Build chart deps (if needed) and render with grafana enabled**

Run:
```bash
cd /Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts
helm dependency build charts/gateway 2>/dev/null || true
helm template gw charts/gateway \
  --set metrics.grafana.enable=true \
  --api-versions grafana.integreatly.org/v1beta1/GrafanaDashboard \
  --api-versions integreatly.org/v1alpha1/GrafanaDashboard \
  | tee /tmp/gw-render.yaml >/dev/null
grep -c "key: gateway-lifecycle.json" /tmp/gw-render.yaml
grep -c "lifecycle-dashboard" /tmp/gw-render.yaml
grep -c "Conduktor Gateway Lifecycle" /tmp/gw-render.yaml
```
Expected: `key: gateway-lifecycle.json` count = **2** (v5 + v4 CRs); `lifecycle-dashboard` count = **2**; `Conduktor Gateway Lifecycle` count ≥ **1** (patched title in the ConfigMap).

- [ ] **Step 6: Verify it does NOT render when grafana disabled**

Run:
```bash
cd /Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts
helm template gw charts/gateway | grep -c "gateway-lifecycle" || echo 0
```
Expected: `0`.

- [ ] **Step 7: Commit**

```bash
cd /Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts
git add charts/gateway/templates/grafana-dashboards.yaml
git commit -m "feat(gateway): wire lifecycle dashboard into chart (YSH-869)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: Overview row (total, where-the-time-goes, throughput)

**Files:**
- Modify: `<scratchpad>/build_lifecycle_dashboard.py`
- Regenerate: `charts/gateway/grafana-dashboards/gateway-lifecycle.json`

**Interfaces:**
- Consumes: `ts_panel`, `row`, `target`, `PANELS`, prefix constants, `F` from Task 1.
- Produces: panels with ids 100–103.

- [ ] **Step 1: Append the overview panels**

In `build_lifecycle_dashboard.py`, immediately **above** the `# ---- emit ----` marker, add:

```python
# ---- Overview ----
SEG = [("preprocess", PRE), ("authorization", AUTH), ("request.interceptor", RINT),
       ("request.rebuilder", RREB), ("upstreamqueue", UQ), ("upstreamwait", UW),
       ("response.rebuilder", SREB), ("response.interceptor", SINT),
       ("response.authorization", SAUTH), ("response.send", SEND)]

PANELS.append(row(100, "Overview", 4))

PANELS.append(ts_panel(101, "Total request latency (T0→T10)",
    "Full-pipeline latency (gateway.request.total.duration). Mean and max are exact at any magnitude; "
    "P99 is meaningful once the pipeline crosses ~1ms. A ~30s spike with no upstreamwait count is an "
    "upstream timeout (ADR §7 #6).",
    {"h": 8, "w": 12, "x": 0, "y": 5}, [
        (f'sum(rate({TOTAL}_sum{{{F}}}[$__rate_interval])) / sum(rate({TOTAL}_count{{{F}}}[$__rate_interval]))', "mean"),
        (f'histogram_quantile(0.99, sum by(le) (rate({TOTAL}_bucket{{{F}}}[$__rate_interval])))', "p99"),
        (f'max({TOTAL}_max{{{F}}})', "max"),
    ]))

PANELS.append(ts_panel(102, "Where the time goes (mean per stage)",
    "Stacked mean latency per lifecycle stage — the dominant band is the bottleneck. "
    "Interceptor stages are per-invocation means (their _count is interceptors run, not requests, ADR §1); "
    "use the Interceptors section for per-interceptor attribution.",
    {"h": 8, "w": 12, "x": 12, "y": 5},
    [(f'sum(rate({m}_sum{{{F}}}[$__rate_interval])) / sum(rate({m}_count{{{F}}}[$__rate_interval]))', name)
     for name, m in SEG],
    stack="normal"))

PANELS.append(ts_panel(103, "Per-stage throughput (samples/s)",
    "Recording rate per stage. A missing/zero series means traffic didn't reach that stage (ADR §7), "
    "e.g. cache hits skip upstreamwait; interceptor rates count invocations, not requests.",
    {"h": 8, "w": 24, "x": 0, "y": 13},
    [(f'sum(rate({m}_count{{{F}}}[$__rate_interval]))', name) for name, m in SEG],
    unit="reqps"))
```

- [ ] **Step 2: Regenerate and validate JSON**

Run:
```bash
python3 <scratchpad>/build_lifecycle_dashboard.py
python3 -m json.tool /Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts/charts/gateway/grafana-dashboards/gateway-lifecycle.json > /dev/null && echo JSON_OK
```
Expected: `wrote ... with 5 panels` then `JSON_OK`.

- [ ] **Step 3: Verify overview PromQL uses the right tags/series**

Run:
```bash
python3 - <<'PY'
import json
d=json.load(open("/Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts/charts/gateway/grafana-dashboards/gateway-lifecycle.json"))
p={x["id"]:x for x in d["panels"]}
tot=p[101]["targets"]
assert "gateway_request_total_duration_seconds_sum" in tot[0]["expr"]
assert "histogram_quantile(0.99" in tot[1]["expr"]
assert 'api_key=~"$api_key"' in tot[0]["expr"] and "apiKeys" not in tot[0]["expr"]
assert p[102]["fieldConfig"]["defaults"]["custom"]["stacking"]["mode"]=="normal"
assert len(p[102]["targets"])==10 and len(p[103]["targets"])==10
print("OVERVIEW_OK")
PY
```
Expected: `OVERVIEW_OK`.

- [ ] **Step 4: Commit**

```bash
cd /Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts
git add charts/gateway/grafana-dashboards/gateway-lifecycle.json
git commit -m "feat(gateway): add lifecycle overview panels (YSH-869)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: Request-path stage panels

**Files:**
- Modify: `<scratchpad>/build_lifecycle_dashboard.py`
- Regenerate: `charts/gateway/grafana-dashboards/gateway-lifecycle.json`

**Interfaces:**
- Consumes: `ts_panel`, `row`, `PANELS`, `F`, prefix constants, and (added here) the `stage_panel` helper.
- Produces: a reusable `stage_panel(pid, title, prefix, gridpos, extra_desc="")` helper (mean+p99+max) and panels ids 200–205.

- [ ] **Step 1: Add the `stage_panel` helper and request-path panels**

In `build_lifecycle_dashboard.py`, immediately **above** the `# ---- emit ----` marker (below the Task 3 block), add:

```python
# ---- reusable single-stage panel (mean + p99 + max) ----
def stage_panel(pid, title, prefix, gridpos, extra_desc=""):
    desc = ("Mean and max are exact; P99 reads flat inside the first bucket (1ms) until this stage "
            "degrades (ADR §4). " + extra_desc).strip()
    return ts_panel(pid, title, desc, gridpos, [
        (f'sum(rate({prefix}_sum{{{F}}}[$__rate_interval])) / sum(rate({prefix}_count{{{F}}}[$__rate_interval]))', "mean"),
        (f'histogram_quantile(0.99, sum by(le) (rate({prefix}_bucket{{{F}}}[$__rate_interval])))', "p99"),
        (f'max({prefix}_max{{{F}}})', "max"),
    ])

# ---- Request path ----
PANELS.append(row(200, "Request path", 21))
PANELS.append(stage_panel(201, "T0→T1 request.preprocess", PRE, {"h": 8, "w": 12, "x": 0, "y": 22},
    "channelRead to just before ACL. Records even on ACL denial (ADR §7 #1)."))
PANELS.append(stage_panel(202, "T1→T2 request.authorization", AUTH, {"h": 8, "w": 12, "x": 12, "y": 22},
    "ACL lookup. Zero is normal for superuser/ACL-disabled requests (ADR §7 #1)."))
PANELS.append(stage_panel(203, "T3→T4 request.rebuilder", RREB, {"h": 8, "w": 12, "x": 0, "y": 30},
    "API-specific request rebuild. Skipped on cache hit and on all-topics-blocked produce (ADR §7 #2, #9)."))
PANELS.append(stage_panel(204, "T4→T5 request.upstreamqueue", UQ, {"h": 8, "w": 12, "x": 12, "y": 30},
    "Rebuilt request waiting for broker/channel then sent to Kafka wire."))
PANELS.append(stage_panel(205, "T5→T6 request.upstreamwait", UW, {"h": 8, "w": 12, "x": 0, "y": 38},
    "Kafka round-trip — the one stage where P99 is directly meaningful. Skipped on acks=0 and on "
    "upstream timeout (ADR §7 #5, #6)."))
```

- [ ] **Step 2: Regenerate and validate JSON**

Run:
```bash
python3 <scratchpad>/build_lifecycle_dashboard.py
python3 -m json.tool /Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts/charts/gateway/grafana-dashboards/gateway-lifecycle.json > /dev/null && echo JSON_OK
```
Expected: `wrote ... with 11 panels` then `JSON_OK`.

- [ ] **Step 3: Verify request-path panels**

Run:
```bash
python3 - <<'PY'
import json
d=json.load(open("/Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts/charts/gateway/grafana-dashboards/gateway-lifecycle.json"))
p={x["id"]:x for x in d["panels"]}
for pid,pre in [(201,"preprocess"),(202,"authorization"),(203,"rebuilder"),(204,"upstreamqueue"),(205,"upstreamwait")]:
    t=p[pid]["targets"]
    assert len(t)==3 and [x["legendFormat"] for x in t]==["mean","p99","max"], (pid,t)
    assert f"gateway_request_{pre}_duration_seconds" in t[0]["expr"], (pid,pre)
print("REQPATH_OK")
PY
```
Expected: `REQPATH_OK`.

- [ ] **Step 4: Commit**

```bash
cd /Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts
git add charts/gateway/grafana-dashboards/gateway-lifecycle.json
git commit -m "feat(gateway): add request-path lifecycle stage panels (YSH-869)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: Response-path stage panels

**Files:**
- Modify: `<scratchpad>/build_lifecycle_dashboard.py`
- Regenerate: `charts/gateway/grafana-dashboards/gateway-lifecycle.json`

**Interfaces:**
- Consumes: `stage_panel`, `row`, `PANELS` (from Task 4).
- Produces: panels ids 300–303.

- [ ] **Step 1: Append response-path panels**

In `build_lifecycle_dashboard.py`, immediately **above** the `# ---- emit ----` marker (below the Task 4 block), add:

```python
# ---- Response path ----
PANELS.append(row(300, "Response path", 46))
PANELS.append(stage_panel(301, "T6→T7 response.rebuilder", SREB, {"h": 8, "w": 12, "x": 0, "y": 47},
    "API-specific response rebuild. Skipped on cache hit (ADR §7 #9)."))
PANELS.append(stage_panel(302, "T8→T9 response.authorization", SAUTH, {"h": 8, "w": 12, "x": 12, "y": 47},
    "Response ACL lookup."))
PANELS.append(stage_panel(303, "T9→T10 response.send", SEND, {"h": 8, "w": 12, "x": 0, "y": 55},
    "Serialize + hop to event loop + head-of-line wait + socket write. A spike usually means "
    "head-of-line blocking behind a slow earlier request on the same connection, not a slow client "
    "(ADR §1). Not a delivery signal."))
```

- [ ] **Step 2: Regenerate and validate JSON**

Run:
```bash
python3 <scratchpad>/build_lifecycle_dashboard.py
python3 -m json.tool /Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts/charts/gateway/grafana-dashboards/gateway-lifecycle.json > /dev/null && echo JSON_OK
```
Expected: `wrote ... with 15 panels` then `JSON_OK`.

- [ ] **Step 3: Verify response-path panels**

Run:
```bash
python3 - <<'PY'
import json
d=json.load(open("/Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts/charts/gateway/grafana-dashboards/gateway-lifecycle.json"))
p={x["id"]:x for x in d["panels"]}
for pid,pre in [(301,"response_rebuilder"),(302,"response_authorization"),(303,"response_send")]:
    t=p[pid]["targets"]
    assert len(t)==3, (pid,t)
    assert f"gateway_{pre}_duration_seconds" in t[0]["expr"], (pid,pre)
print("RESPPATH_OK")
PY
```
Expected: `RESPPATH_OK`.

- [ ] **Step 4: Commit**

```bash
cd /Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts
git add charts/gateway/grafana-dashboards/gateway-lifecycle.json
git commit -m "feat(gateway): add response-path lifecycle stage panels (YSH-869)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 6: SLO / fraction-over-threshold panel

**Files:**
- Modify: `<scratchpad>/build_lifecycle_dashboard.py`
- Regenerate: `charts/gateway/grafana-dashboards/gateway-lifecycle.json`

**Interfaces:**
- Consumes: `ts_panel`, `row`, `PANELS`, `SEG` (defined in Task 3), `F`.
- Produces: panels ids 400–401.

- [ ] **Step 1: Append the fraction-over-100ms panel**

In `build_lifecycle_dashboard.py`, immediately **above** the `# ---- emit ----` marker (below the Task 5 block), add:

```python
# ---- SLO / fraction over threshold ----
PANELS.append(row(400, "SLO — fraction of requests over 100ms per stage", 63))
PANELS.append(ts_panel(401, "Fraction over 100ms per stage",
    "Share of samples slower than 100ms per stage. 100ms is a real bucket bound so this is exact "
    "(no interpolation, ADR §4). Use it to spot which stage breached the SLO.",
    {"h": 8, "w": 24, "x": 0, "y": 64},
    [(f'1 - (sum(rate({m}_bucket{{le="0.1", {F}}}[$__rate_interval])) / '
      f'sum(rate({m}_count{{{F}}}[$__rate_interval])))', name) for name, m in SEG],
    unit="percentunit"))
```

- [ ] **Step 2: Regenerate and validate JSON**

Run:
```bash
python3 <scratchpad>/build_lifecycle_dashboard.py
python3 -m json.tool /Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts/charts/gateway/grafana-dashboards/gateway-lifecycle.json > /dev/null && echo JSON_OK
```
Expected: `wrote ... with 17 panels` then `JSON_OK`.

- [ ] **Step 3: Verify the SLO panel**

Run:
```bash
python3 - <<'PY'
import json
d=json.load(open("/Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts/charts/gateway/grafana-dashboards/gateway-lifecycle.json"))
p={x["id"]:x for x in d["panels"]}
slo=p[401]
assert slo["fieldConfig"]["defaults"]["unit"]=="percentunit"
assert len(slo["targets"])==10
assert 'le="0.1"' in slo["targets"][0]["expr"]
print("SLO_OK")
PY
```
Expected: `SLO_OK`.

- [ ] **Step 4: Commit**

```bash
cd /Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts
git add charts/gateway/grafana-dashboards/gateway-lifecycle.json
git commit -m "feat(gateway): add lifecycle SLO fraction-over-100ms panel (YSH-869)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 7: Interceptor section

**Files:**
- Modify: `<scratchpad>/build_lifecycle_dashboard.py`
- Regenerate: `charts/gateway/grafana-dashboards/gateway-lifecycle.json`

**Interfaces:**
- Consumes: `ts_panel`, `row`, `PANELS`, `RINT`, `SINT`, `FI` (interceptor filter, from Task 1).
- Produces: panels ids 500–502.

- [ ] **Step 1: Append the interceptor panels**

In `build_lifecycle_dashboard.py`, immediately **above** the `# ---- emit ----` marker (below the Task 6 block), add:

```python
# ---- Interceptors (per-interceptor breakdown) ----
def interceptor_panel(pid, title, prefix, gridpos, extra_desc):
    return ts_panel(pid, title,
        "Per-interceptor latency (legend = interceptor name). _count is interceptors run, not "
        "requests (ADR §1). " + extra_desc, gridpos, [
            (f'sum by(interceptor) (rate({prefix}_sum{{{FI}}}[$__rate_interval])) / '
             f'sum by(interceptor) (rate({prefix}_count{{{FI}}}[$__rate_interval]))', "{{interceptor}} mean"),
            (f'histogram_quantile(0.99, sum by(le, interceptor) (rate({prefix}_bucket{{{FI}}}[$__rate_interval])))',
             "{{interceptor}} p99"),
        ])

PANELS.append(row(500, "Interceptors", 72))
PANELS.append(interceptor_panel(501, "T2→T3 request.interceptor per interceptor", RINT,
    {"h": 8, "w": 12, "x": 0, "y": 73},
    "Isolates a slow request-side interceptor deployment."))
PANELS.append(interceptor_panel(502, "T7→T8 response.interceptor per interceptor", SINT,
    {"h": 8, "w": 12, "x": 12, "y": 73},
    "Isolates a slow response-side interceptor deployment."))
```

- [ ] **Step 2: Regenerate and validate JSON**

Run:
```bash
python3 <scratchpad>/build_lifecycle_dashboard.py
python3 -m json.tool /Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts/charts/gateway/grafana-dashboards/gateway-lifecycle.json > /dev/null && echo JSON_OK
```
Expected: `wrote ... with 20 panels` then `JSON_OK`.

- [ ] **Step 3: Verify the interceptor panels**

Run:
```bash
python3 - <<'PY'
import json
d=json.load(open("/Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts/charts/gateway/grafana-dashboards/gateway-lifecycle.json"))
p={x["id"]:x for x in d["panels"]}
for pid,pre in [(501,"request_interceptor"),(502,"response_interceptor")]:
    t=p[pid]["targets"]
    assert 'interceptor=~"$interceptor"' in t[0]["expr"], (pid,t[0]["expr"])
    assert "by(interceptor)" in t[0]["expr"] and "{{interceptor}}" in t[0]["legendFormat"]
    assert f"gateway_{pre}_duration_seconds" in t[0]["expr"]
print("INTERCEPTOR_OK")
PY
```
Expected: `INTERCEPTOR_OK`.

- [ ] **Step 4: Commit**

```bash
cd /Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts
git add charts/gateway/grafana-dashboards/gateway-lifecycle.json
git commit -m "feat(gateway): add per-interceptor lifecycle panels (YSH-869)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 8: Final integration verification

**Files:**
- No source changes (verification + optional bump).

**Interfaces:**
- Consumes: the complete `gateway-lifecycle.json` and wired `grafana-dashboards.yaml`.

- [ ] **Step 1: Full structural + no-overlap check**

Run:
```bash
python3 - <<'PY'
import json
d=json.load(open("/Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts/charts/gateway/grafana-dashboards/gateway-lifecycle.json"))
ps=d["panels"]
ids=[p["id"] for p in ps]
assert len(ids)==len(set(ids)), "duplicate panel ids"
# no two non-row panels overlap in the grid
boxes=[(p["gridPos"]["x"],p["gridPos"]["y"],p["gridPos"]["w"],p["gridPos"]["h"]) for p in ps if p["type"]!="row"]
def overlap(a,b):
    ax,ay,aw,ah=a; bx,by,bw,bh=b
    return not (ax+aw<=bx or bx+bw<=ax or ay+ah<=by or by+bh<=ay)
for i in range(len(boxes)):
    for j in range(i+1,len(boxes)):
        assert not overlap(boxes[i],boxes[j]), (boxes[i],boxes[j])
# every prometheus expr uses _seconds series, api_key tag, no legacy apiKeys tag
import re
for p in ps:
    for t in p.get("targets",[]):
        e=t["expr"]
        assert "apiKeys" not in e, e
        assert "_seconds_" in e, e
print("STRUCTURE_OK panels=",len(ps))
PY
```
Expected: `STRUCTURE_OK panels= 20`.

- [ ] **Step 2: Render the whole chart (both operator versions) and confirm the dashboard JSON embeds valid**

Run:
```bash
cd /Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts
helm dependency build charts/gateway 2>/dev/null || true
helm template gw charts/gateway \
  --set metrics.grafana.enable=true \
  --set metrics.grafana.datasources.prometheus=my-prom \
  --api-versions grafana.integreatly.org/v1beta1/GrafanaDashboard \
  --api-versions integreatly.org/v1alpha1/GrafanaDashboard \
  | python3 - <<'PY'
import sys,yaml,json
docs=[d for d in yaml.safe_load_all(sys.stdin) if d]
cm=[d for d in docs if d.get("kind")=="ConfigMap" and "gateway-lifecycle.json" in d.get("data",{})]
assert cm, "lifecycle json not in any ConfigMap"
dash=json.loads(cm[0]["data"]["gateway-lifecycle.json"])
assert dash["title"].startswith("Conduktor Gateway Lifecycle"), dash["title"]
# helper patched the datasource input value
inp={i["name"]:i.get("value") for i in dash["__inputs"]}
assert inp["INPUT_DS_PROMETHEUS"]=="my-prom", inp
crs=[d for d in docs if d.get("kind")=="GrafanaDashboard" and d["spec"]["configMapRef"]["key"]=="gateway-lifecycle.json"]
assert len(crs)==2, [ (d["apiVersion"]) for d in crs]
print("HELM_RENDER_OK crs=",len(crs))
PY
```
Expected: `HELM_RENDER_OK crs= 2`.

- [ ] **Step 3: Optionally import into Grafana**

If a Grafana instance with the ADR-0015 metrics is reachable, import `gateway-lifecycle.json` (providing `INPUT_DS_PROMETHEUS` and `INPUT_GATEWAY_JOB_NAME`) and confirm variables resolve and panels populate. If not reachable, note this step as skipped — the structural + helm checks above are the gate.

- [ ] **Step 4: Final commit (if any doc/notes tweaks were made)**

If Step 1–2 required no fixes, there is nothing to commit here. If fixes were made to the generator/JSON, regenerate and:

```bash
cd /Users/badaiaqrandista/Sources/conduktor/conduktor-public-charts
git add charts/gateway/grafana-dashboards/gateway-lifecycle.json
git commit -m "test(gateway): finalize lifecycle dashboard integration checks (YSH-869)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Self-Review notes (for the executor)

- **`api_key` vs `apiKeys`:** the new metrics use `api_key`. Task 8 Step 1 fails the build if any legacy `apiKeys` tag slips in.
- **The generator is throwaway** (scratchpad only). Do not commit it. The committed artifact is `gateway-lifecycle.json`. Future maintenance edits the JSON directly (repo convention), same as `gateway.json`.
- **`trunc` lengths** on the two new CR names (42 for v5, 44 for v4) leave room for the `-lifecycle-dashboard` suffix within the 63-char k8s name limit; do not raise them.
- **Panel count checkpoints:** 1 → 5 → 11 → 15 → 17 → 20 across Tasks 1,3,4,5,6,7.
