# v2.3 Ablation Scoring — File-1-Only Responses
Date: 2025-07-22

---

### blind-aiohttp-1 (2/4)

F1: **COVERED** — Response identifies `read` as the common entry point for consuming request bytes and explicitly names `HTTPRequestEntityTooLarge` as the raised exception. Does not mention `readany` by name, but the incremental-read + accumulation + size-limit behavior is >50% captured.

F2: **COVERED** — Response states "JSON goes through a text layer first: json … calls text, and can raise HTTPBadRequest" and traces the chain `json → text → read`. Mimetype-rejection reason not explicitly named, but core mechanism (calls text first, HTTPBadRequest) is captured.

F3: **MISS** — Response acknowledges "File 1 does not expose the full body of the top-level post method." No mention of returning empty MultiDict for non-POST-like or unsupported content types.

F4: **MISS** — Response describes multipart chunk-by-chunk reading via BodyPartReader but does not mention TemporaryFile or executor-based writing for file parts.

---

### blind-aiohttp-2 (3/4)

F1: **COVERED** — Response states startup "Causes on_startup signal" and mentions CleanupContext / `_on_cleanup` for resource unwind. The separation between signal-only startup/shutdown and resource-managing CleanupContext is captured, though the distinction could be sharper.

F2: **COVERED** — Response explicitly notes `cleanup` "branches on `on_cleanup.frozen`" and that "cleanup behavior differs depending on how far initialization/signals progressed." This captures the fallback-if-not-frozen mechanism.

F3: **MISS** — Response says `_on_startup` has `ACCUMULATE(loop -> exits)` but does not identify that it accepts async context managers or async-generator callbacks as input types.

F4: **COVERED** — Response states `_on_cleanup` has `ACCUMULATE(loop -> errors); UNWIND(reversed)`, cleanup runs in reverse order, and "multiple failures are gathered and rethrown as one cleanup-specific exception" (`CleanupError`, a `RuntimeError` subclass). Core mechanism fully captured.

---

### blind-fiber-1 (2/4)

F1: **COVERED** — Response identifies `DefaultCtx.Path(override ...string)` as accepting an optional override that rewrites the path. Does not name fasthttp URI mutation specifically, but the path-override/mutation behavior is >50% captured.

F2: **MISS** — Response explicitly states "File 1 does not expose the exact 'restart routing' API." No mention of `RestartRouting` or resetting `indexRoute` to -1.

F3: **MISS** — No mention of `App.next`, `treeStack`, or method+path hash scanning. Response discusses `DefaultRouter.Route` instead, which is a different mechanism.

F4: **COVERED** — Response states Fiber "distinguishes 'matching path but wrong method' from 'no route at all'" and that `routeMethods.updateAllowHeader` "prepares Allow-header information for the former case," explicitly calling it "the 405-style case."

---

### blind-click-1 (2/4)

F1: **COVERED** — Response identifies `command` decorator as creating a new `Command` from the decorated function, and notes `UNWIND(reversed)` behavior for gathering decorator-added metadata. This corresponds to collecting `__click_params__` in reverse. Core mechanism captured.

F2: **MISS** — Response discusses `Group` as a class but does not mention the `group` decorator or that it defaults `cls` to `Group`.

F3: **COVERED** — Response states `add_command` "Registers another Command with this group." The concept of registering into the group's command namespace is captured even though "command map" isn't literally named.

F4: **MISS** — Response discusses context/subcontext hierarchy and `list_commands` for name resolution but does not identify the specific chain `parse_args → _protected_args → resolve_command → invoke`.

---

### blind-click-2 (1/4)

F1: **MISS** — Response identifies CLI parse as the first source and mentions envvar existence, but explicitly states "File 1 does not expose the exact precedence between envvar values, prompting, and defaults." `default_map` is never mentioned. The 4-level precedence chain is not captured.

F2: **MISS** — No mention of `type_cast_value` or single/tuple/variadic dispatch.

F3: **MISS** — No mention of `Choice`, `normalize_choice`, or case-fold behavior.

F4: **COVERED** — Response identifies `File` conversion leading to `LazyFile` (via `open_file`) and `Path` calling `coerce_path_result`. Both halves of the fact captured.

---

### blind-requests-mech-2 (1/4)

F1: **MISS** — Response discusses streaming via `iter_content` and `generate` but does not mention that `stream=False` downloads the body immediately.

F2: **MISS** — Response mentions `generate` branching on streaming capability (`BRANCH(hasattr_stream)`) but does not describe how `iter_content(None)` behavior differs between streaming and non-streaming modes.

F3: **MISS** — Response mentions `get_encoding_from_headers` in the context of `get_unicode_from_response` but does not connect headers-first + charset-detection-fallback to `Response.text` specifically.

F4: **COVERED** — Response states `json` "decodes the body as JSON and raises `RequestsJSONDecodeError`," which is the requests wrapper for `JSONDecodeError`. Core behavior captured.

---

### blind-echo-rel-2 (4/4)

F1: **COVERED** — Response explicitly states `Echo.Pre` adds middleware "before router tries to find matching route" while `Echo.Use` adds middleware "after router has found matching route." Two-stage middleware model fully identified.

F2: **COVERED** — Response describes `DefaultRouter` with tree-based routing (`findStaticChild`, `node`, `find`) using "precedence and an accumulating search." Radix-tree structure and match-type priority captured through mechanism description.

F3: **COVERED** — Response states `Echo.Any` registers for all methods and `Echo.Match` registers one path for multiple methods. Both convenience APIs identified.

F4: **COVERED** — Response identifies group-level middleware via `Echo.Group` with `Use`, route-level middleware via handler arguments, and the full ordering: "pre-routing middleware → router match → Use/group middleware → route-level handler stack."

---

### blind-echo-mech-1 (2/4)

F1: **COVERED** — Response states static child lookup gets "first crack" via `findStaticChild` and parameterized routes are tracked via `paramsCount`. Acknowledges it cannot prove param-vs-wildcard ordering, but static-before-parameterized is >50% of the 3-level chain.

F2: **COVERED** — Response describes matching via structural tree traversal (`findStaticChild`, `node`, `find`, `precedence`) rather than insertion order. Registration-time `paramsCount` precedence bookkeeping reinforces structural priority. Core concept captured implicitly.

F3: **MISS** — Response does not discuss wildcard behavior or that wildcards consume zero or more remaining characters.

F4: **MISS** — No mention of only the first match-any segment mattering.

---

### blind-zod-mech-2 (1/4)

F1: **COVERED** — Response states schema-level check messages become `issue.message` and `ZodError.format` prefers `issue.message` over the default path. Highest-precedence for schema-level messages captured.

F2: **MISS** — Response explicitly states "File 1 does not show … the full ordering among every possible customization layer (for example, whether there are multiple stacked error maps at schema, parse-call, or global scope)."

F3: **MISS** — No mention of `z.config()` or locale-level error maps.

F4: **MISS** — No mention of `undefined` yielding to the next precedence level.

---

## Summary Table

| Task | F1 | F2 | F3 | F4 | Score |
|---|---|---|---|---|---|
| blind-aiohttp-1 | ✅ | ✅ | ❌ | ❌ | **2/4** |
| blind-aiohttp-2 | ✅ | ✅ | ❌ | ✅ | **3/4** |
| blind-fiber-1 | ✅ | ❌ | ❌ | ✅ | **2/4** |
| blind-click-1 | ✅ | ❌ | ✅ | ❌ | **2/4** |
| blind-click-2 | ❌ | ❌ | ❌ | ✅ | **1/4** |
| blind-requests-mech-2 | ❌ | ❌ | ❌ | ✅ | **1/4** |
| blind-echo-rel-2 | ✅ | ✅ | ✅ | ✅ | **4/4** |
| blind-echo-mech-1 | ✅ | ✅ | ❌ | ❌ | **2/4** |
| blind-zod-mech-2 | ✅ | ❌ | ❌ | ❌ | **1/4** |
| **Total** | **7/9** | **4/9** | **2/9** | **5/9** | **18/36 (50.0%)** |
