# Enterprise Eval: ent-maybe-mech-1
Date: 2026-04-17

## Question
What is the documented lifecycle when creating a chat or message, and how does a client observe the AI response?

---

## Reasoning Trace

### 1. Relevant Symbols from FOCUS, SYM, and INDEX

The most relevant module is `chat_controller.js` (INDEX line 36: 60L, methods: `autoResize`, `connect`, `disconnect`, `handleInputKeyDown`, `submitSampleQuestion`).

From FOCUS:
- **`extends` (chat_controller.js:2–61)**: extends Controller, methods: `autoResize`, `connect`, `disconnect`, `handleInputKeyDown`, `submitSampleQuestion`. Uses `this.messagesObserver`, `this.messagesObserver.disconnect`, `this.inputTarget`, `input.style.height` (FOCUS lines 218–222).
- **`extends.connect` (chat_controller.js:6–8)**: called_by extends (FOCUS lines 229–230). No further detail — the connect body is not provided in source snippets nor FOCUS.
- **`extends.disconnect` (chat_controller.js:10–14)**: uses `this.messagesObserver`, `this.messagesObserver.disconnect` (FOCUS lines 233–236).
- **`extends.submitSampleQuestion` (chat_controller.js:27–35)**: sig `(e)`, uses `this.inputTarget.value`, `e.target.dataset.chatQuestionParam`, `this.formTarget.requestSubmit` (FOCUS lines 212–216).
- **`extends.handleInputKeyDown` (chat_controller.js:36–43)**: sig `(e)`, uses `e.key`, `e.shiftKey`, `e.preventDefault`, `this.formTarget.requestSubmit` (FOCUS lines 238–242).
- **`extends.autoResize` (chat_controller.js:16–27)**: uses `this.inputTarget`, `input.style.height`, `Math.min`, `input.scrollHeight` (FOCUS lines 224–227).

Also relevant: `turbo_frame_timeout_controller.js` (source snippet L2–42) — provides context on Turbo frame loading patterns.

### 2. Documented Lifecycle: Creating a Chat/Message

From the source snippets, two message-creation paths are documented:

**Path A — User types a message (source: `handleInputKeyDown`, chat_controller.js L36–43):**
1. User presses a key in the chat input field.
2. If `e.key === "Enter"` and `!e.shiftKey`, the default action is prevented (`e.preventDefault()`).
3. The form is submitted programmatically via `this.formTarget.requestSubmit()`.
4. Comment in source (L513): *"Newlines require shift+enter, otherwise submit the form (same functionality as ChatGPT and others)"*.

**Path B — User clicks a sample question (source: `submitSampleQuestion`, chat_controller.js L27–35):**
1. User clicks a sample question element.
2. The input value is set from the element's data attribute: `this.inputTarget.value = e.target.dataset.chatQuestionParam`.
3. After a 200ms `setTimeout` delay, the form is submitted: `this.formTarget.requestSubmit()`.

**Auto-resize during input (source: `autoResize`, chat_controller.js L16–27):**
- As the user types, the input element's height is dynamically adjusted.
- Line height is 20px, max 3 lines (60px total).
- If content exceeds max height, `overflowY` is set to `"auto"`; otherwise `"hidden"`.

### 3. Documented Client Observation of AI Response

**`messagesObserver` pattern (FOCUS: `extends` and `extends.disconnect`):**
- The chat_controller class uses a `this.messagesObserver` instance (FOCUS: `extends` entry, `uses: this.messagesObserver`).
- On `disconnect()`, the observer is torn down: `this.messagesObserver.disconnect()` (FOCUS: `extends.disconnect`, lines 233–236).
- The `connect()` method (FOCUS lines 229–230) is where this observer would be initialized, but its body is **not provided** in the source snippets — it only shows 2 lines and the GAPS section lists it as a drill target with ~2 lines for `disconnect` only.

This pattern shows the client keeps some observer object attached to message updates in the DOM: `extends` uses `this.messagesObserver`, and `extends.disconnect` calls `this.messagesObserver.disconnect()` (`chat_controller.js:2–61`, `chat_controller.js:10–14`). The exact observer type and callback behavior are not provided.

**Turbo frame context (source: `turbo_frame_timeout_controller.js` L2–42):**
- The codebase includes a `turbo-frame-timeout` controller, which:
  - Listens for `"turbo:frame-load"` events (L308/L460: `this.element.addEventListener("turbo:frame-load", this.clearTimeout.bind(this))`).
  - Has a configurable timeout (default 10000ms, L300/L451).
  - On timeout, replaces content with a warning "Timeout" error state (L323–336/L473–487).
- This shows the frontend handles `turbo:frame-load` events somewhere in the UI, but it does **not** prove that chat responses use the same mechanism.

### 4. What GAPS Says Cannot Be Determined

The GAPS section states:
- **type: MECHANISTIC** — body logic needed for full answer (GAPS line 244).
- **coverage: 22 symbols in L3, 2 with behavior annotations** (GAPS line 246).
- Drill targets include `chat_controller.js` disconnect (~2 lines) and autoResize (~9 lines) (GAPS lines 248–249).

**Cannot be determined from the evidence:**
- The **body of `connect()`** in chat_controller.js — how exactly the `messagesObserver` is initialized, what DOM element it observes, and what callback fires when new messages appear.
- Whether the form submission triggers a **Turbo Stream**, **Turbo Frame**, or a standard HTTP form POST.
- The **server-side lifecycle**: what happens after `requestSubmit()` — how the backend creates the chat/message record, invokes the AI model, and returns the response.
- Whether AI responses are **streamed** (SSE/WebSocket) or delivered as a single server-rendered HTML response.
- The data model for chats and messages (IDs, associations, status fields).

### 5. Synthesis

**Supported conclusions (from evidence):**

The documented client-side chat lifecycle is:
1. **Input**: User types in an auto-resizing input field (max 3 lines) or selects a sample question (source: `autoResize`, `submitSampleQuestion`).
2. **Submission**: Form is submitted via `this.formTarget.requestSubmit()` — triggered by Enter key (source: `handleInputKeyDown`) or sample question click with 200ms delay (source: `submitSampleQuestion`).
3. **Observation**: A `messagesObserver` (FOCUS: `extends`, `extends.disconnect`) watches for new messages in the DOM and is cleaned up when the controller disconnects.
4. **Timeout safety**: A separate `turbo-frame-timeout` controller (source: L2–42) provides a 10-second default timeout for Turbo frame loads, showing an error state if loading fails — suggesting Turbo is the response delivery mechanism.

**Remaining uncertainty:**
- The exact mechanism of response delivery (Turbo Streams vs. Frames vs. other) cannot be confirmed.
- The `messagesObserver` initialization logic (in `connect()`) is not documented.
- All server-side lifecycle steps (message persistence, AI invocation, response generation) are outside the clue's JavaScript-only scope.
