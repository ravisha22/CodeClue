# Cross-Model (Sonnet): blind-echo-rel-1
Date: 2026-04-16

Based on the clue file and source snippets, the main relationships among `Echo`, `Group`, `Context`, and handlers during normal request dispatch form a hierarchical delegation and composition pattern:

## Core Architectural Relationships

### 1. Echo as Root Framework Instance

**Echo** serves as the top-level orchestrator:
- **Definition**: "Echo is the top-level framework instance" (echo.go:68-68)
- **HTTP Interface**: `Echo.ServeHTTP` (echo.go:695): "ServeHTTP implements `http.Handler` interface" - this is the entry point for all HTTP requests
- **Route Registration**: `Echo.Add` (echo.go:642): "Add registers a new route for an HTTP method"
- **Middleware Chain**: `Echo.Use` (echo.go:431): "Use adds middleware to the chain which is run a"

### 2. Group as Route Organization Layer

**Group** provides sub-routing and route organization within Echo:
- **Definition**: "Group is a set of sub-routes for a specified ro" (group.go:14)
- **Echo Delegation**: `Group.Add` "Add implements `Echo#Add()` for sub-routes with" (group.go:158)
- **Source Evidence**: `func (g *Group) Add(method, path string, handler HandlerFunc, middleware ...MiddlewareFunc) RouteInfo` - Groups accept handlers and delegate to Echo's routing system
- **Method Delegation**: Multiple methods like `Group.GET` (group.go:37): "GET implements `Echo#GET()` for sub-routes with" showing Groups mirror Echo's HTTP method interface

### 3. Context as Request-Scoped State Container

**Context** represents individual request processing state:
- **Definition**: "Context represents the context of the current HTTP request" (context.go:40)
- **Request Access**: `Context.Request` (context.go:129): "Request returns `*http.Request`" 
- **Response Access**: `Context.Response` (context.go:139): "Response returns `*Response`"
- **Data Binding**: `Context.Bind` (context.go:399): "Bind binds path params, query params and the request body"
- **Echo Reference**: `Context.Echo` (context.go:665): "Echo returns the `Echo` instance" - showing Context maintains reference back to Echo

### 4. Handler Functions as Request Processors

**Handlers** are functions that process requests using Context:
- **Signature Evidence**: From source snippet `func (g *Group) Add(method, path string, handler HandlerFunc, middleware ...MiddlewareFunc)` - handlers have type `HandlerFunc`
- **Context Integration**: Handlers work with Context to process requests and generate responses
- **Middleware Integration**: Handlers can be wrapped with middleware as seen in Group.Add signature

## Request Dispatch Flow

### 1. Request Entry
1. **HTTP Server → Echo.ServeHTTP**: All requests enter through `Echo.ServeHTTP` (echo.go:695) which implements `http.Handler`
2. **Context Creation**: Echo creates or acquires a Context for the request via `Echo.AcquireContext` (from echo.go INDEX)

### 2. Route Resolution  
1. **Router Lookup**: Echo uses its router to find matching route
2. **Handler Selection**: Router identifies the appropriate HandlerFunc for the request
3. **Path Parameters**: Context receives path values via `Context.setPathValues` (context.go:269)

### 3. Handler Execution
1. **Middleware Chain**: Middleware added via `Echo.Use` executes before handler
2. **Handler Invocation**: The matched HandlerFunc executes with the Context
3. **Response Generation**: Handler uses Context methods like `Context.Blob`, `Context.String`, etc. to generate responses

### 4. Group Integration
- **Route Registration**: Groups use `Group.Add` which delegates to `Echo.Add` via "behavior: DELEGATE(g.Add -> result)" patterns
- **Path Prefixing**: Groups handle path prefixing for their sub-routes
- **Middleware Inheritance**: Groups can add middleware that applies to their sub-routes

## Key Relationship Patterns

### Delegation Hierarchy
```
HTTP Request → Echo.ServeHTTP → Router → Handler(Context)
                ↓
            Group.Add → Echo.Add (route registration)
```

### Context Flow
- **Request In**: `Context.Request()` provides access to `*http.Request`
- **Response Out**: `Context.Response()` provides access to response writer
- **Data Binding**: `Context.Bind()` handles parameter/body binding
- **Echo Reference**: `Context.Echo()` maintains connection to framework instance

### Testing Integration
The `ContextConfig` (echotest/context.go:20-20) provides testing support:
- **Test Context Creation**: `func (conf ContextConfig) ToContext(t *testing.T) *echo.Context` creates Context for testing
- **Response Recording**: `func (conf ContextConfig) ToContextRecorder(t *testing.T) (*echo.Context, *httptest.ResponseRecorder)` provides response capture

This architecture creates a clean separation where Echo orchestrates the overall framework, Groups organize routes hierarchically, Context encapsulates request-specific state and operations, and handlers contain the actual business logic for processing requests.