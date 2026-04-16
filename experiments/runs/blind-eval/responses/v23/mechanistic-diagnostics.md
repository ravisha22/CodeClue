# Mechanistic v2.3 Miss Diagnostics

### blind-aiohttp-1 (2/4)
F3 [MISS]: BaseRequest.post returns an empty MultiDict for non-POST-like methods or unsupported content types.
  Category: FOCUS_MISS
  Symbol in FOCUS: no
  Symbol in GAPS drill: no
  Symbol in drill snippets: no
  Behavior annotation: none
  Notes: Gold symbol is BaseRequest.post. The clue focuses read/json/multipart helpers, but post itself is missing from FOCUS and never selected for drill-down.
F4 [MISS]: Multipart file parts are streamed into a TemporaryFile via the executor, size-checked while streaming, and surfaced as FileField values.
  Category: FOCUS_MISS
  Symbol in FOCUS: no
  Symbol in GAPS drill: no
  Symbol in drill snippets: no
  Behavior annotation: none
  Notes: The relevant BaseRequest.post/FileField upload path is absent from FOCUS and GAPS, so the drill-down never reached the multipart file-body logic.

### blind-aiohttp-2 (3/4)
F3 [MISS]: CleanupContext._on_startup accepts async context managers or async-generator callbacks, wraps generators with asynccontextmanager, and stores exits in order.
  Category: BEHAVIOR_SHALLOW
  Symbol in FOCUS: yes
  Symbol in GAPS drill: no
  Symbol in drill snippets: no
  Behavior annotation: shallow
  Notes: CleanupContext._on_startup is in FOCUS, but only as ACCUMULATE(loop -> exits). That abstraction misses the key generator-vs-context-manager normalization step; drill-down targeted _cleanup_server/shutdown instead.

### blind-fiber-1 (0/4)
F1 [MISS]: DefaultCtx.Path(override) mutates the underlying fasthttp URI, stores the override, and recomputes Fiber path fields.
  Category: BEHAVIOR_SHALLOW
  Symbol in FOCUS: yes
  Symbol in GAPS drill: no
  Symbol in drill snippets: no
  Behavior annotation: shallow
  Notes: DefaultCtx.Path is in FOCUS, but its DELEGATE(c.app.toString -> result) annotation is far too abstract to reveal the URI mutation and path recomputation behavior.
F2 [MISS]: DefaultCtx.RestartRouting resets indexRoute to -1 and restarts dispatch through app.next/app.nextCustom.
  Category: FOCUS_MISS
  Symbol in FOCUS: no
  Symbol in GAPS drill: no
  Symbol in drill snippets: no
  Behavior annotation: none
  Notes: RestartRouting is not present in FOCUS, so the clue never surfaced the actual rerouting entry point.
F3 [MISS]: App.next scans treeStack for the current method/path, skips mounted routes, uses Route.match, records the matched route, and executes the first handler.
  Category: FOCUS_MISS
  Symbol in FOCUS: no
  Symbol in GAPS drill: no
  Symbol in drill snippets: no
  Behavior annotation: none
  Notes: App.next is the core dispatcher, but it is absent from FOCUS and therefore never available for drill-down.
F4 [MISS]: If another method matches the same path, App.next appends Allow and returns ErrMethodNotAllowed; otherwise it returns ErrNotFound.
  Category: FOCUS_MISS
  Symbol in FOCUS: no
  Symbol in GAPS drill: no
  Symbol in drill snippets: no
  Behavior annotation: none
  Notes: The 404-vs-405 branch lives in App.next/method-match handling, which is missing from FOCUS entirely.

### blind-fiber-2 (3/4)
F3 [MISS]: Fiber constructor New installs DefaultErrorHandler when Config.ErrorHandler is nil.
  Category: CLASSIFIER_WRONG
  Symbol in FOCUS: no
  Symbol in GAPS drill: no
  Symbol in drill snippets: no
  Behavior annotation: none
  Notes: The task is mechanistic, but the clue labeled it STRUCTURAL, so no drill-down was produced. The constructor path (New/config initialization) never entered FOCUS.

### blind-click-1 (2/4)
F2 [MISS]: decorators.group is a thin wrapper around command that defaults cls to Group.
  Category: FOCUS_MISS
  Symbol in FOCUS: no
  Symbol in GAPS drill: no
  Symbol in drill snippets: no
  Behavior annotation: none
  Notes: The clue includes the Group class but not the decorators.group helper, so the Group-defaulting mechanism is missing at the source.
F4 [MISS]: Runtime dispatch is Group.parse_args -> _protected_args -> resolve_command -> invoke -> subcontext invocation.
  Category: FOCUS_MISS
  Symbol in FOCUS: no
  Symbol in GAPS drill: no
  Symbol in drill snippets: no
  Behavior annotation: none
  Notes: The core Group.parse_args/resolve_command/invoke dispatch chain is absent from FOCUS; drill-down covered unrelated completion/type helpers instead.

### blind-click-2 (3/4)
F2 [MISS]: Parameter.type_cast_value applies types differently for single values, fixed tuples, variadic tuples, and multiple=True collections.
  Category: FOCUS_MISS
  Symbol in FOCUS: no
  Symbol in GAPS drill: no
  Symbol in drill snippets: no
  Behavior annotation: none
  Notes: The clue focused convert_type, which is about choosing a ParamType, not type_cast_value, which does the collection/tuple dispatch.

### blind-requests-mech-1 (1/4)
F2 [MISS]: merge_setting treats a method-level None as a tombstone that suppresses the session-level key.
  Category: CLASSIFIER_WRONG
  Symbol in FOCUS: yes
  Symbol in GAPS drill: no
  Symbol in drill snippets: no
  Behavior annotation: shallow
  Notes: The clue mislabeled this mechanistic task as RELATIONAL, so no drill-down ran. merge_setting is in FOCUS, but only with a generic ACCUMULATE(loop -> result) annotation that hides the None-suppression rule.
F3 [MISS]: Request.prepare skips session state, whereas Session.prepare_request injects session cookies/defaults during preparation.
  Category: CLASSIFIER_WRONG
  Symbol in FOCUS: no
  Symbol in GAPS drill: no
  Symbol in drill snippets: no
  Behavior annotation: none
  Notes: Because the task was misclassified as RELATIONAL, the prompt stayed clue-only. Session.prepare_request is focused, but Request.prepare—the differentiating symbol—is not.
F4 [MISS]: Prepared-request flows do not auto-apply environment settings; callers must explicitly call Session.merge_environment_settings before send().
  Category: CLASSIFIER_WRONG
  Symbol in FOCUS: yes
  Symbol in GAPS drill: no
  Symbol in drill snippets: no
  Behavior annotation: none
  Notes: merge_environment_settings is in FOCUS, but the task got no drill-down because of the RELATIONAL label, so the explicit-call requirement never became visible.

### blind-requests-mech-2 (1/4)
F1 [MISS]: With stream=False, Session.send eagerly downloads response bytes instead of deferring body fetch until later access.
  Category: FOCUS_MISS
  Symbol in FOCUS: no
  Symbol in GAPS drill: no
  Symbol in drill snippets: no
  Behavior annotation: none
  Notes: The eager-download step lives in the send path, but the clue only focused Response-side helpers (iter_content/content/text) and never surfaced Session.send.
F2 [MISS]: Response.iter_content(None) yields arriving chunks when streaming, but returns the whole body as one chunk when the body was already buffered.
  Category: BEHAVIOR_SHALLOW
  Symbol in FOCUS: yes
  Symbol in GAPS drill: no
  Symbol in drill snippets: no
  Behavior annotation: none
  Notes: iter_content is in FOCUS, but only as “calls: generate” with no behavioral detail about the chunk_size=None branch or the streamed-vs-buffered split.
F3 [MISS]: Response.text prefers header-declared encoding and only falls back to charset detection when encoding is unset.
  Category: BEHAVIOR_SHALLOW
  Symbol in FOCUS: yes
  Symbol in GAPS drill: no
  Symbol in drill snippets: no
  Behavior annotation: none
  Notes: Response.text is in FOCUS, but it has no behavior annotation and no drill-down, so the header-first / detector-fallback rule is lost.

### blind-echo-mech-1 (2/4)
F3 [MISS]: A match-any wildcard like /users/* consumes zero or more remaining characters from that point in the path.
  Category: FOCUS_MISS
  Symbol in FOCUS: no
  Symbol in GAPS drill: no
  Symbol in drill snippets: no
  Behavior annotation: none
  Notes: The clue focused static-file helpers and reverse-routing symbols, not the router wildcard-match internals that define match-any consumption.
F4 [MISS]: If a pattern has multiple match-any segments, only the first effective * matters because it captures the rest of the path.
  Category: FOCUS_MISS
  Symbol in FOCUS: no
  Symbol in GAPS drill: no
  Symbol in drill snippets: no
  Behavior annotation: none
  Notes: The effective-first-* rule lives in route-pattern matching internals that never entered FOCUS or GAPS.

### blind-echo-mech-2 (3/4)
F1 [MISS]: Echo's default HTTP error handler emits JSON error responses by default.
  Category: CLASSIFIER_WRONG
  Symbol in FOCUS: yes
  Symbol in GAPS drill: no
  Symbol in drill snippets: no
  Behavior annotation: none
  Notes: This mechanistic task was mislabeled STRUCTURAL, so there was no drill-down. DefaultHTTPErrorHandler appears in FOCUS only as a signature/called_by entry, not with its response-formatting body.

### blind-zod-mech-1 (4/4)
No missed facts.

### blind-zod-mech-2 (2/4)
F2 [MISS]: A per-parse error map passed to parse ranks below schema-level messages but above global configuration.
  Category: FOCUS_MISS
  Symbol in FOCUS: no
  Symbol in GAPS drill: no
  Symbol in drill snippets: no
  Behavior annotation: none
  Notes: The clue surfaces ZodError.message and a ZodErrorMap type alias, but not the parse/error-map resolution path where per-parse precedence is enforced.
F4 [MISS]: Returning undefined from an error map yields to the next lower-precedence error source instead of finalizing the message.
  Category: FOCUS_MISS
  Symbol in FOCUS: no
  Symbol in GAPS drill: no
  Symbol in drill snippets: no
  Behavior annotation: none
  Notes: The fallback-chain logic is absent from FOCUS/GAPS; the drill-down only targeted constructors and ZodError.message stubs.

## Summary

| Category | Count | % of misses |
|---|---:|---:|
| FOCUS_MISS | 13 | 59.1% |
| BEHAVIOR_SHALLOW | 4 | 18.2% |
| DRILL_MISS | 0 | 0.0% |
| DRILL_ABSENT | 0 | 0.0% |
| CLASSIFIER_WRONG | 5 | 22.7% |
| BUDGET_EXHAUSTED | 0 | 0.0% |

## Top symbols to add to FOCUS or GAPS

- `App.next` and `DefaultCtx.RestartRouting` (drive 3 misses in `blind-fiber-1`, including the reroute restart and 404/405 branch).
- `BaseRequest.post` / `FileField` (drive both multipart/form misses in `blind-aiohttp-1`).
- Click dispatch symbols: `decorators.group`, `Group.parse_args`, `Group.resolve_command`, `Group.invoke`, and `Parameter.type_cast_value`.
- Requests precedence/send symbols: `Request.prepare`, `Session.send`, `merge_setting`, and `Session.merge_environment_settings`.
- Echo router wildcard-match internals (the code that interprets match-any `*` segments).
- Zod error-map resolution helpers for per-parse precedence and `undefined` fallthrough.
- `CleanupContext._on_startup` and `DefaultCtx.Path` need richer behavioral annotations even though they are already in FOCUS.
