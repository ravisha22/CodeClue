# v2.2 Blind Evaluation Scoring
Date: 2025-07-18

---

## REQUESTS

### blind-requests-struct-1 (3/4)
F1: COVERED — Response documents `request`, `get`, `post`, etc. under `src/requests/api.py` with full listing of all HTTP-verb convenience functions.
F2: COVERED — Response documents `Session`, `prepare_request`, `send`, `merge_setting`, `get_adapter`, `mount` all under `src/requests/sessions.py`.
F3: COVERED — Response documents `Request`, `PreparedRequest`, `Response` all under `src/requests/models.py` with class details.
F4: MISS — Response only covers three modules (api, sessions, models). Does not discuss `BaseAdapter`/`HTTPAdapter` from `adapters.py` or exceptions from `exceptions.py` as dedicated modules in this structural answer.

### blind-requests-struct-2 (4/4)
F1: COVERED — Response organizes into Layer 1 (Convenience API), Layer 2 (Session), Layer 3 (Models), Layer 4 (Transport Adapters), plus Supporting Modules table listing exceptions, auth, cookies, etc.
F2: COVERED — Layer 1 described as module-level convenience functions that all delegate to `request`; labeled "the simplest public surface."
F3: COVERED — Layer 2 centers on `Session` class providing "stateful session orchestration" with persistent attributes like cookies, headers, auth.
F4: COVERED — Layer 3 explicitly separates `Request` ("user-created"), `PreparedRequest` ("fully mutable … ready for transmission"), and `Response` as distinct model classes.

### blind-requests-rel-1 (3/4)
F1: COVERED — Explicitly states "The Request → PreparedRequest transition is a preparation step" and documents the four-stage pipeline.
F2: COVERED — `prepare_request` "merges session-level settings (headers, cookies, auth, hooks) into it" using `merge_hooks` and `merge_setting`.
F3: COVERED — `send` takes a `PreparedRequest` (sig shown), `get_adapter` finds adapter, `build_response` creates `Response` from urllib3.
F4: MISS — Response never mentions `Response.request` attribute that back-references the `PreparedRequest`.

### blind-requests-rel-2 (4/4)
F1: COVERED — `mount` documented as "Registers a connection adapter to a prefix" with `sig: mount(prefix, adapter)`.
F2: COVERED — Response infers prefixes are "likely ordered (e.g., longest-prefix-first) so that more specific prefixes match before general ones" from the ACCUMULATE behavior.
F3: COVERED — `get_adapter` documented as "Returns the appropriate connection adapter for the given URL" by iterating prefix→adapter pairs.
F4: COVERED — `HTTPAdapter` described as "The built-in HTTP Adapter for urllib3"; `send` takes `PreparedRequest`; `build_response` creates `Response` from urllib3 response.

### blind-requests-mech-1 (2/4)
F1: COVERED — Response identifies per-call over session precedence: `merge_setting(request_setting, session_setting)` parameter order confirms "per-call settings take precedence over session defaults."
F2: MISS — Response explicitly states it cannot determine how None values are treated; listed under "What Cannot Be Fully Determined."
F3: MISS — Response does not discuss `Request.prepare()` as a standalone path that skips session state.
F4: COVERED — `merge_environment_settings` documented as merging environment into settings; called by `Session.request` for proxies, certs, env vars.

### blind-requests-mech-2 (2/4)
F1: MISS — Response does not discuss the `stream` parameter or that `stream=False` eagerly downloads bytes.
F2: MISS — Response does not discuss `iter_content(None)` behavior differences by mode.
F3: COVERED — Response identifies `get_encoding_from_headers` for header-based charset extraction and mentions fallback encoding detection; `text` property uses detected encoding or fallback.
F4: COVERED — `json()` documented as raising `RequestsJSONDecodeError` for malformed/missing JSON.

---

## ECHO

### blind-echo-struct-1 (3/4)
F1: COVERED — Core framework section documents `Echo`, `Context`, routing (`Group`, `DefaultRouter`), data binding (`ValueBinder`, `Bind*` functions) from top-level .go files.
F2: COVERED — Middleware in separate `middleware/` package with 24 files, fully listed in Section 3.
F3: COVERED — Explicitly notes "Every middleware follows a consistent dual-function pattern: a convenience constructor and a WithConfig variant" with full table.
F4: MISS — Response only discusses the in-repo `middleware/` package; no mention of external middleware in separate repositories.

### blind-echo-struct-2 (4/4)
F1: COVERED — `Echo` (echo.go:68) as app type, `Context` (context.go:40) per-request, `DefaultRouter` (router.go:60) all documented.
F2: COVERED — `Echo.GET` and other method-specific functions documented with signature returning `RouteInfo`; `*Route` type also documented.
F3: COVERED — `Group` (group.go:14) described as "a set of sub-routes for a specified route prefix"; `Echo.Group` creates it.
F4: COVERED — Binding (ValueBinder, BindingError), JSON (DefaultJSONSerializer), and middleware configuration (MiddlewareConfigurator interface) documented as separate interfaces.

### blind-echo-rel-1 (3/4)
F1: COVERED — "Echo manages the lifecycle of Context objects"; handlers registered through `Echo.Add` receive `Context` which wraps `http.Request` internally.
F2: COVERED — "Group is a thin facade over Echo. Route registration always flows back to Echo.add" with prefix-based sub-routing.
F3: MISS — Response does not address whether middleware from parent groups is inherited by child groups; only shows Group.Use exists.
F4: COVERED — Dispatch flow shows both middleware chain and handler receive the same `Context`; `applyMiddleware` wraps handler and middleware together.

### blind-echo-rel-2 (3/4)
F1: COVERED — `Echo.Pre` runs "before router tries to find matching route"; `Echo.Use` runs "after router has found matching route" — two distinct stages.
F2: MISS — Response mentions tree-based routing with PRECEDENCE but explicitly says "The exact tree data structure (radix tree, trie, or other) is not fully determinable." Radix-tree not confirmed.
F3: COVERED — `Echo.Any` "registers a route for all HTTP methods"; `Echo.Match` "registers a route for multiple HTTP methods" — both documented.
F4: COVERED — Execution order shows route-level middleware (step 4) stacking on top of post-router middleware (step 3) which stacks on pre-router middleware (step 1).

### blind-echo-mech-1 (2/4)
F1: COVERED — "Inferred priority order: 1. Static segments (highest priority), 2. Parameter segments, 3. Wildcard/catch-all segments (lowest priority)."
F2: COVERED — Priority described as node-type-based (structural) through tree traversal with GUARD/PRECEDENCE annotations; backtracking between node types, not based on registration order.
F3: MISS — Response says "matches remaining path" but does not specify that wildcard consumes zero or more characters (i.e., can match empty suffix).
F4: MISS — Response does not discuss the rule that only the first match-any/wildcard segment matters.

### blind-echo-mech-2 (2/4)
F1: MISS — Response discusses `DISPATCH(m)` but does not confirm JSON as the default error response format (mentions JSON/plain text as possibilities).
F2: COVERED — Plain error defaults to "HTTP 500 Internal Server Error"; `HTTPError.StatusCode` provides embedded code directly.
F3: COVERED — `exposeError bool` parameter on `DefaultHTTPErrorHandler` controls "whether internal error details are exposed in responses" — equivalent to debug mode.
F4: MISS — Response discusses committed-response detection in the default handler but does not state the guidance that custom handlers should check whether response is committed.

---

## ZOD

### blind-zod-struct-1 (3/4)
F1: COVERED — Response labels zod as "Full / Classic" package, describing the class-based developer-facing API surface.
F2: COVERED — `zod/mini` documented as a separate "Lightweight Interface-Based API" with its own base types and schema interfaces.
F3: COVERED — `zod/v4/core` described as "Shared Foundation" that "both the full and mini packages build upon."
F4: MISS — Response does not mention English locale auto-loading or any locale difference between zod and zod/mini.

### blind-zod-struct-2 (2/4)
F1: COVERED — `ZodType` documented as root base class (v3) and `_ZodType` as internal base (v4) with concrete schema subclasses extending them.
F2: MISS — Response mentions `_def` in v3 context but does not describe the `_zod` property with `def` field (v4/core pattern).
F3: MISS — Response discusses `_addCheck` mechanism and check params but does not describe `$ZodCheck` as a class hierarchy with subclasses for refinements.
F4: COVERED — `ZodError` documented in v3 (extends Error) and v4 (interface); issue types listed with `core.$ZodIssue` references.

### blind-zod-rel-1 (2/4)
F1: COVERED — Response shows all v3 schemas extending `ZodType` and v4 mini types extending `_ZodMiniType`; core inheritance chain documented.
F2: MISS — Response shows `ZodMiniType` as a separate top-level interface but does not establish it extends `$ZodType`; notes relationship "cannot be determined."
F3: MISS — Response does not describe `ZodError` (v4 classic) as a subclass of `$ZodError` (v4 core); only shows v3 ZodError extends Error and v4 is an interface.
F4: COVERED — String-format types shown in both schema hierarchy (ZodMiniEmail etc. extending _ZodMiniString in mini) and refinement pattern (_addCheck on ZodString in v3).

### blind-zod-rel-2 (2/4)
F1: COVERED — `ZodString._parse` behavior shows `PRECEDENCE(_def_coerce -> parsedType -> check -> default)` with checks evaluated after type parsing — parse-then-check pipeline.
F2: MISS — Response lists both `parse` and `safeParse` methods but does not explain the difference (parse throws on error vs safeParse returns result object).
F3: MISS — Response does not discuss async refinements forcing async parsing.
F4: COVERED — Error maps documented via `ZodType.setError` and `getErrorMap` as customization layers on top of validation issues.

### blind-zod-mech-1 (2/4)
F1: MISS — Response explicitly says default unknown-key mode "cannot be determined" from the clue.
F2: COVERED — `strict` documented as "rejects input containing unrecognized keys (raises an error)."
F3: MISS — Response attributes "passes through" to `passthrough`, not to `loose`; says exact semantics of `loose` are unclear.
F4: COVERED — `catchall(schema: T)` documented as "validates unrecognized keys against a provided schema."

### blind-zod-mech-2 (1/4)
F1: COVERED — Per-check inline message identified as highest precedence in the inferred ordering; equivalent to schema-level message on individual checks.
F2: MISS — Response does not discuss per-parse error maps or their precedence relative to schema and global levels.
F3: MISS — Response mentions `getErrorMap` delegating to `core.config` but does not describe `z.config()` precedence relative to per-parse maps and locale.
F4: MISS — Response does not describe the behavior that undefined/unset messages yield to the next customization level.

---

## Summary Table

| Task | Category | Score |
|------|----------|-------|
| blind-requests-struct-1 | structural | 3/4 |
| blind-requests-struct-2 | structural | 4/4 |
| blind-requests-rel-1 | relational | 3/4 |
| blind-requests-rel-2 | relational | 4/4 |
| blind-requests-mech-1 | mechanistic | 2/4 |
| blind-requests-mech-2 | mechanistic | 2/4 |
| **Requests subtotal** | | **18/24** |
| blind-echo-struct-1 | structural | 3/4 |
| blind-echo-struct-2 | structural | 4/4 |
| blind-echo-rel-1 | relational | 3/4 |
| blind-echo-rel-2 | relational | 3/4 |
| blind-echo-mech-1 | mechanistic | 2/4 |
| blind-echo-mech-2 | mechanistic | 2/4 |
| **Echo subtotal** | | **17/24** |
| blind-zod-struct-1 | structural | 3/4 |
| blind-zod-struct-2 | structural | 2/4 |
| blind-zod-rel-1 | relational | 2/4 |
| blind-zod-rel-2 | relational | 2/4 |
| blind-zod-mech-1 | mechanistic | 2/4 |
| blind-zod-mech-2 | mechanistic | 1/4 |
| **Zod subtotal** | | **12/24** |
| | | |
| **By category** | structural | 19/24 |
| | relational | 17/24 |
| | mechanistic | 11/24 |
| **GRAND TOTAL** | | **47/72 (65.3%)** |
