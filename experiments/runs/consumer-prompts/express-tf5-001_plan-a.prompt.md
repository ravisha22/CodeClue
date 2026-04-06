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
Security in Express request parsing?

## Clue Artifact (Entity-Centric)
```json
{
  "task": {
    "id": "trace-OF5-20260403094653",
    "repo": "",
    "family": "OF5",
    "operation_family": "OF5",
    "question": "Security in Express request parsing?"
  },
  "summary": "authenticate: Function authenticate. restrict: Function restrict. defineGetter: Function defineGetter.",
  "entities": [
    {
      "id": "n1",
      "class": "utility",
      "name": "authenticate",
      "file": "examples/auth/index.js",
      "lines": [
        60,
        60
      ],
      "weight": 0.86,
      "behavior": "Function authenticate.",
      "sig": "function authenticate(name, pass, fn)"
    },
    {
      "id": "n2",
      "class": "utility",
      "name": "restrict",
      "file": "examples/auth/index.js",
      "lines": [
        75,
        75
      ],
      "weight": 0.8,
      "behavior": "Function restrict.",
      "sig": "function restrict(req, res, next)"
    },
    {
      "id": "n3",
      "class": "utility",
      "name": "defineGetter",
      "file": "lib/request.js",
      "lines": [
        521,
        521
      ],
      "weight": 0.75,
      "behavior": "Function defineGetter.",
      "sig": "function defineGetter(obj, name, getter)"
    },
    {
      "id": "n4",
      "class": "utility",
      "name": "header",
      "file": "lib/request.js",
      "lines": [
        64,
        64
      ],
      "weight": 0.69,
      "behavior": "Function header.",
      "sig": "function header(name)"
    },
    {
      "id": "n5",
      "class": "utility",
      "name": "host",
      "file": "lib/request.js",
      "lines": [
        418,
        418
      ],
      "weight": 0.63,
      "behavior": "Function host.",
      "sig": "function host()"
    },
    {
      "id": "n6",
      "class": "utility",
      "name": "hostname",
      "file": "lib/request.js",
      "lines": [
        444,
        444
      ],
      "weight": 0.57,
      "behavior": "Function hostname.",
      "sig": "function hostname()"
    },
    {
      "id": "n7",
      "class": "utility",
      "name": "ip",
      "file": "lib/request.js",
      "lines": [
        340,
        340
      ],
      "weight": 0.52,
      "behavior": "Function ip.",
      "sig": "function ip()"
    },
    {
      "id": "n8",
      "class": "utility",
      "name": "ips",
      "file": "lib/request.js",
      "lines": [
        357,
        357
      ],
      "weight": 0.46,
      "behavior": "Function ips.",
      "sig": "function ips()"
    },
    {
      "id": "n9",
      "class": "utility",
      "name": "is",
      "file": "lib/request.js",
      "lines": [
        269,
        269
      ],
      "weight": 0.4,
      "behavior": "Function is.",
      "sig": "function is(types)"
    },
    {
      "id": "n10",
      "class": "utility",
      "name": "path",
      "file": "lib/request.js",
      "lines": [
        403,
        403
      ],
      "weight": 0.34,
      "behavior": "Function path.",
      "sig": "function path()"
    },
    {
      "id": "n11",
      "class": "utility",
      "name": "protocol",
      "file": "lib/request.js",
      "lines": [
        297,
        297
      ],
      "weight": 0.29,
      "behavior": "Function protocol.",
      "sig": "function protocol()"
    },
    {
      "id": "n12",
      "class": "data_accessor",
      "name": "query",
      "file": "lib/request.js",
      "lines": [
        230,
        230
      ],
      "weight": 0.23,
      "behavior": "Accesses data store.",
      "sig": "function query()"
    },
    {
      "id": "n13",
      "class": "utility",
      "name": "range",
      "file": "lib/request.js",
      "lines": [
        214,
        214
      ],
      "weight": 0.17,
      "behavior": "Function range.",
      "sig": "function range(size, options)"
    },
    {
      "id": "n14",
      "class": "utility",
      "name": "secure",
      "file": "lib/request.js",
      "lines": [
        326,
        326
      ],
      "weight": 0.11,
      "behavior": "Function secure.",
      "sig": "function secure()"
    },
    {
      "id": "n15",
      "class": "utility",
      "name": "stale",
      "file": "lib/request.js",
      "lines": [
        497,
        497
      ],
      "weight": 0.06,
      "behavior": "Function stale.",
      "sig": "function stale()"
    }
  ],
  "uncertainty": {
    "confidence": 0.97,
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
