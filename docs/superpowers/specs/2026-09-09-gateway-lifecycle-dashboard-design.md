# Gateway Request Lifecycle Grafana Dashboard — Design

- **Date:** 2026-09-09
- **Ticket:** [YSH-869 — LifecycleMetrics Stage 6: Grafana dashboard](https://linear.app/conduktor/issue/YSH-869/lifecyclemetrics-stage-6-grafana-dashboard)
- **Parent:** TEC-1 (Gateway metrics supportability)
- **Source ADR:** `conduktor-proxy/docs/adrs/0015-request-lifecycle-metrics.md`
- **Repo:** `conduktor-public-charts` (this repo)

## Summary

Add a new Grafana dashboard, `gateway-lifecycle.json`, to the gateway Helm chart that
visualizes the eleven per-stage request-lifecycle histogram metrics introduced by ADR-0015.
The dashboard breaks a request's end-to-end latency into its T0→T10 lifecycle segments so an
operator can tell *which* stage (queue, authorization, an interceptor, the Kafka round-trip,
response send, …) crossed into user-visible latency — without thread dumps or profilers
(the motivating friction in Zendesk #3766, #3803).

This is a chart-only change: no proxy code is touched. The metrics themselves are delivered by
ADR-0015 Stages 0–5; this is Stage 6.

## Goals

- One new dashboard file wired into the existing chart dashboard machinery, deployable via both
  the v5 (`grafana.integreatly.org/v1beta1`) and v4 (`integreatly.org/v1alpha1`) Grafana operators
  and via the Sidecar ConfigMap, exactly like `gateway.json`/`gateway-logs.json`.
- Per-stage latency panels for all nine self-performed stages plus the full-pipeline total.
- A dedicated per-interceptor breakdown driven by an `interceptor` template variable.
- Queries chosen to be diagnostically honest against the ADR §4 bucket ladder (exact mean + max +
  fraction-over-threshold; `histogram_quantile` P99 where it is meaningful).
- Panels annotated so that expected data gaps (§7 short-circuit scenarios) read as
  "traffic didn't reach that stage," not "instrumentation broken."

## Non-goals

- No changes to the proxy / metric instrumentation (owned by ADR-0015 Stages 0–5).
- No changes to the existing `gateway.json` or `gateway-logs.json` dashboards.
- No new alerting rules (dashboard only).
- No deprecation/removal of the existing `gateway.latency.request_response` panels.
- No new Helm values toggle — deployment is gated by the existing `metrics.grafana.enable`.

## Background: the metrics (from ADR-0015 §1)

All eleven metrics are Micrometer `Timer`s exported by Prometheus with the `_seconds` base unit,
producing `<prefix>_seconds_bucket` / `_sum` / `_count` / `_max` series. They share one explicit
bucket ladder (ADR §4): **1ms, 10ms, 50ms, 100ms, 500ms, 1s, 5s, 30s** (+`+Inf`).

| Prometheus prefix | Segment (boundary) | Tags |
|---|---|---|
| `gateway_request_preprocess_duration_seconds` | T0→T1 channelRead → before ACL | `api_key` |
| `gateway_request_authorization_duration_seconds` | T1→T2 ACL check | `api_key` |
| `gateway_request_interceptor_duration_seconds` | T2→T3 per request interceptor | `api_key`, `interceptor` |
| `gateway_request_rebuilder_duration_seconds` | T3→T4 request rebuild | `api_key` |
| `gateway_request_upstreamqueue_duration_seconds` | T4→T5 rebuilt → sent to Kafka | `api_key` |
| `gateway_request_upstreamwait_duration_seconds` | T5→T6 Kafka round-trip | `api_key` |
| `gateway_response_rebuilder_duration_seconds` | T6→T7 response rebuild | `api_key` |
| `gateway_response_interceptor_duration_seconds` | T7→T8 per response interceptor | `api_key`, `interceptor` |
| `gateway_response_authorization_duration_seconds` | T8→T9 response ACL | `api_key` |
| `gateway_response_send_duration_seconds` | T9→T10 ACL → writeAndFlush done | `api_key` |
| `gateway_request_total_duration_seconds` | T0→T10 full pipeline | `api_key` |

The nine "self-performed" stages (everything except `upstreamwait` and `total`) normally sit
**sub-millisecond**, i.e. inside the first bucket bound (1ms).

**Tag note:** these metrics use the `api_key` label (snake_case). This differs from the existing
dashboard's per-ApiKey panels, which use the older `apiKeys` label on
`gateway_apiKeys_latency_request_response_*`. Do not mix them.

## Key design decisions

1. **Separate dashboard file** — `gateway-lifecycle.json`, not additions to `gateway.json`.
   Keeps the stable 5,600-line existing dashboard untouched and matches the ADR's intent of
   "a new Grafana dashboard built on the lifecycle metrics."
2. **Follow ADR §4 for statistics** — per-stage panels use exact **mean** =
   `rate(_sum)/rate(_count)`, `_max`, and **fraction-over-threshold** on a real bucket bound; plus
   `histogram_quantile` **P99**, which is understood to read flat/interpolated for the sub-ms stages
   and to become meaningful only when a stage degrades or for the inherently slow `upstreamwait`.
   We deliberately do **not** ship uniform P50/P99 as the primary read, because that misrepresents
   the sub-ms stages given a ladder that starts at 1ms.
3. **Dedicated interceptor section + `interceptor` variable** — surfaces the "which interceptor
   deployment is slow" use case directly.
4. **Gate on `metrics.grafana.enable` only** — no new values toggle. A dashboard with no data
   (when the default-off `lifecycleMetrics` feature flag is disabled) is harmless and self-documents
   the feature.
5. **Unit = seconds (`s`)** on all latency fields — Grafana auto-scales to ms/µs for display, so no
   `* 1000` expressions are needed (ADR §1 permits either; `unit=s` is cleaner and keeps queries
   readable).

## Dashboard structure

### File format

`gateway-lifecycle.json` is a Grafana dashboard export mirroring `gateway.json`'s envelope so the
existing `patchGrafanaDashboardInputs` helper works unchanged:

- `__inputs`: `INPUT_DS_PROMETHEUS` (datasource) and `INPUT_GATEWAY_JOB_NAME` (constant), with the
  same `name`/`label`/`type` as `gateway.json`. The helper patches these by name.
- `__requires`: at minimum `grafana`, `prometheus` (datasource), and the panel types used
  (`timeseries`, `stat`, plus `text` for the notes panel).
- Standard top-level keys (`schemaVersion`, `templating`, `panels`, `time`, `refresh`, etc.)
  consistent with `gateway.json`.

### Template variables

Reuse the same variable *names* as `gateway.json` so the helper patches them (`datasource`, `job`),
plus `pod`, and add the two new query variables:

| name | type | query | notes |
|---|---|---|---|
| `datasource` | datasource (hidden) | `${INPUT_DS_PROMETHEUS}` | patched by helper |
| `job` | constant (hidden) | `${INPUT_GATEWAY_JOB_NAME}` | patched by helper |
| `pod` | query (multi, includeAll) | `label_values(up{job="$job"}, pod)` | same as existing |
| `api_key` | query (multi, includeAll) | `label_values(gateway_request_total_duration_seconds_count{job="$job"}, api_key)` | new; uses `api_key` tag |
| `interceptor` | query (multi, includeAll) | `label_values(gateway_request_interceptor_duration_seconds_count{job="$job"}, interceptor)` | new; scopes interceptor section |

All Prometheus panel targets carry `datasource: {type: prometheus, uid: "${datasource}"}` and filter
by `{job="$job", pod=~"$pod", api_key=~"$api_key"}` (interceptor panels add `interceptor=~"$interceptor"`).

### Panels (top → bottom, T0→T10 order)

**Row 1 — Overview**
- **Total request latency** (`request.total.duration`): three series — mean
  `sum(rate(_sum[$__rate_interval]))/sum(rate(_count[$__rate_interval]))`, P99
  `histogram_quantile(0.99, sum by(le)(rate(_bucket[$__rate_interval])))`, and `max(_max)`.
- **Where the time goes** — stacked timeseries, one series per self-performed stage, each the stage
  mean `sum(rate(stage_sum))/sum(rate(stage_count))`. The dominant band is the bottleneck stage.
  This is the panel that answers ADR §4's core question.
- **Per-stage throughput** — one series per stage, `sum(rate(stage_count[$__rate_interval]))`.
  Missing/zero series map to §7 short-circuit scenarios and are expected, not errors.

**Row 2 — Request path stages** (one timeseries panel each, in order):
`request.preprocess`, `request.authorization`, `request.rebuilder`, `request.upstreamqueue`,
`request.upstreamwait`.

**Row 3 — Response path stages** (one timeseries panel each, in order):
`response.rebuilder`, `response.authorization`, `response.send`.

Each per-stage panel shows **mean + P99 + max** (three series), unit `s`, filtered by
`$api_key`/`$pod`. Panel description notes the ADR §4 caveat where relevant (P99 flat until the
stage degrades) and the §7 scenario that explains expected gaps (e.g. `upstreamwait` skipped on
`acks=0`, cache hits, ACL denials).

**Row 4 — SLO / fraction over threshold**
- One panel, one series per stage: fraction of requests **over 100 ms** =
  `1 - (sum(rate(_bucket{le="0.1"}[$__rate_interval])) / sum(rate(_count[$__rate_interval])))`.
  100 ms is a real bucket bound, so this is exact (no interpolation). Quick "which stage breached SLO."

**Row 5 — Interceptors** (uses `$interceptor`)
- **Request interceptor latency** (`request.interceptor.duration`): mean and P99, legend
  `{{interceptor}}`.
- **Response interceptor latency** (`response.interceptor.duration`): mean and P99, legend
  `{{interceptor}}`.
- Panel note: for these two metrics `_count` equals *interceptors run*, not requests (ADR §1).

**Notes panel (text)** at the top or bottom: brief operator guidance distilled from ADR §7 —
gaps mean "traffic didn't reach that stage" (cache hits are healthy gaps; `acks=0` skips
`total.duration`; a ~30s spike in `total.duration` with no `upstreamwait` is an upstream timeout).

### Chart wiring — `templates/grafana-dashboards.yaml`

Additive changes only, all inside the existing `{{- if .Values.metrics.grafana.enable }}` guard:

1. Load and patch the new file alongside the existing two:
   ```
   {{- $lifecycleDashboard := .Files.Get "grafana-dashboards/gateway-lifecycle.json" | fromJson }}
   {{- $lifecycleTitle := printf "Conduktor Gateway Lifecycle [%s]" $gatewayNsRelease -}}
   {{- $_ := (include "conduktor-gateway.patchGrafanaDashboardInputs" (dict "dashboard" $lifecycleDashboard "title" $lifecycleTitle "context" $)) -}}
   ```
2. Add a `gateway-lifecycle.json` key to the ConfigMap `data`.
3. Add a `GrafanaDashboard` CR for the **v1beta1 (v5)** operator (inside the existing
   `.Capabilities.APIVersions.Has "grafana.integreatly.org/v1beta1/GrafanaDashboard"` block), with
   `configMapRef.key: gateway-lifecycle.json` and datasource mappings `DS_PROMETHEUS` + `GATEWAY_NAME`.
4. Add a `GrafanaDashboard` CR for the **v1alpha1 (v4)** operator (inside the existing
   `.Capabilities.APIVersions.Has "integreatly.org/v1alpha1/GrafanaDashboard"` block), with
   `configMapRef.key: gateway-lifecycle.json` and `INPUT_DS_PROMETHEUS` + `INPUT_GATEWAY_JOB_NAME`.
5. Metadata names must stay within the existing `trunc` limits, e.g.
   `{{ include "conduktor-gateway.fullname" . | trunc 42 }}-lifecycle-dashboard`.

No change to `_helpers.tpl` is required: the helper patches inputs/variables by name
(`INPUT_DS_PROMETHEUS`, `INPUT_GATEWAY_JOB_NAME`, `datasource`, `job`), which the new file reuses.

## Testing / verification

- `helm template` the gateway chart with `metrics.grafana.enable=true` and confirm:
  - the ConfigMap contains a valid `gateway-lifecycle.json` entry;
  - the v5 and v4 `GrafanaDashboard` CRs render (test with the relevant `--api-versions` flags);
  - the patched title and datasource names are correct.
- `helm template` with `metrics.grafana.enable=false` (default) confirms nothing lifecycle-related renders.
- Validate `gateway-lifecycle.json` parses as JSON (e.g. `python3 -m json.tool` / `jq`).
- Spot-check every PromQL target: `_seconds` series only, `api_key`/`interceptor` tags (not `apiKeys`),
  `$__rate_interval`, and `{job="$job", pod=~"$pod"}` filters.
- Optional but recommended: import the dashboard into a Grafana instance with the ADR-0015 feature
  flag enabled and confirm panels populate and variables resolve.

## Risks / considerations

- **Empty dashboard when feature flag off.** Expected and acceptable (decision 4). The notes panel
  should mention that data requires `GATEWAY_FEATURE_FLAGS_LIFECYCLE_METRICS=true` on the gateway.
- **Cardinality.** The dashboard does not create series, but heavy use of the `api_key`/`interceptor`
  `includeAll` variables can produce broad queries; aggregate with `sum by(...)` and rely on the
  variable filters. (Series-count risk itself is an ADR-0015 concern, mitigated by its scoping config.)
- **Grafana version skew.** Match `schemaVersion`/`__requires` to what `gateway.json` already targets
  (Grafana 9.3.2 baseline) so both operators accept it.
- **`api_key` vs `apiKeys` tag mismatch** is the most likely authoring bug — called out explicitly above.
