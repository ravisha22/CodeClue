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
Express middleware architecture?

## Clue Artifact (Entity-Centric)
```json
{
  "task": {
    "id": "trace-OF1-20260403094653",
    "repo": "",
    "family": "OF1",
    "operation_family": "OF1",
    "question": "Express middleware architecture?"
  },
  "summary": "andRestrictTo: Function andRestrictTo. andRestrictToSelf: Function andRestrictToSelf. loadUser: Function loadUser.",
  "entities": [
    {
      "id": "n1",
      "class": "utility",
      "name": "andRestrictTo",
      "file": "examples/route-middleware/index.js",
      "lines": [
        50,
        50
      ],
      "weight": 0.86,
      "behavior": "Function andRestrictTo.",
      "sig": "function andRestrictTo(role)"
    },
    {
      "id": "n2",
      "class": "utility",
      "name": "andRestrictToSelf",
      "file": "examples/route-middleware/index.js",
      "lines": [
        36,
        36
      ],
      "weight": 0.8,
      "behavior": "Function andRestrictToSelf.",
      "sig": "function andRestrictToSelf(req, res, next)"
    },
    {
      "id": "n3",
      "class": "utility",
      "name": "loadUser",
      "file": "examples/route-middleware/index.js",
      "lines": [
        25,
        25
      ],
      "weight": 0.75,
      "behavior": "Function loadUser.",
      "sig": "function loadUser(req, res, next)"
    },
    {
      "id": "n4",
      "class": "utility",
      "name": "testMethod",
      "file": "test/Route.js",
      "lines": [
        78,
        78
      ],
      "weight": 0.69,
      "behavior": "Function testMethod.",
      "sig": "function testMethod(method)"
    },
    {
      "id": "n5",
      "class": "utility",
      "name": "fn1",
      "file": "test/Router.js",
      "lines": [
        481,
        481
      ],
      "weight": 0.63,
      "behavior": "Function fn1.",
      "sig": "function fn1(req, res, next)"
    },
    {
      "id": "n6",
      "class": "utility",
      "name": "fn2",
      "file": "test/Router.js",
      "lines": [
        486,
        486
      ],
      "weight": 0.57,
      "behavior": "Function fn2.",
      "sig": "function fn2(req, res, next)"
    },
    {
      "id": "n7",
      "class": "utility",
      "name": "no",
      "file": "test/Router.js",
      "lines": [
        463,
        463
      ],
      "weight": 0.52,
      "behavior": "Function no.",
      "sig": "function no()"
    },
    {
      "id": "n8",
      "class": "utility",
      "name": "testMethod",
      "file": "test/Router.js",
      "lines": [
        424,
        424
      ],
      "weight": 0.46,
      "behavior": "Function testMethod.",
      "sig": "function testMethod(method)"
    },
    {
      "id": "n9",
      "class": "error_handler",
      "name": "createError",
      "file": "test/app.route.js",
      "lines": [
        114,
        114
      ],
      "weight": 0.4,
      "behavior": "Error handler; produces error response.",
      "sig": "function createError (req, res, next)"
    },
    {
      "id": "n10",
      "class": "error_handler",
      "name": "createError",
      "file": "test/app.route.js",
      "lines": [
        133,
        133
      ],
      "weight": 0.34,
      "behavior": "Error handler; produces error response.",
      "sig": "function createError (req, res, next)"
    },
    {
      "id": "n11",
      "class": "error_handler",
      "name": "createError",
      "file": "test/app.route.js",
      "lines": [
        155,
        155
      ],
      "weight": 0.29,
      "behavior": "Error handler; produces error response.",
      "sig": "function createError (req, res, next)"
    },
    {
      "id": "n12",
      "class": "error_handler",
      "name": "createError",
      "file": "test/app.route.js",
      "lines": [
        177,
        177
      ],
      "weight": 0.23,
      "behavior": "Error handler; produces error response.",
      "sig": "function createError (req, res, next)"
    },
    {
      "id": "n13",
      "class": "error_handler",
      "name": "createError",
      "file": "test/app.route.js",
      "lines": [
        70,
        70
      ],
      "weight": 0.17,
      "behavior": "Error handler; produces error response.",
      "sig": "function createError (req, res, next)"
    },
    {
      "id": "n14",
      "class": "error_handler",
      "name": "createError",
      "file": "test/app.route.js",
      "lines": [
        92,
        92
      ],
      "weight": 0.11,
      "behavior": "Error handler; produces error response.",
      "sig": "function createError (req, res, next)"
    },
    {
      "id": "n15",
      "class": "error_handler",
      "name": "handleError",
      "file": "test/app.route.js",
      "lines": [
        100,
        100
      ],
      "weight": 0.06,
      "behavior": "Error handler; produces error response.",
      "sig": "function handleError (err, req, res, next)"
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
