You are a senior software engineer performing a development task.
You have access to a CodeClue artifact — a compact comprehension file
that describes the relevant code subsystem. Use it to plan your approach.

## Task
Audit Gin's middleware chain for security risks. Identify where auth middleware runs relative to route handlers and whether middleware can be bypassed.

## CodeClue Artifact
```json
{
  "task": {
    "id": "trace-OF5-20260403094901",
    "repo": "",
    "family": "OF5",
    "question": "Audit Gin's middleware chain for security risks. Identify where auth middleware runs relative to route handlers and whether middleware can be bypassed."
  },
  "summary": "BasicAuth: Function BasicAuth. BasicAuthForProxy: Function BasicAuthForProxy. BasicAuthForRealm: Function BasicAuthForRealm.",
  "entities": [
    {
      "id": "n1",
      "class": "utility",
      "name": "BasicAuth",
      "file": "auth.go",
      "lines": [
        72,
        72
      ],
      "confidence": 0.71,
      "purpose": "function BasicAuth",
      "behavior": "Function BasicAuth.",
      "sig": "func BasicAuth(accounts Accounts) HandlerFunc",
      "called_by": [
        "auth.go"
      ]
    },
    {
      "id": "n2",
      "class": "utility",
      "name": "BasicAuthForProxy",
      "file": "auth.go",
      "lines": [
        98,
        98
      ],
      "confidence": 0.71,
      "purpose": "function BasicAuthForProxy",
      "behavior": "Function BasicAuthForProxy.",
      "sig": "func BasicAuthForProxy(accounts Accounts, realm string) HandlerFunc",
      "called_by": [
        "auth.go"
      ]
    },
    {
      "id": "n3",
      "class": "utility",
      "name": "BasicAuthForRealm",
      "file": "auth.go",
      "lines": [
        48,
        48
      ],
      "confidence": 0.71,
      "purpose": "function BasicAuthForRealm",
      "behavior": "Function BasicAuthForRealm.",
      "sig": "func BasicAuthForRealm(accounts Accounts, realm string) HandlerFunc",
      "called_by": [
        "auth.go"
      ]
    },
    {
      "id": "n4",
      "class": "utility",
      "name": "authPair",
      "file": "auth.go",
      "lines": [
        25,
        25
      ],
      "confidence": 0.71,
      "purpose": "struct authPair",
      "behavior": "Struct authPair."
    },
    {
      "id": "n5",
      "class": "utility",
      "name": "authorizationHeader",
      "file": "auth.go",
      "lines": [
        91,
        91
      ],
      "confidence": 0.71,
      "purpose": "function authorizationHeader",
      "behavior": "Function authorizationHeader.",
      "sig": "func authorizationHeader(user, password string) string",
      "called_by": [
        "auth.go"
      ]
    },
    {
      "id": "n6",
      "class": "utility",
      "name": "processAccounts",
      "file": "auth.go",
      "lines": [
        76,
        76
      ],
      "confidence": 0.71,
      "purpose": "function processAccounts",
      "behavior": "Function processAccounts.",
      "sig": "func processAccounts(accounts Accounts) authPairs",
      "called_by": [
        "auth.go"
      ]
    },
    {
      "id": "n7",
      "class": "utility",
      "name": "searchCredential",
      "file": "auth.go",
      "lines": [
        32,
        32
      ],
      "confidence": 0.71,
      "purpose": "function searchCredential",
      "behavior": "Function searchCredential.",
      "sig": "func (a authPairs) searchCredential(authValue string) (string, bool)",
      "called_by": [
        "auth.go"
      ]
    },
    {
      "id": "n8",
      "class": "utility",
      "name": "TestBasicAuth401",
      "file": "auth_test.go",
      "lines": [
        101,
        101
      ],
      "confidence": 0.71,
      "purpose": "function TestBasicAuth401",
      "behavior": "Function TestBasicAuth401.",
      "sig": "func TestBasicAuth401(t *testing.T)",
      "called_by": [
        "auth_test.go"
      ]
    },
    {
      "id": "n9",
      "class": "utility",
      "name": "TestBasicAuth401WithCustomRealm",
      "file": "auth_test.go",
      "lines": [
        121,
        121
      ],
      "confidence": 0.71,
      "purpose": "function TestBasicAuth401WithCustomRealm",
      "behavior": "Function TestBasicAuth401WithCustomRealm.",
      "sig": "func TestBasicAuth401WithCustomRealm(t *testing.T)",
      "called_by": [
        "auth_test.go"
      ]
    },
    {
      "id": "n10",
      "class": "utility",
      "name": "TestBasicAuth",
      "file": "auth_test.go",
      "lines": [
        16,
        16
      ],
      "confidence": 0.71,
      "purpose": "function TestBasicAuth",
      "behavior": "Function TestBasicAuth.",
      "sig": "func TestBasicAuth(t *testing.T)",
      "called_by": [
        "auth_test.go"
      ]
    },
    {
      "id": "n11",
      "class": "utility",
      "name": "TestBasicAuthAuthorizationHeader",
      "file": "auth_test.go",
      "lines": [
        80,
        80
      ],
      "confidence": 0.71,
      "purpose": "function TestBasicAuthAuthorizationHeader",
      "behavior": "Function TestBasicAuthAuthorizationHeader.",
      "sig": "func TestBasicAuthAuthorizationHeader(t *testing.T)",
      "called_by": [
        "auth_test.go"
      ]
    },
    {
      "id": "n12",
      "class": "utility",
      "name": "TestBasicAuthFails",
      "file": "auth_test.go",
      "lines": [
        38,
        38
      ],
      "confidence": 0.71,
      "purpose": "function TestBasicAuthFails",
      "behavior": "Function TestBasicAuthFails.",
      "sig": "func TestBasicAuthFails(t *testing.T)",
      "called_by": [
        "auth_test.go"
      ]
    },
    {
      "id": "n13",
      "class": "utility",
      "name": "TestBasicAuthForProxy407",
      "file": "auth_test.go",
      "lines": [
        158,
        158
      ],
      "confidence": 0.71,
      "purpose": "function TestBasicAuthForProxy407",
      "behavior": "Function TestBasicAuthForProxy407.",
      "sig": "func TestBasicAuthForProxy407(t *testing.T)",
      "called_by": [
        "auth_test.go"
      ]
    },
    {
      "id": "n14",
      "class": "utility",
      "name": "TestBasicAuthForProxySucceed",
      "file": "auth_test.go",
      "lines": [
        141,
        141
      ],
      "confidence": 0.71,
      "purpose": "function TestBasicAuthForProxySucceed",
      "behavior": "Function TestBasicAuthForProxySucceed.",
      "sig": "func TestBasicAuthForProxySucceed(t *testing.T)",
      "called_by": [
        "auth_test.go"
      ]
    },
    {
      "id": "n15",
      "class": "utility",
      "name": "TestBasicAuthSearchCredential",
      "file": "auth_test.go",
      "lines": [
        48,
        48
      ],
      "confidence": 0.71,
      "purpose": "function TestBasicAuthSearchCredential",
      "behavior": "Function TestBasicAuthSearchCredential.",
      "sig": "func TestBasicAuthSearchCredential(t *testing.T)",
      "called_by": [
        "auth_test.go"
      ]
    }
  ],
  "uncertainty": {
    "confidence": 0.64,
    "hint": "targeted_lookup",
    "gaps": []
  }
}
```

## Required Output
- List every file that must be modified
- List every function/class that is involved (cite entity IDs)
- Explain the execution/impact path based on the clue
- Identify what additional source you would need via drill-down