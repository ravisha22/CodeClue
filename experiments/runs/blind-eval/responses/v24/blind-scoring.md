# Blind Scoring (v24)

Rubric: **COVERED** = describes the specific mechanism with evidence and captures >50% of the gold fact. **MISS** = absent, too vague, or wrong.

## Per-task scoring

### blind-requests-struct-1 — 4/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 helpers under `requests.api` | COVERED | Explicitly places verb helpers in `src/requests/api.py`. |
| F2 `Session` under `requests.sessions` | COVERED | Explicitly places `Session` in `src/requests/sessions.py`. |
| F3 `Request`/`PreparedRequest`/`Response` under `requests.models` | COVERED | All three are located in `src/requests/models.py` with evidence. |
| F4 `BaseAdapter`/`HTTPAdapter` and exceptions from dedicated modules | COVERED | Cites `adapters.py` and `exceptions.py` as dedicated modules. |

### blind-requests-struct-2 — 4/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 API organized into layers | COVERED | Response explicitly frames Requests as layered. |
| F2 Main interface = convenience functions returning `Response` | COVERED | Top layer is module-level helper functions delegating to `request()`. |
| F3 `Session` with persistent state | COVERED | Describes stateful session with cookies/config/adapters. |
| F4 Lower layers separate `Request` from `PreparedRequest` | COVERED | Clearly distinguishes user-facing `Request` from wire-ready `PreparedRequest`. |

### blind-requests-rel-1 — 3/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 `Request`→`PreparedRequest` before transport | COVERED | Pipeline is explicitly described in that order. |
| F2 `Session.prepare_request` merges state | COVERED | Says it merges session headers/params/auth/cookies/hooks. |
| F3 `Session.send` accepts `PreparedRequest` | COVERED | Explicitly states `Session.send()` sends a `PreparedRequest`. |
| F4 `Response.request` back-ref | MISS | No mention of `Response.request` pointing back to the request. |

### blind-requests-rel-2 — 4/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 `Session.mount` by prefix | COVERED | Describes/presents prefix-keyed adapter mounting. |
| F2 Descending prefix length sort | COVERED | Explicitly notes longest-prefix-first ordering. |
| F3 `get_adapter` returns `BaseAdapter` | COVERED | Identifies return type as `BaseAdapter`. |
| F4 `HTTPAdapter` bridges to urllib3 | COVERED | Explicitly describes adapter as urllib3 bridge. |

### blind-requests-mech-1 — 3/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 Method-level merged, method priority | COVERED | Explains per-call settings override session defaults. |
| F2 `None` suppresses session key | COVERED | Explicitly says `None` deletes merged keys. |
| F3 `Request.prepare` skips session state | MISS | Does not contrast direct `Request.prepare()` with `Session.prepare_request()`. |
| F4 Needs `merge_environment_settings` | COVERED | Explicitly includes environment merge stage. |

### blind-requests-mech-2 — 1/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 `stream=False` downloads immediately | MISS | No explicit coverage of `stream=False` immediate download behavior. |
| F2 `iter_content(None)` differs by mode | MISS | No clear explanation of `iter_content(None)` behavior by mode. |
| F3 `text` headers first, charset fallback | MISS | Covers header-based encoding but explicitly says fallback cannot be determined. |
| F4 `json` raises `JSONDecodeError` | COVERED | Explicitly states JSON decode error path (`RequestsJSONDecodeError`). |

### blind-echo-struct-1 — 3/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 Core defines Echo/Context/routing/binding | COVERED | Attributes Echo, Context, routing, and binding to core package. |
| F2 Middleware separate package | COVERED | Clearly separates `middleware/` package from core. |
| F3 Paired constructor pattern | COVERED | Describes config + `ToMiddleware()` plus convenience constructor pattern. |
| F4 External middleware separate repos | MISS | No mention of external middleware repositories. |

### blind-echo-struct-2 — 4/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 `Echo`/`Context`/`DefaultRouter` | COVERED | All three are explicitly identified. |
| F2 Method-specific registration→`*Route` | COVERED | Explains verb registration delegating to central route registration. |
| F3 `Echo.Group`→`*Group` | COVERED | Explicitly says `Echo.Group` creates a `Group`. |
| F4 Binding/JSON/validation interfaces | COVERED | Covers `Context.Bind`, JSON serializer, and binder/validation surface. |

### blind-echo-rel-1 — 3/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 Echo owns registration, handlers use `Context` | COVERED | Explicitly states Echo registers routes and handlers receive Context. |
| F2 Group prefixed sub-router | COVERED | Describes Group as prefixing paths and delegating into Echo/router. |
| F3 Group middleware inherited | COVERED | Explicitly says group middleware is attached/inherited by group routes. |
| F4 Handlers/middleware share context | MISS | Mentions middleware interaction with Context, but not clearly that handlers and middleware share the same Context object. |

### blind-echo-rel-2 — 4/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 Pre vs regular = two stages | COVERED | Clearly distinguishes pre-routing and regular middleware stages. |
| F2 Radix-tree, match-type priority | COVERED | Describes trie/radix routing and priority ordering. |
| F3 `Any`/`Match` APIs | COVERED | Explicit coverage of both APIs. |
| F4 Route-level stacks on root/group | COVERED | Explains route-level middleware on root/group registrations. |

### blind-echo-mech-1 — 2/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 Static>parameterized>wildcard | COVERED | Explicitly states this priority. |
| F2 Structural priority | COVERED | Grounds priority in traversal structure/order. |
| F3 Wildcard zero+ chars | MISS | No explicit zero-or-more semantics for wildcard. |
| F4 Only first match-any matters | MISS | Does not state the first match-any handler rule. |

### blind-echo-mech-2 — 3/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 Default handler emits JSON | MISS | Response says exact JSON/plain-text formatting is not available. |
| F2 error=500, HTTPError=embedded code | COVERED | States HTTPError uses embedded code and ordinary errors default to 500. |
| F3 Debug exposes message | COVERED | Explicitly ties `exposeError`/debug behavior to message exposure. |
| F4 Check response committed | COVERED | Explicitly describes committed-response guard/early return. |

### blind-zod-struct-1 — 3/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 `zod` full package | COVERED | Identifies classic/full `zod` layer. |
| F2 `zod/mini` functional | COVERED | Describes mini as lightweight functional surface. |
| F3 `zod/v4/core` substrate | COVERED | Clearly identifies core as the foundational substrate. |
| F4 English locale auto-loaded by `zod` not mini | MISS | No locale auto-load distinction mentioned. |

### blind-zod-struct-2 — 3/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 `$ZodType` base class | COVERED | Explicitly identifies `$ZodType` as the base/root type. |
| F2 `_zod.def` field | MISS | `_zod.def` is not mentioned. |
| F3 `$ZodCheck` refinements | COVERED | Explicitly covers centralized `$ZodCheck`/check types. |
| F4 `$ZodError`+issues | COVERED | Covers `$ZodError` and issue-based error structure. |

### blind-zod-rel-1 — 4/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 schemas extend `$ZodType` | COVERED | Describes schema hierarchy extending core base types. |
| F2 `ZodMiniType` extends `$ZodType` | COVERED | Explicitly stated. |
| F3 `ZodError` subclass `$ZodError` | COVERED | Explicitly stated. |
| F4 String-format dual hierarchy | COVERED | Covers string-format hierarchy in detail. |

### blind-zod-rel-2 — 4/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 Parse then check | COVERED | Pipeline explicitly says parse first, then checks. |
| F2 `parse` vs `safeParse` | COVERED | Explicitly contrasts throwing vs result-returning APIs. |
| F3 Async forces async parsing | COVERED | Explicitly covers sync parse throwing on Promise / need for async parse. |
| F4 Error maps on top | COVERED | Explicitly layers error-map resolution over validation/checking. |

### blind-zod-mech-1 — 4/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 object strips unknown | COVERED | Explicitly says strip mode removes unknown keys. |
| F2 `strictObject` errors | COVERED | Explicitly says strict mode errors on unknown keys. |
| F3 `looseObject` passes | COVERED | Explicitly says loose/passthrough preserves unknown keys. |
| F4 `catchall` validates | COVERED | Explicitly states unknown keys are validated via catchall schema. |

### blind-zod-mech-2 — 3/4
| Fact | Verdict | Notes |
|---|---|---|
| F1 Schema-level highest | COVERED | Highest-priority schema/check-level message is described. |
| F2 Per-parse below schema above global | MISS | No distinct per-parse layer is identified. |
| F3 `z.config` below per-parse | COVERED | Global config layer is explicitly placed below more specific settings. |
| F4 `undefined` yields | COVERED | Explicit fallback to built-in/default message is described. |

## Summary by task

| Task | Score |
|---|---:|
| blind-requests-struct-1 | 4/4 |
| blind-requests-struct-2 | 4/4 |
| blind-requests-rel-1 | 3/4 |
| blind-requests-rel-2 | 4/4 |
| blind-requests-mech-1 | 3/4 |
| blind-requests-mech-2 | 1/4 |
| blind-echo-struct-1 | 3/4 |
| blind-echo-struct-2 | 4/4 |
| blind-echo-rel-1 | 3/4 |
| blind-echo-rel-2 | 4/4 |
| blind-echo-mech-1 | 2/4 |
| blind-echo-mech-2 | 3/4 |
| blind-zod-struct-1 | 3/4 |
| blind-zod-struct-2 | 3/4 |
| blind-zod-rel-1 | 4/4 |
| blind-zod-rel-2 | 4/4 |
| blind-zod-mech-1 | 4/4 |
| blind-zod-mech-2 | 3/4 |
| **Grand total** | **59/72** |

## Summary by repo

| Repo | Score | Pct |
|---|---:|---:|
| requests | 19/24 | 79.2% |
| echo | 19/24 | 79.2% |
| zod | 21/24 | 87.5% |
| **All repos** | **59/72** | **81.9%** |

## Summary by type

| Type | Score | Pct |
|---|---:|---:|
| struct | 21/24 | 87.5% |
| rel | 22/24 | 91.7% |
| mech | 16/24 | 66.7% |
| **All types** | **59/72** | **81.9%** |
