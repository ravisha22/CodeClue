# v2.5 Response: blind-gin-struct-1
Date: 2026-04-16

## Question
What public constructors and core handler types define Gin's routing surface in the docs?

## Answer

The clue file reveals Gin's routing surface is built around three core types — `Engine`, `RouterGroup`, and `Context` — along with a `HandlerFunc` callback type and several public constructors.

### 1. Core Types

**`Engine`** (`gin.go:92`): "the framework's instance, it contains the muxer, middleware and configuration settings." Methods include `Delims`, `HandleContext`, `Handler`, `LoadHTMLFS`, `LoadHTMLFiles`, `LoadHTMLGlob` (FOCUS: `Engine`). It conforms to `http.Handler` via `ServeHTTP` (`gin.go:662`), which calls `reset`, `handleHTTPRequest`, and `updateRouteTrees`.

**`RouterGroup`** (documented via its methods in `routergroup.go`): Provides the HTTP verb routing methods. Key methods:
- `RouterGroup.GET` (`routergroup.go:116`): "GET is a shortcut for router.Handle('GET', path, handlers)." Delegates to `handle`.
- `RouterGroup.POST`, `PUT`, `DELETE`, `PATCH`, `HEAD`, `OPTIONS` — all follow the same pattern, delegating to `handle` (FOCUS entries at lines 111, 131, 121, 126, 141, 136 respectively).
- `RouterGroup.Any` (`routergroup.go:147`): "registers a route that matches all the HTTP methods." Calls `handle` in a loop.
- `RouterGroup.Match` (`routergroup.go:156`): "registers a route that matches the specified methods that you declared." Also loops over `handle`.
- `RouterGroup.Handle` (`routergroup.go:103`): "registers a new request handle and middleware with the given path and method." Validates the HTTP method with a regex guard and panics on invalid methods.

**`RouterGroup.handle`** (`routergroup.go:86`): The internal method all verb shortcuts delegate to. It calls `calculateAbsolutePath`, `combineHandlers`, and `returnObj` (FOCUS: `RouterGroup.handle`).

**`Context`** (`context.go:61`): "the most important part of gin." Methods include `Abort`, `AbortWithError`, `AbortWithStatus`, `AddParam`, etc. (FOCUS: `Context`).

### 2. Handler Types

**`HandlerFunc`**: The callback type used throughout. All routing methods accept `...HandlerFunc` parameters. `HandlersChain` is a slice of `HandlerFunc` — `HandlersChain.Last` (`gin.go:60`) returns the last handler in the chain with behavior `GUARD(length > 0 -> return c[length-1])`.

**`Context.Handler`** (`context.go:167`): "returns the main handler." Behavior: `DELEGATE(c.handlers.Last -> result)`.

**`Context.HandlerName`** (`context.go:149`): "returns the main handler's name." Behavior: `DELEGATE(nameOfFunction -> result)`.

**`Context.HandlerNames`** (`context.go:155`): "returns a list of all registered handlers for this context in descending order." Behavior: `ACCUMULATE(append loop -> hn)`.

### 3. Public Constructors

**`Engine.Handler`** (`gin.go:243`): behavior `GUARD(!engine.UseH2C -> return engine)`. Called by `Run`, `RunListener`, `RunQUIC`, `RunTLS`, `RunUnix` — this is the entry point for producing the `http.Handler` used to serve requests.

The INDEX shows `gin.go` exports `Default` (line 832), which is a public constructor. `Engine.With` is mentioned elsewhere as accepting `OptionFunc` to configure the engine (from blind-gin-rel-1 clue). `New` and `Default` are referenced as callers of `allocateContext` (`gin.go:252`, called by `New`, `CreateTestContext`, `CreateTestContextOnly`).

**`RouteInfo`** (`gin.go:68`): "represents a request route's specification which contains method and path and its handler." Used by `Engine.Routes` (`gin.go:390`), which returns all registered routes.

### 4. Interfaces

**`IRouter`** (`routergroup.go:27`): "defines all router handle interface includes single and group router."

**`IRoutes`** (`routergroup.go:33`): "defines all router handle interface." All verb methods return `IRoutes`.

### 5. Middleware as Handlers

Middleware functions are `HandlerFunc` values. Built-in middleware constructors include:
- `Logger` (`logger.go:224`): delegates to `LoggerWithConfig`.
- `Recovery`/`RecoveryWithWriter` (`recovery.go:45`): returns a middleware `HandlerFunc`.
- `CustomRecoveryWithWriter` (`recovery.go:53`): returns a custom recovery middleware.
- `ErrorLogger`/`ErrorLoggerT` (`logger.go:207/212`): error-logging middleware.
- `BasicAuth`/`BasicAuthForRealm`/`BasicAuthForProxy` (`auth.go`): authentication middleware.

### What Cannot Be Determined
GAPS notes uncovered symbols: `redirectFixedPath`, `redirectTrailingSlash`, `serveError`, `updateRouteTree`. The full constructor parameter list for `Engine` (via `New` or `Default`) is not detailed in the clue. The internal structure of `node` in `tree.go` (the radix tree) is not exposed.
