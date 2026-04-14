# Step 1: Gold Task Creator Prompt
# Paste this ENTIRE prompt into GPT-5.4 or Gemini (NOT Claude)

You are creating evaluation tasks for a code comprehension system. Your job is
to write questions and gold-standard answers that test whether the system can
understand a codebase from a compressed summary.

IMPORTANT RULES:
- You are NOT testing the LLM's general knowledge. You are testing whether
  specific facts about THIS codebase can be recovered from a summary.
- Each gold fact MUST reference specific symbols, files, or mechanisms that
  exist in the source code.
- Do NOT write facts that could be guessed from framework documentation alone.
  Facts must require reading the actual implementation.
- Mix question types: some structural ("what files/classes are involved"),
  some mechanistic ("how does X work internally"), some about error handling
  or edge cases.
- Use natural language in questions — avoid using exact class or function
  names when possible. A developer might ask "how does the server handle
  slow clients?" not "what does StreamResponse do?"

For EACH of the 3 repositories below, create exactly 2 tasks.

Output as a JSON array with this schema per task:
```json
{
  "task_id": "blind-{repo}-{number}",
  "repo": "{repo_name}",
  "repo_path": "experiments/external-repos/{repo_name}",
  "question": "A realistic developer question",
  "gold_files": ["path/to/relevant/file.py", ...],
  "gold_symbols": ["ClassName", "function_name", ...],
  "gold_facts": [
    "Specific fact 1 that must be in the answer",
    "Specific fact 2 ...",
    "Specific fact 3 ...",
    "Specific fact 4 ..."
  ]
}
```

## Repository 1: aiohttp (Python async HTTP framework)

This is the aiohttp library source code. Key directories:
- `aiohttp/` — main package (web server, client, routing, middleware)
- `tests/` — test suite

To help you write accurate gold facts, here are some key files and their
contents. Read them carefully before creating tasks.

### aiohttp/web_app.py (Application class)
```
Check the source at: https://github.com/aio-libs/aiohttp
Key classes: Application, CleanupError
Key methods: _handle, startup, shutdown, cleanup, on_startup, on_shutdown
```

### aiohttp/web_request.py (Request handling)
```
Key classes: BaseRequest, Request
Key methods: read, json, post, multipart, content
```

Create 2 tasks for aiohttp. One should be about request processing or
middleware, one about error handling or lifecycle management.

## Repository 2: fiber (Go HTTP framework)

This is the Fiber web framework for Go. Key files:
- `app.go` — main App struct, routing, server lifecycle
- `ctx.go` — request/response Context
- `router.go` — route registration and matching
- `middleware/` — built-in middleware

Check source at: https://github.com/gofiber/fiber

Create 2 tasks for fiber. One should be about routing or context handling,
one about middleware or error recovery.

## Repository 3: click (Python CLI framework)

This is the Click library for building command-line interfaces. Key files:
- `src/click/core.py` — Command, Group, Context classes
- `src/click/decorators.py` — @command, @option, @argument decorators
- `src/click/types.py` — parameter type system
- `src/click/testing.py` — CLI test utilities

Check source at: https://github.com/pallets/click

Create 2 tasks for click. One should be about command/group structure,
one about parameter parsing or type conversion.

## Output

Return ONLY the JSON array with 6 tasks. No explanation needed.
