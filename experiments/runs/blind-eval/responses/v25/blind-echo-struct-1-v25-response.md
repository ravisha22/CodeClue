# v2.5 Response: blind-echo-struct-1
Date: 2026-04-16

## Question

How is Echo's public API split between the core framework package and middleware packages?

---

## Answer

Echo's public API is divided along a clear structural boundary: a **core framework package** rooted in a handful of top-level source files, and a **middleware/ subdirectory** containing 24 dedicated middleware files. The two layers interact through a well-defined interface (`MiddlewareConfigurator`) and a single application method (`Echo.Use`). Below is a detailed breakdown, citing only the clue entries provided.

---

### 1. Core Framework Package — Top-Level Files

The TREE clue shows the repository root contains the following key source files:

| File | Lines (INDEX) | Primary Responsibility |
|---|---|---|
| `echo.go` | 865 L | Framework instance, routing verbs, middleware registration, server lifecycle |
| `context.go` | 667 L | Per-request context: request/response access, parameter binding, rendering |
| `router.go` | 1074 L | Route tree, pattern matching, path-parameter storage |
| `group.go` | 178 L | Sub-router groups that mirror the top-level API |
| `binder.go` | 1329 L | Request-body and query-parameter binding |
| `bind.go` | (listed in TREE) | Additional binding support |
| `response.go` | (listed in TREE) | HTTP response wrapper |
| `httperror.go` | (listed in TREE) | Structured HTTP error type |
| `server.go` | 202 L | HTTP server start/stop lifecycle |
| `route.go` | (listed in TREE) | Route metadata type |

#### 1.1 The `Echo` Type (echo.go:68)

The FOCUS entry identifies **`Echo`** as the "top-level framework instance." Its public surface falls into several categories:

**HTTP-verb route registration**
All verb helpers live in `echo.go` and DELEGATE to a single entry point:

- `Echo.GET`, `Echo.POST`, `Echo.PUT`, `Echo.DELETE`, `Echo.PATCH`, `Echo.HEAD`, `Echo.TRACE`, `Echo.CONNECT` — each DELEGATES to `Echo.Add`.
- `Echo.Any` — registers a route for every HTTP method; also DELEGATES to `Echo.Add`.
- `Echo.Match` — registers a route for a caller-specified set of methods; DELEGATES to `Echo.Add`.
- `Echo.Add` (echo.go:642) — the canonical registration method. It "registers route for HTTP method" and calls the internal `add` helper.
- `Echo.AddRoute` (echo.go:617) — registers a `Route` with the default host Router; also calls `add`.

**File-serving helpers** (all in `echo.go`):

- `Echo.File`, `Echo.FileFS`, `Echo.Static`, `Echo.StaticFS` — convenience methods that register routes for serving static assets directly from the core package.

**Middleware registration**:

- `Echo.Use` (echo.go:431) — "adds middleware to the chain which is run after router." This is the primary mechanism for attaching both core-defined and middleware-package-defined middleware.
- `applyMiddleware` (echo.go:785) — internal helper that applies the registered middleware chain.
- `WrapMiddleware` (echo.go:766) — wraps a standard `http.Handler` middleware so it can be used with Echo's middleware chain.

**Router grouping**:

- `Echo.Group` (echo.go:659) — creates a `Group` (group.go), which mirrors the top-level verb methods for sub-route scoping.

**Server lifecycle**:

- `Echo.Start` (echo.go:744) — starts the HTTP server.
- `Config` (echo.go, INDEX) — top-level configuration struct.
- `DefaultHTTPErrorHandler` (echo.go, INDEX) — fallback error handler.

**Request context**:

- `Echo.AcquireContext` (echo.go, INDEX) — acquires a `Context` from the pool (noted in GAPS as uncovered, so behavior details are uncertain — see §4).
- `Context` (context.go) — per-request type exposing methods for request/response access, parameter retrieval, and response rendering.

#### 1.2 The `MiddlewareConfigurator` Interface (echo.go:121)

The FOCUS entry describes `MiddlewareConfigurator` as the interface that "defines interface for creating middleware handlers." This is the contract that middleware configuration structs must satisfy so they can be converted into executable middleware via their `ToMiddleware` method. Crucially, this interface is **declared in the core package** (`echo.go:121`), establishing the bridge between core and middleware packages.

---

### 2. Middleware Package — `middleware/` Subdirectory

The TREE clue lists a `middleware/` subdirectory with **24 files**. The INDEX confirms individual files such as `static.go`, `compress.go`, `proxy.go`, `slash.go`, `csrf.go`, and others.

Each middleware is exposed as a **Config struct** that implements `ToMiddleware` (satisfying `MiddlewareConfigurator`). The clue entries enumerate the following concrete configs, all residing in `middleware/`:

| Config Type | File (middleware/) | Purpose |
|---|---|---|
| `GzipConfig` | `compress.go` | Response compression |
| `DecompressConfig` | `compress.go` | Request decompression |
| `StaticConfig` | `static.go` | Static file serving middleware |
| `ProxyConfig` | `proxy.go` | Reverse proxy |
| `CORSConfig` | (middleware/) | Cross-Origin Resource Sharing |
| `RequestLoggerConfig` | (middleware/) | Structured request logging |
| `CSRFConfig` | `csrf.go` | CSRF protection |
| `RemoveTrailingSlashConfig` | `slash.go` | URL normalization (remove slash) |
| `AddTrailingSlashConfig` | `slash.go` | URL normalization (add slash) |
| `BodyLimitConfig` | (middleware/) | Request body size limiting |
| `ContextTimeoutConfig` | (middleware/) | Per-request timeout |
| `SecureConfig` | (middleware/) | Security headers |
| `RedirectConfig` | (middleware/) | HTTP → HTTPS redirection |
| `BodyDumpConfig` | (middleware/) | Request/response body dumping |
| `BasicAuthConfig` | (middleware/) | HTTP Basic authentication |
| `RequestIDConfig` | (middleware/) | Unique request-ID injection |
| `MethodOverrideConfig` | (middleware/) | HTTP method override |
| `RewriteConfig` | (middleware/) | URL rewriting |
| `RateLimiterConfig` | (middleware/) | Rate limiting |

All of these follow the same pattern: the config struct lives in `middleware/`, implements `ToMiddleware`, and the resulting middleware is attached to an `Echo` instance via `Echo.Use` from the core package.

---

### 3. The Boundary Between Core and Middleware

The split can be summarized as:

| Concern | Location | Key Symbol(s) |
|---|---|---|
| Route registration & HTTP verbs | Core (`echo.go`) | `Echo.Add`, `Echo.GET`, etc. |
| Middleware attachment point | Core (`echo.go:431`) | `Echo.Use` |
| Middleware contract/interface | Core (`echo.go:121`) | `MiddlewareConfigurator` |
| Middleware wrapping utility | Core (`echo.go:766`) | `WrapMiddleware` |
| Middleware application | Core (`echo.go:785`) | `applyMiddleware` |
| Router internals | Core (`router.go`) | (1074 L, largest file) |
| Request context | Core (`context.go`) | `Context` (667 L) |
| Request binding | Core (`binder.go`) | (1329 L) |
| Grouping | Core (`group.go`) | `Echo.Group` (echo.go:659) |
| Server lifecycle | Core (`server.go`, `echo.go`) | `Echo.Start` (echo.go:744) |
| Concrete middleware behaviors | `middleware/` (24 files) | 19 named `*Config` types with `ToMiddleware` |

The core package owns the **routing, context, binding, error handling, and server lifecycle**. It also defines the `MiddlewareConfigurator` interface and the `Use`/`applyMiddleware`/`WrapMiddleware` plumbing. The `middleware/` package provides **concrete, opt-in behaviors** — each encapsulated in a config struct that plugs into the core via `ToMiddleware`.

---

### 4. Gaps and Uncertainties

The GAPS entry flags the following as **STRUCTURAL, uncovered**:

- **`Echo.AcquireContext`** — listed in INDEX as present in `echo.go` and mentioned in the FOCUS entry's method list, but its detailed behavior is not covered by the clue set. Its role in context pooling is implied but unconfirmed.
- **`Echo.Middlewares`** — not described in any FOCUS entry. Whether this is a getter for the registered middleware list or serves another purpose is unknown from the clues alone.
- **`Echo.NewContext`** — similarly uncovered. Likely a factory for `Context`, but specifics are unavailable.
- **`Echo.PreMiddlewares`** — uncovered. The name suggests middleware that runs *before* the router (contrasting with `Echo.Use` which runs "after router"), but this is speculative given the gap.

These gaps mean the **pre-router middleware layer** and **context lifecycle management** are not fully characterizable from the provided clues.

---

### 5. Summary

Echo's public API is cleanly partitioned:

1. **Core package** — provides the `Echo` framework instance, HTTP-verb registration (all delegating to `Echo.Add`), the `Context` type, router internals, request binding, response wrapping, error types, grouping, server lifecycle, and the `MiddlewareConfigurator` interface that defines the middleware contract.
2. **`middleware/` package** — provides 19+ concrete middleware config types (compression, CORS, CSRF, logging, auth, rate limiting, etc.), each implementing `ToMiddleware` and attached via the core's `Echo.Use`.

The interface declared in core (`MiddlewareConfigurator` at echo.go:121) is the formal seam; `Echo.Use` (echo.go:431) is the runtime attachment point; and every middleware config's `ToMiddleware` method is the bridge call.
