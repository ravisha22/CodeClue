You are a senior software engineer performing a development task.
You have access to a CodeClue artifact — a compact comprehension file
that describes the relevant code subsystem. Use it to plan your approach.

## Task
Add a new 'after_dispatch' hook that runs after the view function returns but before after_request hooks. Specify the exact file and insertion point.

## CodeClue Artifact
```json
{
  "task": {
    "id": "trace-OF3-20260403093041",
    "repo": "",
    "family": "OF3",
    "question": "Add a new 'after_dispatch' hook that runs after the view function returns but before after_request hooks. Specify the exact file and insertion point."
  },
  "summary": "__call__: Function __call__. __init__: Middleware between __init__ and __init__. __init_subclass__: Function __init_subclass__.",
  "entities": [
    {
      "id": "n1",
      "class": "utility",
      "name": "__call__",
      "file": "src/flask/app.py",
      "lines": [
        1618,
        1625
      ],
      "confidence": 0.77,
      "purpose": "function __call__",
      "behavior": "Function __call__.",
      "sig": "def __call__( self, environ: WSGIEnvironment, start_response: StartResponse ) -> cabc.Iterable[bytes]:",
      "calls": [
        "wsgi_app"
      ]
    },
    {
      "id": "n2",
      "class": "middleware",
      "name": "__init__",
      "file": "src/flask/app.py",
      "lines": [
        310,
        363
      ],
      "confidence": 0.77,
      "purpose": "function __init__",
      "behavior": "Middleware between __init__ and __init__.",
      "sig": "def __init__( self, import_name: str, static_url_path: str | None = None, static_folder: str | os.PathLike[str] | None = \"static\", static_host: str | None = None, host_matching: bool = False, subdo...",
      "calls": [
        "n2",
        "send_static_file"
      ],
      "called_by": [
        "n2"
      ]
    },
    {
      "id": "n3",
      "class": "utility",
      "name": "__init_subclass__",
      "file": "src/flask/app.py",
      "lines": [
        254,
        308
      ],
      "confidence": 0.77,
      "purpose": "function __init_subclass__",
      "behavior": "Function __init_subclass__.",
      "sig": "def __init_subclass__(cls, **kwargs: t.Any) -> None:",
      "calls": [
        "add_ctx",
        "remove_ctx"
      ]
    },
    {
      "id": "n4",
      "class": "utility",
      "name": "app_context",
      "file": "src/flask/app.py",
      "lines": [
        1481,
        1499
      ],
      "confidence": 0.77,
      "purpose": "function app_context",
      "behavior": "Function app_context.",
      "sig": "def app_context(self) -> AppContext:"
    },
    {
      "id": "n5",
      "class": "handler",
      "name": "async_to_sync",
      "file": "src/flask/app.py",
      "lines": [
        1079,
        1100
      ],
      "confidence": 0.77,
      "purpose": "function async_to_sync",
      "behavior": "Async Leaf handler invoked by ensure_sync.",
      "sig": "def async_to_sync( self, func: t.Callable[..., t.Coroutine[t.Any, t.Any, t.Any]] ) -> t.Callable[..., t.Any]:",
      "called_by": [
        "n11"
      ]
    },
    {
      "id": "n6",
      "class": "utility",
      "name": "create_jinja_environment",
      "file": "src/flask/app.py",
      "lines": [
        469,
        507
      ],
      "confidence": 0.77,
      "purpose": "function create_jinja_environment",
      "behavior": "Function create_jinja_environment.",
      "sig": "def create_jinja_environment(self) -> Environment:"
    },
    {
      "id": "n7",
      "class": "utility",
      "name": "create_url_adapter",
      "file": "src/flask/app.py",
      "lines": [
        509,
        560
      ],
      "confidence": 0.77,
      "purpose": "function create_url_adapter",
      "behavior": "Function create_url_adapter.",
      "sig": "def create_url_adapter(self, request: Request | None) -> MapAdapter | None:",
      "called_by": [
        "url_for"
      ]
    },
    {
      "id": "n8",
      "class": "middleware",
      "name": "dispatch_request",
      "file": "src/flask/app.py",
      "lines": [
        966,
        990
      ],
      "confidence": 0.57,
      "purpose": "function dispatch_request",
      "behavior": "Middleware between full_dispatch_request and ensure_sync.",
      "sig": "def dispatch_request(self, ctx: AppContext) -> ft.ResponseReturnValue:",
      "calls": [
        "n11",
        "make_default_options_response",
        "raise_routing_exception"
      ],
      "called_by": [
        "n13"
      ]
    },
    {
      "id": "n9",
      "class": "entrypoint",
      "name": "do_teardown_appcontext",
      "file": "src/flask/app.py",
      "lines": [
        1453,
        1479
      ],
      "confidence": 0.77,
      "purpose": "function do_teardown_appcontext",
      "behavior": "Entrypoint that delegates to ensure_sync.",
      "sig": "def do_teardown_appcontext( self, ctx: AppContext, exc: BaseException | None = None ) -> None:",
      "calls": [
        "n11"
      ]
    },
    {
      "id": "n10",
      "class": "entrypoint",
      "name": "do_teardown_request",
      "file": "src/flask/app.py",
      "lines": [
        1420,
        1451
      ],
      "confidence": 0.77,
      "purpose": "function do_teardown_request",
      "behavior": "Entrypoint that delegates to ensure_sync.",
      "sig": "def do_teardown_request( self, ctx: AppContext, exc: BaseException | None = None ) -> None:",
      "calls": [
        "n11"
      ]
    },
    {
      "id": "n11",
      "class": "utility",
      "name": "ensure_sync",
      "file": "src/flask/app.py",
      "lines": [
        1065,
        1077
      ],
      "confidence": 0.77,
      "purpose": "function ensure_sync",
      "behavior": "Function ensure_sync.",
      "sig": "def ensure_sync(self, func: t.Callable[..., t.Any]) -> t.Callable[..., t.Any]:",
      "calls": [
        "n5"
      ],
      "called_by": [
        "n8",
        "n9",
        "n10",
        "n15",
        "handle_http_exception",
        "handle_user_exception",
        "preprocess_request",
        "process_response",
        "update_template_context"
      ]
    },
    {
      "id": "n12",
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
        "n13",
        "n15"
      ],
      "risks": [
        "broad_exception_handler"
      ]
    },
    {
      "id": "n13",
      "class": "error_handler",
      "name": "full_dispatch_request",
      "file": "src/flask/app.py",
      "lines": [
        992,
        1019
      ],
      "confidence": 0.57,
      "purpose": "function full_dispatch_request",
      "behavior": "Error handler; produces dispatch_request, finalize_request; catches broad exceptions; mutates state outside __init__.",
      "sig": "def full_dispatch_request(self, ctx: AppContext) -> Response:",
      "calls": [
        "n8",
        "n12",
        "handle_user_exception",
        "preprocess_request"
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
      "id": "n14",
      "class": "utility",
      "name": "get_send_file_max_age",
      "file": "src/flask/app.py",
      "lines": [
        365,
        390
      ],
      "confidence": 0.77,
      "purpose": "function get_send_file_max_age",
      "behavior": "Function get_send_file_max_age.",
      "sig": "def get_send_file_max_age(self, filename: str | None) -> int | None:",
      "called_by": [
        "send_static_file"
      ]
    },
    {
      "id": "n15",
      "class": "error_handler",
      "name": "handle_exception",
      "file": "src/flask/app.py",
      "lines": [
        897,
        948
      ],
      "confidence": 0.57,
      "purpose": "function handle_exception",
      "behavior": "Error handler; produces ensure_sync, finalize_request.",
      "sig": "def handle_exception(self, ctx: AppContext, e: Exception) -> Response:",
      "calls": [
        "n11",
        "n12",
        "log_exception"
      ],
      "called_by": [
        "wsgi_app"
      ]
    }
  ],
  "uncertainty": {
    "confidence": 0.9,
    "hint": "clue_only",
    "gaps": [
      "Low confidence on dispatch_request (0.57)",
      "Low confidence on full_dispatch_request (0.57)",
      "Low confidence on handle_exception (0.57)"
    ]
  }
}
```

## Required Output
- List every file that must be modified
- List every function/class that is involved (cite entity IDs)
- Explain the execution/impact path based on the clue
- Identify what additional source you would need via drill-down