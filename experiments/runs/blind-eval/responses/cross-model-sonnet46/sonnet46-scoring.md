### blind-requests-struct-1 (3/4)
- F1: COVERED — identifies the top-level helpers in `src/requests/api.py`.
- F2: COVERED — places `Session` and orchestration in `src/requests/sessions.py`.
- F3: COVERED — places `Request`, `PreparedRequest`, and `Response` in `src/requests/models.py`.
- F4: MISS — does not clearly identify `BaseAdapter`/`HTTPAdapter` as separate module owners; exceptions are only mentioned incidentally.

### blind-echo-struct-2 (2/4)
- F1: COVERED — names `Echo`, `Context`, and `DefaultRouter` as core public routing/request types.
- F2: MISS — method-specific APIs are described as delegating to `Add`, not clearly to the expected `*Route` layer.
- F3: COVERED — `Echo.Group` is identified as creating the `Group` sub-router surface.
- F4: MISS — does not identify binding/JSON/validation interfaces as part of the public surface.

### blind-requests-rel-1 (3/4)
- F1: COVERED — explicitly describes the `Request -> PreparedRequest` transformation.
- F2: COVERED — says `Session.prepare_request` merges session-level and per-request settings.
- F3: COVERED — explicitly states `Session.send` accepts a `PreparedRequest`.
- F4: MISS — does not mention the `Response.request` back-reference.

### blind-echo-rel-1 (3/4)
- F1: COVERED — says `Echo` owns registration/dispatch and handlers receive `Context`.
- F2: COVERED — describes `Group` as a prefixed, sub-scoped router view over `Echo`.
- F3: MISS — mentions group middleware attachment, but not the inheritance behavior.
- F4: COVERED — shows middleware wrapping handlers around the same `Context` argument.

### blind-requests-mech-2 (0/4)
- F1: MISS — does not explain that `stream=False` downloads content immediately.
- F2: MISS — does not cover the special `iter_content(None)` behavior.
- F3: MISS — mentions header-based decoding, but not the charset fallback mechanism.
- F4: MISS — says `json` raises `RequestsJSONDecodeError`, not the expected `JSONDecodeError` fact.

### blind-echo-mech-1 (2/4)
- F1: COVERED — explicitly states static beats parameter beats wildcard.
- F2: COVERED — explains trie/structural precedence during routing.
- F3: MISS — does not mention wildcard matching zero or more trailing characters.
- F4: MISS — does not mention the single match-any restriction.

### blind-click-2 (1/4)
- F1: MISS — gives a partial CLI/envvar/default story, but omits `default_map` and the expected precedence chain.
- F2: MISS — does not cover `type_cast_value` single/tuple/variadic handling.
- F3: MISS — does not mention `Choice.convert` normalization.
- F4: COVERED — explicitly covers `File` -> `LazyFile` and `Path` -> `coerce_path_result`.

### blind-zod-mech-1 (2/4)
- F1: COVERED — states unknown keys are stripped by default.
- F2: MISS — does not identify `strictObject` specifically as the erroring mode.
- F3: MISS — discusses `.loose()`, but not `looseObject` specifically.
- F4: COVERED — states `catchall` validates unknown keys against its schema.

| Task | Score |
|---|---:|
| blind-requests-struct-1 | 3/4 |
| blind-echo-struct-2 | 2/4 |
| blind-requests-rel-1 | 3/4 |
| blind-echo-rel-1 | 3/4 |
| blind-requests-mech-2 | 0/4 |
| blind-echo-mech-1 | 2/4 |
| blind-click-2 | 1/4 |
| blind-zod-mech-1 | 2/4 |
| **Total** | **16/32** |
