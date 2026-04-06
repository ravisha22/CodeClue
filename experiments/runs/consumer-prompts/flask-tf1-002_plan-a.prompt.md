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
How are Flask blueprints structured?

## Clue Artifact (Entity-Centric)
```json
{
  "task": {
    "id": "trace-OF1-20260403093059",
    "repo": "",
    "family": "OF1",
    "operation_family": "OF1",
    "question": "How are Flask blueprints structured?"
  },
  "summary": "__init__: Middleware between upstream and downstream. get_send_file_max_age: Leaf handler invoked by dispatcher. open_resource: Function open_resource.",
  "entities": [
    {
      "id": "n1",
      "class": "middleware",
      "name": "__init__",
      "file": "src/flask/blueprints.py",
      "lines": [
        19,
        53
      ],
      "weight": 0.92,
      "behavior": "Middleware between upstream and downstream.",
      "sig": "def __init__( self, name: str, import_name: str, static_folder: str | os.PathLike[str] | None = None, static_url_path: str | None = None, template_folder: str | os.PathLike[str] | None = None, url_..."
    },
    {
      "id": "n2",
      "class": "handler",
      "name": "get_send_file_max_age",
      "file": "src/flask/blueprints.py",
      "lines": [
        55,
        80
      ],
      "weight": 0.86,
      "behavior": "Leaf handler invoked by dispatcher.",
      "sig": "def get_send_file_max_age(self, filename: str | None) -> int | None:"
    },
    {
      "id": "n3",
      "class": "utility",
      "name": "open_resource",
      "file": "src/flask/blueprints.py",
      "lines": [
        104,
        128
      ],
      "weight": 0.8,
      "behavior": "Function open_resource.",
      "sig": "def open_resource( self, resource: str, mode: str = \"rb\", encoding: str | None = \"utf-8\" ) -> t.IO[t.AnyStr]:"
    },
    {
      "id": "n4",
      "class": "entrypoint",
      "name": "send_static_file",
      "file": "src/flask/blueprints.py",
      "lines": [
        82,
        102
      ],
      "weight": 0.74,
      "behavior": "Entrypoint that delegates to downstream handlers.",
      "sig": "def send_static_file(self, filename: str) -> Response:"
    },
    {
      "id": "n5",
      "class": "utility",
      "name": "Blueprint",
      "file": "src/flask/blueprints.py",
      "lines": [
        18,
        128
      ],
      "weight": 0.67,
      "behavior": "Class Blueprint.",
      "sig": "def __init__( self, name: str, import_name: str, static_folder: str | os.PathLike[str] | None = None, static_url_path: str | None = None, template_folder: str | os.PathLike[str] | None = None, url_..."
    },
    {
      "id": "n6",
      "class": "middleware",
      "name": "__init__",
      "file": "src/flask/sansio/app.py",
      "lines": [
        279,
        408
      ],
      "weight": 0.61,
      "behavior": "Middleware between upstream and downstream.",
      "sig": "def __init__( self, import_name: str, static_url_path: str | None = None, static_folder: str | os.PathLike[str] | None = \"static\", static_host: str | None = None, host_matching: bool = False, subdo..."
    },
    {
      "id": "n7",
      "class": "validator",
      "name": "_check_setup_finished",
      "file": "src/flask/sansio/app.py",
      "lines": [
        410,
        420
      ],
      "weight": 0.55,
      "behavior": "Validates input before processing.",
      "sig": "def _check_setup_finished(self, f_name: str) -> None:"
    },
    {
      "id": "n8",
      "class": "error_handler",
      "name": "_find_error_handler",
      "file": "src/flask/sansio/app.py",
      "lines": [
        865,
        888
      ],
      "weight": 0.49,
      "behavior": "Error handler; produces error response.",
      "sig": "def _find_error_handler( self, e: Exception, blueprints: list[str] ) -> ft.ErrorHandlerCallable | None:"
    },
    {
      "id": "n9",
      "class": "utility",
      "name": "add_template_filter",
      "file": "src/flask/sansio/app.py",
      "lines": [
        696,
        708
      ],
      "weight": 0.43,
      "behavior": "Function add_template_filter.",
      "sig": "def add_template_filter( self, f: ft.TemplateFilterCallable, name: str | None = None ) -> None:"
    },
    {
      "id": "n10",
      "class": "utility",
      "name": "add_template_global",
      "file": "src/flask/sansio/app.py",
      "lines": [
        807,
        821
      ],
      "weight": 0.37,
      "behavior": "Function add_template_global.",
      "sig": "def add_template_global( self, f: ft.TemplateGlobalCallable, name: str | None = None ) -> None:"
    },
    {
      "id": "n11",
      "class": "utility",
      "name": "add_template_test",
      "file": "src/flask/sansio/app.py",
      "lines": [
        753,
        767
      ],
      "weight": 0.31,
      "behavior": "Function add_template_test.",
      "sig": "def add_template_test( self, f: ft.TemplateTestCallable, name: str | None = None ) -> None:"
    },
    {
      "id": "n12",
      "class": "utility",
      "name": "add_url_rule",
      "file": "src/flask/sansio/app.py",
      "lines": [
        602,
        658
      ],
      "weight": 0.25,
      "behavior": "Function add_url_rule.",
      "sig": "def add_url_rule( self, rule: str, endpoint: str | None = None, view_func: ft.RouteCallable | None = None, provide_automatic_options: bool | None = None, **options: t.Any, ) -> None:"
    },
    {
      "id": "n13",
      "class": "data_accessor",
      "name": "auto_find_instance_path",
      "file": "src/flask/sansio/app.py",
      "lines": [
        507,
        518
      ],
      "weight": 0.18,
      "behavior": "Accesses data store.",
      "sig": "def auto_find_instance_path(self) -> str:"
    },
    {
      "id": "n14",
      "class": "utility",
      "name": "create_global_jinja_loader",
      "file": "src/flask/sansio/app.py",
      "lines": [
        520,
        531
      ],
      "weight": 0.12,
      "behavior": "Function create_global_jinja_loader.",
      "sig": "def create_global_jinja_loader(self) -> DispatchingJinjaLoader:"
    },
    {
      "id": "n15",
      "class": "utility",
      "name": "create_jinja_environment",
      "file": "src/flask/sansio/app.py",
      "lines": [
        476,
        477
      ],
      "weight": 0.06,
      "behavior": "Function create_jinja_environment.",
      "sig": "def create_jinja_environment(self) -> Environment:"
    }
  ],
  "uncertainty": {
    "confidence": 0.97,
    "hint": "clue_only",
    "gaps": [
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
- **Key entities**: List the entity IDs most relevant to your answer
- **Evidence**: Brief explanation of how the clue entities support your answer
- **Confidence**: How confident you are (high/medium/low) based on the clue alone
- **Gaps**: Any information you would need but is missing from the clue
