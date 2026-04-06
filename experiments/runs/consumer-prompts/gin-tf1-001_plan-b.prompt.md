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
Gin router architecture?

## Clue Artifact (Flat-Table)
```json
{
  "task": {
    "id": "trace-OF1-20260403094853",
    "repo": "",
    "family": "OF1",
    "operation_family": "OF1",
    "question": "Gin router architecture?"
  },
  "clue_summary": {
    "system_behavior": [
      "Engine: Function Engine.",
      "Error: Error handler; produces error response.",
      "ValidateStruct: Function ValidateStruct.",
      "defaultValidator: Struct defaultValidator.",
      "lazyinit: Function lazyinit."
    ],
    "key_files": [
      "binding/default_validator.go",
      "context.go"
    ],
    "key_symbols": [
      "Engine",
      "Error",
      "ValidateStruct",
      "defaultValidator",
      "lazyinit"
    ]
  },
  "nodes": [
    {
      "id": "n1",
      "type": "function",
      "name": "Engine",
      "summary": "Function Engine.",
      "file": "binding/default_validator.go",
      "lines": [
        85,
        85
      ],
      "importance": 1,
      "role": "utility",
      "sig": "func (v *defaultValidator) Engine() any"
    },
    {
      "id": "n2",
      "type": "function",
      "name": "Error",
      "summary": "Error handler; produces error response.",
      "file": "binding/default_validator.go",
      "lines": [
        24,
        24
      ],
      "importance": 2,
      "role": "error_handler",
      "sig": "func (err SliceValidationError) Error() string"
    },
    {
      "id": "n3",
      "type": "function",
      "name": "ValidateStruct",
      "summary": "Function ValidateStruct.",
      "file": "binding/default_validator.go",
      "lines": [
        44,
        44
      ],
      "importance": 3,
      "role": "utility",
      "sig": "func (v *defaultValidator) ValidateStruct(obj any) error"
    },
    {
      "id": "n4",
      "type": "struct",
      "name": "defaultValidator",
      "summary": "Struct defaultValidator.",
      "file": "binding/default_validator.go",
      "lines": [
        16,
        16
      ],
      "importance": 4,
      "role": "utility"
    },
    {
      "id": "n5",
      "type": "function",
      "name": "lazyinit",
      "summary": "Function lazyinit.",
      "file": "binding/default_validator.go",
      "lines": [
        90,
        90
      ],
      "importance": 5,
      "role": "utility",
      "sig": "func (v *defaultValidator) lazyinit()"
    },
    {
      "id": "n6",
      "type": "function",
      "name": "validateStruct",
      "summary": "Function validateStruct.",
      "file": "binding/default_validator.go",
      "lines": [
        76,
        76
      ],
      "importance": 6,
      "role": "utility",
      "sig": "func (v *defaultValidator) validateStruct(obj any) error"
    },
    {
      "id": "n7",
      "type": "function",
      "name": "Abort",
      "summary": "Function Abort.",
      "file": "context.go",
      "lines": [
        207,
        207
      ],
      "importance": 7,
      "role": "utility",
      "sig": "func (c *Context) Abort()"
    },
    {
      "id": "n8",
      "type": "function",
      "name": "AbortWithError",
      "summary": "Error handler; produces error response.",
      "file": "context.go",
      "lines": [
        238,
        238
      ],
      "importance": 8,
      "role": "error_handler",
      "sig": "func (c *Context) AbortWithError(code int, err error)"
    },
    {
      "id": "n9",
      "type": "function",
      "name": "AbortWithStatus",
      "summary": "Function AbortWithStatus.",
      "file": "context.go",
      "lines": [
        213,
        213
      ],
      "importance": 9,
      "role": "utility",
      "sig": "func (c *Context) AbortWithStatus(code int)"
    },
    {
      "id": "n10",
      "type": "function",
      "name": "AbortWithStatusJSON",
      "summary": "Function AbortWithStatusJSON.",
      "file": "context.go",
      "lines": [
        230,
        230
      ],
      "importance": 10,
      "role": "utility",
      "sig": "func (c *Context) AbortWithStatusJSON(code int, jsonObj any)"
    },
    {
      "id": "n11",
      "type": "function",
      "name": "AbortWithStatusPureJSON",
      "summary": "Function AbortWithStatusPureJSON.",
      "file": "context.go",
      "lines": [
        222,
        222
      ],
      "importance": 11,
      "role": "utility",
      "sig": "func (c *Context) AbortWithStatusPureJSON(code int, jsonObj any)"
    },
    {
      "id": "n12",
      "type": "function",
      "name": "AddParam",
      "summary": "Function AddParam.",
      "file": "context.go",
      "lines": [
        512,
        512
      ],
      "importance": 12,
      "role": "utility",
      "sig": "func (c *Context) AddParam(key, value string)"
    },
    {
      "id": "n13",
      "type": "function",
      "name": "AsciiJSON",
      "summary": "Function AsciiJSON.",
      "file": "context.go",
      "lines": [
        1211,
        1211
      ],
      "importance": 13,
      "role": "utility",
      "sig": "func (c *Context) AsciiJSON(code int, obj any)"
    },
    {
      "id": "n14",
      "type": "function",
      "name": "BSON",
      "summary": "Function BSON.",
      "file": "context.go",
      "lines": [
        1249,
        1249
      ],
      "importance": 14,
      "role": "utility",
      "sig": "func (c *Context) BSON(code int, obj any)"
    },
    {
      "id": "n15",
      "type": "function",
      "name": "Bind",
      "summary": "Function Bind.",
      "file": "context.go",
      "lines": [
        757,
        757
      ],
      "importance": 15,
      "role": "utility",
      "sig": "func (c *Context) Bind(obj any) error"
    }
  ],
  "relations": [],
  "assertions": [],
  "uncertainty": {
    "overall_confidence": 0.73,
    "lookup_hint": "targeted_lookup",
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
