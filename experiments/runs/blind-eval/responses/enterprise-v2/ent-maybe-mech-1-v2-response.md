# Enterprise v2: ent-maybe-mech-1
Date: 2026-04-17

## Question
What is the documented lifecycle when creating a chat or message, and how does a client observe the AI response?

## Answer

### 1. Relevant Symbols Traced

The clue and source snippets document the front-end lifecycle of the chat interaction through `chat_controller.js` and supporting controllers. The key symbols are:

- **Chat controller class:** `extends` at `chat_controller.js:2-61` — extends `Controller` with methods: `autoResize`, `connect`, `disconnect`, `handleInputKeyDown`, `submitSampleQuestion` (FOCUS, extends at chat_controller.js:2-61).
- **Turbo frame timeout controller:** `extends` at `turbo_frame_timeout_controller.js:2-42` — provides timeout/error-state handling for Turbo frame loads (FOCUS, extends at turbo_frame_timeout_controller.js:2-42; SOURCE SNIPPET, extends at turbo_frame_timeout_controller.js L2-42).
- **Mobile cell interaction controller:** `extends` at `mobile_cell_interaction_controller.js:2-149` — handles touch interactions, cell highlighting, and error tooltips (FOCUS, extends at mobile_cell_interaction_controller.js:2-149).

### 2. Chat Lifecycle: Message Creation

#### Step 1: Controller Connection
When the chat UI element connects to the DOM, `connect()` fires (FOCUS, extends.connect at chat_controller.js:6-8). The clue shows this method is called by the class but does not detail its body — the source snippet is not provided for `connect`. However, the class-level `uses` annotation shows it references `this.messagesObserver` (FOCUS, extends at chat_controller.js:2-61 — `uses: this.messagesObserver`), suggesting the observer is initialized during connection.

#### Step 2: User Composes a Message
The `autoResize()` method dynamically adjusts the input textarea height. From the source snippet (SOURCE SNIPPET, extends.autoResize at chat_controller.js L16-27):

```javascript
autoResize() {
    const input = this.inputTarget;
    const lineHeight = 20; // text-sm line-height (14px * 1.429 ≈ 20px)
    const maxLines = 3;    // 3 lines = 60px total
    input.style.height = "auto";
    input.style.height = `${Math.min(input.scrollHeight, lineHeight * maxLines)}px`;
    input.style.overflowY = input.scrollHeight > lineHeight * maxLines ? "auto" : "hidden";
}
```

This caps the input at 3 lines (60px), then switches to scrollable overflow (SOURCE SNIPPET, extends.autoResize at chat_controller.js L16-27).

#### Step 3a: User Submits via Keyboard
`handleInputKeyDown(e)` intercepts Enter without Shift and submits the form. From the source snippet (SOURCE SNIPPET, extends.handleInputKeyDown at chat_controller.js L36-43):

```javascript
handleInputKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        this.formTarget.requestSubmit();
    }
}
```

The source comment explicitly says that Shift+Enter creates newlines while Enter submits the form (SOURCE SNIPPET, `extends.handleInputKeyDown` at `chat_controller.js` L36-43).

#### Step 3b: User Submits a Sample Question
`submitSampleQuestion(e)` copies a pre-configured question and auto-submits. From the source snippet (SOURCE SNIPPET, extends.submitSampleQuestion at chat_controller.js L27-35):

```javascript
submitSampleQuestion(e) {
    this.inputTarget.value = e.target.dataset.chatQuestionParam;
    setTimeout(() => {
        this.formTarget.requestSubmit();
    }, 200);
}
```

The 200ms delay allows the UI to update the input value before submitting (SOURCE SNIPPET, extends.submitSampleQuestion at chat_controller.js L27-35). The question text comes from `data-chat-question-param` on the triggering element.

#### Step 4: Form Submission
Both paths call `this.formTarget.requestSubmit()`, which performs a standard HTML form submission. The form action URL and payload structure are **not documented** in the clue or source snippets.

### 3. Observing the AI Response

#### messagesObserver Pattern
The chat controller uses `this.messagesObserver` to watch for new messages appearing in the chat (FOCUS, extends at chat_controller.js:2-61 — `uses: this.messagesObserver, this.messagesObserver.disconnect`). On `disconnect()`, the observer is cleaned up:

```javascript
disconnect() {
    this.messagesObserver.disconnect()  // inferred from uses annotation
}
```

(FOCUS, extends.disconnect at chat_controller.js:10-14 — `uses: this.messagesObserver, this.messagesObserver.disconnect`).

This supports the narrower claim that the client keeps some observer attached to the messages area and tears it down on disconnect (FOCUS, `extends` at `app/javascript/controllers/chat_controller.js:2-61`; FOCUS, `extends.disconnect` at `app/javascript/controllers/chat_controller.js:10-14`). The clue does not identify the observer type or the exact response transport.

#### Turbo Frame Timeout as Error Recovery
The `turbo_frame_timeout_controller.js` provides a timeout mechanism for frame loads that may apply to chat response delivery. From the source snippet (SOURCE SNIPPET, extends at turbo_frame_timeout_controller.js L2-42):

- On `connect()`, it sets a timeout (default 10000ms via `static values = { timeout: { type: Number, default: 10000 } }`) and listens for `turbo:frame-load` events.
- If the frame loads successfully, `clearTimeout()` cancels the timer.
- If the timeout fires, `handleTimeout()` replaces the element's content with a warning SVG icon and "Timeout" text (SOURCE SNIPPET, extends.handleTimeout at turbo_frame_timeout_controller.js — `this.element.innerHTML = ...`).

This documents a Turbo-frame timeout fallback with a visible `"Timeout"` error state if a frame does not load within the configured window; the clue does not prove that chat responses specifically use that path.

### 4. Mobile Cell Interaction (Supplementary Context)

The `mobile_cell_interaction_controller.js` documents a parallel pattern of DOM observation and tooltip management for mobile table cells. Key mechanisms from source snippets:

- **toggleErrorMessage:** Shows/hides error tooltips with a 3-second auto-dismiss via `setTimeout` (SOURCE SNIPPET, extends.toggleErrorMessage at mobile_cell_interaction_controller.js L73-102). Calls `hideAllTooltipsExcept(tooltip)` first, then toggles visibility.
- **handleCellTouch:** Highlights touched cells with opacity transitions and shows error tooltips if errors exist (SOURCE SNIPPET, extends.handleCellTouch at mobile_cell_interaction_controller.js L50-71). Uses a 1-second timeout to auto-unhighlight.
- **handleDocumentClick:** Dismisses all error tooltips on outside clicks, guarding against clicks on tooltip/icon targets (SOURCE SNIPPET, extends.handleDocumentClick at mobile_cell_interaction_controller.js L23-30).
- **hideAllErrorTooltips:** Iterates all error tooltip targets in the document and adds the `hidden` class (SOURCE SNIPPET, extends.hideAllErrorTooltips at mobile_cell_interaction_controller.js L119-124).

These are not directly part of the Chat API lifecycle but demonstrate the application's pattern of DOM-mutation-based UI updates with timer-driven auto-dismiss — a pattern that may also apply to chat message rendering.

### 5. Lifecycle Summary

```
1. connect()           → Controller attaches; observer setup is implied but not shown
2. autoResize()        → Input textarea dynamically sizes (max 3 lines)
3. handleInputKeyDown() or submitSampleQuestion()
                       → Form submitted via requestSubmit()
4. Server processes    → [NOT DOCUMENTED]
5. Response update     → [NOT DOCUMENTED]
6. messagesObserver    → Some UI observation exists, but exact behavior is not shown
7. turbo-frame-timeout → Some frame loads can show "Timeout" after 10s
8. disconnect()        → messagesObserver.disconnect() on teardown
```

### 6. Gaps and Uncertainties

- **GAPS states:** "type: MECHANISTIC (body logic needed for full answer), coverage: 22 symbols in L3, 2 with behavior annotations" (GAPS).
- **Drill targets identified:** `mobile_cell_interaction_controller.js` (~19 lines, `toggleErrorMessage`), `chat_controller.js` (~2 lines, `disconnect`), `chat_controller.js` (~9 lines, `autoResize`) (GAPS drill entries). The source snippets for these were provided and analyzed above.
- **Server-side lifecycle** (message persistence, AI service invocation, response streaming) is entirely undocumented in the clue.
- The **`connect()` body** of the chat controller is not in the source snippets — the observer initialization logic is inferred from the `uses` annotation.
- **Response delivery mechanism** is not explicitly stated; the clue does not distinguish among frame loads, DOM replacement, streaming, polling, or other transport paths.
- The **SYNTH_API_KEY** in `.env.example` (FOCUS, .env.example:1-86) is the only hint of AI service integration; no client-side AI SDK usage is documented.
