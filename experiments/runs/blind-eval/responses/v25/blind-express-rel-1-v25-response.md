# v2.5 Response: blind-express-rel-1
Date: 2026-04-16

## Question

What is the relationship between an Express app, mounted routers, and router-level middleware?

## Answer

### The App Object: `createApplication`

The Express application object is produced by the `createApplication` factory at `lib/express.js:35-56`. The FOCUS annotation shows that this function wires together several foundational pieces:

- **`app.handle`** — The app delegates incoming requests through `app.handle`, making the app itself a request handler (FOCUS createApplication, uses: app.handle).
- **`EventEmitter.prototype`** — The app mixes in Node's EventEmitter, so it can emit and listen for events such as mount events when sub-apps or routers are attached (FOCUS createApplication, uses: EventEmitter.prototype).
- **`app.request` via `Object.create`** — The app creates its own request prototype using `Object.create`, meaning each app (or mounted sub-app/router) can extend the request object independently (FOCUS createApplication, uses: app.request, Object.create).

This factory establishes the app as a callable function that receives `(req, res, next)` and processes them through its middleware stack via `app.handle` (FOCUS createApplication).

### Mounted Routers: The Multi-Router Example

The TREE listing and INDEX show `examples/multi-router/` containing `controllers/api_v1.js`, `controllers/api_v2.js`, and `index.js` (TREE: examples/multi-router/ with controllers/api_v1.js, api_v2.js, index.js). This structure demonstrates the mounted-router pattern:

- Separate controller files (`api_v1.js`, `api_v2.js`) each presumably define their own router instance with version-specific routes.
- The `index.js` file serves as the composition root, mounting these routers onto the main app at specific path prefixes.

This establishes a **hierarchical relationship**: the top-level app (created by `createApplication`) acts as a parent that delegates request handling to child routers based on path prefixes. Each mounted router processes only the requests that match its mount point (TREE: examples/multi-router/).

### Router-Level Middleware: The Route-Middleware Example

The `examples/route-middleware/` directory provides three FOCUS-annotated middleware functions that demonstrate router-level middleware patterns:

1. **`loadUser`** (`examples/route-middleware/index.js:24-34`) — A standard `(req, res, next)` middleware. It reads `req.params.id` to look up a user, then decorates the request by setting `req.user`. This shows middleware enriching the request object for downstream handlers (FOCUS loadUser, sig: loadUser(req, res, next), uses: req.params.id, req.user).

2. **`andRestrictToSelf`** (`examples/route-middleware/index.js:35-48`) — Another `(req, res, next)` middleware. It reads `req.authenticatedUser.id` and `req.user.id` and compares them, implementing an authorization check that depends on `req.user` having been set by a prior middleware like `loadUser` (FOCUS andRestrictToSelf, sig: andRestrictToSelf(req, res, next), uses: req.authenticatedUser.id, req.user.id).

3. **`andRestrictTo`** (`examples/route-middleware/index.js:49-58`) — A middleware factory (not a middleware itself). Its signature is `andRestrictTo(role)`, and its behavior annotation is `DELEGATE(function -> result)`, meaning it returns a new middleware function. The returned function checks `req.authenticatedUser.role` against the provided role parameter (FOCUS andRestrictTo, sig: andRestrictTo(role), behavior: DELEGATE(function -> result), uses: req.authenticatedUser.role).

### Relationships Between the Three Layers

The clue data reveals a three-layer relationship:

**App → Router → Middleware chain:**

1. **App level**: `createApplication` produces the root app object that receives all requests via `app.handle` (FOCUS createApplication). The app can mount child routers at specific paths.

2. **Router level**: Mounted routers (as shown in `examples/multi-router/`) partition the request space. Each router handles a subset of requests based on its mount path. The presence of `api_v1.js` and `api_v2.js` as separate controllers shows routers enabling modular, independently-defined route groups (TREE: examples/multi-router/).

3. **Middleware level**: Within a router, individual route definitions can chain multiple middleware functions. The route-middleware example shows this chaining pattern: `loadUser` runs first to populate `req.user`, then `andRestrictToSelf` or `andRestrictTo(role)` runs to enforce authorization. Each middleware either calls `next()` to pass control forward or terminates the chain (FOCUS loadUser, andRestrictToSelf, andRestrictTo).

### The `req / res / next` Contract

All three layers share the `(req, res, next)` contract:

- **`req`** serves as a shared context object. `loadUser` writes to `req.user` (FOCUS loadUser, uses: req.user). `andRestrictToSelf` reads from both `req.authenticatedUser.id` and `req.user.id` (FOCUS andRestrictToSelf). `andRestrictTo` reads `req.authenticatedUser.role` (FOCUS andRestrictTo).
- **`res`** is the response object (referenced in all middleware signatures but not detailed in the FOCUS data for these middleware functions).
- **`next`** is the continuation callback. Middleware calls `next()` to pass control to the next handler in the chain. `andRestrictTo`'s `DELEGATE` behavior annotation confirms it produces a function that participates in this next-based flow (FOCUS andRestrictTo, behavior: DELEGATE(function -> result)).

### What Cannot Be Determined (GAPS)

The GAPS annotation states: `type: RELATIONAL (answerable from L2-L3 structure), coverage: 4 symbols in L3, 1 with behavior annotations`. This means:

- **`lib/router.js` is not visible in the clue file's SYM listing.** The six `lib/` files listed are `application.js`, `express.js`, `request.js`, `response.js`, `utils.js`, and `view.js` (TREE: lib/ 6 files). There is no `router.js` in this set. This means the actual Router constructor, its mounting mechanism, route-matching algorithm, and parameter extraction logic are entirely outside the clue's coverage.
- **How routers are mounted onto the app** (e.g., `app.use('/api/v1', router)`) cannot be confirmed from the clue data — we can only infer it from the directory structure of `examples/multi-router/` (TREE).
- **How `app.handle` dispatches to mounted routers** is opaque. The FOCUS for `createApplication` shows `app.handle` is used but does not expand its implementation.
- **The `examples/multi-router/` files** (`api_v1.js`, `api_v2.js`, `index.js`) have no FOCUS annotations, so we cannot describe their internal wiring — only that they exist and suggest a multi-router pattern (TREE, INDEX).
- Only `andRestrictTo` carries a behavior annotation (`DELEGATE`); the other three FOCUS symbols (`loadUser`, `andRestrictToSelf`, `createApplication`) have `uses` data but no behavior tags, limiting what can be said about their control flow beyond the references they make (GAPS: 1 with behavior annotations).
