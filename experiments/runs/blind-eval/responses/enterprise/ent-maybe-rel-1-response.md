# Enterprise Eval: ent-maybe-rel-1
Date: 2026-04-17

## Question
How are authentication, AI enablement, and endpoint scopes related across Maybe's Chat API?

---

## Reasoning Trace

### 1. Relevant Symbols from FOCUS, SYM, and INDEX

The question targets three concepts — authentication, AI enablement, and endpoint scopes — and their relationships in a Chat API. The most relevant symbol is `chat_controller.js` (INDEX, line 36: 60L, methods: `autoResize`, `connect`, `disconnect`, `handleInputKeyDown`, `submitSampleQuestion`).

The FOCUS section provides detailed analysis of the chat_controller:

- **`extends` (chat_controller.js:2–61)**: extends Controller, with methods `autoResize`, `connect`, `disconnect`, `handleInputKeyDown`, `submitSampleQuestion`. Uses `this.messagesObserver`, `this.inputTarget`, `input.style.height` (FOCUS lines 120–125).
- **`extends.submitSampleQuestion` (chat_controller.js:27–35)**: takes event `e`, uses `this.inputTarget.value`, `e.target.dataset.chatQuestionParam`, `this.formTarget.requestSubmit` (FOCUS lines 114–118). Source snippet (L27–35) confirms it sets the input value from a dataset attribute and submits the form after a 200ms delay.
- **`extends.handleInputKeyDown` (chat_controller.js:36–43)**: takes event `e`, uses `e.key`, `e.shiftKey`, `e.preventDefault`, `this.formTarget.requestSubmit` (FOCUS lines 140–144). Source snippet (L36–43) confirms Enter without Shift submits the form.
- **`extends.connect` (chat_controller.js:6–8)**: called_by extends, no further detail in FOCUS (lines 131–133).
- **`extends.disconnect` (chat_controller.js:10–14)**: uses `this.messagesObserver`, `this.messagesObserver.disconnect` (FOCUS lines 135–138).
- **`extends.autoResize` (chat_controller.js:16–27)**: adjusts input height with max 3 lines (source snippet L16–27).

### 2. Searching for Authentication, AI Enablement, and Endpoint Scopes

**Authentication:** No symbols, modules, or references in the clue file relate to authentication. There are no controllers named `auth_controller`, `session_controller`, or `login_controller` in the INDEX. No SYM entries reference tokens, sessions, API keys, OAuth, or authentication middleware. The `password_validator_controller.js` (SYM: `extends.validate`, `extends.validateRequirementText`) handles password field validation only — it is a UI input validator, not an authentication flow.

**AI Enablement:** No symbols reference AI configuration, feature flags, model selection, or AI service enablement. The `chat_controller.js` provides a chat UI but does not expose any AI-specific configuration or enablement logic in its documented interface. It simply submits a form via `this.formTarget.requestSubmit()` (source snippet, chat_controller.js L27–35 and L36–43).

**Endpoint Scopes:** No symbols reference API endpoints, route definitions, scopes, permissions, or authorization. The only service-layer symbol is `CurrenciesService.get` (SYM line 94, `app/javascript/services/currencies_service.js:2`), which is unrelated to chat.

### 3. What GAPS Says Cannot Be Determined

The GAPS section states:
- **type: MECHANISTIC** — body logic needed for full answer (GAPS line 147).
- **coverage: 6 symbols in L3, 0 with behavior annotations** (GAPS line 148).
- Drill targets: `chat_controller.js` disconnect (~2 lines), autoResize (~9 lines), submitSampleQuestion (~4 lines) (GAPS lines 149–151).

The GAPS section confirms that even at the deepest documented level, only 6 symbols are covered and none have behavior annotations. The entire clue file is scoped to **client-side JavaScript** (TREE: `app/javascript/`, `vendor/javascript/`). Backend API controllers, authentication middleware, AI service configuration, and endpoint routing are entirely outside the clue's scope.

### 4. Synthesis

**Supported conclusions (from evidence):**
The only documented Chat API surface is the **frontend `chat_controller.js`** (INDEX + FOCUS), which is a controller module that:
1. Submits user messages via HTML form submission (`this.formTarget.requestSubmit()`) — either through Enter key (source: `handleInputKeyDown` L36–43) or sample question buttons (source: `submitSampleQuestion` L27–35).
2. Auto-resizes the text input up to 3 lines (source: `autoResize` L16–27).
3. Uses a `messagesObserver` (FOCUS: `extends.disconnect` uses `this.messagesObserver.disconnect`) to observe chat message updates in the DOM.

**What cannot be determined:**
- **Authentication**: No authentication mechanisms, tokens, session management, or user identity verification are documented anywhere in the clue file. The relationship between authentication and the Chat API cannot be established.
- **AI enablement**: No AI feature flags, model configuration, or enablement gates are documented. Whether AI features require opt-in, subscription, or configuration is unknown.
- **Endpoint scopes**: No API endpoint definitions, route constraints, or authorization scopes appear in the evidence. The backend Chat API (routes, controllers, middleware) is entirely absent from this JavaScript-only clue file.

**The three concepts asked about — authentication, AI enablement, and endpoint scopes — have no documented relationships in this clue file because the clue exclusively covers frontend JavaScript controllers, not backend API infrastructure.**
