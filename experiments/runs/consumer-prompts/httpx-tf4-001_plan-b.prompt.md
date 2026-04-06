# Plan B: Flat-Table Consumer Prompt

You are a senior software engineer answering a code comprehension question.
You will receive a **compact clue artifact** with separate node, relation, and assertion tables.

## Instructions
1. Read the task question carefully.
2. Use ONLY the information in the clue artifact to answer.
3. Cite node IDs (n1, n2, etc.) as evidence for your claims.
4. Cross-reference the relations and assertions tables for behavioral context.
5. Do NOT speculate about code not described in the clue.
6. Structure your answer clearly.

## Task Question
Gotchas in httpx connection pooling?

## Clue Artifact (Flat-Table)
```json
{
  "task": {
    "id": "trace-OF4-20260403094649",
    "repo": "",
    "family": "OF4",
    "operation_family": "OF4",
    "question": "Gotchas in httpx connection pooling?"
  },
  "clue_summary": {
    "system_behavior": [
      "__aenter__: Async Middleware between __aenter__, __aenter__ and __aenter__, __aenter__; mutates state outside __init__.",
      "__aexit__: Async Middleware between __aexit__, __aexit__ and __aexit__, __aexit__; mutates state outside __init__.",
      "__init__: Function __init__.",
      "_init_proxy_transport: Function _init_proxy_transport.",
      "_init_transport: Function _init_transport."
    ],
    "key_files": [
      "httpx/_client.py"
    ],
    "key_symbols": [
      "__aenter__",
      "__aexit__",
      "__init__",
      "_init_proxy_transport",
      "_init_transport"
    ],
    "risk_summary": "Detected risks: state_mutation_outside_init, broad_exception_handler, runs_in_finally."
  },
  "nodes": [
    {
      "id": "n1",
      "type": "async_function",
      "name": "__aenter__",
      "summary": "Async Middleware between __aenter__, __aenter__ and __aenter__, __aenter__; mutates state outside __init__.",
      "file": "httpx/_client.py",
      "lines": [
        1990,
        2006
      ],
      "importance": 1,
      "role": "middleware",
      "sig": "async def __aenter__(self: U) -> U:",
      "risks": [
        "state_mutation_outside_init"
      ]
    },
    {
      "id": "n2",
      "type": "async_function",
      "name": "__aexit__",
      "summary": "Async Middleware between __aexit__, __aexit__ and __aexit__, __aexit__; mutates state outside __init__.",
      "file": "httpx/_client.py",
      "lines": [
        2008,
        2019
      ],
      "importance": 2,
      "role": "middleware",
      "sig": "async def __aexit__( self, exc_type: type[BaseException] | None = None, exc_value: BaseException | None = None, traceback: TracebackType | None = None, ) -> None:",
      "risks": [
        "state_mutation_outside_init"
      ]
    },
    {
      "id": "n3",
      "type": "function",
      "name": "__init__",
      "summary": "Function __init__.",
      "file": "httpx/_client.py",
      "lines": [
        1353,
        1430
      ],
      "importance": 3,
      "role": "utility"
    },
    {
      "id": "n4",
      "type": "function",
      "name": "_init_proxy_transport",
      "summary": "Function _init_proxy_transport.",
      "file": "httpx/_client.py",
      "lines": [
        1454,
        1472
      ],
      "importance": 4,
      "role": "utility",
      "sig": "def _init_proxy_transport( self, proxy: Proxy, verify: ssl.SSLContext | str | bool = True, cert: CertTypes | None = None, trust_env: bool = True, http1: bool = True, http2: bool = False, limits: Li..."
    },
    {
      "id": "n5",
      "type": "function",
      "name": "_init_transport",
      "summary": "Function _init_transport.",
      "file": "httpx/_client.py",
      "lines": [
        1432,
        1452
      ],
      "importance": 5,
      "role": "utility",
      "sig": "def _init_transport( self, verify: ssl.SSLContext | str | bool = True, cert: CertTypes | None = None, trust_env: bool = True, http1: bool = True, http2: bool = False, limits: Limits = DEFAULT_LIMIT..."
    },
    {
      "id": "n6",
      "type": "async_function",
      "name": "_send_handling_auth",
      "summary": "Async Error handler; produces error response; catches broad exceptions; runs in finally block.",
      "file": "httpx/_client.py",
      "lines": [
        1645,
        1677
      ],
      "importance": 6,
      "role": "error_handler",
      "sig": "async def _send_handling_auth( self, request: Request, auth: Auth, follow_redirects: bool, history: list[Response], ) -> Response:",
      "risks": [
        "broad_exception_handler",
        "runs_in_finally"
      ]
    },
    {
      "id": "n7",
      "type": "async_function",
      "name": "_send_handling_redirects",
      "summary": "Async Error handler; produces error response; catches broad exceptions.",
      "file": "httpx/_client.py",
      "lines": [
        1679,
        1715
      ],
      "importance": 7,
      "role": "error_handler",
      "sig": "async def _send_handling_redirects( self, request: Request, follow_redirects: bool, history: list[Response], ) -> Response:",
      "risks": [
        "broad_exception_handler"
      ]
    },
    {
      "id": "n8",
      "type": "async_function",
      "name": "_send_single_request",
      "summary": "Async Async_function _send_single_request.",
      "file": "httpx/_client.py",
      "lines": [
        1717,
        1749
      ],
      "importance": 8,
      "role": "utility",
      "sig": "async def _send_single_request(self, request: Request) -> Response:"
    },
    {
      "id": "n9",
      "type": "function",
      "name": "_transport_for_url",
      "summary": "Async Function _transport_for_url.",
      "file": "httpx/_client.py",
      "lines": [
        1474,
        1483
      ],
      "importance": 9,
      "role": "utility",
      "sig": "def _transport_for_url(self, url: URL) -> AsyncBaseTransport:"
    },
    {
      "id": "n10",
      "type": "async_function",
      "name": "aclose",
      "summary": "Async Async_function aclose; mutates state outside __init__.",
      "file": "httpx/_client.py",
      "lines": [
        1978,
        1988
      ],
      "importance": 10,
      "role": "utility",
      "sig": "async def aclose(self) -> None:",
      "risks": [
        "state_mutation_outside_init"
      ]
    },
    {
      "id": "n11",
      "type": "async_function",
      "name": "delete",
      "summary": "Async Accesses data store.",
      "file": "httpx/_client.py",
      "lines": [
        1949,
        1976
      ],
      "importance": 11,
      "role": "data_accessor",
      "sig": "async def delete( self, url: URL | str, *, params: QueryParamTypes | None = None, headers: HeaderTypes | None = None, cookies: CookieTypes | None = None, auth: AuthTypes | UseClientDefault = USE_CL..."
    },
    {
      "id": "n12",
      "type": "async_function",
      "name": "get",
      "summary": "Async Async_function get.",
      "file": "httpx/_client.py",
      "lines": [
        1751,
        1778
      ],
      "importance": 12,
      "role": "utility",
      "sig": "async def get( self, url: URL | str, *, params: QueryParamTypes | None = None, headers: HeaderTypes | None = None, cookies: CookieTypes | None = None, auth: AuthTypes | UseClientDefault | None = US..."
    },
    {
      "id": "n13",
      "type": "async_function",
      "name": "head",
      "summary": "Async Async_function head.",
      "file": "httpx/_client.py",
      "lines": [
        1809,
        1836
      ],
      "importance": 13,
      "role": "utility",
      "sig": "async def head( self, url: URL | str, *, params: QueryParamTypes | None = None, headers: HeaderTypes | None = None, cookies: CookieTypes | None = None, auth: AuthTypes | UseClientDefault = USE_CLIE..."
    },
    {
      "id": "n14",
      "type": "async_function",
      "name": "options",
      "summary": "Async Async_function options.",
      "file": "httpx/_client.py",
      "lines": [
        1780,
        1807
      ],
      "importance": 14,
      "role": "utility",
      "sig": "async def options( self, url: URL | str, *, params: QueryParamTypes | None = None, headers: HeaderTypes | None = None, cookies: CookieTypes | None = None, auth: AuthTypes | UseClientDefault = USE_C..."
    },
    {
      "id": "n15",
      "type": "async_function",
      "name": "patch",
      "summary": "Async Async_function patch.",
      "file": "httpx/_client.py",
      "lines": [
        1912,
        1947
      ],
      "importance": 15,
      "role": "utility",
      "sig": "async def patch( self, url: URL | str, *, content: RequestContent | None = None, data: RequestData | None = None, files: RequestFiles | None = None, json: typing.Any | None = None, params: QueryPar..."
    }
  ],
  "relations": [
    {
      "type": "calls",
      "from": "n1",
      "to": "n1",
      "note": "__aenter__ calls __aenter__"
    },
    {
      "type": "calls",
      "from": "n1",
      "to": "n1",
      "note": "__aenter__ calls __aenter__"
    },
    {
      "type": "calls",
      "from": "n2",
      "to": "n2",
      "note": "__aexit__ calls __aexit__"
    },
    {
      "type": "calls",
      "from": "n2",
      "to": "n2",
      "note": "__aexit__ calls __aexit__"
    }
  ],
  "assertions": [
    {
      "path": [
        "n6"
      ],
      "fact": "_send_handling_auth catches broad exceptions; specific errors may be masked."
    },
    {
      "path": [
        "n7"
      ],
      "fact": "_send_handling_redirects catches broad exceptions; specific errors may be masked."
    },
    {
      "path": [
        "n1",
        "n1",
        "n1"
      ],
      "fact": "Call chain: __aenter__ → __aenter__ → __aenter__."
    },
    {
      "path": [
        "n2",
        "n2",
        "n2"
      ],
      "fact": "Call chain: __aexit__ → __aexit__ → __aexit__."
    }
  ],
  "uncertainty": {
    "overall_confidence": 0.93,
    "lookup_hint": "clue_only",
    "known_gaps": [
      "Low confidence on this node; source verification recommended",
      "Low confidence on this node; source verification recommended",
      "Low confidence on this node; source verification recommended"
    ]
  }
}
```

## Required Answer Format
Provide a structured answer with:
- **Answer**: Your response to the question (2-5 sentences)
- **Key nodes**: List the node IDs most relevant to your answer
- **Evidence**: Brief explanation of how nodes, relations, and assertions support your answer
- **Confidence**: How confident you are (high/medium/low) based on the clue alone
- **Gaps**: Any information you would need but is missing from the clue
