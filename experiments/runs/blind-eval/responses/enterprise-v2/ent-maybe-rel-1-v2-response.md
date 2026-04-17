# Enterprise v2: ent-maybe-rel-1
Date: 2026-04-17

## Question
How are authentication, AI enablement, and endpoint scopes related across Maybe's Chat API?

## Answer

### 1. Relevant Symbols Identified

The most relevant symbols to this question are found in the `chat_controller.js` module and the `.env.example` configuration:

- **Chat controller:** `extends` at `app/javascript/controllers/chat_controller.js:2-61` — extends `Controller`, with methods: `autoResize`, `connect`, `disconnect`, `handleInputKeyDown`, `submitSampleQuestion` (FOCUS, extends at chat_controller.js:2-61).
- **submitSampleQuestion:** `extends.submitSampleQuestion` at `chat_controller.js:27-35` — takes a parameter from `e.target.dataset.chatQuestionParam` and submits via `this.formTarget.requestSubmit` (FOCUS, extends.submitSampleQuestion at chat_controller.js:27-35).
- **handleInputKeyDown:** `extends.handleInputKeyDown` at `chat_controller.js:36-43` — handles Enter key (without Shift) to submit the form via `this.formTarget.requestSubmit` (FOCUS, extends.handleInputKeyDown at chat_controller.js:36-43).
- **.env.example:** Contains `SYNTH_API_KEY=<set>` (FOCUS, .env.example:1-86).

### 2. Authentication

The clue provides **no direct evidence** of authentication mechanisms for the Chat API. The `chat_controller.js` entries only show a front-end controller submitting a form through `this.formTarget.requestSubmit()` (FOCUS, `extends.submitSampleQuestion` at `app/javascript/controllers/chat_controller.js:27-35`; FOCUS, `extends.handleInputKeyDown` at `app/javascript/controllers/chat_controller.js:36-43`). However, the clue does not document:
- Any authentication controller or middleware
- Session management logic
- Token-based or API-key-based auth for the chat endpoint
- Any explicit connection between the password-related controllers in SYM and the chat flow

The `.env.example` includes `SECRET_KEY_BASE=secret-value` (FOCUS, .env.example:1-86), which is likely used for server-side session signing, but the clue does not link this to the chat endpoint specifically.

### 3. AI Enablement

The clue shows limited but suggestive evidence of AI enablement:

- **SYNTH_API_KEY:** The `.env.example` contains `SYNTH_API_KEY=<set>` (FOCUS, `.env.example:1-86`). That is the clearest configuration-level evidence that some synthesis/AI capability is expected.
- **Chat controller uses:** The chat controller uses `this.messagesObserver`, and `disconnect` tears that observer down through `this.messagesObserver.disconnect` (FOCUS, `extends` at `app/javascript/controllers/chat_controller.js:2-61`; FOCUS, `extends.disconnect` at `app/javascript/controllers/chat_controller.js:10-14`). This shows the UI watches message-area changes, but the clue does not identify the observer implementation.
- The `submitSampleQuestion` method references `e.target.dataset.chatQuestionParam` (FOCUS, `extends.submitSampleQuestion` at `app/javascript/controllers/chat_controller.js:27-35`), so the UI supports canned/sample chat prompts.

### 4. Endpoint Scopes

The clue **does not document API endpoint definitions, route scopes, or server-side controllers**. The clue artifact covers only the JavaScript front-end layer (91 modules, 270 symbols — clue header). The chat controller submits to a form target (`this.formTarget.requestSubmit()`), but the form action URL and any endpoint scoping/routing are not visible.

The README.md mentions sections "Maybe Hosting" and "Local Development Setup" (FOCUS, README.md:1-64), but these section titles do not reveal API endpoint documentation.

### 5. Relationship Analysis

From what is documented, the relationship can be characterized as:

1. **Authentication → Chat:** Undocumented at the clue level. The chat controller submits a form, but the clue does not expose any auth mechanism attached to that submission (FOCUS, `extends.submitSampleQuestion` at `app/javascript/controllers/chat_controller.js:27-35`; FOCUS, `extends.handleInputKeyDown` at `app/javascript/controllers/chat_controller.js:36-43`).

2. **AI Enablement → Chat:** The `SYNTH_API_KEY` environment variable is the documented link between the application and some synthesis capability, and the chat controller keeps a `messagesObserver` associated with the UI (FOCUS, `.env.example:1-86`; FOCUS, `extends` at `app/javascript/controllers/chat_controller.js:2-61`). However, the server-side wiring — including whether `SYNTH_API_KEY` is used specifically by the chat endpoint — is not shown.

3. **Endpoint Scopes → Chat:** Not documented. No route definitions, API scopes, or authorization policies are present in the clue.

### 6. Gaps and Uncertainties

- **GAPS states:** "type: STRUCTURAL (answerable from L0-L2), coverage: 8 symbols in L3, 0 with behavior annotations" (GAPS). This means 8 symbols have L3 (body-level) detail but none have behavior annotations, limiting mechanistic analysis.
- The clue covers **only the JavaScript front-end** (TREE shows `app/javascript/` and `app/components/DS/`). Server-side code (Ruby/Rails controllers, models, routes, middleware) is entirely absent.
- Authentication mechanisms, AI service integration logic, and endpoint scoping/authorization are **not determinable** from this clue alone.
- The `SELF_HOSTED=true` flag (FOCUS, .env.example:1-86) may affect which AI features or endpoints are available, but this relationship is not documented in the clue.
