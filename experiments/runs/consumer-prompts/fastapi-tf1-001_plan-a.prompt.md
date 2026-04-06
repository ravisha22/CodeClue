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
What is FastAPI's request routing architecture?

## Clue Artifact (Entity-Centric)
```json
{
  "task": {
    "id": "trace-OF1-20260403093112",
    "repo": "",
    "family": "OF1",
    "operation_family": "OF1",
    "question": "What is FastAPI's request routing architecture?"
  },
  "summary": "ParamDetails: Leaf handler invoked by dispatcher. SolvedDependency: Class SolvedDependency. _extract_form_body: Async Entrypoint that delegates to downstream handlers.",
  "entities": [
    {
      "id": "n1",
      "class": "handler",
      "name": "ParamDetails",
      "file": "fastapi/dependencies/utils.py",
      "lines": [
        384,
        387
      ],
      "weight": 0.92,
      "behavior": "Leaf handler invoked by dispatcher."
    },
    {
      "id": "n2",
      "class": "utility",
      "name": "SolvedDependency",
      "file": "fastapi/dependencies/utils.py",
      "lines": [
        587,
        592
      ],
      "weight": 0.86,
      "behavior": "Class SolvedDependency."
    },
    {
      "id": "n3",
      "class": "entrypoint",
      "name": "_extract_form_body",
      "file": "fastapi/dependencies/utils.py",
      "lines": [
        909,
        945
      ],
      "weight": 0.8,
      "behavior": "Async Entrypoint that delegates to downstream handlers.",
      "sig": "async def _extract_form_body( body_fields: list[ModelField], received_body: FormData, ) -> dict[str, Any]:"
    },
    {
      "id": "n4",
      "class": "utility",
      "name": "_get_flat_fields_from_params",
      "file": "fastapi/dependencies/utils.py",
      "lines": [
        190,
        199
      ],
      "weight": 0.74,
      "behavior": "Function _get_flat_fields_from_params.",
      "sig": "def _get_flat_fields_from_params(fields: list[ModelField]) -> list[ModelField]:"
    },
    {
      "id": "n5",
      "class": "middleware",
      "name": "_get_multidict_value",
      "file": "fastapi/dependencies/utils.py",
      "lines": [
        750,
        778
      ],
      "weight": 0.67,
      "behavior": "Middleware between upstream and downstream; may return None implicitly.",
      "sig": "def _get_multidict_value( field: ModelField, values: Mapping[str, Any], alias: str | None = None ) -> Any:",
      "risks": [
        "implicit_none_return"
      ]
    },
    {
      "id": "n6",
      "class": "utility",
      "name": "_get_signature",
      "file": "fastapi/dependencies/utils.py",
      "lines": [
        211,
        223
      ],
      "weight": 0.61,
      "behavior": "Function _get_signature.",
      "sig": "def _get_signature(call: Callable[..., Any]) -> inspect.Signature:"
    },
    {
      "id": "n7",
      "class": "handler",
      "name": "_is_json_field",
      "file": "fastapi/dependencies/utils.py",
      "lines": [
        746,
        747
      ],
      "weight": 0.55,
      "behavior": "Leaf handler invoked by dispatcher.",
      "sig": "def _is_json_field(field: ModelField) -> bool:"
    },
    {
      "id": "n8",
      "class": "utility",
      "name": "_should_embed_body_fields",
      "file": "fastapi/dependencies/utils.py",
      "lines": [
        885,
        906
      ],
      "weight": 0.49,
      "behavior": "Function _should_embed_body_fields.",
      "sig": "def _should_embed_body_fields(fields: list[ModelField]) -> bool:"
    },
    {
      "id": "n9",
      "class": "utility",
      "name": "_solve_generator",
      "file": "fastapi/dependencies/utils.py",
      "lines": [
        575,
        583
      ],
      "weight": 0.43,
      "behavior": "Async Async_function _solve_generator.",
      "sig": "async def _solve_generator( *, dependant: Dependant, stack: AsyncExitStack, sub_values: dict[str, Any] ) -> Any:"
    },
    {
      "id": "n10",
      "class": "validator",
      "name": "_validate_value_with_model_field",
      "file": "fastapi/dependencies/utils.py",
      "lines": [
        735,
        743
      ],
      "weight": 0.37,
      "behavior": "Validates input before processing.",
      "sig": "def _validate_value_with_model_field( *, field: ModelField, value: Any, values: dict[str, Any], loc: tuple[str, ...] ) -> tuple[Any, list[Any]]:"
    },
    {
      "id": "n11",
      "class": "utility",
      "name": "add_non_field_param_to_dependency",
      "file": "fastapi/dependencies/utils.py",
      "lines": [
        359,
        380
      ],
      "weight": 0.31,
      "behavior": "Function add_non_field_param_to_dependency.",
      "sig": "def add_non_field_param_to_dependency( *, param_name: str, type_annotation: Any, dependant: Dependant ) -> bool | None:"
    },
    {
      "id": "n12",
      "class": "utility",
      "name": "add_param_to_fields",
      "file": "fastapi/dependencies/utils.py",
      "lines": [
        559,
        572
      ],
      "weight": 0.25,
      "behavior": "Function add_param_to_fields.",
      "sig": "def add_param_to_fields(*, field: ModelField, dependant: Dependant) -> None:"
    },
    {
      "id": "n13",
      "class": "entrypoint",
      "name": "analyze_param",
      "file": "fastapi/dependencies/utils.py",
      "lines": [
        390,
        556
      ],
      "weight": 0.18,
      "behavior": "Entrypoint that delegates to downstream handlers.",
      "sig": "def analyze_param( *, param_name: str, annotation: Any, value: Any, is_path_param: bool, ) -> ParamDetails:"
    },
    {
      "id": "n14",
      "class": "handler",
      "name": "ensure_multipart_is_installed",
      "file": "fastapi/dependencies/utils.py",
      "lines": [
        94,
        118
      ],
      "weight": 0.12,
      "behavior": "Leaf handler invoked by dispatcher.",
      "sig": "def ensure_multipart_is_installed() -> None:"
    },
    {
      "id": "n15",
      "class": "validator",
      "name": "get_body_field",
      "file": "fastapi/dependencies/utils.py",
      "lines": [
        998,
        1049
      ],
      "weight": 0.06,
      "behavior": "Validates input before processing.",
      "sig": "def get_body_field( *, flat_dependant: Dependant, name: str, embed_body_fields: bool ) -> ModelField | None:"
    }
  ],
  "uncertainty": {
    "confidence": 0.8,
    "hint": "targeted_lookup",
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
