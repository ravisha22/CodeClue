# Blind Evaluation Scoring — v23

## Scoring Rubric
- **COVERED**: Response describes the specific mechanism/behavior with supporting evidence. Core behavior must be identified, not just function named. If >50% of mechanism captured, score COVERED.
- **MISS**: Response does not contain the info, gives wrong behavior, or says it cannot determine.

---

## Requests

### blind-requests-struct-1 (4/4)
F1: COVERED — api.py explicitly described with request, get, post, put, patch, delete, options, head all delegating to request().
F2: COVERED — Session class in sessions.py described with prepare_request, send, get_adapter, mount, merge functions, and HTTP verb methods.
F3: COVERED — Request, PreparedRequest, Response all described under models.py with their roles and methods.
F4: COVERED — adapters.py described as transport adapter layer with build_response, request_url; exceptions module referenced throughout (InvalidSchema, MissingSchema, etc.).

### blind-requests-struct-2 (4/4)
F1: COVERED — Four layers explicitly enumerated: top-level convenience API, session orchestration, request/response models, transport adapters + supporting modules.
F2: COVERED — api.py functions described as "stateless HTTP verb functions" that "Constructs and sends a Request"; flow diagram shows Response as the output.
F3: COVERED — Session described as "stateful engine" managing "persistent settings, cookie jars, adapter mounting."
F4: COVERED — Request ("user-facing, immutable-ish request") clearly separated from PreparedRequest ("fully mutable…prepared object") in models layer.

### blind-requests-rel-1 (3/4)
F1: COVERED — "Request…Calls PreparedRequest" and "its job is to produce a PreparedRequest"; pipeline clearly described.
F2: COVERED — "Session.prepare_request…converts the user Request into a PreparedRequest, merging session-level settings via merge_hooks and merge_setting."
F3: COVERED — "Session.send…Send a given PreparedRequest"; build_response constructs Response from urllib3.
F4: MISS — Response.request back-reference to PreparedRequest is never mentioned; Response is described only with iter_content, json, raise_for_status, close.

### blind-requests-rel-2 (3/4)
F1: COVERED — "mount…Registers a connection adapter to a prefix. This means Session stores adapters keyed by URL prefix strings."
F2: MISS — Response explicitly says "whether it uses longest-prefix matching or first-match is not determinable." Descending prefix-length sorting not identified.
F3: COVERED — "get_adapter…Returns the appropriate connection adapter for the given URL" with ACCUMULATE behavior; InvalidSchema on no match.
F4: COVERED — HTTPAdapter described as "built-in HTTP Adapter for urllib3"; send takes PreparedRequest, build_response creates Response from urllib3 response.

### blind-requests-mech-1 (1/4)
F1: COVERED — "per-call (request-level) settings take precedence over session defaults" with merge_setting parameter ordering as evidence.
F2: MISS — Response says "whether None request settings fall through to session defaults…cannot be confirmed." None-suppression not identified.
F3: MISS — Request.prepare() as a standalone method that skips session state is not mentioned.
F4: MISS — merge_environment_settings described as part of Session.request flow, but the insight that manual prepared flow *requires* calling it separately is not captured.

### blind-requests-mech-2 (1/4)
F1: MISS — stream=False downloading immediately is not discussed; only streaming mechanics via iter_content are covered.
F2: MISS — iter_content(None) behavior differences by mode not addressed.
F3: MISS — Response.text encoding detection described as uncertain: "The text property's encoding detection logic…is not detailed in the clue file."
F4: COVERED — "json…Decodes the JSON response body…raises RequestsJSONDecodeError."

---

## Echo

### blind-echo-struct-1 (3/4)
F1: COVERED — Echo, Context, DefaultRouter, ValueBinder/binding all described in core package root-level files.
F2: COVERED — middleware/ directory described as separate package with 24 files and distinct middleware components.
F3: COVERED — "Every middleware follows the same pattern: A convenience function…that delegates to a WithConfig variant." New/NewWithConfig also shown.
F4: MISS — External middleware in separate repos never mentioned; only the in-repo middleware/ package is described.

### blind-echo-struct-2 (4/4)
F1: COVERED — Echo as "top-level framework instance", Context as "per-request state", DefaultRouter as route matching registry.
F2: COVERED — Method-specific registration (GET, POST, etc.) returning RouteInfo described; all delegate to Echo.Add.
F3: COVERED — "Group is a set of sub-routes for a specified route" with its own HTTP method shortcuts and Use.
F4: COVERED — Context.Bind delegates to "c.echo.Binder.Bind"; Context.json delegates to "c.echo.JSONSerializer.Serialize"; separate interface pattern identified.

### blind-echo-rel-1 (3/4)
F1: COVERED — "Echo is the central owner of the router, context pool, and middleware chain"; handlers receive Context for input/output.
F2: COVERED — "Echo.Group creates a new router group with prefix and optional group-level middleware."
F3: MISS — Group middleware inheritance from parent Echo/Group not mentioned; only "Groups can have their own middleware" stated.
F4: COVERED — "each middleware receiving Context and calling the next" and "handler receives Context" — both share the same context object.

### blind-echo-rel-2 (4/4)
F1: COVERED — Two middleware phases explicitly described: Pre-router (Echo.Pre, runs before routing) and Post-router (Echo.Use, runs after routing).
F2: COVERED — DefaultRouter.Route described with PRECEDENCE + ACCUMULATE annotations; trie-based routing with findStaticChild; match-type priority shown.
F3: COVERED — Echo.Any and Echo.Match described as multi-method convenience registration APIs.
F4: COVERED — "Every route registration method accepts optional middleware…parameters. This allows per-route middleware in addition to global middleware."

### blind-echo-mech-1 (2/4)
F1: COVERED — "Static segments win first…Parameterized segments come second…Wildcard segments are lowest priority" explicitly stated.
F2: COVERED — Priority based on radix-tree node type (structural), not registration order; "Static children are tried before any other node type."
F3: MISS — Wildcard consuming "zero or more chars" not stated; only described as lowest priority.
F4: MISS — "Only first match-any matters" not addressed; routeMethods.find fallbackToAny is about HTTP method fallback, not route matching.

### blind-echo-mech-2 (3/4)
F1: MISS — Response explicitly says "The specific logic for choosing response content type (JSON vs plain text)…cannot be confirmed."
F2: COVERED — "plain error…the error handler likely defaults to HTTP 500"; HTTPError/HTTPStatusCoder provides StatusCode() for embedded code.
F3: COVERED — "DefaultHTTPErrorHandler(exposeError bool), taking a boolean that controls whether error details are exposed to the client."
F4: COVERED — Response.WriteHeader GUARD(r -> none) for already-committed responses; ResolveResponseStatus GUARD(resp -> pass_through); error handler cannot change status after commit.

---

## Zod

### blind-zod-struct-1 (3/4)
F1: COVERED — "zod" / "v4/classic" described as the full-featured API with richer ZodError and convenience methods.
F2: COVERED — "This is a lightweight/tree-shakeable variant" with ZodMini prefix types.
F3: COVERED — "This is the foundational layer. All types here use the $Zod prefix convention, indicating internal/core types."
F4: MISS — English locale auto-loaded by zod but not mini is never mentioned.

### blind-zod-struct-2 (3/4)
F1: COVERED — $ZodType described as "the foundational type" and base of all schema hierarchies.
F2: MISS — The _zod property with def field not explained as a general pattern; only a tangential reference to _ZodMiniJSONSchema["_zod"] in struct-1.
F3: COVERED — $ZodChecks union type and $ZodStringFormatChecks described; individual check subclasses enumerated ($ZodCheckRegex, $ZodCheckLowerCase, etc.).
F4: COVERED — $ZodError described as core error interface; $ZodIssue referenced; ZodError extends $ZodError with addIssue, flatten, format.

### blind-zod-rel-1 (4/4)
F1: COVERED — All mini schemas shown extending $ZodType via ZodMiniType; core.output and core.input referenced as type utilities.
F2: COVERED — "ZodMiniType…extends: $ZodType. Methods: clone, parse, parseAsync, safeParse" — reduced method set compared to full ZodType.
F3: COVERED — "ZodError…extends: $ZodError (from core)" explicitly stated.
F4: COVERED — String-format types appear in both schema hierarchy (ZodMiniStringFormat → $ZodStringFormat) and check hierarchy ($ZodStringFormatChecks union).

### blind-zod-rel-2 (2/4)
F1: COVERED — Validation pipeline flow described: parse → schema validation → checks → issue generation → error construction.
F2: MISS — parse vs safeParse behavioral difference (throw vs return result) not explicitly articulated; both are listed as separate types but the contrast isn't drawn.
F3: MISS — Async refinements forcing async parsing not mentioned in this response; $ZodAsyncError mechanism appears only in rel-1/mech-2 responses.
F4: COVERED — Error maps described as running "after check/validation failures are detected but before the final issue is assembled with a message."

### blind-zod-mech-1 (4/4)
F1: COVERED — "If UnknownKeysParam specifies stripping: unknown keys are removed from the output" describes the strip behavior.
F2: COVERED — "If it specifies strict mode: an error is raised for unknown keys" matches strictObject behavior.
F3: COVERED — "If it specifies passthrough: unknown keys are passed through to the output" matches looseObject behavior.
F4: COVERED — v4 catchall mechanism described: "The catchall schema is applied to any keys not in the shape…Any other schema: unknown keys are validated against it."

### blind-zod-mech-2 (2/4)
F1: COVERED — "Per-check message parameter…This is the most specific customization" — schema-level message identified as highest precedence.
F2: MISS — Per-parse error maps not mentioned; response only describes per-check messages, customError (global), and localeError (global).
F3: COVERED — z.config() described with customError overriding localeError; config function shown setting globalConfig. Correctly positioned above locale.
F4: MISS — undefined yielding to next level in the error map chain not mentioned.

---

## Summary Table — By Task

| Task | Score |
|------|-------|
| blind-requests-struct-1 | 4/4 |
| blind-requests-struct-2 | 4/4 |
| blind-requests-rel-1 | 3/4 |
| blind-requests-rel-2 | 3/4 |
| blind-requests-mech-1 | 1/4 |
| blind-requests-mech-2 | 1/4 |
| blind-echo-struct-1 | 3/4 |
| blind-echo-struct-2 | 4/4 |
| blind-echo-rel-1 | 3/4 |
| blind-echo-rel-2 | 4/4 |
| blind-echo-mech-1 | 2/4 |
| blind-echo-mech-2 | 3/4 |
| blind-zod-struct-1 | 3/4 |
| blind-zod-struct-2 | 3/4 |
| blind-zod-rel-1 | 4/4 |
| blind-zod-rel-2 | 2/4 |
| blind-zod-mech-1 | 4/4 |
| blind-zod-mech-2 | 2/4 |
| **TOTAL** | **53/72** |

## Summary Table — By Repository

| Repository | Covered | Total | % |
|------------|---------|-------|---|
| requests | 16 | 24 | 66.7% |
| echo | 19 | 24 | 79.2% |
| zod | 18 | 24 | 75.0% |
| **All** | **53** | **72** | **73.6%** |

## Summary Table — By Knowledge Type

| Type | Covered | Total | % |
|------|---------|-------|---|
| struct | 21 | 24 | 87.5% |
| rel | 19 | 24 | 79.2% |
| mech | 13 | 24 | 54.2% |
| **All** | **53** | **72** | **73.6%** |
