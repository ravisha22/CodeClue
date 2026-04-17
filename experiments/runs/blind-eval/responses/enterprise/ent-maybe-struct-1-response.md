# Enterprise Eval: ent-maybe-struct-1
Date: 2026-04-17

## Question
What documented surfaces and usage modes does Maybe expose for users, self-hosters, and developers?

---

## Reasoning Trace

### 1. Relevant Symbols from FOCUS, SYM, and INDEX

The clue file covers **91 modules and 267 symbols** across `app/javascript/` and `vendor/javascript/` (TREE). All documented code is **client-side JavaScript**, predominantly controller-style modules following an `extends Controller` pattern. The following surfaces can be identified:

### 2. Documented User-Facing Surfaces

**Chat / AI Assistant Interface:**
- `chat_controller.js` (INDEX, 60L): exposes `autoResize`, `connect`, `disconnect`, `handleInputKeyDown`, `submitSampleQuestion`. This documents an interactive chat UI surface where users can type messages and submit sample questions (FOCUS: `extends.submitSampleQuestion` uses `e.target.dataset.chatQuestionParam` and `this.formTarget.requestSubmit`).

**Theming / Appearance Modes:**
- `theme_controller.js` (FOCUS, L2–87): extends Controller with methods `applyTheme`, `setTheme`, `toggle`, `updateTheme`, `systemPrefersDark`, `startSystemThemeListener`, `stopSystemThemeListener`. Source snippet `applyTheme` (L32–40) shows three user preference modes: `"system"`, `"dark"`, and explicit light (else branch). `setTheme` (L43–49) sets `data-theme` attribute to `"dark"` or `"light"` on `document.documentElement`. `toggle` (L62–69) flips between current dark/light. `userPreferenceValueChanged` (L15–17) triggers `applyTheme()` on preference change. `startSystemThemeListener` (L71–77) listens to `prefers-color-scheme: dark` media query changes.

**Financial Management Surfaces:**
- `budget_form_controller.js` (INDEX, 25L): `toggleAutoFill` method — budgeting UI (SYM: `extends.toggleAutoFill`).
- `trade_form_controller.js` (SYM): `async_method extends.changeType` — trading/investment form.
- `transfer_match_controller.js` (SYM): `extends.update` — transfer matching.
- `money_field_controller.js` (SYM): `extends.updateAmount` — monetary input fields.
- `CurrenciesService.get` (SYM, `app/javascript/services/currencies_service.js:2`): currency data service.

**Banking Integration:**
- `plaid_controller.js` (SYM): `extends.open` (L16) — Plaid banking integration surface.

**Data Visualization:**
- `time_series_chart_controller.js` (INDEX, 570L): extensive D3-based charting with trendlines, tooltips, gradients, empty states. Methods include `_drawChart`, `_drawTrendline`, `_drawGradientBelowTrendline`, `_trackMouseForShowingTooltip`, `_tooltipTemplate` (SYM, multiple entries).
- `donut_chart_controller.js` (INDEX, 168L): donut chart visualization.

**Layout & Navigation:**
- `app_layout_controller.js` (INDEX, 56L): `closeMobileSidebar`, `openMobileSidebar`, `toggleLeftSidebar`, `toggleRightSidebar` — responsive layout with mobile and desktop sidebar modes.

**Design System (DS) Components:**
- `DS/dialog_controller.js` (INDEX, 33L): `clickOutside`, `close`, `connect`.
- `DS/menu_controller.js` (INDEX, 117L): `addEventListeners`, `close`, `connect`, `disconnect`, `focusFirstElement`.
- `DS/tabs_controller.js` (INDEX, 57L): `show`.
- `DS/tooltip_controller.js` (INDEX, 87L): `addEventListeners`, `connect`, `disconnect`, `removeEventListeners`, `startAutoUpdate`.

**Rules / Automation:**
- `rules_controller.js` (SYM): `extends.updateConditionPrefixes` — rule condition management.

**Onboarding:**
- `onboarding_controller.js` (SYM): `extends.refreshWithParam` — onboarding flow.

**Bulk Operations:**
- `bulk_select_controller.js` (INDEX, 165L): `bulkEditDrawerHeaderTargetConnected`, `connect`, `deselectAll`, `disconnect`, `selectedIdsValueChanged` — bulk selection and editing.

**Support Integration:**
- `intercom_controller.js` (SYM): `extends.show` — Intercom chat/support widget.

**Security:**
- `password_validator_controller.js` (SYM): `extends.validate`, `extends.validateRequirementText` — password validation.

**Turbo Frame Timeout Handling:**
- `turbo_frame_timeout_controller.js` (source snippet, L2–42): data-controller `"turbo-frame-timeout"` with configurable `timeout` value (default 10000ms). On timeout, replaces content with a warning SVG icon and "Timeout" text.

### 3. What GAPS Says Cannot Be Determined

The GAPS section states:
- **type: MECHANISTIC** — body logic is needed for full answer (GAPS L180).
- **coverage: 11 symbols in L3, 1 with behavior annotations** (GAPS L181).
- Drill targets are limited to `theme_controller.js` functions (GAPS L182–183).

**Critical limitation:** The entire clue file covers **only the JavaScript frontend layer** (91 modules under `app/javascript/` and `vendor/javascript/`). There is **no documentation** of:
- Backend/server-side code (controllers, models, API endpoints)
- Self-hosting configuration files (Dockerfiles, docker-compose, .env)
- Developer API documentation or REST/GraphQL endpoints
- Database schemas or migrations
- Authentication/authorization flows on the server side
- Self-hoster administration panels or configuration surfaces

### 4. Synthesis

**Supported conclusions (from evidence):**

Maybe's documented frontend exposes the following surfaces and modes:
1. **Personal finance management** — budgets, trades, transfers, money fields, currencies, categories (INDEX + SYM across multiple controllers).
2. **AI chat interface** — interactive chat with sample questions and auto-resizing input (INDEX: `chat_controller.js`).
3. **Three theme modes** — system, dark, light — with live OS preference tracking (FOCUS + source: `theme_controller.js`).
4. **Data visualization** — time-series charts with D3 and donut charts (INDEX + SYM: `time_series_chart_controller.js`, `donut_chart_controller.js`).
5. **Design system** — reusable dialog, menu, tabs, tooltip components (INDEX: `DS/` directory).
6. **Plaid banking integration** (SYM: `plaid_controller.js`).
7. **Intercom support** (SYM: `intercom_controller.js`).
8. **Onboarding flow** (SYM: `onboarding_controller.js`).
9. **Responsive layout** with mobile/desktop sidebar toggling (INDEX: `app_layout_controller.js`).
10. **Rules/automation engine** UI (SYM: `rules_controller.js`).
11. **Bulk operations** with selection bar (INDEX: `bulk_select_controller.js`).

**Remaining uncertainty:**
- No self-hosting surfaces, developer APIs, or deployment modes are documented in this clue file. The question's scope regarding self-hosters and developers **cannot be answered** from the available evidence, which is limited exclusively to client-side JavaScript controllers.
