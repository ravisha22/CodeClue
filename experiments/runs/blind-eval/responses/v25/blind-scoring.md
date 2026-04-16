# Blind scoring for v25

- Rubric: **C = COVERED**, **M = MISS**
- Overall: **86/168 covered** (51.2%)

## REQUESTS

| Task | Type | F1 | F2 | F3 | F4 | Score | Notes |
|---|---|---|---|---|---|---:|---|
| blind-requests-struct-1 | struct | M | C | C | C | 3/4 | Missed helpers-under-api detail. |
| blind-requests-struct-2 | struct | C | C | C | C | 4/4 | - |
| blind-requests-rel-1 | rel | C | C | C | M | 3/4 | Missed Response.request back-reference. |
| blind-requests-rel-2 | rel | C | C | C | C | 4/4 | - |
| blind-requests-mech-1 | mech | M | C | M | C | 2/4 | Missed method-priority merge and prepare-skip-session. |
| blind-requests-mech-2 | mech | M | M | M | C | 1/4 | Missed stream=False immediate load, iter_content distinction, text fallback. |
| **requests subtotal** |  |  |  |  |  | **17/24** | **70.8%** |

## ECHO

| Task | Type | F1 | F2 | F3 | F4 | Score | Notes |
|---|---|---|---|---|---|---:|---|
| blind-echo-struct-1 | struct | C | C | M | M | 2/4 | Missed paired-constructor and external-repos facts. |
| blind-echo-struct-2 | struct | C | C | C | M | 3/4 | Missed binding/JSON/validation interfaces. |
| blind-echo-rel-1 | rel | C | C | M | M | 2/4 | Missed middleware inheritance and shared-context fact. |
| blind-echo-rel-2 | rel | C | M | C | M | 2/4 | Missed radix-tree priority and route-level stacks. |
| blind-echo-mech-1 | mech | C | C | M | C | 3/4 | Missed wildcard zero-or-more detail. |
| blind-echo-mech-2 | mech | M | C | M | C | 2/4 | Missed JSON-not-HTML and debug-exposes detail. |
| **echo subtotal** |  |  |  |  |  | **14/24** | **58.3%** |

## ZOD

| Task | Type | F1 | F2 | F3 | F4 | Score | Notes |
|---|---|---|---|---|---|---:|---|
| blind-zod-struct-1 | struct | C | M | C | M | 2/4 | Missed mini-as-functional API and locale auto-load. |
| blind-zod-struct-2 | struct | C | C | C | C | 4/4 | - |
| blind-zod-rel-1 | rel | C | C | C | C | 4/4 | - |
| blind-zod-rel-2 | rel | C | C | C | C | 4/4 | - |
| blind-zod-mech-1 | mech | C | C | C | C | 4/4 | - |
| blind-zod-mech-2 | mech | M | M | C | C | 2/4 | Missed schema-highest and per-parse override. |
| **zod subtotal** |  |  |  |  |  | **20/24** | **83.3%** |

## FASTAPI

| Task | Type | F1 | F2 | F3 | F4 | Score | Notes |
|---|---|---|---|---|---|---:|---|
| blind-fastapi-struct-1 | struct | C | M | M | M | 1/4 | Missed dependencies/, openapi/, and security/ facts. |
| blind-fastapi-struct-2 | struct | M | M | M | M | 0/4 | Did not cover the target core-type/validation/middleware/testclient structure. |
| blind-fastapi-rel-1 | rel | C | M | C | M | 2/4 | Covered Starlette + dependency chain, but not APIRouter grouping or route merge into app. |
| blind-fastapi-rel-2 | rel | M | M | M | C | 1/4 | Only lifespan/startup-shutdown was covered. |
| blind-fastapi-mech-1 | mech | M | M | M | M | 0/4 | Did not cover dependency caching / 422 / yield cleanup / recursive sub-dependencies. |
| blind-fastapi-mech-2 | mech | C | M | M | C | 2/4 | Missed response_model filtering and BackgroundTasks timing. |
| **fastapi subtotal** |  |  |  |  |  | **6/24** | **25.0%** |

## GIN

| Task | Type | F1 | F2 | F3 | F4 | Score | Notes |
|---|---|---|---|---|---|---:|---|
| blind-gin-struct-1 | struct | C | M | M | M | 1/4 | Missed binding/, render/, and internal/ package split. |
| blind-gin-struct-2 | struct | M | C | M | M | 1/4 | Only per-request Context was clearly covered. |
| blind-gin-rel-1 | rel | C | C | C | C | 4/4 | - |
| blind-gin-rel-2 | rel | M | M | C | M | 1/4 | Only Abort/stops-chain was covered. |
| blind-gin-mech-1 | mech | M | M | C | M | 1/4 | Only trailing-slash redirect was clearly covered. |
| blind-gin-mech-2 | mech | C | C | M | M | 2/4 | Missed Context.JSON content-type/serialization and panic-recovery 500. |
| **gin subtotal** |  |  |  |  |  | **10/24** | **41.7%** |

## EXPRESS

| Task | Type | F1 | F2 | F3 | F4 | Score | Notes |
|---|---|---|---|---|---|---:|---|
| blind-express-struct-1 | struct | C | C | C | C | 4/4 | - |
| blind-express-struct-2 | struct | C | M | M | M | 1/4 | Only application factory/createApplication was clearly surfaced. |
| blind-express-rel-1 | rel | C | C | C | M | 3/4 | Missed 4-argument error-middleware fact. |
| blind-express-rel-2 | rel | M | C | M | M | 1/4 | Only next() handoff was clearly covered. |
| blind-express-mech-1 | mech | M | C | M | M | 1/4 | Only req.params extraction from path pattern was clearly covered. |
| blind-express-mech-2 | mech | M | M | M | C | 1/4 | Only error-middleware catch behavior was clearly covered. |
| **express subtotal** |  |  |  |  |  | **11/24** | **45.8%** |

## HTTPX

| Task | Type | F1 | F2 | F3 | F4 | Score | Notes |
|---|---|---|---|---|---|---:|---|
| blind-httpx-struct-1 | struct | C | M | C | M | 2/4 | Missed _transports/ and _urls/_headers split. |
| blind-httpx-struct-2 | struct | C | M | M | M | 1/4 | Only Client/AsyncClient split was clearly covered. |
| blind-httpx-rel-1 | rel | C | C | C | M | 3/4 | Missed auth-flow request injection. |
| blind-httpx-rel-2 | rel | M | M | M | M | 0/4 | Did not cover BaseTransport / HTTPTransport / MockTransport / mount(). |
| blind-httpx-mech-1 | mech | M | M | M | M | 0/4 | Did not cover follow_redirects flag, per-request timeout, event hooks, or proxy-via-transport. |
| blind-httpx-mech-2 | mech | C | C | M | M | 2/4 | Missed response.json encoding behavior and HTTP/2 support. |
| **httpx subtotal** |  |  |  |  |  | **8/24** | **33.3%** |

## Summary by repo

| Repo | Covered | Miss | Coverage |
|---|---:|---:|---:|
| requests | 17 | 7 | 70.8% |
| echo | 14 | 10 | 58.3% |
| zod | 20 | 4 | 83.3% |
| fastapi | 6 | 18 | 25.0% |
| gin | 10 | 14 | 41.7% |
| express | 11 | 13 | 45.8% |
| httpx | 8 | 16 | 33.3% |

## Summary by knowledge type

| Knowledge type | Covered | Miss | Coverage |
|---|---:|---:|---:|
| struct | 29 | 27 | 51.8% |
| rel | 34 | 22 | 60.7% |
| mech | 23 | 33 | 41.1% |

## Notes

- Scoring is against the provided gold facts only, not overall answer quality.
- A fact is marked COVERED only when the response states the relevant mechanism with enough specificity/evidence; otherwise MISS.