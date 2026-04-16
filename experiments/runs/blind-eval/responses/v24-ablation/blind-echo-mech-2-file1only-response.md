# v2.4 Ablation (File 1 Only): blind-echo-mech-2
Date: 2026-04-16

Echo’s centralized error handler is `DefaultHTTPErrorHandler`, created by `New`. [DefaultHTTPErrorHandler (echo.go:374-374)]

The key decision point visible in the clue is `ResolveResponseStatus(rw, err)`. It returns both the response object and the HTTP status that should be (or has been) sent, and its first guard says that if there is already a response and it is committed, it immediately returns that response and its status. [ResolveResponseStatus (httperror.go:66-66)]

That committed-response behavior lines up with `Response.WriteHeader`, which refuses to write headers again once `r.Committed` is true. [Response.WriteHeader (response.go:49-49)]

For typed HTTP errors, the clue shows multiple status-code aware paths: `StatusCode` is a generic helper that returns a status code from an error when available; `HTTPError` exposes `StatusCode`; and the internal `httpError` type also exposes `StatusCode`. [StatusCode (httperror.go:45); HTTPError.StatusCode (httperror.go:115-115); httpError (httperror.go:144-144)]

Both `HTTPError` and `httpError` also support `Wrap(err)`, so ordinary errors can be wrapped into HTTP-aware error objects before status resolution. [HTTPError.Wrap (httperror.go:132-132); httpError.Wrap (httperror.go:156-156)]

So, from the clue alone: if a handler returns an error after the response is already committed, the centralized path short-circuits and preserves the existing response/status; if it receives an HTTP-aware error, status comes from the error’s status-code path; and if it receives an ordinary error, the framework has wrapping/status-code helpers available to convert that into an HTTP status decision. [ResolveResponseStatus (httperror.go:66-66); StatusCode (httperror.go:45); HTTPError.Wrap (httperror.go:132-132)]

What I cannot determine from this clue file: the exact default status chosen for a plain, unwrapped error, or the exact response body shape emitted by `DefaultHTTPErrorHandler`, because the handler body itself is not exposed. [DefaultHTTPErrorHandler (echo.go:374-374); GAPS]
