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
Impact of TypeORM connection changes?

## Clue Artifact (Flat-Table)
```json
{
  "task": {
    "id": "trace-OF2-20260403094757",
    "repo": "",
    "family": "OF2",
    "operation_family": "OF2",
    "question": "Impact of TypeORM connection changes?"
  },
  "clue_summary": {
    "system_behavior": [
      "src/metadata/EntityMetadata.ts: Module containing 0 projected symbol(s)."
    ],
    "key_files": [
      "src/metadata/EntityMetadata.ts"
    ],
    "key_symbols": []
  },
  "nodes": [
    {
      "id": "n1",
      "type": "module",
      "name": "src/metadata/EntityMetadata.ts",
      "summary": "Module containing 0 projected symbol(s).",
      "file": "src/metadata/EntityMetadata.ts",
      "lines": [
        1,
        1170
      ],
      "importance": 1,
      "role": "module_root"
    }
  ],
  "relations": [],
  "assertions": [],
  "uncertainty": {
    "overall_confidence": 0.0,
    "lookup_hint": "expanded_lookup",
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
