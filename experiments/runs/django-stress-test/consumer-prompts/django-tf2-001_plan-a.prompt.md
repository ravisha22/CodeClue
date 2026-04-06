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
What is the downstream impact of modifying Django's BaseHandler.get_response method?

## Clue Artifact (Entity-Centric)
```json
{
  "task": {
    "id": "trace-django-fast-OF2",
    "repo": "",
    "family": "OF2",
    "operation_family": "OF2",
    "question": "What is the downstream impact of modifying Django's BaseHandler.get_response method?"
  },
  "summary": "get_response_async: Async Leaf handler invoked by dispatcher. check_response: Validates input before processing; may return None implicitly. process_exception_by_middleware: Error handler; produces error response.",
  "entities": [
    {
      "id": "n1",
      "class": "handler",
      "name": "get_response_async",
      "file": "django/core/handlers/base.py",
      "lines": [
        154,
        174
      ],
      "weight": 0.92,
      "behavior": "Async Leaf handler invoked by dispatcher.",
      "sig": "async def get_response_async(self, request):",
      "inflow": [
        {
          "from": "n13",
          "via": "contains"
        }
      ]
    },
    {
      "id": "n2",
      "class": "validator",
      "name": "check_response",
      "file": "django/core/handlers/base.py",
      "lines": [
        319,
        343
      ],
      "weight": 0.85,
      "behavior": "Validates input before processing; may return None implicitly.",
      "sig": "def check_response(self, response, callback, name=None):",
      "inflow": [
        {
          "from": "n7",
          "via": "calls",
          "condition": "normal"
        },
        {
          "from": "n7",
          "via": "calls",
          "condition": "normal"
        },
        {
          "from": "n10",
          "via": "calls",
          "condition": "normal"
        },
        {
          "from": "n10",
          "via": "calls",
          "condition": "normal"
        },
        {
          "from": "n13",
          "via": "contains"
        }
      ],
      "risks": [
        "implicit_none_return"
      ]
    },
    {
      "id": "n3",
      "class": "error_handler",
      "name": "process_exception_by_middleware",
      "file": "django/core/handlers/base.py",
      "lines": [
        358,
        367
      ],
      "weight": 0.78,
      "behavior": "Error handler; produces error response.",
      "sig": "def process_exception_by_middleware(self, exception, request):",
      "inflow": [
        {
          "from": "n7",
          "via": "calls",
          "condition": "normal"
        },
        {
          "from": "n7",
          "via": "calls",
          "condition": "normal"
        },
        {
          "from": "n13",
          "via": "contains"
        }
      ]
    },
    {
      "id": "n4",
      "class": "handler",
      "name": "reset_urlconf",
      "file": "django/core/handlers/base.py",
      "lines": [
        370,
        372
      ],
      "weight": 0.71,
      "behavior": "Leaf handler invoked by dispatcher.",
      "sig": "def reset_urlconf(sender, **kwargs):",
      "inflow": [
        {
          "from": "n13",
          "via": "contains"
        }
      ]
    },
    {
      "id": "n5",
      "class": "hub",
      "name": "adapt_method_mode",
      "file": "django/core/handlers/base.py",
      "lines": [
        106,
        136
      ],
      "weight": 0.64,
      "behavior": "Async Hub called by load_middleware, load_middleware; routes to multiple targets.",
      "sig": "def adapt_method_mode( self, is_async, method, method_is_async=None, debug=False, name=None, ):",
      "inflow": [
        {
          "from": "n9",
          "via": "calls",
          "condition": "normal"
        },
        {
          "from": "n9",
          "via": "calls",
          "condition": "normal"
        },
        {
          "from": "n9",
          "via": "calls",
          "condition": "normal"
        },
        {
          "from": "n9",
          "via": "calls",
          "condition": "normal"
        },
        {
          "from": "n9",
          "via": "calls",
          "condition": "normal"
        },
        {
          "from": "n13",
          "via": "contains"
        }
      ]
    },
    {
      "id": "n6",
      "class": "handler",
      "name": "get_response",
      "file": "django/core/handlers/base.py",
      "lines": [
        138,
        152
      ],
      "weight": 0.57,
      "behavior": "Leaf handler invoked by dispatcher.",
      "sig": "def get_response(self, request):",
      "inflow": [
        {
          "from": "n13",
          "via": "contains"
        }
      ]
    },
    {
      "id": "n7",
      "class": "error_handler",
      "name": "_get_response",
      "file": "django/core/handlers/base.py",
      "lines": [
        176,
        228
      ],
      "weight": 0.5,
      "behavior": "Error handler; produces check_response, check_response, make_view_atomic; catches broad exceptions.",
      "sig": "def _get_response(self, request):",
      "inflow": [
        {
          "from": "n13",
          "via": "contains"
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
        },
        {
          "to": "n12",
          "via": "calls",
          "condition": "normal"
        },
        {
          "to": "n3",
          "via": "calls",
          "condition": "normal"
        },
        {
          "to": "n3",
          "via": "calls",
          "condition": "normal"
        },
        {
          "to": "n11",
          "via": "calls",
          "condition": "normal"
        }
      ],
      "risks": [
        "broad_exception_handler"
      ],
      "invariants": [
        "Catches broad exceptions; specific errors may be masked."
      ]
    },
    {
      "id": "n8",
      "class": "error_handler",
      "name": "BaseHandler",
      "file": "django/core/handlers/base.py",
      "lines": [
        21,
        367
      ],
      "weight": 0.42,
      "behavior": "Async Error handler; produces error response; catches broad exceptions; may return None implicitly.",
      "sig": "def load_middleware(self, is_async=False):",
      "inflow": [
        {
          "from": "n13",
          "via": "contains"
        }
      ],
      "risks": [
        "broad_exception_handler",
        "implicit_none_return",
        "state_mutation_outside_init"
      ],
      "invariants": [
        "Catches broad exceptions; specific errors may be masked.",
        "Mutates instance state outside constructor."
      ]
    },
    {
      "id": "n9",
      "class": "dispatcher",
      "name": "load_middleware",
      "file": "django/core/handlers/base.py",
      "lines": [
        27,
        104
      ],
      "weight": 0.35,
      "behavior": "Async Dispatcher that routes to adapt_method_mode, adapt_method_mode, adapt_method_mode; mutates state outside __init__.",
      "sig": "def load_middleware(self, is_async=False):",
      "inflow": [
        {
          "from": "n13",
          "via": "contains"
        }
      ],
      "outflow": [
        {
          "to": "n5",
          "via": "calls",
          "condition": "normal"
        },
        {
          "to": "n5",
          "via": "calls",
          "condition": "normal"
        },
        {
          "to": "n5",
          "via": "calls",
          "condition": "normal"
        },
        {
          "to": "n5",
          "via": "calls",
          "condition": "normal"
        },
        {
          "to": "n5",
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
      "id": "n10",
      "class": "error_handler",
      "name": "_get_response_async",
      "file": "django/core/handlers/base.py",
      "lines": [
        230,
        300
      ],
      "weight": 0.28,
      "behavior": "Async Error handler; produces check_response, check_response, make_view_atomic; catches broad exceptions.",
      "sig": "async def _get_response_async(self, request):",
      "inflow": [
        {
          "from": "n13",
          "via": "contains"
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
        },
        {
          "to": "n12",
          "via": "calls",
          "condition": "normal"
        },
        {
          "to": "n11",
          "via": "calls",
          "condition": "normal"
        }
      ],
      "risks": [
        "broad_exception_handler"
      ],
      "invariants": [
        "Catches broad exceptions; specific errors may be masked."
      ]
    },
    {
      "id": "n11",
      "class": "handler",
      "name": "resolve_request",
      "file": "django/core/handlers/base.py",
      "lines": [
        302,
        317
      ],
      "weight": 0.21,
      "behavior": "Leaf handler invoked by _get_response, _get_response_async.",
      "sig": "def resolve_request(self, request):",
      "inflow": [
        {
          "from": "n7",
          "via": "calls",
          "condition": "normal"
        },
        {
          "from": "n10",
          "via": "calls",
          "condition": "normal"
        },
        {
          "from": "n13",
          "via": "contains"
        }
      ]
    },
    {
      "id": "n12",
      "class": "handler",
      "name": "make_view_atomic",
      "file": "django/core/handlers/base.py",
      "lines": [
        347,
        356
      ],
      "weight": 0.14,
      "behavior": "Leaf handler invoked by _get_response, _get_response_async.",
      "sig": "def make_view_atomic(self, view):",
      "inflow": [
        {
          "from": "n7",
          "via": "calls",
          "condition": "normal"
        },
        {
          "from": "n10",
          "via": "calls",
          "condition": "normal"
        },
        {
          "from": "n13",
          "via": "contains"
        }
      ]
    },
    {
      "id": "n13",
      "class": "module_root",
      "name": "django/core/handlers/base.py",
      "file": "django/core/handlers/base.py",
      "lines": [
        1,
        376
      ],
      "weight": 0.08,
      "behavior": "Module containing 12 projected symbol(s); catches broad exceptions; may return None implicitly.",
      "outflow": [
        {
          "to": "n7",
          "via": "contains"
        },
        {
          "to": "n10",
          "via": "contains"
        },
        {
          "to": "n5",
          "via": "contains"
        },
        {
          "to": "n2",
          "via": "contains"
        },
        {
          "to": "n6",
          "via": "contains"
        },
        {
          "to": "n1",
          "via": "contains"
        },
        {
          "to": "n9",
          "via": "contains"
        },
        {
          "to": "n12",
          "via": "contains"
        },
        {
          "to": "n3",
          "via": "contains"
        },
        {
          "to": "n11",
          "via": "contains"
        },
        {
          "to": "n8",
          "via": "contains"
        },
        {
          "to": "n4",
          "via": "contains"
        }
      ],
      "risks": [
        "broad_exception_handler",
        "implicit_none_return",
        "state_mutation_outside_init"
      ],
      "invariants": [
        "Catches broad exceptions; specific errors may be masked.",
        "Mutates instance state outside constructor."
      ]
    }
  ],
  "uncertainty": {
    "confidence": 0.65,
    "hint": "targeted_lookup",
    "gaps": []
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
