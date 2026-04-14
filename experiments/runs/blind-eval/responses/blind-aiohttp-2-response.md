During shutdown, the runner first performs shutdown-oriented steps, then application cleanup. The clue explicitly shows a shutdown phase in the runner (“Call any shutdown hooks to help server close gracefully”) before cleanup is invoked, and `AppRunner.cleanup` is the runner-side cleanup entrypoint. ([shutdown — `aiohttp/web_runner.py:302-303`], [cleanup — `aiohttp/web_runner.py:305-330`], [AppRunner — `aiohttp/web_runner.py:380-453`])

For application-owned startup resources, the unwind path appears to be `Application.cleanup`, which “Causes on_cleanup signal,” branches on a `frozen_on_cleanup_self` condition, and calls `_on_cleanup`. That strongly indicates cleanup is delegated into the application’s cleanup machinery rather than being inlined in the runner. ([cleanup — `aiohttp/web_app.py:351-360`])

The key unwind behavior is in `_on_cleanup(app)`: it is annotated as `ACCUMULATE(loop); UNWIND(reversed)`. Based solely on that clue, the application records cleanup items while iterating, then unwinds them in reverse order during shutdown. This is the strongest evidence for “startup resources are unwound in reverse order.” ([`_on_cleanup` — `aiohttp/web_app.py:430-441`])

The clue also exposes `cleanup_ctx` on `Application`, which strongly suggests the resources being unwound are cleanup-context-managed startup resources, but the exact body logic is not shown. So I can say the cleanup path is tied to application cleanup context, but I cannot prove the exact data structure or protocol from the clue alone. ([cleanup_ctx — `aiohttp/web_app.py:326-327`], [GAPS — mechanistic body logic needed, `aiohttp/web_runner.py` / overall clue footer])

If cleanup was only partially initialized, the `ACCUMULATE(loop)` annotation on `_on_cleanup` suggests only the successfully accumulated/initialized cleanup entries are available to be unwound; the clue does not support claiming that uninitialized entries are run. This is an inference from the “accumulate then unwind” behavior, not a fully exposed implementation. ([`_on_cleanup` — `aiohttp/web_app.py:430-441`], [GAPS — clue footer])

If one or more cleanup steps fail, `_on_cleanup` is explicitly marked as calling and raising `CleanupError`. Because `_on_cleanup` also has `ACCUMULATE(loop)`, the most supportable reading is that cleanup failures are collected during the loop and surfaced as `CleanupError` rather than stopping at the first failure. However, the clue does not reveal the exact shape of the aggregated error or whether partial successes continue after a failure beyond that accumulation annotation. ([`_on_cleanup` — `aiohttp/web_app.py:430-441`], [CleanupError — `aiohttp/web_app.py:403`])

So, based only on the clue file:

1. The server shuts down gracefully via runner shutdown hooks, then enters cleanup. ([shutdown — `aiohttp/web_runner.py:302-303`], [cleanup — `aiohttp/web_runner.py:305-330`])
2. Application cleanup delegates into `_on_cleanup`. ([cleanup — `aiohttp/web_app.py:351-360`])
3. `_on_cleanup` unwinds accumulated cleanup/startup resources in reverse order. ([`_on_cleanup` — `aiohttp/web_app.py:430-441`])
4. If initialization was only partial, only the accumulated portion appears eligible to be unwound, but the exact mechanics are not fully visible in the clue. ([`_on_cleanup` — `aiohttp/web_app.py:430-441`], [GAPS — clue footer])
5. If multiple cleanup steps fail, those failures are associated with `CleanupError`; the clue suggests accumulation of failures, but not the precise aggregation details. ([`_on_cleanup` — `aiohttp/web_app.py:430-441`], [CleanupError — `aiohttp/web_app.py:403`])
