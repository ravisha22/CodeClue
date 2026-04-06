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
What gotcha exists in FastAPI dependency injection?

## Clue Artifact (Flat-Table)
```json
{
  "task": {
    "id": "trace-OF4-20260403093228",
    "repo": "",
    "family": "OF4",
    "operation_family": "OF4",
    "question": "What gotcha exists in FastAPI dependency injection?"
  },
  "clue_summary": {
    "system_behavior": [
      "Item: Class Item.",
      "Message: Class Message.",
      "read_item: Async Async_function read_item.",
      "Item: Class Item.",
      "read_item: Async Async_function read_item."
    ],
    "key_files": [
      "docs_src/additional_responses/tutorial001_py310.py",
      "docs_src/additional_responses/tutorial002_py310.py",
      "docs_src/additional_responses/tutorial003_py310.py",
      "docs_src/additional_responses/tutorial004_py310.py",
      "docs_src/additional_status_codes/tutorial001_an_py310.py",
      "docs_src/additional_status_codes/tutorial001_py310.py",
      "docs_src/advanced_middleware/tutorial001_py310.py",
      "docs_src/advanced_middleware/tutorial002_py310.py",
      "docs_src/advanced_middleware/tutorial003_py310.py"
    ],
    "key_symbols": [
      "Item",
      "Message",
      "read_item",
      "Item",
      "read_item"
    ]
  },
  "nodes": [
    {
      "id": "n1",
      "type": "class",
      "name": "Item",
      "summary": "Class Item.",
      "file": "docs_src/additional_responses/tutorial001_py310.py",
      "lines": [
        6,
        8
      ],
      "importance": 1,
      "role": "utility"
    },
    {
      "id": "n2",
      "type": "class",
      "name": "Message",
      "summary": "Class Message.",
      "file": "docs_src/additional_responses/tutorial001_py310.py",
      "lines": [
        11,
        12
      ],
      "importance": 2,
      "role": "utility"
    },
    {
      "id": "n3",
      "type": "async_function",
      "name": "read_item",
      "summary": "Async Async_function read_item.",
      "file": "docs_src/additional_responses/tutorial001_py310.py",
      "lines": [
        19,
        22
      ],
      "importance": 3,
      "role": "utility",
      "sig": "async def read_item(item_id: str):"
    },
    {
      "id": "n4",
      "type": "class",
      "name": "Item",
      "summary": "Class Item.",
      "file": "docs_src/additional_responses/tutorial002_py310.py",
      "lines": [
        6,
        8
      ],
      "importance": 4,
      "role": "utility"
    },
    {
      "id": "n5",
      "type": "async_function",
      "name": "read_item",
      "summary": "Async Async_function read_item.",
      "file": "docs_src/additional_responses/tutorial002_py310.py",
      "lines": [
        24,
        28
      ],
      "importance": 5,
      "role": "utility",
      "sig": "async def read_item(item_id: str, img: bool | None = None):"
    },
    {
      "id": "n6",
      "type": "class",
      "name": "Item",
      "summary": "Class Item.",
      "file": "docs_src/additional_responses/tutorial003_py310.py",
      "lines": [
        6,
        8
      ],
      "importance": 6,
      "role": "utility"
    },
    {
      "id": "n7",
      "type": "class",
      "name": "Message",
      "summary": "Class Message.",
      "file": "docs_src/additional_responses/tutorial003_py310.py",
      "lines": [
        11,
        12
      ],
      "importance": 7,
      "role": "utility"
    },
    {
      "id": "n8",
      "type": "async_function",
      "name": "read_item",
      "summary": "Async Async_function read_item.",
      "file": "docs_src/additional_responses/tutorial003_py310.py",
      "lines": [
        33,
        37
      ],
      "importance": 8,
      "role": "utility",
      "sig": "async def read_item(item_id: str):"
    },
    {
      "id": "n9",
      "type": "class",
      "name": "Item",
      "summary": "Class Item.",
      "file": "docs_src/additional_responses/tutorial004_py310.py",
      "lines": [
        6,
        8
      ],
      "importance": 9,
      "role": "utility"
    },
    {
      "id": "n10",
      "type": "async_function",
      "name": "read_item",
      "summary": "Async Async_function read_item.",
      "file": "docs_src/additional_responses/tutorial004_py310.py",
      "lines": [
        26,
        30
      ],
      "importance": 10,
      "role": "utility",
      "sig": "async def read_item(item_id: str, img: bool | None = None):"
    },
    {
      "id": "n11",
      "type": "async_function",
      "name": "upsert_item",
      "summary": "Async_function upsert_item.",
      "file": "docs_src/additional_status_codes/tutorial001_an_py310.py",
      "lines": [
        12,
        25
      ],
      "importance": 11,
      "role": "utility"
    },
    {
      "id": "n12",
      "type": "async_function",
      "name": "upsert_item",
      "summary": "Async_function upsert_item.",
      "file": "docs_src/additional_status_codes/tutorial001_py310.py",
      "lines": [
        10,
        23
      ],
      "importance": 12,
      "role": "utility"
    },
    {
      "id": "n13",
      "type": "async_function",
      "name": "main",
      "summary": "Async Async_function main.",
      "file": "docs_src/advanced_middleware/tutorial001_py310.py",
      "lines": [
        10,
        11
      ],
      "importance": 13,
      "role": "utility",
      "sig": "async def main():"
    },
    {
      "id": "n14",
      "type": "async_function",
      "name": "main",
      "summary": "Async Async_function main.",
      "file": "docs_src/advanced_middleware/tutorial002_py310.py",
      "lines": [
        12,
        13
      ],
      "importance": 14,
      "role": "utility",
      "sig": "async def main():"
    },
    {
      "id": "n15",
      "type": "async_function",
      "name": "main",
      "summary": "Async Async_function main.",
      "file": "docs_src/advanced_middleware/tutorial003_py310.py",
      "lines": [
        10,
        11
      ],
      "importance": 15,
      "role": "utility",
      "sig": "async def main():"
    }
  ],
  "relations": [],
  "assertions": [],
  "uncertainty": {
    "overall_confidence": 0.85,
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
