# Scoring: v2.2 dev-structrel

### struct-aiohttp-1 (1/2)
F1: COVERED — Response explicitly lists "aiohttp/" package and enumerates server/web modules including "web_app.py", "web_request.py", "web_response.py" with symbol-level evidence.
F2: MISS — Response mentions "tests/ contains autobahn/ and isolated/" but never claims that tests mirror the main package structure.

### struct-aiohttp-2 (0/2)
F1: MISS — Response identifies web_request.py for request processing and web_response.py for response handling, but never names BaseRequest or Request classes. Only method-level symbols (read, _etag_values, remote, version) are cited.
F2: MISS — Response covers web_app.py (Application) and web_urldispatcher (UrlDispatcher) but omits web_server.py and the Server class entirely. Only AppRunner/ServerRunner in web_runner.py are mentioned.

### rel-aiohttp-1 (2/2)
F1: COVERED — Response explicitly states "BaseRequest extends HeadersMixin, and Request extends BaseRequest" with both located in web_request.py (lines 109-823 and 826-884).
F2: COVERED — Response states "StreamResponse extends HeadersMixin, CookieMixin" and "Response" extends StreamResponse, citing both in web_response.py (lines 74-532 and 535-740).

### rel-aiohttp-2 (0/2)
F1: MISS — Response lists Application's calls (freeze, handler, reg_handler, etc.) but never mentions startup, shutdown, or cleanup as methods Application calls, nor signal handlers. Server is mentioned only in the lifecycle section as a separate class, not as something Application creates/uses.
F2: MISS — No mention of Application.startup/shutdown dispatching to signal handlers or CleanupContext. Response mentions CleanupError but not CleanupContext.

### struct-fiber-1 (1/2)
F1: MISS — Response identifies app.go with App struct and routing methods but completely omits ctx.go (request context). Only res.go, bind.go, and redirect.go are named as root-level files.
F2: COVERED — Response identifies "dedicated middleware/ directory with 134 files" and lists many separate subpackages (cache, limiter, paginate, idempotency, adaptor, session, skip, earlydata, requestid, encryptcookie).

### struct-fiber-2 (1/2)
F1: COVERED — Response identifies ctx.go with DefaultCtx methods (Get, String, Matched, IsMiddleware, Path) and references CustomCtx extending Ctx in ctx_interface.go, establishing the Ctx interface and DefaultCtx struct.
F2: MISS — Response describes routing across app.go, group.go, domain.go, register.go, and path.go but never mentions router.go. The gold fact specifically requires routing logic split between router.go and app.go.

### rel-fiber-1 (1/2)
F1: COVERED — Response shows App with HTTP method helpers (Add, All, Connect, Delete) for route registration, and App.printRoutesMessage "prints all routes with method, path, name, and handlers" implying stored routes.
F2: MISS — Response covers Group well ("collection of routes that share middleware and a common path prefix") with hierarchical sub-routing via App.Group. However, it explicitly states "the visible entries do not expose a standalone Router type," so the Router type from the gold fact is not identified.

### rel-fiber-2 (0/2)
F1: MISS — Response discusses middleware registration (App.Use, Group.Use) and handler wrapping (domainRouter.wrapHandlers) but never mentions Ctx.Next() as the chaining mechanism that advances to the next handler.
F2: MISS — Response describes middleware pipeline construction and context interaction but never explicitly states that middleware runs in registration order or that each middleware can short-circuit the chain.

---
**Total: 6/16**

| Task | Score |
|------|-------|
| struct-aiohttp-1 | 1/2 |
| struct-aiohttp-2 | 0/2 |
| rel-aiohttp-1 | 2/2 |
| rel-aiohttp-2 | 0/2 |
| struct-fiber-1 | 1/2 |
| struct-fiber-2 | 1/2 |
| rel-fiber-1 | 1/2 |
| rel-fiber-2 | 0/2 |
