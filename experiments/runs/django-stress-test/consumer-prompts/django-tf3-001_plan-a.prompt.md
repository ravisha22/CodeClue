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
Where in Django's codebase should an edit be made to add a new middleware hook that runs after URL resolution but before view dispatch?

## Clue Artifact (Entity-Centric)
```json
{
  "task": {
    "id": "trace-django-fast-OF3",
    "repo": "",
    "family": "OF3",
    "operation_family": "OF3",
    "question": "Where in Django's codebase should an edit be made to add a new middleware hook that runs after URL resolution but before view dispatch?"
  },
  "summary": "test_cache_read_for_model_instance_with_deferred: Function test_cache_read_for_model_instance_with_deferred. test_cull_delete_when_store_empty: Accesses data store; runs in finally block. test_get_or_set: Function test_get_or_set.",
  "entities": [
    {
      "id": "n1",
      "class": "utility",
      "name": "test_cache_read_for_model_instance_with_deferred",
      "file": "tests/cache/tests.py",
      "lines": [
        487,
        503
      ],
      "weight": 0.92,
      "behavior": "Function test_cache_read_for_model_instance_with_deferred.",
      "sig": "def test_cache_read_for_model_instance_with_deferred(self):"
    },
    {
      "id": "n2",
      "class": "data_accessor",
      "name": "test_cull_delete_when_store_empty",
      "file": "tests/cache/tests.py",
      "lines": [
        712,
        726
      ],
      "weight": 0.86,
      "behavior": "Accesses data store; runs in finally block.",
      "sig": "def test_cull_delete_when_store_empty(self):",
      "risks": [
        "runs_in_finally"
      ],
      "invariants": [
        "Executes unconditionally (in finally block)."
      ]
    },
    {
      "id": "n3",
      "class": "utility",
      "name": "test_get_or_set",
      "file": "tests/cache/tests.py",
      "lines": [
        1130,
        1138
      ],
      "weight": 0.8,
      "behavior": "Function test_get_or_set.",
      "sig": "def test_get_or_set_callable(self):"
    },
    {
      "id": "n4",
      "class": "utility",
      "name": "get_response",
      "file": "tests/middleware/tests.py",
      "lines": [
        511,
        516
      ],
      "weight": 0.74,
      "behavior": "Function get_response.",
      "sig": "def get_response(self, req):"
    },
    {
      "id": "n5",
      "class": "utility",
      "name": "test_get_or_set_callable",
      "file": "tests/cache/tests.py",
      "lines": [
        283,
        291
      ],
      "weight": 0.67,
      "behavior": "Function test_get_or_set_callable.",
      "sig": "def test_get_or_set_callable(self):"
    },
    {
      "id": "n6",
      "class": "utility",
      "name": "test_with_many_vary_on",
      "file": "tests/cache/tests.py",
      "lines": [
        3044,
        3048
      ],
      "weight": 0.61,
      "behavior": "Function test_with_many_vary_on.",
      "sig": "def test_proper_escaping(self):"
    },
    {
      "id": "n7",
      "class": "utility",
      "name": "test_empty_cache_file_considered_expired",
      "file": "tests/cache/tests.py",
      "lines": [
        1869,
        1877
      ],
      "weight": 0.55,
      "behavior": "Function test_empty_cache_file_considered_expired.",
      "sig": "def test_empty_cache_file_considered_expired(self):"
    },
    {
      "id": "n8",
      "class": "utility",
      "name": "__init__",
      "file": "tests/cache/tests.py",
      "lines": [
        1887,
        1891
      ],
      "weight": 0.49,
      "behavior": "Function __init__; mutates state outside __init__.",
      "sig": "def time(self):",
      "risks": [
        "state_mutation_outside_init"
      ],
      "invariants": [
        "Mutates instance state outside constructor."
      ]
    },
    {
      "id": "n9",
      "class": "utility",
      "name": "test_long_vary_on",
      "file": "tests/cache/tests.py",
      "lines": [
        3060,
        3065
      ],
      "weight": 0.43,
      "behavior": "Function test_long_vary_on.",
      "sig": "def test_same_instance(self):"
    },
    {
      "id": "n10",
      "class": "utility",
      "name": "test_get_or_set",
      "file": "tests/cache/tests.py",
      "lines": [
        279,
        283
      ],
      "weight": 0.37,
      "behavior": "Function test_get_or_set.",
      "sig": "def test_get_or_set(self):"
    },
    {
      "id": "n11",
      "class": "data_accessor",
      "name": "test_delete_many_no_keys",
      "file": "tests/cache/tests.py",
      "lines": [
        617,
        620
      ],
      "weight": 0.31,
      "behavior": "Accesses data store.",
      "sig": "def test_clear(self):"
    },
    {
      "id": "n12",
      "class": "utility",
      "name": "test_middleware_doesnt_cache_streaming_response",
      "file": "tests/cache/tests.py",
      "lines": [
        2585,
        2605
      ],
      "weight": 0.25,
      "behavior": "Function test_middleware_doesnt_cache_streaming_response.",
      "sig": "def test_middleware_doesnt_cache_streaming_response(self):"
    },
    {
      "id": "n13",
      "class": "utility",
      "name": "test_middleware",
      "file": "tests/cache/tests.py",
      "lines": [
        2702,
        2732
      ],
      "weight": 0.18,
      "behavior": "Function test_middleware.",
      "sig": "def test_view_decorator(self):"
    },
    {
      "id": "n14",
      "class": "utility",
      "name": "test_set_many",
      "file": "tests/cache/tests.py",
      "lines": [
        588,
        593
      ],
      "weight": 0.12,
      "behavior": "Function test_set_many.",
      "sig": "def test_set_many_returns_empty_list_on_success(self):"
    },
    {
      "id": "n15",
      "class": "utility",
      "name": "FileBasedCachePathLibTests",
      "file": "tests/cache/tests.py",
      "lines": [
        2009,
        2017
      ],
      "weight": 0.06,
      "behavior": "Class FileBasedCachePathLibTests.",
      "sig": "def mkdtemp(self):"
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
