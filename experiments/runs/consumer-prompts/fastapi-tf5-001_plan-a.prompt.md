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
Security concerns in FastAPI's CORS handling?

## Clue Artifact (Entity-Centric)
```json
{
  "task": {
    "id": "trace-OF5-20260403093309",
    "repo": "",
    "family": "OF5",
    "operation_family": "OF5",
    "question": "Security concerns in FastAPI's CORS handling?"
  },
  "summary": "http_exception_handler: Async Error handler; produces error response. request_validation_exception_handler: Async Error handler; produces error response. websocket_request_validation_exception_handler: Async Error handler; produces error response.",
  "entities": [
    {
      "id": "n1",
      "class": "error_handler",
      "name": "http_exception_handler",
      "file": "fastapi/exception_handlers.py",
      "lines": [
        11,
        17
      ],
      "weight": 0.92,
      "behavior": "Async Error handler; produces error response.",
      "sig": "async def http_exception_handler(request: Request, exc: HTTPException) -> Response:"
    },
    {
      "id": "n2",
      "class": "error_handler",
      "name": "request_validation_exception_handler",
      "file": "fastapi/exception_handlers.py",
      "lines": [
        20,
        26
      ],
      "weight": 0.86,
      "behavior": "Async Error handler; produces error response.",
      "sig": "async def request_validation_exception_handler( request: Request, exc: RequestValidationError ) -> JSONResponse:"
    },
    {
      "id": "n3",
      "class": "error_handler",
      "name": "websocket_request_validation_exception_handler",
      "file": "fastapi/exception_handlers.py",
      "lines": [
        29,
        34
      ],
      "weight": 0.8,
      "behavior": "Async Error handler; produces error response.",
      "sig": "async def websocket_request_validation_exception_handler( websocket: WebSocket, exc: WebSocketRequestValidationError ) -> None:"
    },
    {
      "id": "n4",
      "class": "error_handler",
      "name": "DependencyScopeError",
      "file": "fastapi/exceptions.py",
      "lines": [
        167,
        171
      ],
      "weight": 0.74,
      "behavior": "Error handler; produces error response."
    },
    {
      "id": "n5",
      "class": "utility",
      "name": "EndpointContext",
      "file": "fastapi/exceptions.py",
      "lines": [
        10,
        14
      ],
      "weight": 0.67,
      "behavior": "Class EndpointContext."
    },
    {
      "id": "n6",
      "class": "utility",
      "name": "FastAPIDeprecationWarning",
      "file": "fastapi/exceptions.py",
      "lines": [
        252,
        256
      ],
      "weight": 0.61,
      "behavior": "Class FastAPIDeprecationWarning."
    },
    {
      "id": "n7",
      "class": "error_handler",
      "name": "FastAPIError",
      "file": "fastapi/exceptions.py",
      "lines": [
        161,
        164
      ],
      "weight": 0.55,
      "behavior": "Error handler; produces error response."
    },
    {
      "id": "n8",
      "class": "utility",
      "name": "__init__",
      "file": "fastapi/exceptions.py",
      "lines": [
        45,
        83
      ],
      "weight": 0.49,
      "behavior": "Function __init__."
    },
    {
      "id": "n9",
      "class": "error_handler",
      "name": "HTTPException",
      "file": "fastapi/exceptions.py",
      "lines": [
        17,
        83
      ],
      "weight": 0.43,
      "behavior": "Async Error handler; produces error response.",
      "sig": "async def read_item(item_id: str):"
    },
    {
      "id": "n10",
      "class": "error_handler",
      "name": "PydanticV1NotSupportedError",
      "file": "fastapi/exceptions.py",
      "lines": [
        246,
        249
      ],
      "weight": 0.37,
      "behavior": "Error handler; produces error response."
    },
    {
      "id": "n11",
      "class": "utility",
      "name": "__init__",
      "file": "fastapi/exceptions.py",
      "lines": [
        213,
        221
      ],
      "weight": 0.31,
      "behavior": "Function __init__.",
      "sig": "def __init__( self, errors: Sequence[Any], *, body: Any = None, endpoint_ctx: EndpointContext | None = None, ) -> None:"
    },
    {
      "id": "n12",
      "class": "error_handler",
      "name": "RequestValidationError",
      "file": "fastapi/exceptions.py",
      "lines": [
        212,
        221
      ],
      "weight": 0.25,
      "behavior": "Error handler; produces error response.",
      "sig": "def __init__( self, errors: Sequence[Any], *, body: Any = None, endpoint_ctx: EndpointContext | None = None, ) -> None:"
    },
    {
      "id": "n13",
      "class": "utility",
      "name": "__init__",
      "file": "fastapi/exceptions.py",
      "lines": [
        235,
        243
      ],
      "weight": 0.18,
      "behavior": "Function __init__.",
      "sig": "def __init__( self, errors: Sequence[Any], *, body: Any = None, endpoint_ctx: EndpointContext | None = None, ) -> None:"
    },
    {
      "id": "n14",
      "class": "error_handler",
      "name": "ResponseValidationError",
      "file": "fastapi/exceptions.py",
      "lines": [
        234,
        243
      ],
      "weight": 0.12,
      "behavior": "Error handler; produces error response.",
      "sig": "def __init__( self, errors: Sequence[Any], *, body: Any = None, endpoint_ctx: EndpointContext | None = None, ) -> None:"
    },
    {
      "id": "n15",
      "class": "utility",
      "name": "__init__",
      "file": "fastapi/exceptions.py",
      "lines": [
        175,
        188
      ],
      "weight": 0.06,
      "behavior": "Function __init__.",
      "sig": "def __init__( self, errors: Sequence[Any], *, endpoint_ctx: EndpointContext | None = None, ) -> None:"
    }
  ],
  "uncertainty": {
    "confidence": 1.0,
    "hint": "clue_only",
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
