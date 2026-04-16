# Blind Scoring (v241)

Rubric: **COVERED** = describes the specific mechanism with evidence and captures >50% of the gold fact. **MISS** = absent, too vague, or wrong.

## Per-task scoring

### blind-requests-struct-1 — 4/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 helpers under `requests.api` | COVERED | Explicitly places verb helpers in `src/requests/api.py`. |
| F2 `Session` under `requests.sessions` | COVERED | Explicitly places `Session` in `src/requests/sessions.py`. |
| F3 `Request`/`PreparedRequest`/`Response` under `requests.models` | COVERED | All three are located in `src/requests/models.py`. |
| F4 `BaseAdapter`/`HTTPAdapter` and exceptions from dedicated modules | COVERED | Identifies `adapters.py` as the adapter module and `exceptions.py` as the exception module. |

### blind-requests-struct-2 — 3/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 API organized into layers | COVERED | Response explicitly frames Requests as layered. |
| F2 Main interface = convenience functions returning `Response` | COVERED | Top layer is module-level convenience helpers around `request()`, which is enough for the public-interface claim. |
| F3 `Session` with persistent state | COVERED | Session is singled out as the orchestration layer with long-lived session behavior. |
| F4 Lower layers separate `Request` from `PreparedRequest` | MISS | It lists both types but does not explain the lower-layer separation between raw `Request` and wire-ready `PreparedRequest`. |

### blind-requests-rel-1 — 3/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 `Request`→`PreparedRequest` | COVERED | Pipeline explicitly says `Session` turns `Request` into `PreparedRequest`. |
| F2 `Session.prepare_request` merges | COVERED | `prepare_request` is tied to `merge_hooks` and `merge_setting`. |
| F3 `Session.send` accepts `PreparedRequest` | COVERED | Explicitly says `Session.send` sends a given `PreparedRequest`. |
| F4 `Response.request` back-ref | MISS | No mention of `Response.request` pointing back to the originating request. |

### blind-requests-rel-2 — 3/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 `Session.mount` by prefix | COVERED | Explicitly says `mount` registers adapters to URL prefixes. |
| F2 Descending prefix length sort | MISS | Response explicitly says longest-prefix behavior cannot be determined. |
| F3 `get_adapter` returns `BaseAdapter` | COVERED | It ties adapter selection to the `BaseAdapter` transport abstraction, which is enough to capture the return-type relationship. |
| F4 `HTTPAdapter` bridges to urllib3 | COVERED | Uses `build_response` from urllib3 response and ties it to `HTTPAdapter`. |

### blind-requests-mech-1 — 2/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 Method merged, method priority | COVERED | Clearly states request/per-call values override session values in `merge_setting`. |
| F2 `None` suppresses session key | COVERED | Explicitly states merged dict keys with `None` are deleted. |
| F3 `Request.prepare` skips session | MISS | No contrast between direct `Request.prepare()` and `Session.prepare_request()`. |
| F4 Needs `merge_environment_settings` | MISS | Describes the helper itself, but not the key implication that manual prepared flow needs a separate `merge_environment_settings()` call. |

### blind-requests-mech-2 — 1/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 `stream=False` downloads immediately | MISS | Immediate-download behavior is not discussed. |
| F2 `iter_content(None)` differs | MISS | No explanation of the `iter_content(None)` special case. |
| F3 `text` headers first, charset fallback | MISS | Mentions header-derived unicode helpers, but not the full header-first then fallback behavior. |
| F4 `json` raises `JSONDecodeError` | COVERED | Explicitly says `json` raises `RequestsJSONDecodeError`. |

### blind-echo-struct-1 — 3/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 Core defines Echo/Context/routing/binding | COVERED | Core package is described as owning Echo, Context, routing, and binding. |
| F2 Middleware separate package | COVERED | Clearly separates `middleware/` from core. |
| F3 Paired constructor pattern | COVERED | Identifies the recurring `Config` + `ToMiddleware` pattern. |
| F4 External middleware separate repos | MISS | No mention of external middleware living in separate repositories. |

### blind-echo-struct-2 — 4/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 `Echo`/`Context`/`DefaultRouter` | COVERED | All three are explicitly identified. |
| F2 Method-specific→`*Route` | COVERED | Method helpers are described as funneling into central route registration. |
| F3 `Echo.Group`→`*Group` | COVERED | Explicitly says `Echo.Group` creates a `Group`. |
| F4 Binding/JSON/validation interfaces | COVERED | Covers binder and JSON serializer interface surfaces well enough to satisfy the interface-organization fact. |

### blind-echo-rel-1 — 2/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 Echo owns registration, handlers use `Context` | COVERED | Echo owns registration flow and handlers are described as receiving `Context`. |
| F2 Group prefixed sub-router | COVERED | Group is described as a prefixed sub-route mechanism delegating into Echo. |
| F3 Group middleware inherited | MISS | It mentions group-scoped middleware, but not inheritance onto descendant routes/groups as a mechanism. |
| F4 Handlers/middleware share context | MISS | It discusses handlers using `Context`, but does not explicitly connect middleware to the same shared `Context` object. |

### blind-echo-rel-2 — 4/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 Pre vs regular = two stages | COVERED | Clearly distinguishes `Echo.Pre` and `Echo.Use` timing. |
| F2 Radix-tree, match priority | COVERED | Describes tree-based route matching with static-child priority. |
| F3 `Any`/`Match` APIs | COVERED | Both APIs are explicitly described. |
| F4 Route-level stacks on root/group | COVERED | It identifies `...MiddlewareFunc` varargs on route registration and mirrors that registration pattern for groups. |

### blind-echo-mech-1 — 1/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 Static>parameterized>wildcard | MISS | It gets static-first, but explicitly says parameter-vs-wildcard priority cannot be confirmed. |
| F2 Structural priority | COVERED | Priority is grounded in traversal structure (`findStaticChild`, route tree walk), not registration order. |
| F3 Wildcard zero+ chars | MISS | Wildcard consumption semantics are not stated. |
| F4 Only first match-any | MISS | It discusses HTTP-method fallback-to-any, not the route-matching “first match-any wins” rule. |

### blind-echo-mech-2 — 2/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 Default handler JSON | MISS | Response says exact JSON/plain-text formatting cannot be determined. |
| F2 error=500, HTTPError=embedded | MISS | It covers embedded `HTTPError` status codes, but does not establish the ordinary-error default as 500. |
| F3 Debug exposes message | COVERED | `exposeError` is explicitly tied to exposing error details. |
| F4 Check committed | COVERED | Strong explicit coverage of committed-response guards. |

### blind-zod-struct-1 — 3/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 `zod` full package | COVERED | Identifies the full/classic `zod` package surface. |
| F2 `zod/mini` functional | COVERED | Describes mini as the lightweight reduced-API surface. |
| F3 `zod/v4/core` substrate | COVERED | Clearly identifies core as the shared foundation. |
| F4 English locale auto-loaded by `zod` not mini | MISS | Locale auto-loading distinction is not mentioned. |

### blind-zod-struct-2 — 2/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 `$ZodType` base class | COVERED | Explicitly identifies `$ZodType` as the base/root type. |
| F2 `_zod.def` field | MISS | `_zod.def` is not discussed. |
| F3 `$ZodCheck` refinements | COVERED | The check layer in `v4/core/checks.ts` is explicitly described. |
| F4 `$ZodError`+issues | MISS | `$ZodError` is mentioned, but the issue-structure side of the fact is not described clearly enough. |

### blind-zod-rel-1 — 3/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 schemas extend `$ZodType` | COVERED | Response describes schema surfaces as extending the core base abstractions. |
| F2 `ZodMiniType` extends `$ZodType` | COVERED | Explicitly stated. |
| F3 `ZodError` subclass `$ZodError` | COVERED | Explicitly stated for the classic v4 error type. |
| F4 String-format dual hierarchy | MISS | It covers the string-format schema hierarchy, but not the dual schema/check hierarchy. |

### blind-zod-rel-2 — 2/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 Parse then check | COVERED | Response explicitly describes parse flow feeding later checks/issues. |
| F2 `parse` vs `safeParse` | MISS | It names safe-parse result types, but does not contrast throwing vs result-returning APIs. |
| F3 Async forces async parsing | MISS | Async APIs are listed, but the “async refinement/check forces async parse” rule is not given. |
| F4 Error maps on top | COVERED | Clearly places error maps after issues/check failures. |

### blind-zod-mech-1 — 4/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 object strips unknown | COVERED | Explicitly says strip mode removes unknown keys. |
| F2 `strictObject` errors | COVERED | Explicitly says strict mode fails on unknown keys. |
| F3 `looseObject` passes | COVERED | Describes passthrough/loose behavior preserving unknown keys. |
| F4 `catchall` validates | COVERED | Explicitly says unknown keys are validated against the catchall schema. |

### blind-zod-mech-2 — 1/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 Schema-level highest | COVERED | It clearly places inline/schema check messages at the top of the stack. |
| F2 Per-parse below schema | MISS | No distinct per-parse error-customization layer is identified. |
| F3 `z.config` below per-parse | MISS | `z.config` is not discussed. |
| F4 `undefined` yields | MISS | No fallback-by-returning-`undefined` behavior is described. |

## Summary by task

| Task | Score |
|---|---:|
| blind-requests-struct-1 | 4/4 |
| blind-requests-struct-2 | 3/4 |
| blind-requests-rel-1 | 3/4 |
| blind-requests-rel-2 | 3/4 |
| blind-requests-mech-1 | 2/4 |
| blind-requests-mech-2 | 1/4 |
| blind-echo-struct-1 | 3/4 |
| blind-echo-struct-2 | 4/4 |
| blind-echo-rel-1 | 2/4 |
| blind-echo-rel-2 | 4/4 |
| blind-echo-mech-1 | 1/4 |
| blind-echo-mech-2 | 2/4 |
| blind-zod-struct-1 | 3/4 |
| blind-zod-struct-2 | 2/4 |
| blind-zod-rel-1 | 3/4 |
| blind-zod-rel-2 | 2/4 |
| blind-zod-mech-1 | 4/4 |
| blind-zod-mech-2 | 1/4 |
| **Grand total** | **47/72** |

## Summary by repo

| Repo | Score | Pct |
|---|---:|---:|
| requests | 16/24 | 66.7% |
| echo | 16/24 | 66.7% |
| zod | 15/24 | 62.5% |
| **All repos** | **47/72** | **65.3%** |

## Summary by type

| Type | Score | Pct |
|---|---:|---:|
| struct | 19/24 | 79.2% |
| rel | 17/24 | 70.8% |
| mech | 11/24 | 45.8% |
| **All types** | **47/72** | **65.3%** |
