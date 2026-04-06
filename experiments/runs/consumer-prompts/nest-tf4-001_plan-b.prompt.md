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
Behavioral gotchas in NestJS middleware pipeline?

## Clue Artifact (Flat-Table)
```json
{
  "task": {
    "id": "trace-OF4-20260403093421",
    "repo": "",
    "family": "OF4",
    "operation_family": "OF4",
    "question": "Behavioral gotchas in NestJS middleware pipeline?"
  },
  "clue_summary": {
    "system_behavior": [
      "CircularDependencyException: Error handler; produces error response.",
      "Barrier: Class Barrier.",
      "Injector: Class Injector.",
      "callback: Function callback.",
      "factoryReturnValue: Function factoryReturnValue."
    ],
    "key_files": [
      "packages/core/errors/exceptions/circular-dependency.exception.ts",
      "packages/core/helpers/barrier.ts",
      "packages/core/injector/injector.ts"
    ],
    "key_symbols": [
      "CircularDependencyException",
      "Barrier",
      "Injector",
      "callback",
      "factoryReturnValue"
    ]
  },
  "nodes": [
    {
      "id": "n1",
      "type": "class",
      "name": "CircularDependencyException",
      "summary": "Error handler; produces error response.",
      "file": "packages/core/errors/exceptions/circular-dependency.exception.ts",
      "lines": [
        3,
        3
      ],
      "importance": 1,
      "role": "error_handler"
    },
    {
      "id": "n2",
      "type": "class",
      "name": "Barrier",
      "summary": "Class Barrier.",
      "file": "packages/core/helpers/barrier.ts",
      "lines": [
        4,
        4
      ],
      "importance": 2,
      "role": "utility"
    },
    {
      "id": "n3",
      "type": "class",
      "name": "Injector",
      "summary": "Class Injector.",
      "file": "packages/core/injector/injector.ts",
      "lines": [
        86,
        86
      ],
      "importance": 3,
      "role": "utility"
    },
    {
      "id": "n4",
      "type": "function",
      "name": "callback",
      "summary": "Function callback.",
      "file": "packages/core/injector/injector.ts",
      "lines": [
        167,
        167
      ],
      "importance": 4,
      "role": "utility"
    },
    {
      "id": "n5",
      "type": "function",
      "name": "factoryReturnValue",
      "summary": "Function factoryReturnValue.",
      "file": "packages/core/injector/injector.ts",
      "lines": [
        854,
        854
      ],
      "importance": 5,
      "role": "utility"
    },
    {
      "id": "n6",
      "type": "function",
      "name": "identity",
      "summary": "Function identity.",
      "file": "packages/core/injector/injector.ts",
      "lines": [
        650,
        650
      ],
      "importance": 6,
      "role": "utility"
    },
    {
      "id": "n7",
      "type": "function",
      "name": "injectionToken",
      "summary": "Function injectionToken.",
      "file": "packages/core/injector/injector.ts",
      "lines": [
        873,
        873
      ],
      "importance": 7,
      "role": "utility"
    },
    {
      "id": "n8",
      "type": "function",
      "name": "isOptionalFactoryDependency",
      "summary": "Function isOptionalFactoryDependency.",
      "file": "packages/core/injector/injector.ts",
      "lines": [
        409,
        409
      ],
      "importance": 8,
      "role": "utility"
    },
    {
      "id": "n9",
      "type": "function",
      "name": "loadEnhancer",
      "summary": "Function loadEnhancer.",
      "file": "packages/core/injector/injector.ts",
      "lines": [
        892,
        892
      ],
      "importance": 9,
      "role": "utility"
    },
    {
      "id": "n10",
      "type": "function",
      "name": "mapFactoryProviderInjectArray",
      "summary": "Function mapFactoryProviderInjectArray.",
      "file": "packages/core/injector/injector.ts",
      "lines": [
        419,
        419
      ],
      "importance": 10,
      "role": "utility"
    },
    {
      "id": "n11",
      "type": "function",
      "name": "resolveParam",
      "summary": "Function resolveParam.",
      "file": "packages/core/injector/injector.ts",
      "lines": [
        318,
        318
      ],
      "importance": 11,
      "role": "utility"
    },
    {
      "id": "n12",
      "type": "module",
      "name": "packages/core/errors/exceptions/circular-dependency.exception.ts",
      "summary": "Module containing 1 projected symbol(s).",
      "file": "packages/core/errors/exceptions/circular-dependency.exception.ts",
      "lines": [
        1,
        11
      ],
      "importance": 12,
      "role": "module_root"
    }
  ],
  "relations": [
    {
      "type": "contains",
      "from": "n12",
      "to": "n1"
    }
  ],
  "assertions": [],
  "uncertainty": {
    "overall_confidence": 0.93,
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
