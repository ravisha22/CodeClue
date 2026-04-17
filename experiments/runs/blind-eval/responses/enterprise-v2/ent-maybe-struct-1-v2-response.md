# Enterprise v2: ent-maybe-struct-1
Date: 2026-04-17

## Question
What documented surfaces and usage modes does Maybe expose for users, self-hosters, and developers?

## Answer

### 1. User-Facing Surfaces

The clue reveals a rich JavaScript front-end structured under `app/javascript/controllers/` and `app/components/DS/` (INDEX). The user-facing surfaces documented include:

- **Chat interface:** A `chat_controller.js` (60L) exposes methods `autoResize`, `connect`, `disconnect`, `handleInputKeyDown`, and `submitSampleQuestion` (INDEX, chat_controller.js). The `submitSampleQuestion` method sets an input value from `e.target.dataset.chatQuestionParam` and submits a form (SYM, extends.submitSampleQuestion at chat_controller.js:27). This indicates an AI-powered chat surface where users can type questions or select sample prompts.

- **Financial dashboards and charts:** `time_series_chart_controller.js` (570L) provides extensive D3-based charting with trendlines, gradients, tooltips, and empty-state rendering (SYM, extends._drawChart at time_series_chart_controller.js:105; extends._drawTrendline at :119; extends._drawEmpty at :76). A `donut_chart_controller.js` (168L) is also present (INDEX).

- **Category management:** `category_controller.js` (262L) includes color picking (`initPicker`, `backgroundColor`, `luminance`, `contrast`, `darkenColor`), icon selection, and avatar customization (SYM, extends.initPicker at category_controller.js:52; extends.updateAvatarColors at :87).

- **Budgeting:** `budget_form_controller.js` (25L) exposes `toggleAutoFill` for auto-filling budget data (SYM, extends.toggleAutoFill at budget_form_controller.js:5).

- **Trading and transfers:** `trade_form_controller.js` has an async `changeType` method (SYM, extends.changeType at trade_form_controller.js:6), and `transfer_match_controller.js` exposes `update` (SYM, extends.update at transfer_match_controller.js:7).

- **Rules engine:** `rules_controller.js` exposes `updateConditionPrefixes` for managing rule conditions (SYM, extends.updateConditionPrefixes at rules_controller.js:58).

- **Bulk operations:** `bulk_select_controller.js` (165L) supports multi-select with methods like `deselectAll`, `selectedIdsValueChanged`, `_addToSelection`, `_removeFromSelection` (SYM, extends._addToSelection at bulk_select_controller.js:108; extends._removeFromSelection at :114).

- **Design System (DS) components:** Under `app/components/DS/`, the clue documents `dialog_controller.js` (click-outside close), `menu_controller.js` (focus management, auto-positioning), `tabs_controller.js` (tab switching), and `tooltip_controller.js` (auto-update positioning) (INDEX; SYM, extends.close at DS/dialog_controller.js:26; extends.show at DS/tabs_controller.js:9).

- **Theme switching:** `theme_controller.js` supports user preference-driven theming with `applyTheme`, `setTheme`, `systemPrefersDark`, `startSystemThemeListener`, and `userPreferenceValueChanged` (SYM, extends.applyTheme at theme_controller.js:32; extends.setTheme at :43; FOCUS, extends.userPreferenceValueChanged at theme_controller.js:15-17 — calls `applyTheme`).

- **Layout controls:** `app_layout_controller.js` (56L) provides `closeMobileSidebar`, `openMobileSidebar`, `toggleLeftSidebar`, `toggleRightSidebar` (INDEX).

- **Onboarding:** `onboarding_controller.js` exposes `refreshWithParam` (SYM, extends.refreshWithParam at onboarding_controller.js:21).

- **Plaid integration:** `plaid_controller.js` exposes `open` for connecting financial accounts (SYM, extends.open at plaid_controller.js:16).

- **Intercom support widget:** `intercom_controller.js` exposes `show` (SYM, extends.show at intercom_controller.js:5).

### 2. Self-Hosting Mode

- The `.env.example` file documents a self-hosting configuration surface with `SELF_HOSTED=true`, `SECRET_KEY_BASE=secret-value`, `SYNTH_API_KEY=<set>`, `PORT=3000`, `SMTP_ADDRESS=<set>`, and `SMTP_PORT=465` (FOCUS, .env.example:1-86). The `SELF_HOSTED=true` flag indicates a dedicated self-hosting mode.

- The `README.md` documents sections titled "Maybe Hosting", "Forking and Attribution", "Local Development Setup", and "Requirements" (FOCUS, README.md:1-64). This confirms documented guidance for self-hosters covering hosting options, local development, and prerequisites.

### 3. Developer Surfaces

- **Controller-based architecture:** Many front-end modules are controller classes with `connect`/`disconnect`-style lifecycle methods and an `extends: Controller` relationship in the clue (SYM, multiple `extends.*` entries; FOCUS, `extends.userPreferenceValueChanged` at `app/javascript/controllers/theme_controller.js:15-17`).

- **Services layer:** `CurrenciesService.get` in `app/javascript/services/currencies_service.js:2` shows a documented service abstraction (SYM, CurrenciesService.get at currencies_service.js:2).

- **Vendor dependencies:** The TREE shows `vendor/` with 41 JavaScript files, indicating bundled dependencies.

- **Package configuration:** `package.json` is present at the root (TREE).

### 4. Gaps and Uncertainties

- The GAPS section states: "type: STRUCTURAL (answerable from L0-L2), coverage: 3 symbols in L3, 0 with behavior annotations." This means the body-level logic of 3 symbols is not covered, and no behavior annotations exist for them. The clue does not document backend API endpoints, database schema, server-side rendering details, or the full set of 73 additional modules listed as truncated in the INDEX. The README summary is compressed and does not reveal the full text of hosting/development instructions. Authentication mechanisms, user registration flows, and API documentation surfaces are not visible in the clue.
