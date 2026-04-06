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
What gotcha exists in FastAPI dependency injection?

## Clue Artifact (Entity-Centric)
```json
{
  "task": {
    "id": "trace-OF4-20260403093228",
    "repo": "",
    "family": "OF4",
    "operation_family": "OF4",
    "question": "What gotcha exists in FastAPI dependency injection?"
  },
  "summary": "Item: Class Item. Message: Class Message. read_item: Async Async_function read_item.",
  "entities": [
    {
      "id": "n1",
      "class": "utility",
      "name": "Item",
      "file": "docs_src/additional_responses/tutorial001_py310.py",
      "lines": [
        6,
        8
      ],
      "weight": 0.92,
      "behavior": "Class Item."
    },
    {
      "id": "n2",
      "class": "utility",
      "name": "Message",
      "file": "docs_src/additional_responses/tutorial001_py310.py",
      "lines": [
        11,
        12
      ],
      "weight": 0.86,
      "behavior": "Class Message."
    },
    {
      "id": "n3",
      "class": "utility",
      "name": "read_item",
      "file": "docs_src/additional_responses/tutorial001_py310.py",
      "lines": [
        19,
        22
      ],
      "weight": 0.8,
      "behavior": "Async Async_function read_item.",
      "sig": "async def read_item(item_id: str):"
    },
    {
      "id": "n4",
      "class": "utility",
      "name": "Item",
      "file": "docs_src/additional_responses/tutorial002_py310.py",
      "lines": [
        6,
        8
      ],
      "weight": 0.74,
      "behavior": "Class Item."
    },
    {
      "id": "n5",
      "class": "utility",
      "name": "read_item",
      "file": "docs_src/additional_responses/tutorial002_py310.py",
      "lines": [
        24,
        28
      ],
      "weight": 0.67,
      "behavior": "Async Async_function read_item.",
      "sig": "async def read_item(item_id: str, img: bool | None = None):"
    },
    {
      "id": "n6",
      "class": "utility",
      "name": "Item",
      "file": "docs_src/additional_responses/tutorial003_py310.py",
      "lines": [
        6,
        8
      ],
      "weight": 0.61,
      "behavior": "Class Item."
    },
    {
      "id": "n7",
      "class": "utility",
      "name": "Message",
      "file": "docs_src/additional_responses/tutorial003_py310.py",
      "lines": [
        11,
        12
      ],
      "weight": 0.55,
      "behavior": "Class Message."
    },
    {
      "id": "n8",
      "class": "utility",
      "name": "read_item",
      "file": "docs_src/additional_responses/tutorial003_py310.py",
      "lines": [
        33,
        37
      ],
      "weight": 0.49,
      "behavior": "Async Async_function read_item.",
      "sig": "async def read_item(item_id: str):"
    },
    {
      "id": "n9",
      "class": "utility",
      "name": "Item",
      "file": "docs_src/additional_responses/tutorial004_py310.py",
      "lines": [
        6,
        8
      ],
      "weight": 0.43,
      "behavior": "Class Item."
    },
    {
      "id": "n10",
      "class": "utility",
      "name": "read_item",
      "file": "docs_src/additional_responses/tutorial004_py310.py",
      "lines": [
        26,
        30
      ],
      "weight": 0.37,
      "behavior": "Async Async_function read_item.",
      "sig": "async def read_item(item_id: str, img: bool | None = None):"
    },
    {
      "id": "n11",
      "class": "utility",
      "name": "upsert_item",
      "file": "docs_src/additional_status_codes/tutorial001_an_py310.py",
      "lines": [
        12,
        25
      ],
      "weight": 0.31,
      "behavior": "Async_function upsert_item."
    },
    {
      "id": "n12",
      "class": "utility",
      "name": "upsert_item",
      "file": "docs_src/additional_status_codes/tutorial001_py310.py",
      "lines": [
        10,
        23
      ],
      "weight": 0.25,
      "behavior": "Async_function upsert_item."
    },
    {
      "id": "n13",
      "class": "utility",
      "name": "main",
      "file": "docs_src/advanced_middleware/tutorial001_py310.py",
      "lines": [
        10,
        11
      ],
      "weight": 0.18,
      "behavior": "Async Async_function main.",
      "sig": "async def main():"
    },
    {
      "id": "n14",
      "class": "utility",
      "name": "main",
      "file": "docs_src/advanced_middleware/tutorial002_py310.py",
      "lines": [
        12,
        13
      ],
      "weight": 0.12,
      "behavior": "Async Async_function main.",
      "sig": "async def main():"
    },
    {
      "id": "n15",
      "class": "utility",
      "name": "main",
      "file": "docs_src/advanced_middleware/tutorial003_py310.py",
      "lines": [
        10,
        11
      ],
      "weight": 0.06,
      "behavior": "Async Async_function main.",
      "sig": "async def main():"
    }
  ],
  "uncertainty": {
    "confidence": 0.85,
    "hint": "clue_only",
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
