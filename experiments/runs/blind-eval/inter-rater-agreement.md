# Inter-rater Agreement (v2.4 sample)

Second scorer: **Claude Sonnet 4.6**  
First scorer: **GPT-5.4**

Rubric used: `experiments/runs/blind-eval/STANDARD-SCORING-RUBRIC.md`  
For agreement, scoring was treated as binary (`COVERED` / `MISS`), with any would-be `PARTIAL` judgments collapsed to `MISS`.

## Sample

8-task stratified sample (32 fact-level decisions):

- `blind-requests-struct-1` (structural, Python)
- `blind-echo-struct-2` (structural, Go)
- `blind-requests-rel-1` (relational, Python)
- `blind-echo-rel-1` (relational, Go)
- `blind-requests-mech-2` (mechanistic, Python)
- `blind-echo-mech-1` (mechanistic, Go)
- `blind-click-2` (mechanistic, Python dev)
- `blind-zod-mech-1` (mechanistic, TypeScript)

## Claude Sonnet 4.6 fact-level scores

| Task | F1 | F2 | F3 | F4 | Sonnet score |
|---|---|---|---|---|---:|
| blind-requests-struct-1 | COVERED | COVERED | COVERED | COVERED | 4/4 |
| blind-echo-struct-2 | COVERED | MISS | COVERED | MISS | 2/4 |
| blind-requests-rel-1 | COVERED | COVERED | COVERED | MISS | 3/4 |
| blind-echo-rel-1 | COVERED | COVERED | MISS | COVERED | 3/4 |
| blind-requests-mech-2 | MISS | MISS | MISS | COVERED | 1/4 |
| blind-echo-mech-1 | COVERED | MISS | MISS | MISS | 1/4 |
| blind-click-2 | MISS | MISS | MISS | MISS | 0/4 |
| blind-zod-mech-1 | COVERED | COVERED | COVERED | COVERED | 4/4 |

## Per-task notes

### blind-requests-struct-1

- F1 **COVERED** — explicitly places the top-level helpers in `requests.api`
- F2 **COVERED** — explicitly places `Session` orchestration in `requests.sessions`
- F3 **COVERED** — explicitly places `Request`, `PreparedRequest`, and `Response` in `requests.models`
- F4 **COVERED** — explicitly names `requests.adapters` and `requests.exceptions` as separate public modules

### blind-echo-struct-2

- F1 **COVERED** — explicitly identifies `Echo`, `Context`, and `DefaultRouter`
- F2 **MISS** — covers method-specific registration, but does not clearly state that each `Echo` registration returns `RouteInfo`
- F3 **COVERED** — explicitly states `Echo.Group(...)` creates a `*Group` with route/middleware registration
- F4 **MISS** — mentions binding and JSON serialization, but misses `DefaultBinder` and the validation-side surfacing from the gold fact

### blind-requests-rel-1

- F1 **COVERED** — explicitly describes `Request -> PreparedRequest` before transport
- F2 **COVERED** — explicitly says `Session.prepare_request()` merges session cookies/defaults
- F3 **COVERED** — explicitly says `Session.send()` consumes a `PreparedRequest`
- F4 **MISS** — does not mention `response.request` as the back-reference

### blind-echo-rel-1

- F1 **COVERED** — explicitly says Echo owns registration and handlers take `*echo.Context`
- F2 **COVERED** — explicitly says group routes are delegated back into the parent Echo router
- F3 **MISS** — does not actually establish nested-group middleware inheritance; it marks the exact merge mechanism as undetermined
- F4 **COVERED** — describes handlers and middleware working through the same context surface

### blind-requests-mech-2

- F1 **MISS** — does not state the immediate-download behavior for `stream=False`
- F2 **MISS** — does not explain the `iter_content(None)` mode split
- F3 **MISS** — explicitly says the fallback decoding path cannot be determined
- F4 **COVERED** — explicitly says `json()` raises `RequestsJSONDecodeError`

### blind-echo-mech-1

- F1 **COVERED** — explicitly gives static > parameterized > wildcard priority
- F2 **MISS** — gives the priority rule, but not the registration-order consequence
- F3 **MISS** — does not explain wildcard consumption as zero-or-more remaining characters
- F4 **MISS** — does not discuss the multi-`*` edge case

### blind-click-2

- F1 **MISS** — omits `Context.default_map` and substitutes a different fallback chain
- F2 **MISS** — does not describe scalar / tuple / variadic / `multiple=True` branching
- F3 **MISS** — never mentions `Choice.convert()` / `normalize_choice()`
- F4 **MISS** — mentions `LazyFile` and some path checks, but misses context cleanup and rwx constraint enforcement

### blind-zod-mech-1

- F1 **COVERED** — explicitly says plain object schemas strip unknown keys by default
- F2 **COVERED** — explicitly says strict object schemas error on unknown keys
- F3 **COVERED** — explicitly says loose object schemas preserve unknown keys
- F4 **COVERED** — explicitly says `.catchall()` validates otherwise-unknown keys against the catchall schema

## Agreement with GPT-5.4

### GPT-5.4 comparison matrix

| Task | GPT F1 | GPT F2 | GPT F3 | GPT F4 | GPT score |
|---|---|---|---|---|---:|
| blind-requests-struct-1 | COVERED | COVERED | COVERED | COVERED | 4/4 |
| blind-echo-struct-2 | COVERED | COVERED | COVERED | COVERED | 4/4 |
| blind-requests-rel-1 | COVERED | COVERED | COVERED | MISS | 3/4 |
| blind-echo-rel-1 | COVERED | COVERED | COVERED | MISS | 3/4 |
| blind-requests-mech-2 | MISS | MISS | MISS | COVERED | 1/4 |
| blind-echo-mech-1 | COVERED | COVERED | MISS | MISS | 2/4 |
| blind-click-2 | MISS | MISS | MISS | COVERED | 1/4 |
| blind-zod-mech-1 | COVERED | COVERED | COVERED | COVERED | 4/4 |

### Summary statistics

| Metric | Value |
|---|---:|
| Fact-level decisions | 32 |
| Exact matches | 26 |
| Percent agreement | 81.2% |
| Cohen's kappa | 0.607 |
| GPT-5.4 `COVERED` count | 22 |
| Sonnet 4.6 `COVERED` count | 18 |

### 2x2 agreement table

| GPT-5.4 \\ Sonnet 4.6 | COVERED | MISS |
|---|---:|---:|
| COVERED | 17 | 5 |
| MISS | 1 | 9 |

## Disagreements

| Task | Fact | GPT-5.4 | Sonnet 4.6 |
|---|---|---|---|
| blind-echo-struct-2 | F2 | COVERED | MISS |
| blind-echo-struct-2 | F4 | COVERED | MISS |
| blind-echo-rel-1 | F3 | COVERED | MISS |
| blind-echo-rel-1 | F4 | MISS | COVERED |
| blind-echo-mech-1 | F2 | COVERED | MISS |
| blind-click-2 | F4 | COVERED | MISS |

## Takeaway

Agreement is **good but not perfect** on this sample:

- **81.2%** raw agreement
- **Cohen's kappa = 0.607**, which indicates moderate-to-substantial agreement
- disagreements are concentrated in borderline Echo structural/relational judgments and one Click conversion fact
- Sonnet 4.6 was the stricter scorer overall (`18 COVERED` vs `22 COVERED`)
