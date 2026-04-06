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
  "summary": "load_logged_in_user: Function load_logged_in_user. login: Function login. wrapped_view: Function wrapped_view.",
  "entities": [
    {
      "id": "n1",
      "class": "utility",
      "name": "load_logged_in_user",
      "file": "examples/tutorial/flaskr/auth.py",
      "lines": [
        33,
        43
      ],
      "confidence": 0.77,
      "purpose": "function load_logged_in_user",
      "behavior": "Function load_logged_in_user.",
      "sig": "def load_logged_in_user():"
    },
    {
      "id": "n2",
      "class": "utility",
      "name": "login",
      "file": "examples/tutorial/flaskr/auth.py",
      "lines": [
        85,
        109
      ],
      "confidence": 0.77,
      "purpose": "function login",
      "behavior": "Function login.",
      "sig": "def login():"
    },
    {
      "id": "n3",
      "class": "utility",
      "name": "wrapped_view",
      "file": "examples/tutorial/flaskr/auth.py",
      "lines": [
        23,
        27
      ],
      "confidence": 0.77,
      "purpose": "function wrapped_view",
      "behavior": "Function wrapped_view.",
      "sig": "def wrapped_view(**kwargs):"
    },
    {
      "id": "n4",
      "class": "utility",
      "name": "login_required",
      "file": "examples/tutorial/flaskr/auth.py",
      "lines": [
        19,
        29
      ],
      "confidence": 0.77,
      "purpose": "function login_required",
      "behavior": "Function login_required.",
      "sig": "def login_required(view):"
    },
    {
      "id": "n5",
      "class": "utility",
      "name": "logout",
      "file": "examples/tutorial/flaskr/auth.py",
      "lines": [
        113,
        116
      ],
      "confidence": 0.77,
      "purpose": "function logout",
      "behavior": "Function logout.",
      "sig": "def logout():"
    },
    {
      "id": "n6",
      "class": "utility",
      "name": "register",
      "file": "examples/tutorial/flaskr/auth.py",
      "lines": [
        47,
        81
      ],
      "confidence": 0.77,
      "purpose": "function register",
      "behavior": "Function register.",
      "sig": "def register():"
    },
    {
      "id": "n7",
      "class": "utility",
      "name": "__init__",
      "file": "examples/tutorial/tests/conftest.py",
      "lines": [
        48,
        49
      ],
      "confidence": 0.77,
      "purpose": "function __init__",
      "behavior": "Function __init__.",
      "sig": "def __init__(self, client):"
    },
    {
      "id": "n8",
      "class": "utility",
      "name": "login",
      "file": "examples/tutorial/tests/conftest.py",
      "lines": [
        51,
        54
      ],
      "confidence": 0.77,
      "purpose": "function login",
      "behavior": "Function login.",
      "sig": "def login(self, username=\"test\", password=\"test\"):"
    },
    {
      "id": "n9",
      "class": "utility",
      "name": "logout",
      "file": "examples/tutorial/tests/conftest.py",
      "lines": [
        56,
        57
      ],
      "confidence": 0.77,
      "purpose": "function logout",
      "behavior": "Function logout.",
      "sig": "def logout(self):"
    },
    {
      "id": "n10",
      "class": "handler",
      "name": "AuthActions",
      "file": "examples/tutorial/tests/conftest.py",
      "lines": [
        47,
        57
      ],
      "confidence": 0.77,
      "purpose": "class AuthActions",
      "behavior": "Leaf handler invoked by auth.",
      "sig": "def __init__(self, client):",
      "called_by": [
        "n12"
      ]
    },
    {
      "id": "n11",
      "class": "utility",
      "name": "app",
      "file": "examples/tutorial/tests/conftest.py",
      "lines": [
        16,
        32
      ],
      "confidence": 0.77,
      "purpose": "function app",
      "behavior": "Function app.",
      "sig": "def app():"
    },
    {
      "id": "n12",
      "class": "entrypoint",
      "name": "auth",
      "file": "examples/tutorial/tests/conftest.py",
      "lines": [
        61,
        62
      ],
      "confidence": 0.77,
      "purpose": "function auth",
      "behavior": "Entrypoint that delegates to AuthActions.",
      "sig": "def auth(client):",
      "calls": [
        "n10"
      ]
    },
    {
      "id": "n13",
      "class": "utility",
      "name": "client",
      "file": "examples/tutorial/tests/conftest.py",
      "lines": [
        36,
        38
      ],
      "confidence": 0.77,
      "purpose": "function client",
      "behavior": "Function client.",
      "sig": "def client(app):"
    },
    {
      "id": "n14",
      "class": "utility",
      "name": "runner",
      "file": "examples/tutorial/tests/conftest.py",
      "lines": [
        42,
        44
      ],
      "confidence": 0.77,
      "purpose": "function runner",
      "behavior": "Function runner.",
      "sig": "def runner(app):"
    },
    {
      "id": "n15",
      "class": "utility",
      "name": "test_login",
      "file": "examples/tutorial/tests/test_auth.py",
      "lines": [
        39,
        52
      ],
      "confidence": 0.77,
      "purpose": "function test_login",
      "behavior": "Function test_login.",
      "sig": "def test_login(client, auth):"
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