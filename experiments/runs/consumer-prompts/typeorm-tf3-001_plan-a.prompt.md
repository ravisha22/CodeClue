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
Where to add TypeORM migration support?

## Clue Artifact (Entity-Centric)
```json
{
  "task": {
    "id": "trace-OF3-20260403094654",
    "repo": "",
    "family": "OF3",
    "operation_family": "OF3",
    "question": "Where to add TypeORM migration support?"
  },
  "summary": "DriverFactory: Leaf handler invoked by dispatcher. src/driver/DriverFactory.ts: Module containing 1 projected symbol(s).",
  "entities": [
    {
      "id": "n1",
      "class": "handler",
      "name": "DriverFactory",
      "file": "src/driver/DriverFactory.ts",
      "lines": [
        25,
        25
      ],
      "weight": 0.86,
      "behavior": "Leaf handler invoked by dispatcher.",
      "inflow": [
        {
          "from": "n2",
          "via": "contains"
        }
      ]
    },
    {
      "id": "n2",
      "class": "module_root",
      "name": "src/driver/DriverFactory.ts",
      "file": "src/driver/DriverFactory.ts",
      "lines": [
        1,
        95
      ],
      "weight": 0.5,
      "behavior": "Module containing 1 projected symbol(s).",
      "outflow": [
        {
          "to": "n1",
          "via": "contains"
        }
      ]
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
