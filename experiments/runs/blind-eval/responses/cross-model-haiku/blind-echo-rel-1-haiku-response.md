# Cross-Model (Haiku): blind-echo-rel-1
Date: 2026-04-16

## Answer

During normal request dispatch, the relationships among `Echo`, `Group`, `Context`, and handlers follow this flow:

### Initialization & Context Setup

**Echo creates Context instances**: Echo maintains a context pool and creates new Context objects for each request [Lines 276-283: "Echo.AcquireContext returns an empty `Context` instance from the pool" with "behavior: DELEGATE(e.contextPool.Get -> result)" and "Echo.NewContext returns a new Context instance" "sig: Echo.NewContext(r *http.Request, w http.ResponseWriter)" "behavior: DELEGATE(newContext -> result)"]. The `newContext` function initializes the Context with the http.Request [Line 291: "called_by: newContext"].

**Context maintains reference to Echo**: The Context holds a back-reference to its parent Echo instance [Line 298-299: "Context.Echo returns the `Echo` instance"]. This allows handlers to access Echo configuration and services.

### Route Registration & Group Delegation

**Group delegates to Echo's routing**: Group provides a convenient namespace for sub-routes [Line 293-296: "Echo.Group creates a new router group with prefix and optional group-level middleware" "calls: Use"]. When Group methods are called (GET, POST, etc.), they delegate through `Group.Add()` [Lines 148-152: "Group.GET implements `Echo#GET()` for sub-routes within the Group" "behavior: DELEGATE(g.Add -> result)" "calls: Add"].

**Group.Add registers handlers**: The Group.Add method [Lines 135-141: "Group.Add implements `Echo#Add()` for sub-routes within the Group" "sig: Group.Add(method, path string, handler HandlerFunc, middleware ...MiddlewareFunc)" "behavior: GUARD(err != nil -> panic(err))" "calls: AddRoute"] validates registration and calls AddRoute to register with the router.

### Request Dispatch Flow

**Context carries request state**: The Context type [Line 131-133: "Context represents the context of the current HTTP request" with "methods: Attachment, Bind, Blob, Cookie, Cookies, Echo"] serves as the primary vehicle for passing request data to handlers. It provides access to:
- The original http.Request [Line 301-303: "Context.Request returns `*http.Request`"]
- Response writing capabilities [Line 298-299]
- Path parameters via `Context.SetPathValues()` [Lines 309-314: "Context.SetPathValues sets path parameters for current request" "calls: setPathValues"]

**Handlers receive Context**: All handlers are invoked with Context as the parameter (implied by the routing signatures), which gives them access to request data, response writers, and services.

### Middleware Integration

**Middleware wraps handler execution**: Echo.Use() adds middleware to the chain [Clue file, mentioned in Group context] which is executed after routing but before handler execution, allowing middleware to inject logic via the same Context object that handlers receive.

**Error handling via HTTPError**: When handlers produce errors, Echo's router and middleware chain can convert them to HTTPError responses [Clue file mentions HTTPError type for error responses].

In essence: **Echo coordinates** → **Group organizes routes** → **Context encapsulates request/response** → **handlers execute with Context** → **responses flow through Context**.
