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
Security in Express request parsing?

## Clue Artifact (Flat-Table)
```json
{
  "task": {
    "id": "trace-OF5-20260403094653",
    "repo": "",
    "family": "OF5",
    "operation_family": "OF5",
    "question": "Security in Express request parsing?"
  },
  "clue_summary": {
    "system_behavior": [
      "authenticate: Function authenticate.",
      "restrict: Function restrict.",
      "defineGetter: Function defineGetter.",
      "header: Function header.",
      "host: Function host."
    ],
    "key_files": [
      "examples/auth/index.js",
      "lib/request.js"
    ],
    "key_symbols": [
      "authenticate",
      "restrict",
      "defineGetter",
      "header",
      "host"
    ]
  },
  "nodes": [
    {
      "id": "n1",
      "type": "function",
      "name": "authenticate",
      "summary": "Function authenticate.",
      "file": "examples/auth/index.js",
      "lines": [
        60,
        60
      ],
      "importance": 1,
      "role": "utility",
      "sig": "function authenticate(name, pass, fn)"
    },
    {
      "id": "n2",
      "type": "function",
      "name": "restrict",
      "summary": "Function restrict.",
      "file": "examples/auth/index.js",
      "lines": [
        75,
        75
      ],
      "importance": 2,
      "role": "utility",
      "sig": "function restrict(req, res, next)"
    },
    {
      "id": "n3",
      "type": "function",
      "name": "defineGetter",
      "summary": "Function defineGetter.",
      "file": "lib/request.js",
      "lines": [
        521,
        521
      ],
      "importance": 3,
      "role": "utility",
      "sig": "function defineGetter(obj, name, getter)"
    },
    {
      "id": "n4",
      "type": "function",
      "name": "header",
      "summary": "Function header.",
      "file": "lib/request.js",
      "lines": [
        64,
        64
      ],
      "importance": 4,
      "role": "utility",
      "sig": "function header(name)"
    },
    {
      "id": "n5",
      "type": "function",
      "name": "host",
      "summary": "Function host.",
      "file": "lib/request.js",
      "lines": [
        418,
        418
      ],
      "importance": 5,
      "role": "utility",
      "sig": "function host()"
    },
    {
      "id": "n6",
      "type": "function",
      "name": "hostname",
      "summary": "Function hostname.",
      "file": "lib/request.js",
      "lines": [
        444,
        444
      ],
      "importance": 6,
      "role": "utility",
      "sig": "function hostname()"
    },
    {
      "id": "n7",
      "type": "function",
      "name": "ip",
      "summary": "Function ip.",
      "file": "lib/request.js",
      "lines": [
        340,
        340
      ],
      "importance": 7,
      "role": "utility",
      "sig": "function ip()"
    },
    {
      "id": "n8",
      "type": "function",
      "name": "ips",
      "summary": "Function ips.",
      "file": "lib/request.js",
      "lines": [
        357,
        357
      ],
      "importance": 8,
      "role": "utility",
      "sig": "function ips()"
    },
    {
      "id": "n9",
      "type": "function",
      "name": "is",
      "summary": "Function is.",
      "file": "lib/request.js",
      "lines": [
        269,
        269
      ],
      "importance": 9,
      "role": "utility",
      "sig": "function is(types)"
    },
    {
      "id": "n10",
      "type": "function",
      "name": "path",
      "summary": "Function path.",
      "file": "lib/request.js",
      "lines": [
        403,
        403
      ],
      "importance": 10,
      "role": "utility",
      "sig": "function path()"
    },
    {
      "id": "n11",
      "type": "function",
      "name": "protocol",
      "summary": "Function protocol.",
      "file": "lib/request.js",
      "lines": [
        297,
        297
      ],
      "importance": 11,
      "role": "utility",
      "sig": "function protocol()"
    },
    {
      "id": "n12",
      "type": "function",
      "name": "query",
      "summary": "Accesses data store.",
      "file": "lib/request.js",
      "lines": [
        230,
        230
      ],
      "importance": 12,
      "role": "data_accessor",
      "sig": "function query()"
    },
    {
      "id": "n13",
      "type": "function",
      "name": "range",
      "summary": "Function range.",
      "file": "lib/request.js",
      "lines": [
        214,
        214
      ],
      "importance": 13,
      "role": "utility",
      "sig": "function range(size, options)"
    },
    {
      "id": "n14",
      "type": "function",
      "name": "secure",
      "summary": "Function secure.",
      "file": "lib/request.js",
      "lines": [
        326,
        326
      ],
      "importance": 14,
      "role": "utility",
      "sig": "function secure()"
    },
    {
      "id": "n15",
      "type": "function",
      "name": "stale",
      "summary": "Function stale.",
      "file": "lib/request.js",
      "lines": [
        497,
        497
      ],
      "importance": 15,
      "role": "utility",
      "sig": "function stale()"
    }
  ],
  "relations": [],
  "assertions": [],
  "uncertainty": {
    "overall_confidence": 0.97,
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
