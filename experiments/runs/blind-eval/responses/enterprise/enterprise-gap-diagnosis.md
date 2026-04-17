# Enterprise gap diagnosis

- Scope: enterprise misses from `batch1-scoring.md` + `supabase-full-scoring.md`
- Baseline: 31/120 = 25.8%
- Misses analyzed: 89

## Context map

### Files analyzed
| File | Purpose |
|---|---|
| `responses/enterprise/batch1-scoring.md` | Enterprise scoring for Saleor, NetBox, Cal.com, Maybe |
| `responses/enterprise/supabase-full-scoring.md` | Enterprise scoring for Supabase |
| `enterprise-gold-tasks.json` | Gold facts per enterprise task |
| `clues/ent-*.codeclue` | Actual clue contents used to judge whether the fact was present, absent, or mis-focused |

### Diagnostic rule of thumb
- **CLUE_EMPTY** = clue is so thin/off-surface that the answer is impossible.
- **FOCUS_MISS / WRONG_FOCUS** = repo graph likely had useful material, but the selected focus did not align to the question.
- **EXTRACTION_GAP** = the needed fact lives in docs/config/policy/cross-layer structure the extractor does not currently carry forward.
- **GOLD_TOO_SPECIFIC** = fact demands path names, field lists, or low-level internals beyond what a 4K clue should be expected to retain.
- **FORMAT_LIMIT** = clue has enough nearby evidence that a better summarization/reasoning layer might recover it.

## Repo-by-repo miss classification

### saleor

| Task | Fact | Gold fact | Category | Why it missed |
|---|---:|---|---|---|
| `ent-saleor-struct-1` | F1 | Saleor is a GraphQL-only, API-only platform. | **WRONG_FOCUS** | The clue centers on GraphQL plumbing and permission symbols, not the product-boundary claim that Saleor is GraphQL-only/API-only. |
| `ent-saleor-struct-1` | F2 | The dashboard is a decoupled project in a separate repository. | **EXTRACTION_GAP** | This fact lives in repo-level product/README context (dashboard in another repo), which the clue format does not surface. |
| `ent-saleor-struct-1` | F4 | Backend extension surfaces include webhooks, apps, subscription queries, API extensions, and dashboard iframes. | **FOCUS_MISS** | The clue surfaces webhooks/apps, but it never focuses the fuller extension-surface symbols needed for subscription queries, API extensions, and dashboard iframes. |
| `ent-saleor-struct-2` | F4 | Tests are split into separate `queries` and `mutations` directories, ideally with one file per query or mutation. | **EXTRACTION_GAP** | The clue summarizes GraphQL modules, but test-folder conventions like queries/mutations splits and one-file-per-operation are not extracted. |
| `ent-saleor-rel-1` | F2 | Mutation permissions are defined in the `Meta.permissions` field. | **FOCUS_MISS** | The permission clue includes query decorators and mutation classes, but it never selects the mutation metadata that would expose `Meta.permissions`. |
| `ent-saleor-rel-1` | F3 | `AuthorizationFilters` represents function-based permission checks instead of named admin permission scopes. | **FOCUS_MISS** | Relevant permission/auth code is nearby, but the focus set never pulls in `AuthorizationFilters` or explains its role. |
| `ent-saleor-rel-1` | F4 | When `PermissionDenied` is raised, the error should state which permissions are required, and those permissions should be mentioned in the GraphQL description. | **EXTRACTION_GAP** | The clue captures `PermissionDenied`, but not the descriptive error-text/docstring policy about naming required permissions. |
| `ent-saleor-rel-2` | F1 | Removing or renaming a GraphQL schema field is a breaking change. | **EXTRACTION_GAP** | This is an API policy/changelog rule; the clue mostly exposes symbols, not the breaking-change guidance that lives in docs/process text. |
| `ent-saleor-rel-2` | F2 | Removing or renaming a webhook payload field is a breaking change. | **EXTRACTION_GAP** | Webhook payload compatibility rules are documentation/policy content that the extractor does not preserve. |
| `ent-saleor-rel-2` | F3 | Changing `PluginsManager` function signatures is a breaking change for existing plugins. | **EXTRACTION_GAP** | The clue never reaches plugin-compatibility guidance around `PluginsManager` signatures because that policy is not extracted into the summary. |
| `ent-saleor-rel-2` | F4 | API fields should be deprecated before removal, and `PREVIEW_FEATURE` changes can be removed in the next minor version. | **EXTRACTION_GAP** | Deprecation policy and the `PREVIEW_FEATURE` exception are governance text, not something the current extractor captures well. |
| `ent-saleor-mech-1` | F1 | The search vector update task is triggered by the Celery beat scheduler. | **EXTRACTION_GAP** | No Celery Beat evidence appears in the clue; the operational scheduler mechanism is missing from extraction. |
| `ent-saleor-mech-1` | F2 | That feature will not work without task queue configuration. | **EXTRACTION_GAP** | Task-queue prerequisites are operational setup guidance that the clue never surfaces. |
| `ent-saleor-mech-1` | F3 | `uv run poe worker` starts the Celery worker. | **EXTRACTION_GAP** | Repo command-level workflow details like `uv run poe worker` are absent from the extracted clue. |
| `ent-saleor-mech-1` | F4 | `uv run poe scheduler` starts the Celery Beat scheduler. | **EXTRACTION_GAP** | The clue omits the paired scheduler command `uv run poe scheduler`, again pointing to missing ops/config extraction. |
| `ent-saleor-mech-2` | F2 | When locking multiple objects, the lock order should be consistent, typically by primary key. | **EXTRACTION_GAP** | The clue shows locking helpers and `select_for_update()`, but not the narrative lock-order rule by primary key. |
| `ent-saleor-mech-2` | F3 | When locking across multiple models, acquire locks in a defined order, such as locking `Order` before `OrderLine`. | **EXTRACTION_GAP** | Cross-model lock ordering guidance is not represented in the extracted clue even though the locking subsystem is present. |

### netbox

| Task | Fact | Gold fact | Category | Why it missed |
|---|---:|---|---|---|
| `ent-netbox-struct-1` | F2 | Its recommended automation architecture centers NetBox as the central authority while other tools handle monitoring, assurance, and execution. | **EXTRACTION_GAP** | The “NetBox as source of truth, other tools around it” architecture guidance is product documentation, not a symbol pattern the clue extracts. |
| `ent-netbox-struct-2` | F1 | Plugins are packaged Django apps that can add models, URLs and views, template content, navigation items, middleware, and configuration parameters. | **FORMAT_LIMIT** | The clue contains many plugin hooks (templates, API views, middleware-adjacent classes), but the 4K summary never assembles them into the full extension-surface answer. |
| `ent-netbox-struct-2` | F4 | Plugin configuration is supplied under `PLUGINS_CONFIG` in `configuration.py`. | **FOCUS_MISS** | Plugin configuration machinery is present, but the clue never explicitly surfaces `PLUGINS_CONFIG` in `configuration.py`. |
| `ent-netbox-rel-1` | F2 | Tenant groups can nest recursively, and a tenant may belong to a group or none. | **EXTRACTION_GAP** | This is a Django ORM/data-model relationship detail (recursive tenant groups, optional membership) that the extractor does not express clearly. |
| `ent-netbox-rel-2` | F1 | Object-based permissions can target object types, users or groups, allowed actions, and JSON constraints. | **EXTRACTION_GAP** | The clue has auth helpers, but not the full object-type/user/group/action/JSON-constraint permission model. |
| `ent-netbox-rel-2` | F2 | Default permissions are auto-applied to any authenticated user, regardless of database permission rows. | **FORMAT_LIMIT** | `settings.DEFAULT_PERM...` is visible in the clue, but the model did not turn that into the explicit “all authenticated users” rule. |
| `ent-netbox-rel-2` | F3 | `EXEMPT_VIEW_PERMISSIONS` can make selected models viewable by all users, including anonymous users. | **FOCUS_MISS** | The clue never selects the specific exemption setting (`EXEMPT_VIEW_PERMISSIONS`) needed to answer anonymous-view behavior. |
| `ent-netbox-mech-1` | F2 | Plugins can add their own jobs via the Job model, and jobs run in `rqworker` processes. | **FORMAT_LIMIT** | The clue includes jobs, enqueueing, plugins, and workers, but it never composes them into the “plugins can add jobs run by rqworker” mechanism. |
| `ent-netbox-mech-1` | F4 | System jobs use `system_job()`, and default worker queues are high, default, and low; custom queues need a dedicated worker configuration. | **FOCUS_MISS** | System jobs are visible, but the clue does not surface default queue names or the dedicated-worker requirement for custom queues. |
| `ent-netbox-mech-2` | F3 | Webhook payloads can use Jinja2 templates and get context like event, timestamp, object_type, username, request_id, data, and pre-change and post-change snapshots. | **FORMAT_LIMIT** | Jinja/template signals exist in the clue, but not in a form the model can use to recover the webhook templating/context answer. |
| `ent-netbox-mech-2` | F4 | Webhook requests succeed only on 2XX responses, failures can be requeued manually, and `webhook_receiver` is a local inspection tool that only prints requests. | **FOCUS_MISS** | The clue does not focus the delivery-status and requeue path details needed for 2XX/manual requeue/`webhook_receiver`. |

### calcom

| Task | Fact | Gold fact | Category | Why it missed |
|---|---:|---|---|---|
| `ent-calcom-struct-1` | F4 | `packages/platform/examples/base` is the example app used to test atoms against the backend. | **GOLD_TOO_SPECIFIC** | The gold asks for an exact example-app path (`packages/platform/examples/base`), a level of path precision that a 4K repo summary is unlikely to preserve. |
| `ent-calcom-struct-2` | F1 | Cal.diy is the open-source community edition and is recommended only for personal, non-production self-hosting. | **EXTRACTION_GAP** | This community-edition/self-hosting positioning is product documentation rather than code-graph content. |
| `ent-calcom-struct-2` | F2 | Teams, team round-robin, team collective, managed event types, instant meeting, and organizations are shown as available in Cal.com but not Cal.diy. | **EXTRACTION_GAP** | The Cal.com-vs-Cal.diy feature split lives in docs/packaging context that the extractor does not capture. |
| `ent-calcom-struct-2` | F3 | SAML SSO, SCIM directory sync, impersonation, workflows, routing forms, insights dashboard, attributes and segments, delegation, workspace platform, and admin panel are Cal.com-only features. | **EXTRACTION_GAP** | Enterprise-only feature gating (SAML/SCIM/workflows/admin) is a product-tier fact missing from the code clue. |
| `ent-calcom-struct-2` | F4 | Cal.diy still includes event types, availability schedules, webhooks, Zapier, API v2, API keys, and platform or OAuth clients. | **EXTRACTION_GAP** | The retained Cal.diy feature list is likewise documentation/product-scoping content, not extracted structure. |
| `ent-calcom-rel-1` | F1 | The router is entered with a `formId` plus field values in the URL. | **WRONG_FOCUS** | The clue for the routing question fixates on webhook DTOs and webhook tasking instead of the router entry flow from form submission. |
| `ent-calcom-rel-1` | F2 | It validates field types and required fields before choosing a route. | **WRONG_FOCUS** | Focus remains in webhook/event plumbing rather than form-field validation before route choice. |
| `ent-calcom-rel-1` | F3 | For an `eventTypeRedirect`, it finds team members matching the routing rules and redirects to the booking page with `routedTeamMemberIds`. | **WRONG_FOCUS** | The needed router handoff symbols (`eventTypeRedirect`, routed members) are not what the clue chose to focus. |
| `ent-calcom-rel-1` | F4 | The booking page shows only the matching members' slots, slot selection temporarily blocks the slot, and confirmation rechecks availability rules before sending emails and webhooks. | **WRONG_FOCUS** | The clue follows webhook scheduling, not the downstream slot filtering/recheck/email/webhook flow asked by the gold. |
| `ent-calcom-rel-2` | F2 | `BOOKING_CREATED` payloads include organizer, attendees, destinationCalendar, uid, metadata, and responses. | **GOLD_TOO_SPECIFIC** | The clue knows booking webhook families, but the gold wants exact `BOOKING_CREATED` payload fields, which is too granular for this format. |
| `ent-calcom-rel-2` | F3 | `BOOKING_CANCELLED` payloads include `cancellationReason`, while `BOOKING_RESCHEDULED` payloads include `rescheduleUid` and `reschedulingReason`. | **GOLD_TOO_SPECIFIC** | Cancellation/reschedule-specific payload field lists are implementation-level detail beyond what a 4K clue can reliably retain. |
| `ent-calcom-rel-2` | F4 | Webhook requests are signed with `X-Cal-Signature-256` using SHA-256 over the payload and secret. | **GOLD_TOO_SPECIFIC** | Exact header/signing details (`X-Cal-Signature-256`, SHA-256) are too specific for the current summary budget. |
| `ent-calcom-mech-1` | F2 | The default is `MANDATORY_HOST_ONLY`, including when the column is null or the booking has no `eventTypeId`. | **FORMAT_LIMIT** | The clue includes `MANDATORY_HOST_ONLY`, but it does not spell out the null/default behavior strongly enough for the model to answer confidently. |
| `ent-calcom-mech-1` | F3 | `handleCancelBooking` validates the reason based on that setting and on whether the canceller is the host or the attendee. | **GOLD_TOO_SPECIFIC** | Requiring the exact handler name `handleCancelBooking` is more implementation-specific than the clue format is designed for. |
| `ent-calcom-mech-1` | F4 | The Cancel Booking UI threads `requiresCancellationReason` through the booking views and shows a required indicator when a reason is mandatory. | **GOLD_TOO_SPECIFIC** | The required-indicator/UI-threading detail is too fine-grained for a compressed mechanistic summary. |
| `ent-calcom-mech-2` | F1 | Root `.env` values `SEED_PLATFORM_OAUTH_CLIENT_ID` and `SEED_PLATFORM_OAUTH_CLIENT_SECRET` are copied into the example app as `NEXT_PUBLIC_X_CAL_ID` and `X_CAL_SECRET_KEY`. | **GOLD_TOO_SPECIFIC** | Exact env-var mapping for platform OAuth client credentials is configuration-level detail that exceeds what the clue preserves. |
| `ent-calcom-mech-2` | F2 | `yarn generate-secrets` in `apps/api/v2` writes both plaintext and hashed OAuth2 secrets to `.generated-secrets`. | **GOLD_TOO_SPECIFIC** | `yarn generate-secrets` and `.generated-secrets` are exact setup details, not stable high-level summary content. |
| `ent-calcom-mech-2` | F3 | The example app uses `NEXT_PUBLIC_OAUTH2_CLIENT_ID` and `OAUTH2_CLIENT_SECRET_PLAIN`, while the root env stores the hashed secret in `SEED_OAUTH2_CLIENT_SECRET_HASHED`. | **GOLD_TOO_SPECIFIC** | The plaintext-vs-hashed OAuth2 secret split is an implementation detail too deep for the 4K format. |
| `ent-calcom-mech-2` | F4 | The authorize flow redirects to `localhost:4321?code=abc`, exchanges the code for access and refresh tokens, and reflects availability updates from the main web app. | **FOCUS_MISS** | The clue is in the OAuth subsystem, but it never focuses the authorize→token-exchange→availability-update flow the gold asks for. |

### maybe

| Task | Fact | Gold fact | Category | Why it missed |
|---|---:|---|---|---|
| `ent-maybe-struct-1` | F2 | The repository explicitly documents Docker-based self-hosting in `docs/hosting/docker.md`. | **CLUE_EMPTY** | The clue is only ~91 modules / 267 symbols and is dominated by front-end controllers; none of the self-hosting docs surfaces are present. |
| `ent-maybe-struct-1` | F3 | The README separates self-hosting users from developers and points self-hosters to the Docker guide instead of the local development steps. | **CLUE_EMPTY** | README audience guidance is completely absent because the clue barely covers the repo beyond JS controllers. |
| `ent-maybe-struct-1` | F4 | The documented API surface includes an AI chat API under `/api/v1/chats`. | **CLUE_EMPTY** | The `/api/v1/chats` surface never appears; the clue is too thin to answer API/doc questions. |
| `ent-maybe-struct-2` | F1 | The Docker guide recommends first installing Docker Engine and verifying it with `docker run hello-world`. | **CLUE_EMPTY** | Docker install/verification steps are not just unfocused; the clue never includes any deployment/docs material at all. |
| `ent-maybe-struct-2` | F2 | The sample compose file is downloaded from the repository as `compose.yml` from `compose.example.yml`. | **CLUE_EMPTY** | `compose.example.yml` / `compose.yml` setup is missing because the clue excludes the relevant files. |
| `ent-maybe-struct-2` | F3 | Optional environment configuration is done through a local `.env` file containing `SECRET_KEY_BASE` and `POSTGRES_PASSWORD`. | **CLUE_EMPTY** | Environment-file setup is absent for the same reason: the clue is far too thin and front-end-only. |
| `ent-maybe-struct-2` | F4 | The documented runtime flow includes `docker compose up`, then `docker compose up -d` for background mode, with `docker compose ls` used to verify it is running. | **CLUE_EMPTY** | Runtime Docker flow commands are nowhere in the clue. |
| `ent-maybe-rel-1` | F1 | All chat endpoints require authentication via OAuth2 or API keys and also require `ai_enabled` to be true. | **CLUE_EMPTY** | Auth/API-key/`ai_enabled` behavior is not derivable because the clue never reaches backend/API surfaces. |
| `ent-maybe-rel-1` | F2 | GET endpoints for listing chats and fetching a chat require the `read` scope. | **CLUE_EMPTY** | Read-scope requirements are absent from the clue entirely. |
| `ent-maybe-rel-1` | F3 | Create, update, delete, create-message, and retry-message operations require the `write` scope. | **CLUE_EMPTY** | Write-scope requirements are absent from the clue entirely. |
| `ent-maybe-rel-1` | F4 | The documented error model distinguishes unauthorized from forbidden, where forbidden covers insufficient permissions or AI not enabled. | **CLUE_EMPTY** | Unauthorized-vs-forbidden semantics do not appear because the clue has no API contract coverage. |
| `ent-maybe-rel-2` | F1 | List Chats returns a `chats` array with chat metadata plus pagination fields including `page`, `per_page`, `total_count`, and `total_pages`. | **CLUE_EMPTY** | Chat payload structure is not answerable from a clue that only surfaces UI controllers and chart code. |
| `ent-maybe-rel-2` | F2 | Get Chat returns a `messages` array that can include both `user_message` and `assistant_message` records. | **CLUE_EMPTY** | `messages` payload typing is absent; the clue does not capture API response models. |
| `ent-maybe-rel-2` | F3 | Assistant messages include a `model` field and a `tool_calls` array. | **CLUE_EMPTY** | Assistant `model` / `tool_calls` fields are missing because the clue has no backend schema/doc extraction. |
| `ent-maybe-rel-2` | F4 | The docs say the AI assistant can make tool calls to access user financial data. | **CLUE_EMPTY** | Tool-call access to financial data never appears in the clue. |
| `ent-maybe-mech-1` | F1 | `POST /api/v1/chats` accepts an optional title, an initial message, and an optional model, and it returns the same shape as Get Chat. | **CLUE_EMPTY** | The clue includes `chat_controller.js`, but nothing about the actual `POST /api/v1/chats` request/response contract. |
| `ent-maybe-mech-1` | F2 | `POST /api/v1/chats/:chat_id/messages` returns the user message immediately with `ai_response_status` set to `pending`. | **CLUE_EMPTY** | `ai_response_status: pending` is absent because API lifecycle details were not extracted. |
| `ent-maybe-mech-1` | F3 | The API processes AI responses asynchronously in the background rather than blocking the create request. | **CLUE_EMPTY** | Asynchronous background response processing is not represented in the clue. |
| `ent-maybe-mech-1` | F4 | Clients are told to poll the chat endpoint and look for new messages with `type` equal to `assistant_message`. | **CLUE_EMPTY** | Polling for `assistant_message` is documentation/API guidance missing from the clue. |
| `ent-maybe-mech-2` | F1 | The documented image source for self-hosting is `ghcr.io/maybe-finance/maybe` with `latest` and `stable` tags. | **CLUE_EMPTY** | Container image tags are not present; the clue has essentially no self-hosting coverage. |
| `ent-maybe-mech-2` | F2 | By default the self-hosted app does not update automatically. | **CLUE_EMPTY** | The no-auto-update default is missing for the same reason. |
| `ent-maybe-mech-2` | F3 | The documented update sequence is `docker compose pull`, `docker compose build`, then `docker compose up --no-deps -d web worker`. | **CLUE_EMPTY** | The documented update sequence is not in the clue at all. |
| `ent-maybe-mech-2` | F4 | If the first start hits an `ActiveRecord::DatabaseConnectionError`, the guide recommends `docker compose down`, removing the `maybe_postgres-data` volume, and starting `docker compose up` again. | **CLUE_EMPTY** | The first-run database recovery flow is entirely absent from the extracted clue. |

### supabase

| Task | Fact | Gold fact | Category | Why it missed |
|---|---:|---|---|---|
| `ent-supabase-struct-1` | F2 | Kong is the API gateway in front of the core services. | **EXTRACTION_GAP** | Kong-as-gateway is a product-architecture fact that never appears in the extracted clue. |
| `ent-supabase-struct-1` | F3 | Postgres is the core of Supabase and is not abstracted away; users can access it with full privileges. | **EXTRACTION_GAP** | The “Postgres is the core, not abstracted away” framing is product documentation, not represented in the clue. |
| `ent-supabase-struct-1` | F4 | Supavisor is described as a cloud-native, multi-tenant Postgres connection pooler. | **EXTRACTION_GAP** | Supavisor is missing because the extractor did not carry top-level architecture/service descriptions into the clue. |
| `ent-supabase-struct-2` | F2 | Preview branches are ephemeral and can be paused or deleted after inactivity or when a pull request is merged or closed. | **FOCUS_MISS** | The clue clearly targets branches, but it focuses query/UI surfaces rather than preview-branch lifecycle semantics. |
| `ent-supabase-struct-2` | F3 | Persistent branches are long-lived and are recommended for staging, QA, or development environments. | **FOCUS_MISS** | Persistent-branch recommendations are branch-domain facts, but the clue never selects the relevant docs semantics. |
| `ent-supabase-struct-2` | F4 | New branches start data-less, and branch isolation covers database schema and data, storage objects, Edge Functions, and auth configurations. | **GOLD_TOO_SPECIFIC** | The exact isolation matrix across schema/data/storage/functions/auth is too detailed for a 4K clue to carry reliably. |
| `ent-supabase-rel-1` | F2 | Publishable and anon keys are public-facing but rely on RLS and the `anon` and `authenticated` Postgres roles for row access. | **FOCUS_MISS** | The clue includes `publishableKey` and `anonKey`, but it does not focus the surrounding role/RLS semantics needed for the full answer. |
| `ent-supabase-rel-1` | F3 | Secret and `service_role` keys are backend-only and bypass RLS through the `service_role` Postgres role. | **FOCUS_MISS** | Management/access-token material is present, but the clue misses the secret/service-role backend-only semantics. |
| `ent-supabase-rel-1` | F4 | Supabase Auth JWTs can scope database access row by row when used with RLS policies. | **EXTRACTION_GAP** | JWT-claims-to-row-policy enforcement is a cross-layer auth/database relation the extractor does not expose. |
| `ent-supabase-rel-2` | F2 | The transfer requires ownership of the source organization and at least membership in the target organization. | **FORMAT_LIMIT** | The clue has transfer-preview and organization context, but not in a form that lets the model recover the exact ownership-membership rule. |
| `ent-supabase-rel-2` | F3 | Project transfers do not move between regions. | **GOLD_TOO_SPECIFIC** | Region immobility is an exact product constraint unlikely to survive clue compression unless stated verbatim. |
| `ent-supabase-rel-2` | F4 | Transfers can be blocked by active GitHub integration, project-scoped roles, or configured log drains. | **GOLD_TOO_SPECIFIC** | Specific blockers like GitHub integration and log drains are too fine-grained for the current summary budget. |
| `ent-supabase-mech-1` | F1 | Realtime clients connect to any node in the cluster over WebSockets. | **GOLD_TOO_SPECIFIC** | The clue shows Realtime client/channel behavior, but WebSocket cluster transport is deeper than the current mechanistic summary granularity. |
| `ent-supabase-mech-1` | F2 | `postgres_changes` starts streaming changes after a client initializes the extension and Realtime connects to Postgres through a replication slot. | **GOLD_TOO_SPECIFIC** | `postgres_changes`, replication slots, and streaming internals are implementation details beyond what the clue retains. |
| `ent-supabase-mech-1` | F3 | Broadcast creates a publication on `realtime.messages`, reads the WAL for that table, and sends JSON packages over WebSockets when inserts happen. | **GOLD_TOO_SPECIFIC** | `realtime.messages`, WAL reads, and JSON packaging are too low-level for this 4K format. |
| `ent-supabase-mech-1` | F4 | Broadcast and private channels require Realtime Authorization, and the cluster routes messages globally across regions. | **GOLD_TOO_SPECIFIC** | Realtime Authorization plus global cross-region routing is too detailed and multi-hop for the current clue budget. |
| `ent-supabase-mech-2` | F2 | Jobs can be created via SQL or the Dashboard and can run from every second to once a year. | **FOCUS_MISS** | The clue focuses cron job counts/timezones/UI rather than creation modes and supported schedule range. |
| `ent-supabase-mech-2` | F3 | A cron job can run SQL snippets, database functions, or HTTP requests such as invoking a Supabase Edge Function. | **FOCUS_MISS** | Cron is the right subsystem, but the clue never selects the supported target types (SQL/functions/HTTP/Edge Functions). |
| `ent-supabase-mech-2` | F4 | Under the hood it uses `pg_cron`, with jobs stored in `cron.job` and run details in `cron.job_run_details`. | **GOLD_TOO_SPECIFIC** | Exact internal table names (`pg_cron`, `cron.job`, `cron.job_run_details`) are implementation details beyond the clue format. |

## Category distribution

| Category | Misses | % of misses | % points if every miss in category were fixed |
|---|---:|---:|---:|
| CLUE_EMPTY | 23 | 25.8% | +19.2 |
| EXTRACTION_GAP | 24 | 27.0% | +20.0 |
| GOLD_TOO_SPECIFIC | 17 | 19.1% | +14.2 |
| FOCUS_MISS | 14 | 15.7% | +11.7 |
| FORMAT_LIMIT | 6 | 6.7% | +5.0 |
| WRONG_FOCUS | 5 | 5.6% | +4.2 |

## Why enterprise underperforms libraries

Libraries mostly ask code-local facts: symbol relations, API shapes, direct control flow. The enterprise set is different: it asks for product packaging, self-hosting docs, permission policy, operational commands, deprecation rules, queueing behavior, and cross-service architecture. The current CodeClue format is still heavily code-symbol-centric, so it systematically drops the very surfaces enterprise apps rely on.

## Top 3 fixable categories

### 1. CLUE_EMPTY coverage repair (23 misses in scope)

Specific code changes needed:
- Expand repository ingestion beyond narrow symbol subsets: include backend app code, route definitions, config files, README/docs markdown, and container/deploy files.
- Add a low-symbol-density guard: if a clue sees <~500 symbols or only one subtree, trigger a fallback whole-repo scan or docs/config pass.
- Teach the summarizer to prefer repo-root docs/config when the question mentions hosting, API, setup, Docker, OAuth, or update flow.
- Estimated improvement: recover about 18/120 facts = **+15.0 points** (roughly 40.8% total).

### 2. Focus selection repair (19 misses in scope)

Specific code changes needed:
- Replace pure lexical/top-centrality FOCUS ranking with question-conditioned retrieval over file paths, symbol names, doc text, and behavior annotations.
- Add intent heuristics so questions about routing, permissions, webhooks, branches, or cron boost matching subsystems instead of adjacent UI plumbing.
- Reserve part of the focus budget for “answer-shaping” artifacts (config constants, DTOs, docs fetchers, policy files) rather than only executable methods.
- Estimated improvement: recover about 14/120 facts = **+11.7 points** (roughly 37.5% total).

### 3. Extraction gap repair (24 misses in scope)

Specific code changes needed:
- Add extractors for docs/config/policy sources: README, docs/, mkdocs/docusaurus content, compose/env examples, pyproject/package scripts, and config.py/settings constants.
- Improve framework-aware relation extraction: Django model relationships, permissions metadata, deprecation policy text, queue/scheduler commands, and auth/database cross-links.
- Emit lightweight factual sentences for non-symbol facts (e.g., “dashboard lives in separate repo”, “Celery Beat drives scheduled tasks”, “Kong is the API gateway”).
- Estimated improvement: recover about 16/120 facts = **+13.3 points** (roughly 39.1% total).

## Estimated improvement by fix bundle

| Fix bundle | Primary categories addressed | Estimated facts recovered | Estimated score impact |
|---|---|---:|---:|
| CLUE_EMPTY coverage repair | CLUE_EMPTY | 18 | +15.0 |
| Focus selection repair | FOCUS_MISS, WRONG_FOCUS | 14 | +11.7 |
| Extraction gap repair | EXTRACTION_GAP | 16 | +13.3 |
| Gold-specific benchmark trim / hybrid doc-aware format redesign | GOLD_TOO_SPECIFIC, part of FORMAT_LIMIT | 10 | +8.3 |

## Does the format fundamentally work for enterprise apps?

**Not as currently implemented.** The evidence says the project does **not** need a total reset, but it **does** need a hybrid redesign for enterprise repos:

- keep symbol/behavior extraction for code-local facts,
- add first-class docs/config/ops extraction,
- upgrade question-conditioned focus selection, and
- stop benchmarking 4K clues against ultra-specific path names, field lists, and deep runtime internals.

If those changes land, the format can still work for enterprise apps at the **architectural / workflow / policy** level. If not, enterprise accuracy will stay structurally capped well below library accuracy because the benchmark is asking for information the current clue format routinely discards.