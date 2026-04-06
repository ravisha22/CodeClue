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
Where to add TypeORM migration support?

## Clue Artifact (Flat-Table)
```json
{
  "task": {
    "id": "trace-OF3-20260403094654",
    "repo": "",
    "family": "OF3",
    "operation_family": "OF3",
    "question": "Where to add TypeORM migration support?"
  },
  "clue_summary": {
    "system_behavior": [
      "DriverFactory: Leaf handler invoked by dispatcher.",
      "src/driver/DriverFactory.ts: Module containing 1 projected symbol(s)."
    ],
    "key_files": [
      "src/driver/DriverFactory.ts"
    ],
    "key_symbols": [
      "DriverFactory"
    ]
  },
  "nodes": [
    {
      "id": "n1",
      "type": "class",
      "name": "DriverFactory",
      "summary": "Leaf handler invoked by dispatcher.",
      "file": "src/driver/DriverFactory.ts",
      "lines": [
        25,
        25
      ],
      "importance": 1,
      "role": "handler"
    },
    {
      "id": "n2",
      "type": "module",
      "name": "src/driver/DriverFactory.ts",
      "summary": "Module containing 1 projected symbol(s).",
      "file": "src/driver/DriverFactory.ts",
      "lines": [
        1,
        95
      ],
      "importance": 2,
      "role": "module_root"
    }
  ],
  "relations": [
    {
      "type": "contains",
      "from": "n2",
      "to": "n1"
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
