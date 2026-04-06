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
Security concerns in NestJS guards?

## Clue Artifact (Entity-Centric)
```json
{
  "task": {
    "id": "trace-OF5-20260403093436",
    "repo": "",
    "family": "OF5",
    "operation_family": "OF5",
    "question": "Security concerns in NestJS guards?"
  },
  "summary": "GuardsConsumer: Leaf handler invoked by dispatcher. ExecutionContextHost: Class ExecutionContextHost. packages/core/guards/guards-consumer.ts: Module containing 1 projected symbol(s).",
  "entities": [
    {
      "id": "n1",
      "class": "handler",
      "name": "GuardsConsumer",
      "file": "packages/core/guards/guards-consumer.ts",
      "lines": [
        7,
        7
      ],
      "weight": 0.86,
      "behavior": "Leaf handler invoked by dispatcher.",
      "inflow": [
        {
          "from": "n3",
          "via": "contains"
        }
      ]
    },
    {
      "id": "n2",
      "class": "utility",
      "name": "ExecutionContextHost",
      "file": "packages/core/helpers/execution-context-host.ts",
      "lines": [
        10,
        10
      ],
      "weight": 0.57,
      "behavior": "Class ExecutionContextHost."
    },
    {
      "id": "n3",
      "class": "module_root",
      "name": "packages/core/guards/guards-consumer.ts",
      "file": "packages/core/guards/guards-consumer.ts",
      "lines": [
        1,
        58
      ],
      "weight": 0.33,
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
