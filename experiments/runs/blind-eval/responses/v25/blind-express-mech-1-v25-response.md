# v2.5 Response: blind-express-mech-1
Date: 2026-04-16

## Question

What matching and dispatch rules do the Express docs describe for route parameters, query strings, and route skipping?

## Answer

### Route Parameters: `req.params`

The clue data demonstrates route parameter access through the `loadUser` middleware. The FOCUS annotation shows `loadUser` at `examples/route-middleware/index.js:24-34` with signature `loadUser(req, res, next)` and uses `req.params.id` (FOCUS loadUser, sig: loadUser(req, res, next), uses: req.params.id, req.user).

The source snippet confirms that `loadUser` accesses `users[req.params.id]` — it uses the route parameter `id` extracted from the URL path as a key to look up a user in a data structure (source: loadUser uses users[req.params.id] to access route params). This establishes that Express populates `req.params` as an object whose keys correspond to named segments in the route pattern (e.g., a route like `/user/:id` makes `req.params.id` available).

The `andRestrictToSelf` middleware further demonstrates route parameter usage downstream. After `loadUser` sets `req.user` from the parameter lookup, `andRestrictToSelf` compares `req.authenticatedUser.id === req.user.id` (FOCUS andRestrictToSelf, uses: req.authenticatedUser.id, req.user.id; source: checks req.authenticatedUser.id === req.user.id). This shows route parameters enabling a chain of middleware where earlier handlers extract data and later handlers enforce constraints on it.

### Query String Parsing: `parseExtendedQueryString`

Query string parsing is handled by `parseExtendedQueryString` at `lib/utils.js:266-271`. The FOCUS annotation shows its signature as `parseExtendedQueryString(str)` with behavior `DELEGATE(qs.parse -> result)` (FOCUS parseExtendedQueryString, sig: parseExtendedQueryString(str), behavior: DELEGATE(qs.parse -> result)).

The source snippet confirms: it calls `qs.parse(str, {allowPrototypes: true})` (source: parseExtendedQueryString calls qs.parse(str, {allowPrototypes: true})). This reveals two important details:

1. **Delegation to `qs` library** — Express does not implement its own query string parser. It delegates to the `qs` module, which supports nested object syntax (e.g., `?user[name]=foo` becomes `{user: {name: 'foo'}}`). The `DELEGATE` behavior annotation confirms this is a thin wrapper (FOCUS parseExtendedQueryString, behavior: DELEGATE(qs.parse -> result)).

2. **`allowPrototypes: true`** — The `qs.parse` call is configured with `allowPrototypes: true`, meaning parsed query objects may include properties that shadow `Object.prototype` methods. This is a deliberate choice that trades some safety for backward compatibility (source: qs.parse options include allowPrototypes: true).

### Content Negotiation: `acceptParams`

The `acceptParams` function at `lib/utils.js:88` handles content-type parameter parsing. The source snippet describes its behavior: it parses semicolon-delimited parameters from content-type strings and extracts a quality factor (SYM: acceptParams lib/utils.js:88; source: parses semicolon-delimited params from content-type strings, extracts quality factor).

This function supports Express's content negotiation by breaking apart header values like `text/html;q=0.9;level=1` into their components, with the quality factor (`q`) used for preference ranking. The quality factor extraction enables Express to select the best response format when multiple are available.

### ETag Generation: `createETagGenerator`

The `createETagGenerator` utility at `lib/utils.js:248` wraps `etag(buf, options)` (SYM: createETagGenerator lib/utils.js:248; source: wraps etag(buf, options)). This function creates ETag generator functions used by response methods to produce cache-validation headers. While not directly a matching/dispatch rule, it participates in the response pipeline by enabling conditional request handling (304 Not Modified responses).

### Route Skipping via `next()` and `next(error)`

Route skipping is demonstrated through the `next` callback pattern visible in the middleware examples:

1. **Normal continuation**: Calling `next()` with no arguments advances to the next middleware or route handler in the chain. `loadUser` calls `next()` on success to continue processing (source: loadUser calls next() on success).

2. **Error-based skipping**: Calling `next(new Error(...))` skips remaining normal middleware and routes the error to error handlers. Both `andRestrictToSelf` and `andRestrictTo` use this pattern — they call `next(new Error('Unauthorized'))` when authorization checks fail (source: andRestrictToSelf calls next(new Error('Unauthorized')) on mismatch; andRestrictTo's returned function calls next() or next(new Error('Unauthorized'))).

3. **Middleware factory pattern**: `andRestrictTo(role)` returns a middleware function (behavior: `DELEGATE(function -> result)`), and the returned function participates in the same `next()`/`next(error)` flow (FOCUS andRestrictTo, behavior: DELEGATE(function -> result); source: returns middleware function checking role).

### The App-Level Dispatch Entry Point

The `createApplication` source confirms the top-level dispatch mechanism: the app is created as `function(req, res, next) { app.handle(req, res, next) }`, with `EventEmitter.prototype` and `proto` mixed in, and `app.request`/`app.response` created via `Object.create`. The app then calls `app.init()` (FOCUS createApplication; source: app = function(req, res, next){app.handle(req, res, next)}; mixin with EventEmitter.prototype and proto; creates app.request/app.response with Object.create; app.init()).

This shows the app itself is a function compatible with Node's HTTP server callback signature, and all matching/dispatch is routed through `app.handle`.

### What Cannot Be Determined (GAPS)

The GAPS annotation states: `type: MECHANISTIC, coverage: 5 symbols in L3, 2 with behavior annotations`. This means:

- The question is MECHANISTIC, requiring body-level implementation detail for a full answer.
- Only 5 symbols have FOCUS data, and only 2 carry behavior annotations (`parseExtendedQueryString` with `DELEGATE` and `andRestrictTo` with `DELEGATE`).
- **`lib/router.js` is absent from the SYM listing** (TREE: lib/ 6 files lists only application.js, express.js, request.js, response.js, utils.js, view.js). This means the actual route matching engine — how Express matches URL patterns against registered routes, how parameterized routes (`:id`) are parsed into `req.params`, how regex routes work, how `next('route')` skips to the next route definition — is **entirely invisible** in this clue file.
- **The `app.handle` implementation** is not expanded in any FOCUS annotation. We know it is the dispatch entry point (FOCUS createApplication) but cannot describe its matching algorithm.
- **How query strings are attached to `req.query`** is not shown. We know `parseExtendedQueryString` exists and delegates to `qs.parse` (FOCUS, source), but the wiring between the parsed result and `req.query` is not visible.
- **Route precedence rules** — how Express handles overlapping routes, the order of route evaluation, and method-specific matching — are not covered in the clue data.
