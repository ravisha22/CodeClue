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
How are Flask blueprints structured?

## Clue Artifact (Flat-Table)
```json
{
  "task": {
    "id": "trace-OF1-20260403093059",
    "repo": "",
    "family": "OF1",
    "operation_family": "OF1",
    "question": "How are Flask blueprints structured?"
  },
  "clue_summary": {
    "system_behavior": [
      "__init__: Middleware between upstream and downstream.",
      "get_send_file_max_age: Leaf handler invoked by dispatcher.",
      "open_resource: Function open_resource.",
      "send_static_file: Entrypoint that delegates to downstream handlers.",
      "Blueprint: Class Blueprint."
    ],
    "key_files": [
      "src/flask/blueprints.py",
      "src/flask/sansio/app.py"
    ],
    "key_symbols": [
      "__init__",
      "get_send_file_max_age",
      "open_resource",
      "send_static_file",
      "Blueprint"
    ]
  },
  "nodes": [
    {
      "id": "n1",
      "type": "function",
      "name": "__init__",
      "summary": "Middleware between upstream and downstream.",
      "file": "src/flask/blueprints.py",
      "lines": [
        19,
        53
      ],
      "importance": 1,
      "role": "middleware",
      "sig": "def __init__( self, name: str, import_name: str, static_folder: str | os.PathLike[str] | None = None, static_url_path: str | None = None, template_folder: str | os.PathLike[str] | None = None, url_..."
    },
    {
      "id": "n2",
      "type": "function",
      "name": "get_send_file_max_age",
      "summary": "Leaf handler invoked by dispatcher.",
      "file": "src/flask/blueprints.py",
      "lines": [
        55,
        80
      ],
      "importance": 2,
      "role": "handler",
      "sig": "def get_send_file_max_age(self, filename: str | None) -> int | None:"
    },
    {
      "id": "n3",
      "type": "function",
      "name": "open_resource",
      "summary": "Function open_resource.",
      "file": "src/flask/blueprints.py",
      "lines": [
        104,
        128
      ],
      "importance": 3,
      "role": "utility",
      "sig": "def open_resource( self, resource: str, mode: str = \"rb\", encoding: str | None = \"utf-8\" ) -> t.IO[t.AnyStr]:"
    },
    {
      "id": "n4",
      "type": "function",
      "name": "send_static_file",
      "summary": "Entrypoint that delegates to downstream handlers.",
      "file": "src/flask/blueprints.py",
      "lines": [
        82,
        102
      ],
      "importance": 4,
      "role": "entrypoint",
      "sig": "def send_static_file(self, filename: str) -> Response:"
    },
    {
      "id": "n5",
      "type": "class",
      "name": "Blueprint",
      "summary": "Class Blueprint.",
      "file": "src/flask/blueprints.py",
      "lines": [
        18,
        128
      ],
      "importance": 5,
      "role": "utility",
      "sig": "def __init__( self, name: str, import_name: str, static_folder: str | os.PathLike[str] | None = None, static_url_path: str | None = None, template_folder: str | os.PathLike[str] | None = None, url_..."
    },
    {
      "id": "n6",
      "type": "function",
      "name": "__init__",
      "summary": "Middleware between upstream and downstream.",
      "file": "src/flask/sansio/app.py",
      "lines": [
        279,
        408
      ],
      "importance": 6,
      "role": "middleware",
      "sig": "def __init__( self, import_name: str, static_url_path: str | None = None, static_folder: str | os.PathLike[str] | None = \"static\", static_host: str | None = None, host_matching: bool = False, subdo..."
    },
    {
      "id": "n7",
      "type": "function",
      "name": "_check_setup_finished",
      "summary": "Validates input before processing.",
      "file": "src/flask/sansio/app.py",
      "lines": [
        410,
        420
      ],
      "importance": 7,
      "role": "validator",
      "sig": "def _check_setup_finished(self, f_name: str) -> None:"
    },
    {
      "id": "n8",
      "type": "function",
      "name": "_find_error_handler",
      "summary": "Error handler; produces error response.",
      "file": "src/flask/sansio/app.py",
      "lines": [
        865,
        888
      ],
      "importance": 8,
      "role": "error_handler",
      "sig": "def _find_error_handler( self, e: Exception, blueprints: list[str] ) -> ft.ErrorHandlerCallable | None:"
    },
    {
      "id": "n9",
      "type": "function",
      "name": "add_template_filter",
      "summary": "Function add_template_filter.",
      "file": "src/flask/sansio/app.py",
      "lines": [
        696,
        708
      ],
      "importance": 9,
      "role": "utility",
      "sig": "def add_template_filter( self, f: ft.TemplateFilterCallable, name: str | None = None ) -> None:"
    },
    {
      "id": "n10",
      "type": "function",
      "name": "add_template_global",
      "summary": "Function add_template_global.",
      "file": "src/flask/sansio/app.py",
      "lines": [
        807,
        821
      ],
      "importance": 10,
      "role": "utility",
      "sig": "def add_template_global( self, f: ft.TemplateGlobalCallable, name: str | None = None ) -> None:"
    },
    {
      "id": "n11",
      "type": "function",
      "name": "add_template_test",
      "summary": "Function add_template_test.",
      "file": "src/flask/sansio/app.py",
      "lines": [
        753,
        767
      ],
      "importance": 11,
      "role": "utility",
      "sig": "def add_template_test( self, f: ft.TemplateTestCallable, name: str | None = None ) -> None:"
    },
    {
      "id": "n12",
      "type": "function",
      "name": "add_url_rule",
      "summary": "Function add_url_rule.",
      "file": "src/flask/sansio/app.py",
      "lines": [
        602,
        658
      ],
      "importance": 12,
      "role": "utility",
      "sig": "def add_url_rule( self, rule: str, endpoint: str | None = None, view_func: ft.RouteCallable | None = None, provide_automatic_options: bool | None = None, **options: t.Any, ) -> None:"
    },
    {
      "id": "n13",
      "type": "function",
      "name": "auto_find_instance_path",
      "summary": "Accesses data store.",
      "file": "src/flask/sansio/app.py",
      "lines": [
        507,
        518
      ],
      "importance": 13,
      "role": "data_accessor",
      "sig": "def auto_find_instance_path(self) -> str:"
    },
    {
      "id": "n14",
      "type": "function",
      "name": "create_global_jinja_loader",
      "summary": "Function create_global_jinja_loader.",
      "file": "src/flask/sansio/app.py",
      "lines": [
        520,
        531
      ],
      "importance": 14,
      "role": "utility",
      "sig": "def create_global_jinja_loader(self) -> DispatchingJinjaLoader:"
    },
    {
      "id": "n15",
      "type": "function",
      "name": "create_jinja_environment",
      "summary": "Function create_jinja_environment.",
      "file": "src/flask/sansio/app.py",
      "lines": [
        476,
        477
      ],
      "importance": 15,
      "role": "utility",
      "sig": "def create_jinja_environment(self) -> Environment:"
    }
  ],
  "relations": [],
  "assertions": [],
  "uncertainty": {
    "overall_confidence": 0.97,
    "lookup_hint": "clue_only",
    "known_gaps": [
      "Low confidence on this node; source verification recommended",
      "Low confidence on this node; source verification recommended",
      "Low confidence on this node; source verification recommended"
    ]
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
