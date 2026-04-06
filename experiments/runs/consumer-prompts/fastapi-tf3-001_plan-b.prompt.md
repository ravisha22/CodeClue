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
Where to edit to add middleware in FastAPI?

## Clue Artifact (Flat-Table)
```json
{
  "task": {
    "id": "trace-OF3-20260403093149",
    "repo": "",
    "family": "OF3",
    "operation_family": "OF3",
    "question": "Where to edit to add middleware in FastAPI?"
  },
  "clue_summary": {
    "system_behavior": [
      "EventSourceResponse: Leaf handler invoked by dispatcher.",
      "_check_data_exclusive: Validates input before processing.",
      "ServerSentEvent: Leaf handler invoked by dispatcher.",
      "_check_id_no_null: Validates input before processing.",
      "format_sse_event: Leaf handler invoked by dispatcher."
    ],
    "key_files": [
      "fastapi/sse.py"
    ],
    "key_symbols": [
      "EventSourceResponse",
      "_check_data_exclusive",
      "ServerSentEvent",
      "_check_id_no_null",
      "format_sse_event"
    ]
  },
  "nodes": [
    {
      "id": "n1",
      "type": "class",
      "name": "EventSourceResponse",
      "summary": "Leaf handler invoked by dispatcher.",
      "file": "fastapi/sse.py",
      "lines": [
        20,
        33
      ],
      "importance": 1,
      "role": "handler"
    },
    {
      "id": "n2",
      "type": "function",
      "name": "_check_data_exclusive",
      "summary": "Validates input before processing.",
      "file": "fastapi/sse.py",
      "lines": [
        136,
        143
      ],
      "importance": 2,
      "role": "validator",
      "sig": "def _check_data_exclusive(self) -> \"ServerSentEvent\":"
    },
    {
      "id": "n3",
      "type": "class",
      "name": "ServerSentEvent",
      "summary": "Leaf handler invoked by dispatcher.",
      "file": "fastapi/sse.py",
      "lines": [
        42,
        143
      ],
      "importance": 3,
      "role": "handler",
      "sig": "@model_validator(mode=\"after\") def _check_data_exclusive(self) -> \"ServerSentEvent\":"
    },
    {
      "id": "n4",
      "type": "function",
      "name": "_check_id_no_null",
      "summary": "Validates input before processing.",
      "file": "fastapi/sse.py",
      "lines": [
        36,
        39
      ],
      "importance": 4,
      "role": "validator",
      "sig": "def _check_id_no_null(v: str | None) -> str | None:"
    },
    {
      "id": "n5",
      "type": "function",
      "name": "format_sse_event",
      "summary": "Leaf handler invoked by dispatcher.",
      "file": "fastapi/sse.py",
      "lines": [
        146,
        214
      ],
      "importance": 5,
      "role": "handler"
    },
    {
      "id": "n6",
      "type": "module",
      "name": "fastapi/sse.py",
      "summary": "Module containing 5 projected symbol(s).",
      "file": "fastapi/sse.py",
      "lines": [
        1,
        223
      ],
      "importance": 6,
      "role": "module_root"
    }
  ],
  "relations": [
    {
      "type": "contains",
      "from": "n6",
      "to": "n1"
    },
    {
      "type": "contains",
      "from": "n6",
      "to": "n2"
    },
    {
      "type": "contains",
      "from": "n6",
      "to": "n3"
    },
    {
      "type": "contains",
      "from": "n6",
      "to": "n4"
    },
    {
      "type": "contains",
      "from": "n6",
      "to": "n5"
    }
  ],
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
