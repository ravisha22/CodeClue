# v2.5 Response: blind-express-struct-2
Date: 2026-04-16

## Question

How do the Express docs divide router configuration, parser behavior, and response-ending APIs?

## Answer

### Router Configuration Patterns

The clue file's TREE listing (TREE: examples/ 43 files) reveals three distinct example directories that demonstrate router configuration patterns:

1. **`examples/multi-router/`** — The INDEX shows files including `controllers/api_v1.js`, `api_v2.js`, and `index.js`. This directory name and structure indicate a pattern for mounting multiple router modules, each presumably handling a version-specific API surface. The presence of separate `api_v1.js` and `api_v2.js` controller files suggests Express supports partitioning routes into independent router instances that are then composed at the application level (TREE: examples/multi-router/ with controllers/api_v1.js, api_v2.js, index.js).

2. **`examples/route-map/`** — Listed in the TREE, this directory's name implies a declarative route-mapping pattern where routes are defined as a data structure rather than imperative `.get()`/`.post()` calls. No FOCUS annotations exist for files in this directory, so internals are not available from the clue data (TREE: examples/route-map/).

3. **`examples/route-separation/`** — Also present in the TREE, suggesting a pattern for organizing routes into separate files or modules. No FOCUS data is available (TREE: examples/route-separation/).

The `createApplication` factory at `lib/express.js:35-56` underpins all router configuration. Its FOCUS annotation shows it creates the app function as a request handler using `app.handle`, mixes in `EventEmitter.prototype`, and creates `app.request` via `Object.create` (FOCUS createApplication, uses: app.handle, EventEmitter.prototype, app.request, Object.create). This establishes the app object that routers are ultimately mounted onto.

### Parser Behavior

Two utility functions in `lib/utils.js` handle parsing:

1. **`parseExtendedQueryString`** (`lib/utils.js:266`) — SYM lists this function, and its FOCUS annotation is not included in this task's clue set at L3 level, but it is known from the SYM listing to exist as a named export for query string parsing (SYM: parseExtendedQueryString lib/utils.js:266).

2. **`acceptParams`** (`lib/utils.js:88`) — Listed in SYM as a utility function. Its name suggests it handles parsing of Accept-header or content-type parameters for content negotiation (SYM: acceptParams lib/utils.js:88).

Additionally, `createETagGenerator` at `lib/utils.js:248` is listed in SYM, providing ETag generation capability used in response caching logic (SYM: createETagGenerator lib/utils.js:248).

### Response-Ending APIs

Two key response helpers are documented in `lib/response.js`:

1. **`sendfile`** (`lib/response.js:919-1009`) — The FOCUS annotation reveals a complex streaming response API. Its signature is `sendfile(res, file, options, callback)`. The behavior annotations describe three patterns:
   - `GUARD(streaming !== false && !done -> onaborted(); return;)` — A guard clause that checks whether streaming is active and the response is not already done; if streaming was aborted, it invokes `onaborted()` and returns early.
   - `PRECEDENCE(streaming -> options)` — Streaming state takes precedence over the options object when determining behavior.
   - `ACCUMULATE(sendfile loop -> result)` — The function accumulates results through a loop, presumably handling chunked file transfer.
   
   Its `uses` list includes `err.code`, `file.on`, `options.headers`, and `Object.keys`, confirming it works with Node streams (`file.on`), handles errors by error code, processes custom headers from the options object, and iterates option keys (FOCUS sendfile, sig: sendfile(res, file, options, callback), uses: err.code, file.on, options.headers, Object.keys).

2. **`stringify`** (`lib/response.js:1022-1047`) — The FOCUS annotation shows this as a JSON serialization wrapper. Its signature is `stringify(value, replacer, spaces, escape)`. The behavior annotation `DISPATCH(c)` suggests character-level dispatch logic for escaping. Its `uses` list includes `arguments.length`, `bugs.chromium.org` (indicating a workaround for a known Chrome bug), `JSON.stringify`, and `json.replace` — confirming it wraps the native `JSON.stringify` and then applies character replacement for security or compatibility (FOCUS stringify, sig: stringify(value, replacer, spaces, escape), behavior: DISPATCH(c), uses: arguments.length, bugs.chromium.org, JSON.stringify, json.replace).

### How These Three Areas Relate

The clue data shows a clear structural division:

- **Router configuration** lives in `examples/` — patterns like multi-router, route-map, and route-separation show how to organize routes, while `createApplication` in `lib/express.js` creates the app object that hosts them (TREE examples/; FOCUS createApplication).
- **Parser behavior** lives in `lib/utils.js` — utility functions for query strings (`parseExtendedQueryString`) and content negotiation parameters (`acceptParams`) (SYM lib/utils.js).
- **Response-ending APIs** live in `lib/response.js` — `sendfile` for streaming file responses and `stringify` for JSON serialization (SYM, FOCUS lib/response.js).

### What Cannot Be Determined (GAPS)

The GAPS annotation states: `type: STRUCTURAL (answerable from L0-L2), coverage: 3 symbols in L3, 2 with behavior annotations`. This means:

- Only 3 symbols have FOCUS detail, and only 2 of those (`sendfile` and `stringify`) carry behavior annotations.
- **Router internals are invisible.** The `examples/multi-router/`, `examples/route-map/`, and `examples/route-separation/` directories appear in TREE but none of their files have FOCUS annotations. We can describe the organizational patterns by directory name but cannot detail how routes are registered, matched, or dispatched.
- **`parseExtendedQueryString` and `acceptParams` lack FOCUS detail** in this clue set. We know they exist in `lib/utils.js` (SYM) but cannot describe their internal logic or full behavior from the provided data alone.
- **No `lib/router.js`** appears in the SYM listing, so the actual routing engine internals — method matching, parameterized paths, regex routes — are entirely outside this clue file's coverage.
