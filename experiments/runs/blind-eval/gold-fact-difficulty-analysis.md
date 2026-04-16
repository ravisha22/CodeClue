# Gold Fact Difficulty Analysis

This calibrates the 48 mechanistic gold facts across the two gold-task files.

## Difficulty labels

- **SURFACE** — answerable from symbol name + docstring + behavioral annotation alone
- **MODERATE** — answerable from call-chain tracing + behavioral patterns
- **DEEP** — requires specific function-body logic (exact condition, exact data structure, exact error type)

## Dev mechanistic facts (`blind-gold-tasks.json`)

| Task | Fact | Difficulty | Why |
|---|---|---|---|
| blind-aiohttp-1 | F1 `read()` incremental body accumulation + immediate size exception | **DEEP** | Needs exact loop behavior, threshold check, and specific exception. |
| blind-aiohttp-1 | F2 `json()` calls `text()` and raises `HTTPBadRequest` on bad mimetype | **DEEP** | Depends on exact guard, call order, and error type. |
| blind-aiohttp-1 | F3 `post()` returns empty `MultiDict` for non-post-like / unsupported bodies | **DEEP** | Requires exact branch conditions and exact return structure. |
| blind-aiohttp-1 | F4 multipart upload streams to `TemporaryFile` via executor into `FileField` | **DEEP** | Relies on precise body logic, streaming limit enforcement, and fallback MIME type. |
| blind-aiohttp-2 | F1 startup/shutdown only emit signals; cleanup context does real enter/exit | **MODERATE** | Mostly recoverable by tracing lifecycle call chains and signal wiring. |
| blind-aiohttp-2 | F2 cleanup fallback when `on_cleanup` not frozen | **DEEP** | Requires the exact fallback condition and direct `_cleanup_ctx._on_cleanup` path. |
| blind-aiohttp-2 | F3 `_on_startup` wraps async generators with `asynccontextmanager` | **DEEP** | Depends on exact accepted callback types and wrapper behavior. |
| blind-aiohttp-2 | F4 `_on_cleanup` reverse unwinding + single vs multi-error behavior | **DEEP** | Needs exact unwind order and precise exception aggregation behavior. |
| blind-fiber-1 | F1 `Path()` override mutates fasthttp URI + recomputes path fields | **DEEP** | Requires specific internal mutations across request/context state. |
| blind-fiber-1 | F2 `RestartRouting()` resets `indexRoute` and restarts full scan | **DEEP** | Needs exact state reset and restart entry point. |
| blind-fiber-1 | F3 `App.next` scans `treeStack`, skips mounts, records matched route | **DEEP** | Depends on concrete dispatch data structures and ordered matching logic. |
| blind-fiber-1 | F4 405 path appends `Allow`; otherwise 404 | **DEEP** | Requires exact fallback condition, header mutation, and returned error values. |
| blind-fiber-2 | F1 recover middleware wraps `c.Next()` in `defer/recover` pipeline | **MODERATE** | Mostly call-chain and middleware-flow reasoning. |
| blind-fiber-2 | F2 `DefaultPanicHandler` preserves errors, wraps non-errors | **DEEP** | Requires exact type check and conversion behavior. |
| blind-fiber-2 | F3 constructor installs default error handler when config handler nil | **MODERATE** | Primarily constructor-default wiring and downstream flow. |
| blind-fiber-2 | F4 `App.ErrorHandler` chooses deepest matching mounted sub-app handler | **DEEP** | Needs specific prefix-selection algorithm and fallback order. |
| blind-click-1 | F1 `command()` builds `Command`, harvests params, docstring help, strips suffixes | **DEEP** | Combines several exact transformations, especially CLI name normalization. |
| blind-click-1 | F2 `group()` is `command()` with `cls=Group` | **SURFACE** | Direct helper behavior visible from symbol role and default class choice. |
| blind-click-1 | F3 `add_command()` stores subcommands under effective names for later lookup/help | **MODERATE** | Requires tracing registration into later lookup/help behavior. |
| blind-click-1 | F4 `parse_args` -> `_protected_args` -> `resolve_command` -> `invoke` | **MODERATE** | Requires multi-step runtime call-chain tracing. |
| blind-click-2 | F1 `consume_value()` precedence CLI -> envvar -> `default_map` -> default | **DEEP** | Exact precedence order requires body-level logic. |
| blind-click-2 | F2 `type_cast_value()` branches across scalar / tuple / variadic / multiple | **DEEP** | Depends on exact branching over `nargs` and `multiple`. |
| blind-click-2 | F3 `Choice.convert()` normalizes then returns original declared choice object | **DEEP** | Requires precise normalization steps and returned value semantics. |
| blind-click-2 | F4 `File.convert()` / `Path.convert()` lazy open + cleanup + path constraints | **DEEP** | Combines several exact side effects and filesystem checks. |

## Blind mechanistic facts (`blind-gold-tasks-v2.json`)

| Task | Fact | Difficulty | Why |
|---|---|---|---|
| blind-requests-mech-1 | F1 per-call dictionaries override session dictionaries | **MODERATE** | Requires understanding the merge flow across request/session layers. |
| blind-requests-mech-1 | F2 method-level `None` suppresses session key | **DEEP** | Depends on a special-case branch in merge logic. |
| blind-requests-mech-1 | F3 `Request.prepare()` skips session state; `Session.prepare_request()` applies it | **MODERATE** | Recoverable by comparing two preparation call paths. |
| blind-requests-mech-1 | F4 env settings must be merged explicitly before `send()` | **MODERATE** | Requires call-chain tracing and noticing an omitted step. |
| blind-requests-mech-2 | F1 `stream=False` downloads body immediately | **SURFACE** | Public response-mode behavior usually documented directly. |
| blind-requests-mech-2 | F2 `iter_content(None)` differs by streaming mode | **DEEP** | The `None` chunk-size edge case requires exact body logic. |
| blind-requests-mech-2 | F3 `text` uses headers first, charset detection second | **MODERATE** | Requires decoding-order reasoning but not deep container logic. |
| blind-requests-mech-2 | F4 `json()` raises `JSONDecodeError` instead of returning `None` | **SURFACE** | Public method behavior and raised error are directly exposed. |
| blind-echo-mech-1 | F1 static > param > wildcard route priority | **SURFACE** | Top-level router priority rule is directly expressible. |
| blind-echo-mech-1 | F2 structural priority means registration order does not matter | **SURFACE** | Follows directly from the documented match-priority rule. |
| blind-echo-mech-1 | F3 wildcard consumes zero or more remaining chars | **SURFACE** | Public route-syntax semantics. |
| blind-echo-mech-1 | F4 only first effective `*` matters in multi-wildcard patterns | **DEEP** | Requires exact parser/matcher corner-case behavior. |
| blind-echo-mech-2 | F1 default HTTP error handler emits JSON, not HTML | **SURFACE** | Direct public behavior of the default handler. |
| blind-echo-mech-2 | F2 plain error -> 500, `*HTTPError` keeps embedded status/message | **SURFACE** | Public mapping behavior. |
| blind-echo-mech-2 | F3 debug mode exposes original error message | **SURFACE** | Public config-dependent behavior. |
| blind-echo-mech-2 | F4 custom handlers should bail if response already committed | **MODERATE** | Requires following centralized error-path behavior. |
| blind-zod-mech-1 | F1 `z.object()` strips unknown keys by default | **SURFACE** | Directly documented API behavior. |
| blind-zod-mech-1 | F2 `z.strictObject()` turns unknown keys into validation errors | **SURFACE** | Directly documented API behavior. |
| blind-zod-mech-1 | F3 `z.looseObject()` preserves unknown keys | **SURFACE** | Directly documented API behavior. |
| blind-zod-mech-1 | F4 `.catchall()` validates unknown keys against catchall schema | **SURFACE** | Directly documented API behavior. |
| blind-zod-mech-2 | F1 schema-level custom message is highest precedence | **SURFACE** | Stated directly in the documented precedence chain. |
| blind-zod-mech-2 | F2 per-parse error map ranks below schema-level, above global | **SURFACE** | Stated directly in the documented precedence chain. |
| blind-zod-mech-2 | F3 `z.config()` ranks below per-parse, above locale defaults | **SURFACE** | Stated directly in the documented precedence chain. |
| blind-zod-mech-2 | F4 returning `undefined` yields to the next lower-precedence source | **SURFACE** | Part of the documented fallback semantics. |

## Distribution comparison

| Split | SURFACE | MODERATE | DEEP | MODERATE+DEEP |
|---|---:|---:|---:|---:|
| Dev (aiohttp, click, fiber) | 1 / 24 (4.2%) | 5 / 24 (20.8%) | 18 / 24 (75.0%) | 23 / 24 (95.8%) |
| Blind v2 (requests, echo, zod) | 16 / 24 (66.7%) | 5 / 24 (20.8%) | 3 / 24 (12.5%) | 8 / 24 (33.3%) |

## Interpretation

The split is strongly imbalanced:

- Dev mechanistic gold facts are overwhelmingly **body-logic-heavy**.
- Blind v2 mechanistic gold facts are mostly **surface-documentable**.
- This matches the observed scoring gap already reported elsewhere: **dev mechanistic 29.2% vs blind mechanistic 66.7%**.

## Known evaluation limitation

Yes — the dev mechanistic set is significantly harder than the blind mechanistic set.

That means raw dev-vs-blind mechanistic comparisons are **not difficulty-matched**, so they should be treated as a known evaluation limitation rather than a clean capability difference.

Recommended interpretation:

- treat current dev-vs-blind mechanistic comparisons as **directional**, not apples-to-apples;
- compare within difficulty bands where possible;
- rebalance future gold sets so dev and blind mechanistic facts have similar SURFACE / MODERATE / DEEP mixes before making stronger comparative claims.
