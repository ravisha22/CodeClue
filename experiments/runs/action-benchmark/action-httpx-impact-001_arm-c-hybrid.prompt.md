You are a senior software engineer performing a development task.
You have access to a CodeClue artifact — a compact comprehension file
that describes the relevant code subsystem. Use it to plan your approach.

## Task
We need to add HTTP/3 support to httpx. Identify every component in the transport layer that would need modification.

## CodeClue Artifact
```json
{
  "task": {
    "id": "trace-OF2-20260403094647",
    "repo": "",
    "family": "OF2",
    "question": "We need to add HTTP/3 support to httpx. Identify every component in the transport layer that would need modification."
  },
  "summary": "__aenter__: Async Middleware between __aenter__, __aenter__ and __aenter__, __aenter__; mutates state outside __init__. __aexit__: Async Middleware between __aexit__, __aexit__ and __aexit__, __aexit__; mutates state outside __init__. _build_auth: Leaf handler invoked by _build_request_auth.",
  "entities": [
    {
      "id": "n1",
      "class": "middleware",
      "name": "__aenter__",
      "file": "httpx/_client.py",
      "lines": [
        1990,
        2006
      ],
      "confidence": 0.77,
      "purpose": "async_function __aenter__",
      "behavior": "Async Middleware between __aenter__, __aenter__ and __aenter__, __aenter__; mutates state outside __init__.",
      "sig": "async def __aenter__(self: U) -> U:",
      "calls": [
        "n1"
      ],
      "called_by": [
        "n1"
      ],
      "risks": [
        "state_mutation_outside_init"
      ]
    },
    {
      "id": "n2",
      "class": "middleware",
      "name": "__aexit__",
      "file": "httpx/_client.py",
      "lines": [
        2008,
        2019
      ],
      "confidence": 0.77,
      "purpose": "async_function __aexit__",
      "behavior": "Async Middleware between __aexit__, __aexit__ and __aexit__, __aexit__; mutates state outside __init__.",
      "sig": "async def __aexit__( self, exc_type: type[BaseException] | None = None, exc_value: BaseException | None = None, traceback: TracebackType | None = None, ) -> None:",
      "calls": [
        "n2"
      ],
      "called_by": [
        "n2"
      ],
      "risks": [
        "state_mutation_outside_init"
      ]
    },
    {
      "id": "n3",
      "class": "handler",
      "name": "_build_auth",
      "file": "httpx/_client.py",
      "lines": [
        445,
        455
      ],
      "confidence": 0.77,
      "purpose": "function _build_auth",
      "behavior": "Leaf handler invoked by _build_request_auth.",
      "sig": "def _build_auth(self, auth: AuthTypes | None) -> Auth | None:",
      "called_by": [
        "n5"
      ]
    },
    {
      "id": "n4",
      "class": "entrypoint",
      "name": "_build_redirect_request",
      "file": "httpx/_client.py",
      "lines": [
        475,
        492
      ],
      "confidence": 0.57,
      "purpose": "function _build_redirect_request",
      "behavior": "Entrypoint that delegates to _redirect_headers, _redirect_method, _redirect_stream.",
      "sig": "def _build_redirect_request(self, request: Request, response: Response) -> Request:",
      "calls": [
        "n10",
        "n11",
        "n12",
        "n13"
      ]
    },
    {
      "id": "n5",
      "class": "entrypoint",
      "name": "_build_request_auth",
      "file": "httpx/_client.py",
      "lines": [
        457,
        473
      ],
      "confidence": 0.77,
      "purpose": "function _build_request_auth",
      "behavior": "Entrypoint that delegates to _build_auth.",
      "sig": "def _build_request_auth( self, request: Request, auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT, ) -> Auth:",
      "calls": [
        "n3"
      ]
    },
    {
      "id": "n6",
      "class": "handler",
      "name": "_merge_cookies",
      "file": "httpx/_client.py",
      "lines": [
        413,
        422
      ],
      "confidence": 0.77,
      "purpose": "function _merge_cookies",
      "behavior": "Leaf handler invoked by build_request.",
      "sig": "def _merge_cookies(self, cookies: CookieTypes | None = None) -> CookieTypes | None:",
      "called_by": [
        "n14"
      ]
    },
    {
      "id": "n7",
      "class": "handler",
      "name": "_merge_headers",
      "file": "httpx/_client.py",
      "lines": [
        424,
        431
      ],
      "confidence": 0.77,
      "purpose": "function _merge_headers",
      "behavior": "Leaf handler invoked by build_request.",
      "sig": "def _merge_headers(self, headers: HeaderTypes | None = None) -> HeaderTypes | None:",
      "called_by": [
        "n14"
      ]
    },
    {
      "id": "n8",
      "class": "handler",
      "name": "_merge_queryparams",
      "file": "httpx/_client.py",
      "lines": [
        433,
        443
      ],
      "confidence": 0.77,
      "purpose": "function _merge_queryparams",
      "behavior": "Leaf handler invoked by build_request.",
      "sig": "def _merge_queryparams( self, params: QueryParamTypes | None = None ) -> QueryParamTypes | None:",
      "called_by": [
        "n14"
      ]
    },
    {
      "id": "n9",
      "class": "handler",
      "name": "_merge_url",
      "file": "httpx/_client.py",
      "lines": [
        391,
        411
      ],
      "confidence": 0.77,
      "purpose": "function _merge_url",
      "behavior": "Leaf handler invoked by build_request.",
      "sig": "def _merge_url(self, url: URL | str) -> URL:",
      "called_by": [
        "n14"
      ]
    },
    {
      "id": "n10",
      "class": "handler",
      "name": "_redirect_headers",
      "file": "httpx/_client.py",
      "lines": [
        546,
        571
      ],
      "confidence": 0.57,
      "purpose": "function _redirect_headers",
      "behavior": "Leaf handler invoked by _build_redirect_request.",
      "sig": "def _redirect_headers(self, request: Request, url: URL, method: str) -> Headers:",
      "calls": [
        "_is_https_redirect",
        "_same_origin"
      ],
      "called_by": [
        "n4"
      ]
    },
    {
      "id": "n11",
      "class": "handler",
      "name": "_redirect_method",
      "file": "httpx/_client.py",
      "lines": [
        494,
        515
      ],
      "confidence": 0.77,
      "purpose": "function _redirect_method",
      "behavior": "Leaf handler invoked by _build_redirect_request.",
      "sig": "def _redirect_method(self, request: Request, response: Response) -> str:",
      "called_by": [
        "n4"
      ]
    },
    {
      "id": "n12",
      "class": "handler",
      "name": "_redirect_stream",
      "file": "httpx/_client.py",
      "lines": [
        573,
        582
      ],
      "confidence": 0.77,
      "purpose": "function _redirect_stream",
      "behavior": "Async Leaf handler invoked by _build_redirect_request.",
      "sig": "def _redirect_stream( self, request: Request, method: str ) -> SyncByteStream | AsyncByteStream | None:",
      "called_by": [
        "n4"
      ]
    },
    {
      "id": "n13",
      "class": "handler",
      "name": "_redirect_url",
      "file": "httpx/_client.py",
      "lines": [
        517,
        544
      ],
      "confidence": 0.77,
      "purpose": "function _redirect_url",
      "behavior": "Leaf handler invoked by _build_redirect_request.",
      "sig": "def _redirect_url(self, request: Request, response: Response) -> URL:",
      "called_by": [
        "n4"
      ]
    },
    {
      "id": "n14",
      "class": "entrypoint",
      "name": "build_request",
      "file": "httpx/_client.py",
      "lines": [
        340,
        389
      ],
      "confidence": 0.57,
      "purpose": "function build_request",
      "behavior": "Entrypoint that delegates to _merge_cookies, _merge_headers, _merge_queryparams.",
      "sig": "def build_request( self, method: str, url: URL | str, *, content: RequestContent | None = None, data: RequestData | None = None, files: RequestFiles | None = None, json: typing.Any | None = None, p...",
      "calls": [
        "n6",
        "n7",
        "n8",
        "n9"
      ]
    },
    {
      "id": "n15",
      "class": "middleware",
      "name": "__enter__",
      "file": "httpx/_client.py",
      "lines": [
        1275,
        1291
      ],
      "confidence": 0.57,
      "purpose": "function __enter__",
      "behavior": "Middleware between __enter__, __enter__ and __enter__, __enter__; mutates state outside __init__.",
      "sig": "def __enter__(self: T) -> T:",
      "calls": [
        "n15"
      ],
      "called_by": [
        "n15"
      ],
      "risks": [
        "state_mutation_outside_init"
      ]
    }
  ],
  "uncertainty": {
    "confidence": 0.08,
    "hint": "expanded_lookup",
    "gaps": [
      "Low confidence on _build_redirect_request (0.57)",
      "Low confidence on _redirect_headers (0.57)",
      "Low confidence on build_request (0.57)"
    ]
  }
}
```

## Required Output
- List every file that must be modified
- List every function/class that is involved (cite entity IDs)
- Explain the execution/impact path based on the clue
- Identify what additional source you would need via drill-down