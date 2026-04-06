# Plan A: Entity-Centric Consumer Prompt

You are a senior software engineer answering a code comprehension question.
You will receive a **compact clue artifact** describing a code subsystem as a set of typed entities.

## Instructions
1. Read the task question carefully.
2. Use ONLY the information in the clue artifact to answer.
3. Cite entity IDs (n1, n2, etc.) as evidence for your claims.
4. Do NOT speculate about code not described in the clue.
5. Structure your answer clearly.

## Task Question
Impact of modifying httpx transport layer?

## Clue Artifact (Entity-Centric)
```json
{
  "task": {
    "id": "trace-OF2-20260403094647",
    "repo": "",
    "family": "OF2",
    "operation_family": "OF2",
    "question": "Impact of modifying httpx transport layer?"
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
      "weight": 0.92,
      "behavior": "Async Middleware between __aenter__, __aenter__ and __aenter__, __aenter__; mutates state outside __init__.",
      "sig": "async def __aenter__(self: U) -> U:",
      "inflow": [
        {
          "from": "n1",
          "via": "calls",
          "condition": "normal"
        },
        {
          "from": "n1",
          "via": "calls",
          "condition": "normal"
        }
      ],
      "outflow": [
        {
          "to": "n1",
          "via": "calls",
          "condition": "normal"
        },
        {
          "to": "n1",
          "via": "calls",
          "condition": "normal"
        }
      ],
      "risks": [
        "state_mutation_outside_init"
      ],
      "invariants": [
        "Mutates instance state outside constructor."
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
      "weight": 0.86,
      "behavior": "Async Middleware between __aexit__, __aexit__ and __aexit__, __aexit__; mutates state outside __init__.",
      "sig": "async def __aexit__( self, exc_type: type[BaseException] | None = None, exc_value: BaseException | None = None, traceback: TracebackType | None = None, ) -> None:",
      "inflow": [
        {
          "from": "n2",
          "via": "calls",
          "condition": "normal"
        },
        {
          "from": "n2",
          "via": "calls",
          "condition": "normal"
        }
      ],
      "outflow": [
        {
          "to": "n2",
          "via": "calls",
          "condition": "normal"
        },
        {
          "to": "n2",
          "via": "calls",
          "condition": "normal"
        }
      ],
      "risks": [
        "state_mutation_outside_init"
      ],
      "invariants": [
        "Mutates instance state outside constructor."
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
      "weight": 0.8,
      "behavior": "Leaf handler invoked by _build_request_auth.",
      "sig": "def _build_auth(self, auth: AuthTypes | None) -> Auth | None:",
      "inflow": [
        {
          "from": "n5",
          "via": "calls",
          "condition": "normal"
        }
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
      "weight": 0.74,
      "behavior": "Entrypoint that delegates to _redirect_headers, _redirect_method, _redirect_stream.",
      "sig": "def _build_redirect_request(self, request: Request, response: Response) -> Request:",
      "outflow": [
        {
          "to": "n10",
          "via": "calls",
          "condition": "normal"
        },
        {
          "to": "n11",
          "via": "calls",
          "condition": "normal"
        },
        {
          "to": "n12",
          "via": "calls",
          "condition": "normal"
        },
        {
          "to": "n13",
          "via": "calls",
          "condition": "normal"
        }
      ],
      "invariants": [
        "Entry point; all request paths flow through here."
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
      "weight": 0.67,
      "behavior": "Entrypoint that delegates to _build_auth.",
      "sig": "def _build_request_auth( self, request: Request, auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT, ) -> Auth:",
      "outflow": [
        {
          "to": "n3",
          "via": "calls",
          "condition": "normal"
        }
      ],
      "invariants": [
        "Entry point; all request paths flow through here."
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
      "weight": 0.61,
      "behavior": "Leaf handler invoked by build_request.",
      "sig": "def _merge_cookies(self, cookies: CookieTypes | None = None) -> CookieTypes | None:",
      "inflow": [
        {
          "from": "n14",
          "via": "calls",
          "condition": "normal"
        }
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
      "weight": 0.55,
      "behavior": "Leaf handler invoked by build_request.",
      "sig": "def _merge_headers(self, headers: HeaderTypes | None = None) -> HeaderTypes | None:",
      "inflow": [
        {
          "from": "n14",
          "via": "calls",
          "condition": "normal"
        }
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
      "weight": 0.49,
      "behavior": "Leaf handler invoked by build_request.",
      "sig": "def _merge_queryparams( self, params: QueryParamTypes | None = None ) -> QueryParamTypes | None:",
      "inflow": [
        {
          "from": "n14",
          "via": "calls",
          "condition": "normal"
        }
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
      "weight": 0.43,
      "behavior": "Leaf handler invoked by build_request.",
      "sig": "def _merge_url(self, url: URL | str) -> URL:",
      "inflow": [
        {
          "from": "n14",
          "via": "calls",
          "condition": "normal"
        }
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
      "weight": 0.37,
      "behavior": "Leaf handler invoked by _build_redirect_request.",
      "sig": "def _redirect_headers(self, request: Request, url: URL, method: str) -> Headers:",
      "inflow": [
        {
          "from": "n4",
          "via": "calls",
          "condition": "normal"
        }
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
      "weight": 0.31,
      "behavior": "Leaf handler invoked by _build_redirect_request.",
      "sig": "def _redirect_method(self, request: Request, response: Response) -> str:",
      "inflow": [
        {
          "from": "n4",
          "via": "calls",
          "condition": "normal"
        }
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
      "weight": 0.25,
      "behavior": "Async Leaf handler invoked by _build_redirect_request.",
      "sig": "def _redirect_stream( self, request: Request, method: str ) -> SyncByteStream | AsyncByteStream | None:",
      "inflow": [
        {
          "from": "n4",
          "via": "calls",
          "condition": "normal"
        }
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
      "weight": 0.18,
      "behavior": "Leaf handler invoked by _build_redirect_request.",
      "sig": "def _redirect_url(self, request: Request, response: Response) -> URL:",
      "inflow": [
        {
          "from": "n4",
          "via": "calls",
          "condition": "normal"
        }
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
      "weight": 0.12,
      "behavior": "Entrypoint that delegates to _merge_cookies, _merge_headers, _merge_queryparams.",
      "sig": "def build_request( self, method: str, url: URL | str, *, content: RequestContent | None = None, data: RequestData | None = None, files: RequestFiles | None = None, json: typing.Any | None = None, p...",
      "outflow": [
        {
          "to": "n6",
          "via": "calls",
          "condition": "normal"
        },
        {
          "to": "n7",
          "via": "calls",
          "condition": "normal"
        },
        {
          "to": "n8",
          "via": "calls",
          "condition": "normal"
        },
        {
          "to": "n9",
          "via": "calls",
          "condition": "normal"
        }
      ],
      "invariants": [
        "Entry point; all request paths flow through here."
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
      "weight": 0.06,
      "behavior": "Middleware between __enter__, __enter__ and __enter__, __enter__; mutates state outside __init__.",
      "sig": "def __enter__(self: T) -> T:",
      "inflow": [
        {
          "from": "n15",
          "via": "calls",
          "condition": "normal"
        },
        {
          "from": "n15",
          "via": "calls",
          "condition": "normal"
        }
      ],
      "outflow": [
        {
          "to": "n15",
          "via": "calls",
          "condition": "normal"
        },
        {
          "to": "n15",
          "via": "calls",
          "condition": "normal"
        }
      ],
      "risks": [
        "state_mutation_outside_init"
      ],
      "invariants": [
        "Mutates instance state outside constructor."
      ]
    }
  ],
  "uncertainty": {
    "confidence": 0.08,
    "hint": "expanded_lookup",
    "gaps": [
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
- **Key entities**: List the entity IDs most relevant to your answer
- **Evidence**: Brief explanation of how the clue entities support your answer
- **Confidence**: How confident you are (high/medium/low) based on the clue alone
- **Gaps**: Any information you would need but is missing from the clue
