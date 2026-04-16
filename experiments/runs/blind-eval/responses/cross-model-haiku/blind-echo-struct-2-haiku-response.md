# Cross-Model (Haiku): blind-echo-struct-2
Date: 2026-04-16

## Answer

Echo's routing and request-handling surface is composed of the following public types and subcomponents:

### Core Framework Type
**`Echo`** (echo.go, line 152-154): "Echo is the top-level framework instance" with methods including `AcquireContext`, `Add`, `AddRoute`, `Any`, `CONNECT`, `DELETE`. The Echo type can be instantiated via `New()` [line 242-245: "New creates an instance of Echo" and "calls: DefaultHTTPErrorHandler, NewDefaultFS"].

### Routing Interface & Implementation
**`Router`** (router.go, line 140-141): "Router is interface for routing request contexts to registered routes."

**`DefaultRouter`** (router.go, line 132-134): "DefaultRouter is the registry of all registered routes for an `Echo` instance for request matching and URL path parameter" with methods `Add`, `Remove`, `Route`, `Routes`, `insert`, `storeRouteInfo`.

### Route Grouping
**`Group`** (group.go, line 119): "Group is a set of sub-routes for a specified route prefix". The Group type implements routing delegation [line 281-287: "Group.Add implements `Echo#Add()` for sub-routes within the Group" and calls `AddRoute`].

### Request Context
**`Context`** (context.go, line 289-291): "Context represents the context of the current HTTP request" with methods including `Attachment`, `Bind`, `Blob`, `Cookie`, `Cookies`, `Echo`. The Context provides request/response access [line 186-189: "Context.Request returns `*http.Request`" called by `fsFile`].

### Response Handling
**`Response`** type (response.go) handles HTTP response writing through `WriteHeader()` [line 68].

**`HTTPError`** (httperror.go, line 136-138): "HTTPError represents an error that occurred while handling a request" with methods `Error`, `StatusCode`, `Unwrap`, `Wrap`.

### Middleware & HTTP Verb Registration
Echo provides HTTP verb methods that delegate to `Add()`: the routing methods on both `Echo` and `Group` register routes via route registration [line 44-46: "Echo.Add registers a new route for an HTTP method" and "Group.Add implements `Echo#Add()` for sub-routes"].

Middleware support is provided through `Echo.Use()` [line 207-210: "Use adds middleware to the chain which is run after router has found matching route and before route/request handler met"].

This architecture separates concerns between the top-level Echo framework, route registration/grouping, request context binding, and middleware application.
