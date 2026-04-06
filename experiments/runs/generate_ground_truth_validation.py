"""Ground-truth validation: gold answers, raw-source prompts, and scoring.

Generates:
1. Gold-truth answer files (verified against source code)
2. Arm A (raw-source) consumer prompts for 10 tasks
3. A scorer that compares clue answers AND raw-source answers against gold truth

Usage:
    python experiments/runs/generate_ground_truth_validation.py

Then:
    1. Paste each .prompt.md into an LLM, save as .response.md
    2. Run: python experiments/runs/score_ground_truth.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from codeclue_research.token_counter import count_tokens

# 10 validation tasks: 2 per family, selected for source-code availability
VALIDATION_TASKS = [
    # TF1: Architecture (Flask, Express)
    {
        "task_id": "flask-tf1-001",
        "family": "TF1",
        "repo": "flask",
        "question": "What is the high-level architecture of Flask's request handling?",
        "gold_answer": (
            "Flask's HTTP request handling follows a pipeline: "
            "(1) __call__ (line 1607) delegates to wsgi_app (line 1567). "
            "(2) wsgi_app creates a RequestContext via request_context(environ), pushes it "
            "to make request/session/g/current_app available. "
            "(3) full_dispatch_request runs before_request hooks, dispatches to the matched "
            "view function via dispatch_request, then finalizes via finalize_request. "
            "(4) Errors route through handle_exception. "
            "(5) Context teardown runs in a finally block via ctx.pop(), which calls "
            "do_teardown_request and do_teardown_appcontext. "
            "Key files: src/flask/app.py (main pipeline), src/flask/ctx.py (context management)."
        ),
        "gold_symbols": ["wsgi_app", "__call__", "full_dispatch_request", "dispatch_request",
                         "finalize_request", "handle_exception", "request_context", "ctx.push", "ctx.pop"],
        "gold_facts": [
            "wsgi_app creates RequestContext",
            "context pushed to activate request/session/g globals",
            "full_dispatch_request runs before_request hooks",
            "dispatch_request calls the view function",
            "finalize_request runs after_request hooks",
            "teardown runs in finally block",
        ],
        "source_files": ["src/flask/app.py", "src/flask/ctx.py"],
    },
    {
        "task_id": "express-tf1-001",
        "family": "TF1",
        "repo": "express",
        "question": "Express middleware architecture?",
        "gold_answer": (
            "Express uses a router-based middleware pipeline. "
            "app.handle(req, res, callback) at lib/application.js line 143 sets up the request "
            "and delegates to this.router.handle(req, res, done) at line 173. "
            "Middleware is registered via app.use(path, fn) which delegates to router.use(). "
            "The router is lazily created. Each middleware receives (req, res, next) and calls "
            "next() to pass to the next handler. Middleware executes in registration order."
        ),
        "gold_symbols": ["app.handle", "router.handle", "app.use", "router.use"],
        "gold_facts": [
            "router-based middleware pipeline",
            "app.handle delegates to router.handle",
            "middleware registered via app.use",
            "middleware receives req, res, next",
            "executed in registration order",
        ],
        "source_files": ["lib/application.js", "lib/router/index.js"],
    },
    # TF2: Impact Analysis (Flask, httpx)
    {
        "task_id": "flask-tf2-001",
        "family": "TF2",
        "repo": "flask",
        "question": "What is the downstream impact of modifying Flask.wsgi_app?",
        "gold_answer": (
            "Modifying wsgi_app impacts the entire request lifecycle: "
            "(1) request_context(environ) — context creation and route matching. "
            "(2) ctx.push() — activation of context variables. "
            "(3) full_dispatch_request — the complete dispatch chain: preprocess_request "
            "(url_value_preprocessors + before_request_funcs), dispatch_request (view invocation), "
            "handle_user_exception, and finalize_request (make_response + process_response + "
            "after_request_funcs + session save). "
            "(4) handle_exception — error handling and 500 response. "
            "(5) ctx.pop(error) — teardown_request_funcs and teardown_appcontext_funcs. "
            "The finally block ensures teardown always runs. Any change to wsgi_app's "
            "try/except/finally structure affects exception propagation for all request paths."
        ),
        "gold_symbols": ["wsgi_app", "request_context", "ctx.push", "full_dispatch_request",
                         "preprocess_request", "dispatch_request", "finalize_request",
                         "handle_exception", "handle_user_exception", "ctx.pop"],
        "gold_facts": [
            "impacts context creation",
            "impacts dispatch chain",
            "impacts before_request hooks",
            "impacts view function invocation",
            "impacts after_request hooks",
            "impacts exception handling",
            "finally block ensures teardown",
        ],
        "source_files": ["src/flask/app.py"],
    },
    {
        "task_id": "httpx-tf2-001",
        "family": "TF2",
        "repo": "httpx",
        "question": "Impact of modifying httpx transport layer?",
        "gold_answer": (
            "The transport layer sits between Client and httpcore connection pool. "
            "Client.request() calls send() which calls _send_single_request(). "
            "This gets the transport via _transport_for_url(url) and calls "
            "transport.handle_request(request). The default transport wraps httpcore: "
            "self._pool.handle_request(req). Modifying transport affects: "
            "socket pooling, SSL/TLS negotiation, proxy handling, HTTP/1.1 vs HTTP/2, "
            "connection limits (max_connections, max_keepalive_connections), "
            "all retries and timeouts, and exception mapping."
        ),
        "gold_symbols": ["Client.request", "send", "_send_single_request",
                         "_transport_for_url", "handle_request", "_pool"],
        "gold_facts": [
            "transport between Client and httpcore",
            "handle_request is the key method",
            "wraps httpcore pool",
            "affects connection pooling",
            "affects SSL/TLS",
            "affects timeouts and retries",
        ],
        "source_files": ["httpx/_client.py", "httpx/_transports/default.py"],
    },
    # TF3: Edit Localization (Flask, FastAPI)
    {
        "task_id": "flask-tf3-001",
        "family": "TF3",
        "repo": "flask",
        "question": "Where should the edit be made to add a new request hook?",
        "gold_answer": (
            "Hook registration is in sansio/scaffold.py: before_request at line 460, "
            "after_request at line 487, teardown_request at line 508. "
            "To add a NEW hook type: (1) add a dict in scaffold.py __init__ like "
            "self.my_hook_funcs, (2) add a decorator method using setdefault/append pattern, "
            "(3) call it in the dispatch chain in app.py at the right moment "
            "(between preprocess and dispatch for pre-hooks, in finalize_request for post-hooks). "
            "Hook execution order: before_request → dispatch → after_request (reversed order) → "
            "teardown_request (reversed order)."
        ),
        "gold_symbols": ["before_request", "after_request", "teardown_request",
                         "teardown_appcontext", "scaffold.py"],
        "gold_facts": [
            "registration in sansio/scaffold.py",
            "before_request runs before dispatch",
            "after_request runs after view returns",
            "teardown runs regardless of exception",
            "hooks run in reverse registration order",
        ],
        "source_files": ["src/flask/sansio/scaffold.py", "src/flask/app.py"],
    },
    {
        "task_id": "fastapi-tf3-001",
        "family": "TF3",
        "repo": "fastapi",
        "question": "Where to edit to add middleware in FastAPI?",
        "gold_answer": (
            "Middleware is added via app.add_middleware(MiddlewareClass, **options). "
            "Internally stored in self.user_middleware list. "
            "build_middleware_stack() in applications.py reverses the middleware list and wraps "
            "the app stack: each middleware wraps the previous as cls(app, *args, **kwargs). "
            "All middleware is pre-composed at startup. Changes require reinitializing "
            "build_middleware_stack(). To add: instantiate Middleware class from Starlette "
            "and append to user_middleware."
        ),
        "gold_symbols": ["add_middleware", "user_middleware", "build_middleware_stack", "Middleware"],
        "gold_facts": [
            "add_middleware is the API",
            "stored in user_middleware list",
            "build_middleware_stack composes at startup",
            "middleware wraps previous handler",
            "order matters",
        ],
        "source_files": ["fastapi/applications.py"],
    },
    # TF4: Behavior/Gotchas (Flask, NestJS)
    {
        "task_id": "flask-tf4-001",
        "family": "TF4",
        "repo": "flask",
        "question": "What behavioral gotcha exists in Flask's request dispatch path?",
        "gold_answer": (
            "Key gotchas: (1) Exception in finalize_request during error handling is silently "
            "logged, not re-raised — can hide bugs. (2) before_request returning non-None "
            "short-circuits dispatch entirely — view never called. (3) after_request runs "
            "in reverse registration order. (4) teardown runs in finally block — always executes "
            "even on exception, but teardown itself must not raise. (5) Debug mode with "
            "PROPAGATE_EXCEPTIONS re-raises unhandled errors, can crash the server. "
            "(6) Session only saves if modified OR (permanent AND SESSION_REFRESH_EACH_REQUEST)."
        ),
        "gold_symbols": ["finalize_request", "before_request", "after_request",
                         "teardown_request", "PROPAGATE_EXCEPTIONS"],
        "gold_facts": [
            "exception in finalize_request silently logged",
            "before_request can short-circuit",
            "reverse order of hook execution",
            "teardown runs in finally block",
            "debug mode re-raises exceptions",
            "session save conditional on modification",
        ],
        "source_files": ["src/flask/app.py", "src/flask/sessions.py"],
    },
    {
        "task_id": "nest-tf4-001",
        "family": "TF4",
        "repo": "nest",
        "question": "Behavioral gotchas in NestJS middleware pipeline?",
        "gold_answer": (
            "Gotchas: (1) resolveInstances is async — middleware must be fully initialized "
            "before routing begins. (2) exclude() removes routes AFTER forRoutes() — call "
            "order matters. (3) Middleware applies only to specified routes/controllers, "
            "not globally by default. (4) Middleware dependencies must be resolvable in current "
            "module scope via DI. (5) No built-in early exit mechanism unlike Gin's Abort()."
        ),
        "gold_symbols": ["resolveInstances", "apply", "forRoutes", "exclude",
                         "MiddlewareBuilder", "MiddlewareResolver"],
        "gold_facts": [
            "async initialization",
            "exclude order matters",
            "route-specific application",
            "dependency injection scope",
            "no early exit mechanism",
        ],
        "source_files": ["packages/core/middleware/resolver.ts", "packages/core/middleware/builder.ts"],
    },
    # TF5: Security (Flask, Gin)
    {
        "task_id": "flask-tf5-001",
        "family": "TF5",
        "repo": "flask",
        "question": "What security concerns exist in Flask's session handling?",
        "gold_answer": (
            "Security concerns: (1) No secret_key = NullSession, writes silently fail. "
            "(2) Sessions signed with HMAC-SHA1 by default (digest_method = sha1). "
            "(3) BadSignature on tampered cookies returns empty session, doesn't reject request. "
            "(4) Cookie flags default to httponly=False, secure=False — XSS/CSRF risk. "
            "(5) Nested dict mutations not tracked — changes silently lost unless "
            "session.modified=True set manually. (6) Vary: Cookie only set if session accessed."
        ),
        "gold_symbols": ["SecureCookieSessionInterface", "NullSession", "get_signing_serializer",
                         "should_set_cookie", "BadSignature"],
        "gold_facts": [
            "no secret_key causes NullSession",
            "HMAC-SHA1 default",
            "tampered cookies return empty session",
            "cookie flags default insecure",
            "nested mutations not tracked",
        ],
        "source_files": ["src/flask/sessions.py"],
    },
    {
        "task_id": "gin-tf5-001",
        "family": "TF5",
        "repo": "gin",
        "question": "Security in Gin middleware chain?",
        "gold_answer": (
            "Security concerns: (1) BasicAuth uses subtle.ConstantTimeCompare (SAFE against timing). "
            "(2) c.Abort() sets index to abortIndex preventing remaining handlers, but does NOT "
            "stop the current handler — code after Abort() still executes. "
            "(3) Middleware order matters — global Use() on Engine applies to ALL routes including "
            "404/405 handlers. (4) Group middleware may execute before/after global middleware "
            "depending on route matching. (5) No built-in RBAC — auth must be manually checked."
        ),
        "gold_symbols": ["ServeHTTP", "handleHTTPRequest", "Next", "Abort",
                         "BasicAuth", "ConstantTimeCompare"],
        "gold_facts": [
            "BasicAuth uses constant-time comparison",
            "Abort doesn't stop current handler",
            "middleware order matters",
            "global middleware on all routes including errors",
            "no built-in RBAC",
        ],
        "source_files": ["gin.go", "context.go", "auth.go"],
    },
]


def _build_raw_source_prompt(task: dict, repo_root: Path) -> str:
    """Build an Arm A (raw-source) prompt for comparison."""
    question = task["question"]
    source_files = task["source_files"]
    repo = task["repo"]

    parts = [
        "You are a senior software engineer answering a code comprehension question.",
        "You will receive the RAW SOURCE CODE of relevant files.",
        "",
        "## Instructions",
        "1. Read the source code carefully.",
        "2. Answer the question based on what you see in the code.",
        "3. Cite specific function names, line numbers, and call chains.",
        "4. Structure your answer clearly.",
        "",
        f"## Task Question",
        f"{question}",
        "",
        "## Source Code",
    ]

    for sf in source_files:
        full_path = repo_root / sf
        if full_path.is_file():
            source = full_path.read_text(encoding="utf-8", errors="replace")
            # Truncate very large files to first 500 lines
            lines = source.splitlines()
            if len(lines) > 500:
                source = "\n".join(lines[:500]) + f"\n\n... [{len(lines) - 500} more lines truncated]"
            parts.append(f"\n### {sf}\n```\n{source}\n```")
        else:
            parts.append(f"\n### {sf}\n[File not found at {full_path}]")

    parts.extend([
        "",
        "## Required Answer Format",
        "- **Answer**: Your response (2-5 sentences)",
        "- **Key symbols**: Functions/classes most relevant",
        "- **Evidence**: Specific line numbers and call chains",
        "- **Confidence**: high/medium/low",
    ])

    return "\n".join(parts)


def main() -> None:
    out_dir = ROOT / "experiments" / "runs" / "ground-truth-validation"
    prompts_dir = out_dir / "prompts"
    gold_dir = out_dir / "gold"
    external_repos = ROOT / "experiments" / "external-repos"
    clue_prompts_dir = ROOT / "experiments" / "runs" / "consumer-prompts"

    out_dir.mkdir(parents=True, exist_ok=True)
    prompts_dir.mkdir(parents=True, exist_ok=True)
    gold_dir.mkdir(parents=True, exist_ok=True)

    manifest: list[dict] = []

    for task in VALIDATION_TASKS:
        task_id = task["task_id"]
        repo = task["repo"]
        family = task["family"]
        question = task["question"]
        repo_root = external_repos / repo

        print(f"  {task_id} ({family})")

        # Save gold answer
        gold_path = gold_dir / f"{task_id}.gold.json"
        gold_data = {
            "task_id": task_id,
            "family": family,
            "question": question,
            "gold_answer": task["gold_answer"],
            "gold_symbols": task["gold_symbols"],
            "gold_facts": task["gold_facts"],
        }
        with open(gold_path, "w", encoding="utf-8") as f:
            json.dump(gold_data, f, indent=2)

        # Generate raw-source (Arm A) prompt
        raw_prompt = _build_raw_source_prompt(task, repo_root)
        raw_fname = f"{task_id}_arm-a-raw.prompt.md"
        (prompts_dir / raw_fname).write_text(raw_prompt, encoding="utf-8")

        # Check if clue (Arm B) prompt exists
        clue_prompt_file = clue_prompts_dir / f"{task_id}_plan-a.prompt.md"
        clue_exists = clue_prompt_file.is_file()

        # Check if clue response exists
        clue_response_file = clue_prompts_dir / f"{task_id}_plan-a.response.md"
        clue_response_exists = clue_response_file.is_file()

        manifest.append({
            "task_id": task_id,
            "family": family,
            "question": question,
            "gold_file": f"gold/{task_id}.gold.json",
            "arm_a_prompt": f"prompts/{raw_fname}",
            "arm_a_response": f"prompts/{raw_fname.replace('.prompt.md', '.response.md')}",
            "arm_b_prompt_exists": clue_exists,
            "arm_b_response_exists": clue_response_exists,
            "raw_prompt_tokens": count_tokens(raw_prompt),
        })

    # Save manifest
    manifest_path = out_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nGenerated {len(VALIDATION_TASKS)} validation tasks:")
    print(f"  Gold answers: {gold_dir}")
    print(f"  Arm A (raw) prompts: {prompts_dir}")
    print(f"  Manifest: {manifest_path}")
    print()
    print("=== WORKFLOW ===")
    print("1. For each Arm A prompt, paste into GPT/Gemini/Claude, save as .response.md")
    print("2. (Arm B responses may already exist from earlier run)")
    print("3. Run: python experiments/runs/score_ground_truth.py")
    print()

    # Summary table
    for entry in manifest:
        arm_b_status = "✓" if entry["arm_b_response_exists"] else "NEEDED"
        print(f"  {entry['task_id']} ({entry['family']}): raw={entry['raw_prompt_tokens']}t, arm_b={arm_b_status}")


if __name__ == "__main__":
    main()
