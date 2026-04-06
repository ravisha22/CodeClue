You are a senior software engineer performing a development task.
You have access to a CodeClue artifact — a compact comprehension file
that describes the relevant code subsystem. Use it to plan your approach.

## Task
Refactor Flask's request handling to support async middleware. List every file and function that must be modified.

## CodeClue Artifact
```json
{
  "task": {
    "id": "trace-OF1-20260403093030",
    "repo": "",
    "family": "OF1",
    "question": "Refactor Flask's request handling to support async middleware. List every file and function that must be modified."
  },
  "summary": "async_to_sync: Async Function async_to_sync. do_teardown_request: Function do_teardown_request. finalize_request: Error handler; produces error response; catches broad exceptions.",
  "entities": [
    {
      "id": "n1",
      "class": "utility",
      "name": "async_to_sync",
      "file": "src/flask/app.py",
      "lines": [
        1079,
        1100
      ],
      "confidence": 0.77,
      "purpose": "function async_to_sync",
      "behavior": "Async Function async_to_sync.",
      "sig": "def async_to_sync( self, func: t.Callable[..., t.Coroutine[t.Any, t.Any, t.Any]] ) -> t.Callable[..., t.Any]:",
      "called_by": [
        "ensure_sync"
      ]
    },
    {
      "id": "n2",
      "class": "handler",
      "name": "dispatch_request",
      "file": "src/flask/app.py",
      "lines": [
        966,
        990
      ],
      "confidence": 0.57,
      "purpose": "function dispatch_request",
      "behavior": "Leaf handler invoked by dispatcher.",
      "sig": "def dispatch_request(self, ctx: AppContext) -> ft.ResponseReturnValue:",
      "calls": [
        "ensure_sync",
        "make_default_options_response",
        "raise_routing_exception"
      ],
      "called_by": [
        "n5"
      ]
    },
    {
      "id": "n3",
      "class": "utility",
      "name": "do_teardown_request",
      "file": "src/flask/app.py",
      "lines": [
        1420,
        1451
      ],
      "confidence": 0.77,
      "purpose": "function do_teardown_request",
      "behavior": "Function do_teardown_request.",
      "sig": "def do_teardown_request( self, ctx: AppContext, exc: BaseException | None = None ) -> None:",
      "calls": [
        "ensure_sync"
      ]
    },
    {
      "id": "n4",
      "class": "error_handler",
      "name": "finalize_request",
      "file": "src/flask/app.py",
      "lines": [
        1021,
        1051
      ],
      "confidence": 0.77,
      "purpose": "function finalize_request",
      "behavior": "Error handler; produces error response; catches broad exceptions.",
      "sig": "def finalize_request( self, ctx: AppContext, rv: ft.ResponseReturnValue | HTTPException, from_error_handler: bool = False, ) -> Response:",
      "calls": [
        "make_response",
        "process_response"
      ],
      "called_by": [
        "n5",
        "handle_exception"
      ],
      "risks": [
        "broad_exception_handler"
      ]
    },
    {
      "id": "n5",
      "class": "error_handler",
      "name": "full_dispatch_request",
      "file": "src/flask/app.py",
      "lines": [
        992,
        1019
      ],
      "confidence": 0.57,
      "purpose": "function full_dispatch_request",
      "behavior": "Error handler; produces error response; catches broad exceptions; mutates state outside __init__.",
      "sig": "def full_dispatch_request(self, ctx: AppContext) -> Response:",
      "calls": [
        "n2",
        "n4",
        "handle_user_exception",
        "n7"
      ],
      "called_by": [
        "wsgi_app"
      ],
      "risks": [
        "broad_exception_handler",
        "state_mutation_outside_init"
      ]
    },
    {
      "id": "n6",
      "class": "handler",
      "name": "get_send_file_max_age",
      "file": "src/flask/app.py",
      "lines": [
        365,
        390
      ],
      "confidence": 0.77,
      "purpose": "function get_send_file_max_age",
      "behavior": "Leaf handler invoked by dispatcher.",
      "sig": "def get_send_file_max_age(self, filename: str | None) -> int | None:",
      "called_by": [
        "n9"
      ]
    },
    {
      "id": "n7",
      "class": "handler",
      "name": "preprocess_request",
      "file": "src/flask/app.py",
      "lines": [
        1366,
        1392
      ],
      "confidence": 0.77,
      "purpose": "function preprocess_request",
      "behavior": "Leaf handler invoked by dispatcher.",
      "sig": "def preprocess_request(self, ctx: AppContext) -> ft.ResponseReturnValue | None:",
      "calls": [
        "ensure_sync"
      ],
      "called_by": [
        "n5"
      ]
    },
    {
      "id": "n8",
      "class": "utility",
      "name": "request_context",
      "file": "src/flask/app.py",
      "lines": [
        1501,
        1515
      ],
      "confidence": 0.77,
      "purpose": "function request_context",
      "behavior": "Function request_context.",
      "sig": "def request_context(self, environ: WSGIEnvironment) -> AppContext:",
      "called_by": [
        "test_request_context",
        "wsgi_app"
      ]
    },
    {
      "id": "n9",
      "class": "entrypoint",
      "name": "send_static_file",
      "file": "src/flask/app.py",
      "lines": [
        392,
        412
      ],
      "confidence": 0.77,
      "purpose": "function send_static_file",
      "behavior": "Entrypoint that delegates to downstream handlers.",
      "sig": "def send_static_file(self, filename: str) -> Response:",
      "calls": [
        "n6"
      ],
      "called_by": [
        "__init__"
      ]
    },
    {
      "id": "n10",
      "class": "utility",
      "name": "has_request",
      "file": "src/flask/ctx.py",
      "lines": [
        351,
        353
      ],
      "confidence": 0.77,
      "purpose": "function has_request",
      "behavior": "Function has_request.",
      "sig": "def has_request(self) -> bool:"
    },
    {
      "id": "n11",
      "class": "utility",
      "name": "match_request",
      "file": "src/flask/ctx.py",
      "lines": [
        405,
        414
      ],
      "confidence": 0.77,
      "purpose": "function match_request",
      "behavior": "Function match_request.",
      "sig": "def match_request(self) -> None:",
      "called_by": [
        "push"
      ]
    },
    {
      "id": "n12",
      "class": "utility",
      "name": "request",
      "file": "src/flask/ctx.py",
      "lines": [
        371,
        379
      ],
      "confidence": 0.77,
      "purpose": "function request",
      "behavior": "Function request.",
      "sig": "def request(self) -> Request:"
    },
    {
      "id": "n13",
      "class": "utility",
      "name": "after_this_request",
      "file": "src/flask/ctx.py",
      "lines": [
        118,
        148
      ],
      "confidence": 0.77,
      "purpose": "function after_this_request",
      "behavior": "Function after_this_request.",
      "sig": "def after_this_request( f: ft.AfterRequestCallable[t.Any], ) -> ft.AfterRequestCallable[t.Any]:",
      "calls": [
        "get"
      ]
    },
    {
      "id": "n14",
      "class": "utility",
      "name": "copy_current_request_context",
      "file": "src/flask/ctx.py",
      "lines": [
        154,
        206
      ],
      "confidence": 0.77,
      "purpose": "function copy_current_request_context",
      "behavior": "Function copy_current_request_context.",
      "sig": "def copy_current_request_context(f: F) -> F:",
      "calls": [
        "copy",
        "get"
      ]
    },
    {
      "id": "n15",
      "class": "utility",
      "name": "has_request_context",
      "file": "src/flask/ctx.py",
      "lines": [
        209,
        232
      ],
      "confidence": 0.77,
      "purpose": "function has_request_context",
      "behavior": "Function has_request_context.",
      "sig": "def has_request_context() -> bool:",
      "calls": [
        "get"
      ]
    }
  ],
  "uncertainty": {
    "confidence": 0.95,
    "hint": "clue_only",
    "gaps": [
      "Low confidence on dispatch_request (0.57)",
      "Low confidence on full_dispatch_request (0.57)"
    ]
  }
}
```

## Required Output
- List every file that must be modified
- List every function/class that is involved (cite entity IDs)
- Explain the execution/impact path based on the clue
- Identify what additional source you would need via drill-down