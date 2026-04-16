# v2.5 Response: blind-express-struct-1
Date: 2026-04-16

## Question

Which public objects and built-in middleware make up Express's documented request-handling surface?

## Answer

### Entry Point: `createApplication`

The clue file's INDEX header (`=CC v2.1 express@HEAD 141mod 116sym`) shows Express at HEAD with 141 modules and 116 symbols. The primary entry point is `createApplication` at `lib/express.js:35-56` (SYM). Its FOCUS annotation reveals it wires together `app.handle`, `EventEmitter.prototype`, `app.request`, and `Object.create` — establishing the application object as an event-emitting request handler that delegates incoming requests through `app.handle` (FOCUS createApplication, uses: app.handle, EventEmitter.prototype, app.request, Object.create).

### Core Library Modules

The TREE listing enumerates exactly six files under `lib/` (TREE: lib/ 6 files):

1. **`lib/application.js`** — Houses application-level helpers. SYM lists `logerror` at line 614 and `tryRender` at line 624, indicating built-in error logging and render-attempt logic (SYM: logerror lib/application.js:614; tryRender lib/application.js:624).

2. **`lib/express.js`** — Contains `createApplication` (SYM: createApplication lib/express.js:35), the factory that produces a new app instance.

3. **`lib/request.js`** — Defines request-object extensions. SYM lists `defineGetter` at line 521. The FOCUS annotation shows its signature as `defineGetter(obj, name, getter)` and that it uses `Object.defineProperty` to attach lazy getters to the request prototype (FOCUS defineGetter, sig: defineGetter(obj, name, getter), uses: Object.defineProperty).

4. **`lib/response.js`** — Provides response helpers. SYM lists `sendfile` at line 919 and `stringify` at line 1022, which are the two documented response-ending utilities visible at this level (SYM: sendfile lib/response.js:919; stringify lib/response.js:1022).

5. **`lib/utils.js`** — Utility functions. SYM lists `acceptParams` at line 88, `createETagGenerator` at line 248, and `parseExtendedQueryString` at line 266 (SYM: acceptParams lib/utils.js:88; createETagGenerator lib/utils.js:248; parseExtendedQueryString lib/utils.js:266).

6. **`lib/view.js`** — Template rendering. SYM lists `View` at line 51 and `tryStat` at line 196, indicating a view constructor and a file-stat helper (SYM: View lib/view.js:51; tryStat lib/view.js:196).

### Middleware Examples in the Clue File

The clue file's SYM section for example symbols enumerates several middleware functions visible in the examples directory (TREE: examples/ 43 files):

- **`loadUser`** (`examples/route-middleware/index.js:24-34`) — A classic `(req, res, next)` middleware. FOCUS shows it accesses `req.params.id` and sets `req.user`, then presumably calls `next()` (FOCUS loadUser, sig: loadUser(req, res, next), uses: req.params.id, req.user).

- **`andRestrictTo`** (`examples/route-middleware/index.js:49-58`) — A middleware factory. FOCUS shows its behavior as `DELEGATE(function -> result)`, returning a new function that checks `req.authenticatedUser.role` (FOCUS andRestrictTo, sig: andRestrictTo(role), behavior: DELEGATE(function -> result), uses: req.authenticatedUser.role).

- **`andRestrictToSelf`** (`examples/route-middleware/index.js:35-48`) — Standard middleware that compares `req.authenticatedUser.id` to `req.user.id` (FOCUS andRestrictToSelf, sig: andRestrictToSelf(req, res, next), uses: req.authenticatedUser.id, req.user.id).

- **`authenticate`** and **`restrict`** — Listed in example SYM but without FOCUS annotations, so their internals are not visible from the clue data (SYM: authenticate, restrict in example symbols).

- **`error`** — Appears in two separate example locations, indicating distinct error-handling middleware patterns (SYM: error appears in two locations, plus error in web-service).

Other example symbols (`format`, `list`, `count`, `count2`, `ferrets`, `users`, `users2`, `User`, `GithubView`, `initializeRedis`) are listed in SYM but without FOCUS annotations, so they serve only as evidence of the breadth of the examples directory (SYM: example symbols list).

### The `req / res / next` Pattern

The middleware examples collectively demonstrate Express's `(req, res, next)` convention. `loadUser` reads from `req.params` and decorates `req.user` (FOCUS loadUser). `andRestrictToSelf` reads from both `req.authenticatedUser` and `req.user` (FOCUS andRestrictToSelf). `andRestrictTo` returns a closure that reads `req.authenticatedUser.role` (FOCUS andRestrictTo). This shows the request object serves as a shared context bag across middleware.

### What Cannot Be Determined (GAPS)

The GAPS annotation states: `type: STRUCTURAL (answerable from L0-L2), coverage: 5 symbols in L3, 1 with behavior annotations`. This means:

- The question is classified as STRUCTURAL, answerable from the tree, index, and symbol layers (L0–L2).
- Only 5 of the symbols have L3 (FOCUS) detail, and only 1 of those carries a behavior annotation (the `DELEGATE` annotation on `andRestrictTo`).
- **No routing internals are visible.** There is no `lib/router.js` in SYM, so the actual route-matching mechanism, method dispatch, and parameter parsing internals cannot be described from this clue file.
- **Middleware registration APIs** (e.g., `app.use`, `app.get`, `app.post`) are not surfaced in SYM or FOCUS, so we cannot describe how middleware is attached — only what individual middleware functions look like from the examples.
- The internal implementation of `app.handle` (referenced in FOCUS createApplication) is not expanded, so the request-dispatch pipeline is opaque beyond the entry point.
