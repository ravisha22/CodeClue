# v2.5 Response: blind-express-rel-2
Date: 2026-04-16

## Question

How do normal middleware, route callback chains, and error handlers interact in Express's middleware stack?

## Answer

### Normal Middleware: The `(req, res, next)` Pattern

Normal middleware functions follow the three-argument `(req, res, next)` signature. The clue data provides three concrete examples:

1. **`loadUser`** (`examples/route-middleware/index.js:24-34`) — Signature: `loadUser(req, res, next)`. It accesses `req.params.id` and sets `req.user`. The source snippet confirms that on success, `loadUser` calls `next()` to pass control forward. On failure (user not found), it calls `next(new Error(...))` to signal an error into the middleware chain (FOCUS loadUser, sig: loadUser(req, res, next), uses: req.params.id, req.user; source: next() on success, next(new Error(...)) on failure).

2. **`andRestrictToSelf`** (`examples/route-middleware/index.js:35-48`) — Signature: `andRestrictToSelf(req, res, next)`. It compares `req.authenticatedUser.id` to `req.user.id`. The source snippet confirms it calls `next()` when IDs match and `next(new Error('Unauthorized'))` when they do not (FOCUS andRestrictToSelf, sig: andRestrictToSelf(req, res, next), uses: req.authenticatedUser.id, req.user.id; source: next() on match, next(new Error('Unauthorized')) on mismatch).

3. **`andRestrictTo`** (`examples/route-middleware/index.js:49-58`) — A middleware factory with signature `andRestrictTo(role)`. Its behavior annotation is `DELEGATE(function -> result)`, meaning it returns a new middleware function. The source snippet confirms the returned function checks `req.authenticatedUser.role` and calls `next()` on match or `next(new Error('Unauthorized'))` on mismatch (FOCUS andRestrictTo, sig: andRestrictTo(role), behavior: DELEGATE(function -> result), uses: req.authenticatedUser.role; source: returned function calls next() or next(new Error('Unauthorized'))).

### Route Callback Chains

The route-middleware examples demonstrate how multiple middleware functions are chained on a single route. The dependency between `loadUser` and `andRestrictToSelf` is visible in the clue data:

- `loadUser` sets `req.user` from `req.params.id` (FOCUS loadUser, uses: req.params.id, req.user).
- `andRestrictToSelf` reads `req.user.id` (FOCUS andRestrictToSelf, uses: req.user.id).

This means `loadUser` **must** run before `andRestrictToSelf` in the chain, because `andRestrictToSelf` depends on `req.user` being populated. The chaining works through the `next()` callback: `loadUser` calls `next()` on success, which advances to `andRestrictToSelf` in the chain (source: loadUser calls next() on success).

Similarly, `andRestrictTo(role)` can be chained after `loadUser` or authentication middleware, since it reads `req.authenticatedUser.role` (FOCUS andRestrictTo, uses: req.authenticatedUser.role).

The chain short-circuits when any middleware calls `next(new Error(...))` instead of `next()`. This skips remaining normal middleware and routes the error to error handlers (source: loadUser calls next(new Error(...)) on failure; andRestrictToSelf calls next(new Error('Unauthorized')) on mismatch).

### Error Creation: The `error(status, msg)` Pattern

The `error` function in `examples/web-service/index.js:10-19` provides a utility for creating error objects. Its signature is `error(status, msg)`. The source snippet shows it creates a new `Error` object and sets a `.status` property on it using `err.status` (FOCUS error web-service, sig: error(status, msg), uses: err.status; source: creates Error with .status property, returns it).

This pattern establishes a convention: errors in Express carry a `.status` property that error-handling middleware can inspect to determine the HTTP status code to send (source: error(status, msg) creates Error with .status).

### Error Handlers: The Four-Argument `(err, req, res, next)` Pattern

Error-handling middleware is distinguished from normal middleware by its four-argument signature. The clue data provides:

**`error`** (`examples/error/index.js:13-27`) — Signature: `error(err, req, res, next)`. Its `uses` list includes `console.error`, `err.stack`, `res.status`, and `res.send` (FOCUS error examples/error, sig: error(err, req, res, next), uses: console.error, err.stack, res.status, res.send).

This shows the error handler pattern:
1. Logs the error via `console.error` with `err.stack` for diagnostics.
2. Sets the HTTP status code via `res.status`.
3. Sends a response body via `res.send`.
4. Receives the `next` parameter, allowing it to optionally forward to additional error handlers.

### Application-Level Error Logging: `logerror`

The `logerror` function at `lib/application.js:614-618` provides Express's built-in error logging. Its signature is `logerror(err)`, and it uses `this.get`, `console.error`, `err.stack`, and `err.toString` (FOCUS logerror, sig: logerror(err), uses: this.get, console.error, err.stack, err.toString).

The source snippet further clarifies: if the environment is not `'test'`, it calls `console.error(err.stack || err.toString())` (source: logerror checks env !== 'test', then console.error(err.stack || err.toString())). The `this.get` reference suggests it reads an application setting (likely `'env'`) to determine whether to suppress logging in test environments.

### The Interaction Flow

Combining the clue data, the interaction between these three layers works as follows:

1. **Normal middleware** processes requests sequentially via `next()`. Each middleware in the chain can enrich `req` (like `loadUser` setting `req.user`) or terminate the chain (FOCUS loadUser; source snippets).

2. **When an error occurs**, middleware calls `next(new Error(...))` instead of `next()`. This is demonstrated by `loadUser` on user-not-found, `andRestrictToSelf` on authorization failure, and `andRestrictTo` on role mismatch (source snippets for all three).

3. **Error handlers** with the `(err, req, res, next)` signature catch these errors. The `error` handler in `examples/error/` logs the stack trace and sends an error response (FOCUS error examples/error).

4. **`logerror`** at the application level provides a fallback logging mechanism, writing `err.stack` or `err.toString()` to `console.error` when not in test mode (FOCUS logerror; source snippet).

5. **`createApplication`** ties it all together: the app function delegates to `app.handle`, which presumably orchestrates the middleware stack and error handler dispatch (FOCUS createApplication, uses: app.handle).

### What Cannot Be Determined (GAPS)

The GAPS annotation states: `type: MECHANISTIC (body logic needed for full answer), coverage: 7 symbols in L3, 1 with behavior annotations`. This means:

- The question is classified as MECHANISTIC, meaning full body-level logic is needed for a complete answer. The clue data provides structural and relational information but not the complete dispatch algorithm.
- **7 symbols have L3 (FOCUS) detail**, but only **1 carries a behavior annotation** — the `DELEGATE` tag on `andRestrictTo` (GAPS: 1 with behavior annotations).
- **The actual middleware dispatch mechanism** — how Express distinguishes 3-argument middleware from 4-argument error handlers, how it decides to skip normal middleware when an error is present, and how `app.handle` orchestrates the stack — is **not visible** in the clue data. We can infer the `next(err)` convention from source snippets but cannot describe the internal implementation.
- **The ordering and registration of error handlers** relative to normal middleware is not shown. We know error handlers exist (from the examples) but cannot describe Express's rules for when they are invoked versus skipped.
- **`lib/router.js`** is absent from the SYM listing (TREE: lib/ 6 files), so router-level error handling dispatch is invisible.
