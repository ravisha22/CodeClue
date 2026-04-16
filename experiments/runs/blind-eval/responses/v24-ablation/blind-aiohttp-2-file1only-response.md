# v2.4 Ablation (File 1 Only): blind-aiohttp-2
Date: 2026-04-16

Startup resources are recorded during startup and unwound in reverse order during cleanup. The clue shows `_on_startup` accumulating `self` into `exits`, and `_on_cleanup` later iterating `reversed(self._exits)` with an explicit `UNWIND(reversed)`. [ _on_startup (aiohttp/web_app.py:420-428); _on_cleanup (aiohttp/web_app.py:430-441) ]

Application cleanup has two paths: `cleanup()` either awaits the frozen `on_cleanup` signal, or it calls the internal cleanup-context unwinder directly via `_on_cleanup`. That suggests cleanup still has an internal fallback path even if the public signal path is not the one used. [cleanup (aiohttp/web_app.py:351-360)]

If cleanup steps fail, `_on_cleanup` accumulates those failures into `errors` and raises `CleanupError`; `CleanupError` is called by both `_on_cleanup` and `CleanupContext`. So multiple cleanup failures are gathered rather than immediately discarded. [ _on_cleanup (aiohttp/web_app.py:430-441); CleanupContext (aiohttp/web_app.py:415-441); CleanupError (aiohttp/web_app.py:403-406) ]

At the runner/server level, shutdown is split into phases: runner shutdown calls shutdown hooks, server pre-shutdown walks connections, runner cleanup stops sites, and `_cleanup_server` is documented as running cleanup steps after shutdown. [shutdown (aiohttp/web_runner.py:302-303); pre_shutdown (aiohttp/web_server.py:107-109); cleanup (aiohttp/web_runner.py:305-330); _cleanup_server (aiohttp/web_runner.py:337-338)]

What I cannot determine from this clue file: the exact data stored in each `exit`, how partially initialized cleanup contexts are represented internally, and the exact structure/content of the raised `CleanupError` when several cleanup steps fail. [GAPS; _on_startup (aiohttp/web_app.py:420-428); _on_cleanup (aiohttp/web_app.py:430-441)]
