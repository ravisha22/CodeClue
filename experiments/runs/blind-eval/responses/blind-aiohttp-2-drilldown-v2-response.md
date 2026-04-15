# Response: blind-aiohttp-2 v2 (with drill-down)
Date: 2026-04-15

## Bottom line
From the supplied clue file, the shutdown path appears to have two layers: a runner/server layer that stops the server and invokes shutdown hooks, and an application layer that unwinds startup-acquired resources in reverse order. The strongest evidence for the unwind semantics is the pairing of `_on_startup` with `_on_cleanup`: startup accumulates `exits`, while cleanup performs `UNWIND(reversed)` and accumulates `errors`. [Clue: `_on_startup` (aiohttp/web_app.py:420-428) `behavior: ACCUMULATE(loop -> exits)`; Clue: `_on_cleanup` (aiohttp/web_app.py:430-441) `behavior: ACCUMULATE(loop -> errors); UNWIND(reversed)`]

## What the shutdown sequence appears to do

1. **A runner-level cleanup entrypoint exists and calls stop-related logic.**  
   The clue file says `cleanup` in `aiohttp/web_runner.py` is called by `AppRunner`, has `behavior: ACCUMULATE(loop -> result)`, and `calls: stop`. That tells us application shutdown goes through a runner cleanup phase that iterates and stops things, but the exact loop contents are not shown in the prompt. [Clue: `cleanup` (aiohttp/web_runner.py:305-330)]

2. **There is also an explicit graceful-shutdown hook path.**  
   The clue file says `shutdown` in `aiohttp/web_runner.py` exists to “Call any shutdown hooks to help server close gracefully,” and the `Server` symbol calls `shutdown`. So, before or during cleanup, the server has a hook-oriented graceful-shutdown phase. However, the exact order relative to `_cleanup_server` and application cleanup is not fully recoverable from the provided material. [Clue: `shutdown` (aiohttp/web_runner.py:302-303); Clue: `Server` (aiohttp/web_server.py:30-126) `calls: shutdown`]

3. **Application-owned startup resources are unwound through the application cleanup path.**  
   The clue file says `cleanup` in `aiohttp/web_app.py` “Causes on_cleanup signal” and branches: if `on_cleanup.frozen` it uses the signal path, otherwise it directly calls `_on_cleanup`. This is important because `_on_cleanup` is the place where reverse-order unwinding is explicitly described. [Clue: `cleanup` (aiohttp/web_app.py:351-360) `behavior: BRANCH(on_cleanup.frozen -> result, else -> result)` and `calls: _on_cleanup`; Clue: `_on_cleanup` (aiohttp/web_app.py:430-441)]

## How startup resources are unwound

4. **Startup appears to register cleanup exits, and cleanup unwinds those exits in reverse order.**  
   `_on_startup` has `behavior: ACCUMULATE(loop -> exits)`, while `_on_cleanup` has `behavior: ACCUMULATE(loop -> errors); UNWIND(reversed)`. The most defensible reading is that startup records a sequence of cleanup callbacks / exit handlers, and shutdown later runs them in reverse order. This is the classic “last initialized, first cleaned up” pattern, but I am not relying on outside knowledge here—the reverse unwind is directly stated in the clue. [Clue: `_on_startup` (aiohttp/web_app.py:420-428); Clue: `_on_cleanup` (aiohttp/web_app.py:430-441)]

5. **`CleanupContext` is part of this mechanism.**  
   The clue file lists `CleanupContext` in `aiohttp/web_app.py:415-441`, says it is called by `Application`, and says it can raise `CleanupError`. That strongly ties startup/cleanup resource lifetime management to `Application` and the `_on_startup` / `_on_cleanup` region. [Clue: `CleanupContext` (aiohttp/web_app.py:415-441); Clue: `Application` (aiohttp/web_app.py:71-400)]

## What happens if cleanup only partially initialized

6. **There is an explicit fallback when the normal `on_cleanup` signal path is not fully available.**  
   The clue for `Application.cleanup` says it branches on `on_cleanup.frozen`: if frozen, it uses the normal `on_cleanup` signal route; otherwise, it directly calls `_on_cleanup`. Since `_on_cleanup` is the function that performs reverse-order unwinding, this strongly suggests cleanup can still unwind already-registered startup resources even if the normal cleanup signal machinery was not fully initialized/frozen. [Clue: `cleanup` (aiohttp/web_app.py:351-360); Clue: `_on_cleanup` (aiohttp/web_app.py:430-441)]

7. **What I can determine about “partial initialization” is limited to that branch.**  
   The prompt does **not** include the body of `Application.cleanup`, `CleanupContext`, or `_on_startup`, so I cannot prove exactly what state counts as “partially initialized,” nor can I prove the exact storage structure for the recorded exits. I can only say that the branch to direct `_on_cleanup` exists, and `_on_cleanup` is the reverse unwinder. [Clue: `cleanup` (aiohttp/web_app.py:351-360); Clue: `_on_startup` (aiohttp/web_app.py:420-428); Clue: `_on_cleanup` (aiohttp/web_app.py:430-441)]

## What happens if multiple cleanup steps fail

8. **Failures are accumulated rather than immediately stopping at the first error.**  
   `_on_cleanup` is annotated with `ACCUMULATE(loop -> errors)`, which indicates cleanup iterates through the cleanup steps and collects failures into an `errors` collection. This is the strongest direct evidence about error handling. [Clue: `_on_cleanup` (aiohttp/web_app.py:430-441)]

9. **After collecting cleanup failures, a `CleanupError` is raised.**  
   The same clue says `_on_cleanup` `calls: CleanupError` and `raises: CleanupError`. Therefore, when cleanup steps fail, the failure is surfaced through `CleanupError` rather than silently ignored. [Clue: `_on_cleanup` (aiohttp/web_app.py:430-441)]

10. **If multiple cleanup steps fail, the resulting error is aggregate in nature, but the exact shape is not shown.**  
    Because `_on_cleanup` both accumulates `errors` and raises `CleanupError`, the supported conclusion is that multiple failures are collected and then reported via `CleanupError`. However, the prompt does not show the body of `CleanupError` or `_on_cleanup`, so I cannot say whether `CleanupError` stores a list of exceptions, wraps only the first one, formats them into a message, or exposes them in some other structure. [Clue: `_on_cleanup` (aiohttp/web_app.py:430-441); Clue: `CleanupError` (aiohttp/web_app.py:403-406) `extends: RuntimeError`]

## What I can and cannot say about runner/server cleanup specifically

11. **I can say that runner cleanup exists, calls `stop`, and the server has shutdown hooks.**  
    That is directly supported by the clue entries for `cleanup` in `web_runner.py`, `stop`, `shutdown`, `Server`, and `AppRunner`. [Clue: `cleanup` (aiohttp/web_runner.py:305-330); Clue: `stop` (aiohttp/web_runner.py:73); Clue: `shutdown` (aiohttp/web_runner.py:302-303); Clue: `Server` (aiohttp/web_server.py:30-126); Clue: `AppRunner` (aiohttp/web_runner.py:380-453) `calls: cleanup`]

12. **I cannot fully reconstruct the exact order of `stop`, graceful shutdown hooks, `_cleanup_server`, and `Application.cleanup`.**  
    The prompt highlights `_cleanup_server` at several locations in `web_runner.py`, but does not provide its body or behavior annotation. So I cannot responsibly claim the precise interleaving of runner-level teardown and application-level cleanup beyond the facts above. [Clue: `_cleanup_server` focus entries at `aiohttp/web_runner.py:337-338`, `376-377`, `452-453`; Clue: `cleanup` (aiohttp/web_runner.py:305-330); Clue: `shutdown` (aiohttp/web_runner.py:302-303)]

## Answer to the question

During shutdown, the server appears to enter a runner-managed cleanup phase that stops components and uses shutdown hooks for graceful closing, while the application layer performs the actual unwind of startup-acquired resources. The application-side unwind is driven by `_on_cleanup`, which runs cleanup in **reverse order** of the startup registrations implied by `_on_startup`’s accumulated `exits`. [Clue: `cleanup` in `web_runner.py`; Clue: `shutdown` in `web_runner.py`; Clue: `Server` calls `shutdown`; Clue: `_on_startup` accumulates `exits`; Clue: `_on_cleanup` does `UNWIND(reversed)`]

If cleanup was only partially initialized, the code path in `Application.cleanup` still has a fallback: when the normal `on_cleanup` signal route is not in the `frozen` state, it directly invokes `_on_cleanup`. From the supplied materials, that is the best evidence that already-registered startup resources can still be unwound even without a fully established cleanup signal path. [Clue: `cleanup` (aiohttp/web_app.py:351-360); Clue: `_on_cleanup` (aiohttp/web_app.py:430-441)]

If multiple cleanup steps fail, `_on_cleanup` does **not** appear to abort on the first one. Instead, it accumulates cleanup errors across the loop and then raises `CleanupError`. What I cannot determine from the supplied prompt is the exact structure/content of that `CleanupError`; only that it is raised after error accumulation and that it is a `RuntimeError` subtype. [Clue: `_on_cleanup` (aiohttp/web_app.py:430-441); Clue: `CleanupError` (aiohttp/web_app.py:403-406)]
