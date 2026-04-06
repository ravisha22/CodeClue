You are a senior software engineer performing a development task.
You have access to a CodeClue artifact — a compact comprehension file
that describes the relevant code subsystem. Use it to plan your approach.

## Task
Audit Flask's session handling for security vulnerabilities. List every file involved in session creation, signing, and cookie setting.

## CodeClue Artifact
```json
{
  "task": {
    "id": "trace-OF5-20260403093054",
    "repo": "",
    "family": "OF5",
    "question": "Audit Flask's session handling for security vulnerabilities. List every file involved in session creation, signing, and cookie setting."
  },
  "summary": "get_signing_serializer: Function get_signing_serializer. open_session: Accesses data store. save_session: Accesses data store; may return None implicitly.",
  "entities": [
    {
      "id": "n1",
      "class": "utility",
      "name": "get_signing_serializer",
      "file": "src/flask/sessions.py",
      "lines": [
        303,
        321
      ],
      "confidence": 0.77,
      "purpose": "function get_signing_serializer",
      "behavior": "Function get_signing_serializer.",
      "sig": "def get_signing_serializer(self, app: Flask) -> URLSafeTimedSerializer | None:"
    },
    {
      "id": "n2",
      "class": "data_accessor",
      "name": "open_session",
      "file": "src/flask/sessions.py",
      "lines": [
        323,
        335
      ],
      "confidence": 0.77,
      "purpose": "function open_session",
      "behavior": "Accesses data store.",
      "sig": "def open_session(self, app: Flask, request: Request) -> SecureCookieSession | None:"
    },
    {
      "id": "n3",
      "class": "data_accessor",
      "name": "save_session",
      "file": "src/flask/sessions.py",
      "lines": [
        337,
        385
      ],
      "confidence": 0.77,
      "purpose": "function save_session",
      "behavior": "Accesses data store; may return None implicitly.",
      "sig": "def save_session( self, app: Flask, session: SessionMixin, response: Response ) -> None:",
      "risks": [
        "implicit_none_return"
      ]
    },
    {
      "id": "n4",
      "class": "utility",
      "name": "get_cookie_domain",
      "file": "src/flask/sessions.py",
      "lines": [
        175,
        185
      ],
      "confidence": 0.77,
      "purpose": "function get_cookie_domain",
      "behavior": "Function get_cookie_domain.",
      "sig": "def get_cookie_domain(self, app: Flask) -> str | None:"
    },
    {
      "id": "n5",
      "class": "utility",
      "name": "get_cookie_httponly",
      "file": "src/flask/sessions.py",
      "lines": [
        195,
        200
      ],
      "confidence": 0.77,
      "purpose": "function get_cookie_httponly",
      "behavior": "Function get_cookie_httponly.",
      "sig": "def get_cookie_httponly(self, app: Flask) -> bool:"
    },
    {
      "id": "n6",
      "class": "utility",
      "name": "get_cookie_name",
      "file": "src/flask/sessions.py",
      "lines": [
        171,
        173
      ],
      "confidence": 0.77,
      "purpose": "function get_cookie_name",
      "behavior": "Function get_cookie_name.",
      "sig": "def get_cookie_name(self, app: Flask) -> str:"
    },
    {
      "id": "n7",
      "class": "utility",
      "name": "get_cookie_partitioned",
      "file": "src/flask/sessions.py",
      "lines": [
        215,
        221
      ],
      "confidence": 0.77,
      "purpose": "function get_cookie_partitioned",
      "behavior": "Function get_cookie_partitioned.",
      "sig": "def get_cookie_partitioned(self, app: Flask) -> bool:"
    },
    {
      "id": "n8",
      "class": "utility",
      "name": "get_cookie_path",
      "file": "src/flask/sessions.py",
      "lines": [
        187,
        193
      ],
      "confidence": 0.77,
      "purpose": "function get_cookie_path",
      "behavior": "Function get_cookie_path.",
      "sig": "def get_cookie_path(self, app: Flask) -> str:"
    },
    {
      "id": "n9",
      "class": "utility",
      "name": "get_cookie_samesite",
      "file": "src/flask/sessions.py",
      "lines": [
        208,
        213
      ],
      "confidence": 0.77,
      "purpose": "function get_cookie_samesite",
      "behavior": "Function get_cookie_samesite.",
      "sig": "def get_cookie_samesite(self, app: Flask) -> str | None:"
    },
    {
      "id": "n10",
      "class": "utility",
      "name": "get_cookie_secure",
      "file": "src/flask/sessions.py",
      "lines": [
        202,
        206
      ],
      "confidence": 0.77,
      "purpose": "function get_cookie_secure",
      "behavior": "Function get_cookie_secure.",
      "sig": "def get_cookie_secure(self, app: Flask) -> bool:"
    },
    {
      "id": "n11",
      "class": "utility",
      "name": "should_set_cookie",
      "file": "src/flask/sessions.py",
      "lines": [
        233,
        247
      ],
      "confidence": 0.77,
      "purpose": "function should_set_cookie",
      "behavior": "Function should_set_cookie.",
      "sig": "def should_set_cookie(self, app: Flask, session: SessionMixin) -> bool:"
    },
    {
      "id": "n12",
      "class": "data_accessor",
      "name": "_get_session",
      "file": "src/flask/ctx.py",
      "lines": [
        381,
        393
      ],
      "confidence": 0.77,
      "purpose": "function _get_session",
      "behavior": "Accesses data store; mutates state outside __init__.",
      "sig": "def _get_session(self) -> SessionMixin:",
      "called_by": [
        "push",
        "n13"
      ],
      "risks": [
        "state_mutation_outside_init"
      ]
    },
    {
      "id": "n13",
      "class": "data_accessor",
      "name": "session",
      "file": "src/flask/ctx.py",
      "lines": [
        396,
        403
      ],
      "confidence": 0.77,
      "purpose": "function session",
      "behavior": "Accesses data store.",
      "sig": "def session(self) -> SessionMixin:",
      "calls": [
        "n12"
      ]
    },
    {
      "id": "n14",
      "class": "data_accessor",
      "name": "is_null_session",
      "file": "src/flask/sessions.py",
      "lines": [
        162,
        169
      ],
      "confidence": 0.77,
      "purpose": "function is_null_session",
      "behavior": "Accesses data store.",
      "sig": "def is_null_session(self, obj: object) -> bool:"
    },
    {
      "id": "n15",
      "class": "data_accessor",
      "name": "make_null_session",
      "file": "src/flask/sessions.py",
      "lines": [
        150,
        160
      ],
      "confidence": 0.77,
      "purpose": "function make_null_session",
      "behavior": "Accesses data store.",
      "sig": "def make_null_session(self, app: Flask) -> NullSession:"
    }
  ],
  "uncertainty": {
    "confidence": 1.0,
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