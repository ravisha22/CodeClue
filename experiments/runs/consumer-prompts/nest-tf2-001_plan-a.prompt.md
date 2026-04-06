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
Impact of changing NestJS dependency injection container?

## Clue Artifact (Entity-Centric)
```json
{
  "task": {
    "id": "trace-OF2-20260403093408",
    "repo": "",
    "family": "OF2",
    "operation_family": "OF2",
    "question": "Impact of changing NestJS dependency injection container?"
  },
  "summary": "packages/core/guards/guards-consumer.ts: Module containing 0 projected symbol(s).",
  "entities": [
    {
      "id": "n1",
      "class": "module_root",
      "name": "packages/core/guards/guards-consumer.ts",
      "file": "packages/core/guards/guards-consumer.ts",
      "lines": [
        1,
        58
      ],
      "weight": 1.0,
      "behavior": "Module containing 0 projected symbol(s)."
    }
  ],
  "uncertainty": {
    "confidence": 0.0,
    "hint": "expanded_lookup",
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
