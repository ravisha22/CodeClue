# Sonnet Scoring

Scoring rubric: **COVERED** = describes the specific mechanism with evidence (>50% of mechanism). **MISS** = absent or explicitly unknown.

## blind-requests-struct-1 (3/4)
- **F1: COVERED** — Identifies top-level helpers in `src/requests/api.py`, including `request` and verb helpers.
- **F2: COVERED** — Places `Session` plus `request`, `prepare_request`, and `send` in `src/requests/sessions.py`.
- **F3: COVERED** — Places `Request`, `PreparedRequest`, and `Response` in `src/requests/models.py`.
- **F4: MISS** — Does not identify `BaseAdapter`/`HTTPAdapter` as transport abstractions or exceptions as coming from dedicated modules.

## blind-echo-struct-2 (2/4)
- **F1: COVERED** — Explicitly identifies `Echo` as top-level app, `Context` as per-request context, and `DefaultRouter` as route registry.
- **F2: COVERED** — Describes method-specific registration helpers (`GET`, `Any`, etc.), though not the `*Route` return type.
- **F3: MISS** — Describes `Group`, but does not state `Echo.Group(...)` creates the grouped subrouter.
- **F4: MISS** — Mentions binding and response helpers, but not the separate binder/JSON/validator interface pattern.

## blind-requests-rel-1 (3/4)
- **F1: COVERED** — States the pipeline as `Request -> PreparedRequest -> Response`.
- **F2: COVERED** — Says `Session.prepare_request` merges session state via `merge_hooks` / `merge_setting`.
- **F3: COVERED** — States `Session.send` sends a `PreparedRequest`, with response creation described via `build_response`.
- **F4: MISS** — Never mentions `Response.request` back-referencing the `PreparedRequest`.

## blind-echo-rel-1 (3/4)
- **F1: COVERED** — States `Echo` owns routing/registration and handlers execute against `Context`.
- **F2: COVERED** — Describes `Group` as sub-routing with path prefixing.
- **F3: MISS** — Says groups can add middleware, but not that parent-group middleware is inherited.
- **F4: COVERED** — Describes middleware and handlers both operating on the same `Context`.

## blind-requests-mech-2 (0/4)
- **F1: MISS** — No statement that `stream=False` downloads immediately.
- **F2: MISS** — No description of `iter_content(None)` differing by streaming mode.
- **F3: MISS** — No explanation of `Response.text` header-first encoding with charset-detection fallback.
- **F4: MISS** — Does not discuss `Response.json()` raising `JSONDecodeError`.

## blind-echo-mech-1 (1/4)
- **F1: COVERED** — Explicitly says static routes win before parameters, and wildcards are last.
- **F2: MISS** — Does not establish that precedence is structural rather than registration-order.
- **F3: MISS** — Does not explain wildcard as consuming zero or more characters.
- **F4: MISS** — Does not mention only the first match-any segment matters.

## blind-click-2 (1/4)
- **F1: COVERED** — Describes precedence as CLI values first, then env vars, then defaults; misses `default_map` but captures most of the chain.
- **F2: MISS** — Does not describe `type_cast_value` single/tuple/variadic dispatch.
- **F3: MISS** — Does not explain `Choice.convert` normalization / case-folding.
- **F4: MISS** — Describes `Path.coerce_path_result`, but does not identify `File.convert -> LazyFile`.

## blind-zod-mech-1 (1/4)
- **F1: MISS** — Does not state default `z.object()` strips unknown keys.
- **F2: MISS** — Does not specifically establish `strictObject` turns unknown keys into errors.
- **F3: COVERED** — States loose mode passes unknown keys through without validation errors.
- **F4: MISS** — Does not mention `.catchall()` validating unknown keys against a schema.

---

## Per-task scores
| Task | Sonnet |
|---|---:|
| blind-requests-struct-1 | 3/4 |
| blind-echo-struct-2 | 2/4 |
| blind-requests-rel-1 | 3/4 |
| blind-echo-rel-1 | 3/4 |
| blind-requests-mech-2 | 0/4 |
| blind-echo-mech-1 | 1/4 |
| blind-click-2 | 1/4 |
| blind-zod-mech-1 | 1/4 |

## Total
**14/32**

## Comparison vs GPT-5.4 on the same tasks
GPT-5.4 scores on these same tasks were: requests-struct-1 **4/4**, echo-struct-2 **4/4**, requests-rel-1 **3/4**, echo-rel-1 **3/4**, requests-mech-2 **1/4**, echo-mech-1 **2/4**, click-2 **3/4**, zod-mech-1 **4/4** — total **24/32**. Sonnet trails GPT-5.4 by **10 points**, tying only on `blind-requests-rel-1` and `blind-echo-rel-1`.
