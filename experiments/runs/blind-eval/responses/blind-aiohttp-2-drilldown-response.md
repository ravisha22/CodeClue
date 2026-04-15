# Response: blind-aiohttp-2 (with drill-down)
2026-04-15

The shutdown path in the runner is:
1. Stop each site one-by-one with `await site.stop()`; the code explicitly avoids `gather()` so a failure does not leave `self._sites` in an unpredictable state, and a site is either removed on success or still present on failure. (Source snippet: `cleanup` in `aiohttp/web_runner.py` L305-330)
2. If `self._server` exists — explicitly noted as “If setup succeeded” — yield once to the event loop, call `self._server.pre_shutdown()`, run `await self.shutdown()`, then `await self._server.shutdown(self._shutdown_timeout)`. (Source snippet: `cleanup` in `aiohttp/web_runner.py` L305-330)
3. After that, call `await self._cleanup_server()`. For `AppRunner`, `_cleanup_server()` is exactly `await self._app.cleanup()`. (Source snippets: `cleanup` L305-330; `AppRunner` / `_cleanup_server` L380-453)

For an application runner, startup and teardown line up symmetrically:
- Setup creates the server by calling `_make_server()`. (Source snippets: `setup` L288-299; `BaseRunner` L252-352)
- `AppRunner._make_server()` freezes `on_startup`, awaits `self._app.startup()`, then freezes the app and returns a `Server`. (Source snippet: `_make_server` in `aiohttp/web_runner.py` L421-430)
- Later, runner shutdown calls `await self._app.shutdown()`. (Source snippets: `shutdown` L418-419; `AppRunner` L380-453)
- Final cleanup calls `await self._app.cleanup()`. (Source snippet: `AppRunner._cleanup_server` L380-453)

The clue file shows how startup resources are unwound inside application cleanup:
- `_on_startup(app)` has behavior `ACCUMULATE(loop -> exits)`, which indicates startup records exit/teardown actions while iterating startup cleanup contexts. (Clue entry: `_on_startup` in `aiohttp/web_app.py:420-428`)
- `_on_cleanup(app)` has behavior `ACCUMULATE(loop -> errors); UNWIND(reversed)`, so cleanup walks those recorded exits in reverse order and keeps collecting cleanup failures instead of stopping at the first one. (Clue entry: `_on_cleanup` in `aiohttp/web_app.py:430-441`)
- `Application.cleanup()` is the method that triggers this, with clue behavior `BRANCH(on_cleanup.frozen -> result, else -> result)` and `calls: _on_cleanup`. (Clue entry: `cleanup` in `aiohttp/web_app.py:351-360`)

So, based only on the provided material, the server unwinds startup resources by delegating from runner cleanup to `app.cleanup()`, and the application cleanup logic unwinds the startup-registered exits in reverse order. (Source snippets: `cleanup` L305-330; `AppRunner._cleanup_server` L380-453. Clue entries: `_on_startup`, `_on_cleanup`, `cleanup` in `aiohttp/web_app.py`)

If cleanup was only partially initialized, the provided material suggests the code is designed to handle that case rather than assuming full initialization:
- `Application.cleanup()` has an explicit branch on whether `on_cleanup` is frozen. (Clue entry: `cleanup` in `aiohttp/web_app.py:351-360`)
- `_on_cleanup` is tied to `Application` / `CleanupContext`, not just the general signal path. (Clue entries: `_on_cleanup` in `aiohttp/web_app.py:430-441`; `CleanupContext` in `aiohttp/web_app.py:415-441`)
- From that, we can determine there is a special cleanup path for cases where the normal cleanup signal state is not in the fully frozen/normal state. What we cannot determine from the prompt alone is the exact internal condition checked beyond `on_cleanup.frozen`, or exactly which partially initialized resources are present in that branch. (Clue entries: `cleanup`, `_on_cleanup`, `CleanupContext`)

If multiple cleanup steps fail, the provided evidence says failures are accumulated and then a `CleanupError` is involved:
- `_on_cleanup` explicitly has behavior `ACCUMULATE(loop -> errors)` and `calls: CleanupError`, `raises: CleanupError`. (Clue entry: `_on_cleanup` in `aiohttp/web_app.py:430-441`)
- `CleanupContext` also `calls: CleanupError` and `raises: CleanupError`. (Clue entry: `CleanupContext` in `aiohttp/web_app.py:415-441`)
- Therefore, if more than one cleanup step fails, the code does not appear to stop at the first failure; it accumulates multiple errors and raises `CleanupError`. What the prompt does not reveal is the exact structure/content of `CleanupError` or whether a single failure is wrapped the same way as multiple failures. (Clue entries: `_on_cleanup`, `CleanupContext`, `CleanupError`)

One more failure-mode detail is directly visible in runner cleanup: site shutdown is intentionally serialized, not gathered, specifically so failure leaves site-registration state predictable. That means cleanup tries to preserve a coherent partial state even when shutdown of one site fails. (Source snippet: `cleanup` in `aiohttp/web_runner.py` L305-330)

In short: runner cleanup stops sites, shuts down the server, then calls `app.cleanup()`; application cleanup unwinds startup-registered exits in reverse order; and cleanup failures are accumulated and surfaced via `CleanupError`, though the exact error payload/format is not recoverable from the provided material alone. (Source snippets: `cleanup` L305-330; `AppRunner._cleanup_server` L380-453. Clue entries: `_on_startup`, `_on_cleanup`, `cleanup`, `CleanupError`, `CleanupContext`)
