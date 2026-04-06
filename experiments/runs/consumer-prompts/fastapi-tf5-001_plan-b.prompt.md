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
Security concerns in FastAPI's CORS handling?

## Clue Artifact (Flat-Table)
```json
{
  "task": {
    "id": "trace-OF5-20260403093309",
    "repo": "",
    "family": "OF5",
    "operation_family": "OF5",
    "question": "Security concerns in FastAPI's CORS handling?"
  },
  "clue_summary": {
    "system_behavior": [
      "http_exception_handler: Async Error handler; produces error response.",
      "request_validation_exception_handler: Async Error handler; produces error response.",
      "websocket_request_validation_exception_handler: Async Error handler; produces error response.",
      "DependencyScopeError: Error handler; produces error response.",
      "EndpointContext: Class EndpointContext."
    ],
    "key_files": [
      "fastapi/exception_handlers.py",
      "fastapi/exceptions.py"
    ],
    "key_symbols": [
      "http_exception_handler",
      "request_validation_exception_handler",
      "websocket_request_validation_exception_handler",
      "DependencyScopeError",
      "EndpointContext"
    ]
  },
  "nodes": [
    {
      "id": "n1",
      "type": "async_function",
      "name": "http_exception_handler",
      "summary": "Async Error handler; produces error response.",
      "file": "fastapi/exception_handlers.py",
      "lines": [
        11,
        17
      ],
      "importance": 1,
      "role": "error_handler",
      "sig": "async def http_exception_handler(request: Request, exc: HTTPException) -> Response:"
    },
    {
      "id": "n2",
      "type": "async_function",
      "name": "request_validation_exception_handler",
      "summary": "Async Error handler; produces error response.",
      "file": "fastapi/exception_handlers.py",
      "lines": [
        20,
        26
      ],
      "importance": 2,
      "role": "error_handler",
      "sig": "async def request_validation_exception_handler( request: Request, exc: RequestValidationError ) -> JSONResponse:"
    },
    {
      "id": "n3",
      "type": "async_function",
      "name": "websocket_request_validation_exception_handler",
      "summary": "Async Error handler; produces error response.",
      "file": "fastapi/exception_handlers.py",
      "lines": [
        29,
        34
      ],
      "importance": 3,
      "role": "error_handler",
      "sig": "async def websocket_request_validation_exception_handler( websocket: WebSocket, exc: WebSocketRequestValidationError ) -> None:"
    },
    {
      "id": "n4",
      "type": "class",
      "name": "DependencyScopeError",
      "summary": "Error handler; produces error response.",
      "file": "fastapi/exceptions.py",
      "lines": [
        167,
        171
      ],
      "importance": 4,
      "role": "error_handler"
    },
    {
      "id": "n5",
      "type": "class",
      "name": "EndpointContext",
      "summary": "Class EndpointContext.",
      "file": "fastapi/exceptions.py",
      "lines": [
        10,
        14
      ],
      "importance": 5,
      "role": "utility"
    },
    {
      "id": "n6",
      "type": "class",
      "name": "FastAPIDeprecationWarning",
      "summary": "Class FastAPIDeprecationWarning.",
      "file": "fastapi/exceptions.py",
      "lines": [
        252,
        256
      ],
      "importance": 6,
      "role": "utility"
    },
    {
      "id": "n7",
      "type": "class",
      "name": "FastAPIError",
      "summary": "Error handler; produces error response.",
      "file": "fastapi/exceptions.py",
      "lines": [
        161,
        164
      ],
      "importance": 7,
      "role": "error_handler"
    },
    {
      "id": "n8",
      "type": "function",
      "name": "__init__",
      "summary": "Function __init__.",
      "file": "fastapi/exceptions.py",
      "lines": [
        45,
        83
      ],
      "importance": 8,
      "role": "utility"
    },
    {
      "id": "n9",
      "type": "class",
      "name": "HTTPException",
      "summary": "Async Error handler; produces error response.",
      "file": "fastapi/exceptions.py",
      "lines": [
        17,
        83
      ],
      "importance": 9,
      "role": "error_handler",
      "sig": "async def read_item(item_id: str):"
    },
    {
      "id": "n10",
      "type": "class",
      "name": "PydanticV1NotSupportedError",
      "summary": "Error handler; produces error response.",
      "file": "fastapi/exceptions.py",
      "lines": [
        246,
        249
      ],
      "importance": 10,
      "role": "error_handler"
    },
    {
      "id": "n11",
      "type": "function",
      "name": "__init__",
      "summary": "Function __init__.",
      "file": "fastapi/exceptions.py",
      "lines": [
        213,
        221
      ],
      "importance": 11,
      "role": "utility",
      "sig": "def __init__( self, errors: Sequence[Any], *, body: Any = None, endpoint_ctx: EndpointContext | None = None, ) -> None:"
    },
    {
      "id": "n12",
      "type": "class",
      "name": "RequestValidationError",
      "summary": "Error handler; produces error response.",
      "file": "fastapi/exceptions.py",
      "lines": [
        212,
        221
      ],
      "importance": 12,
      "role": "error_handler",
      "sig": "def __init__( self, errors: Sequence[Any], *, body: Any = None, endpoint_ctx: EndpointContext | None = None, ) -> None:"
    },
    {
      "id": "n13",
      "type": "function",
      "name": "__init__",
      "summary": "Function __init__.",
      "file": "fastapi/exceptions.py",
      "lines": [
        235,
        243
      ],
      "importance": 13,
      "role": "utility",
      "sig": "def __init__( self, errors: Sequence[Any], *, body: Any = None, endpoint_ctx: EndpointContext | None = None, ) -> None:"
    },
    {
      "id": "n14",
      "type": "class",
      "name": "ResponseValidationError",
      "summary": "Error handler; produces error response.",
      "file": "fastapi/exceptions.py",
      "lines": [
        234,
        243
      ],
      "importance": 14,
      "role": "error_handler",
      "sig": "def __init__( self, errors: Sequence[Any], *, body: Any = None, endpoint_ctx: EndpointContext | None = None, ) -> None:"
    },
    {
      "id": "n15",
      "type": "function",
      "name": "__init__",
      "summary": "Function __init__.",
      "file": "fastapi/exceptions.py",
      "lines": [
        175,
        188
      ],
      "importance": 15,
      "role": "utility",
      "sig": "def __init__( self, errors: Sequence[Any], *, endpoint_ctx: EndpointContext | None = None, ) -> None:"
    }
  ],
  "relations": [],
  "assertions": [],
  "uncertainty": {
    "overall_confidence": 1.0,
    "lookup_hint": "clue_only",
    "known_gaps": []
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
