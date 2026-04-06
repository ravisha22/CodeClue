You are a senior software engineer performing a development task.
You have access to a CodeClue artifact — a compact comprehension file
that describes the relevant code subsystem. Use it to plan your approach.

## Task
A NestJS middleware is not executing for certain routes. Trace the middleware resolution and binding flow to identify why route-specific middleware might be skipped.

## CodeClue Artifact
```json
{
  "task": {
    "id": "trace-OF4-20260403093421",
    "repo": "",
    "family": "OF4",
    "operation_family": "OF4",
    "question": "A NestJS middleware is not executing for certain routes. Trace the middleware resolution and binding flow to identify why route-specific middleware might be skipped."
  },
  "summary": "CircularDependencyException: Error handler; produces error response. Barrier: Class Barrier. Injector: Class Injector.",
  "entities": [
    {
      "id": "n1",
      "class": "error_handler",
      "name": "CircularDependencyException",
      "file": "packages/core/errors/exceptions/circular-dependency.exception.ts",
      "lines": [
        3,
        3
      ],
      "weight": 0.86,
      "behavior": "Error handler; produces error response.",
      "inflow": [
        {
          "from": "n12",
          "via": "contains"
        }
      ]
    },
    {
      "id": "n2",
      "class": "utility",
      "name": "Barrier",
      "file": "packages/core/helpers/barrier.ts",
      "lines": [
        4,
        4
      ],
      "weight": 0.79,
      "behavior": "Class Barrier."
    },
    {
      "id": "n3",
      "class": "utility",
      "name": "Injector",
      "file": "packages/core/injector/injector.ts",
      "lines": [
        86,
        86
      ],
      "weight": 0.72,
      "behavior": "Class Injector."
    },
    {
      "id": "n4",
      "class": "utility",
      "name": "callback",
      "file": "packages/core/injector/injector.ts",
      "lines": [
        167,
        167
      ],
      "weight": 0.65,
      "behavior": "Function callback."
    },
    {
      "id": "n5",
      "class": "utility",
      "name": "factoryReturnValue",
      "file": "packages/core/injector/injector.ts",
      "lines": [
        854,
        854
      ],
      "weight": 0.57,
      "behavior": "Function factoryReturnValue."
    },
    {
      "id": "n6",
      "class": "utility",
      "name": "identity",
      "file": "packages/core/injector/injector.ts",
      "lines": [
        650,
        650
      ],
      "weight": 0.5,
      "behavior": "Function identity."
    },
    {
      "id": "n7",
      "class": "utility",
      "name": "injectionToken",
      "file": "packages/core/injector/injector.ts",
      "lines": [
        873,
        873
      ],
      "weight": 0.43,
      "behavior": "Function injectionToken."
    },
    {
      "id": "n8",
      "class": "utility",
      "name": "isOptionalFactoryDependency",
      "file": "packages/core/injector/injector.ts",
      "lines": [
        409,
        409
      ],
      "weight": 0.36,
      "behavior": "Function isOptionalFactoryDependency."
    },
    {
      "id": "n9",
      "class": "utility",
      "name": "loadEnhancer",
      "file": "packages/core/injector/injector.ts",
      "lines": [
        892,
        892
      ],
      "weight": 0.29,
      "behavior": "Function loadEnhancer."
    },
    {
      "id": "n10",
      "class": "utility",
      "name": "mapFactoryProviderInjectArray",
      "file": "packages/core/injector/injector.ts",
      "lines": [
        419,
        419
      ],
      "weight": 0.21,
      "behavior": "Function mapFactoryProviderInjectArray."
    },
    {
      "id": "n11",
      "class": "utility",
      "name": "resolveParam",
      "file": "packages/core/injector/injector.ts",
      "lines": [
        318,
        318
      ],
      "weight": 0.14,
      "behavior": "Function resolveParam."
    },
    {
      "id": "n12",
      "class": "module_root",
      "name": "packages/core/errors/exceptions/circular-dependency.exception.ts",
      "file": "packages/core/errors/exceptions/circular-dependency.exception.ts",
      "lines": [
        1,
        11
      ],
      "weight": 0.08,
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
    "confidence": 0.93,
    "hint": "clue_only",
    "gaps": []
  }
}
```

## Required Output
- List every file that must be modified
- List every function/class that is involved (cite entity IDs)
- Explain the execution/impact path based on the clue
- Identify what additional source you would need via drill-down