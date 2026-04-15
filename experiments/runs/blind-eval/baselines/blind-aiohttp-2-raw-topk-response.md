# Response: blind-aiohttp-2 (raw-topk baseline)
Date: 2026-04-15

The prompt does **not** include the application cleanup implementation itself, so the shutdown story is only partially visible.

What the supplied code does show:

- In `aiohttp\web_server.py`, `Server.pre_shutdown` walks every active connection and calls `conn.close()` (`lines 167-169`).
- Then `Server.shutdown` builds `conn.shutdown(timeout)` coroutines for every connection, awaits them with `asyncio.gather(*coros)`, and finally clears `_connections` (`lines 171-174`).
- In the example app, `FakeFacebook.stop` delegates shutdown to `await self.runner.cleanup()` (`examples\fake_server.py`, lines 260-261), but the implementation of `runner.cleanup()` is not present in the prompt.

Because the excerpts do **not** include `AppRunner.cleanup`, application startup/cleanup context code, or any `on_startup` / `on_cleanup` machinery, the prompt does not show:

- how startup resources are unwound in reverse order,
- what happens when cleanup only partially initialized, or
- how multiple cleanup failures are aggregated or reported.

So the most supportable answer from the provided source is: connection-level shutdown is `close()` first, then `shutdown(timeout)` across all tracked connections (`aiohttp\web_server.py`, lines 167-174); anything more specific about partially initialized cleanup contexts or multiple cleanup exceptions is not available in the supplied excerpts.
