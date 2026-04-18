# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: ent-maybe-mech-2

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.


--- ARCHITECTURAL CONTEXT (LLM-generated, one-time) ---
(See deep context below for maybe architecture)
--- END ARCHITECTURAL CONTEXT ---

--- DEEP DOMAIN CONTEXT (LLM-generated from key files, one-time) ---
# Maybe Deep Context

-- DOMAIN MODEL
Maybe is fundamentally a family-scoped personal finance ledger with synchronization and analytics layered on top. The root ownership boundary is `Family` (`db/schema.rb`, `app/models/family.rb`), and almost every meaningful financial object—accounts, categories, imports, transactions, holdings, trades, budgets, merchants, chats, invite state—hangs off that family. That design matters because authorization, reporting, and transfer matching all operate at the family boundary rather than purely at the user boundary. Users belong to families; the financial graph belongs to the household.

The core financial abstraction is `Account` in `app/models/account.rb`. It is not a single account type with a subtype enum; it is a delegated type over specific accountable records such as `Depository`, `Investment`, `Crypto`, `Property`, `Vehicle`, `CreditCard`, `Loan`, `OtherAsset`, and `OtherLiability`. The shared `accounts` table stores cross-cutting attributes like `balance`, `cash_balance`, `currency`, `status`, import linkage, and optional Plaid linkage, while the accountable subtype stores type-specific detail. This gives Maybe a unified account list with per-type behavior, while still letting investment, liability, and property accounts diverge where needed.

`Entry` is the real ledger spine. The schema and associations show that `entries` belong to an account and an `entryable` record, with `Transaction`, `Valuation`, and `Trade` all hanging off that polymorphic relationship. In other words, Maybe does not model balances by directly mutating the account row alone. Instead, discrete financial events are recorded as entries, and balances are materialized from those events. That is why accounts have many transactions, valuations, trades, balances, and holdings, yet the system still has a coherent replayable accounting model.

`Transaction` in `app/models/transaction.rb` represents the spending/income layer used for budgeting and cash-flow analysis. Its `kind` enum is analytically meaningful: `standard` transactions participate normally in budgeting, while `funds_movement`, `cc_payment`, `loan_payment`, and `one_time` are treated differently. This is a subtle but important design choice. Maybe is not just storing bank transaction imports; it is classifying financial events into reporting semantics that power budgets, net worth, and transfer logic.

Investment tracking is modeled through `Security`, `Trade`, `Holding`, and price/exchange-rate infrastructure. `Holding` belongs to an account and security, stores dated quantity/price/amount snapshots, and can compute portfolio weight and approximate cost basis from associated trades (`app/models/holding.rb`). `Security` maintains symbol identity and provider-fetched price/details (`app/models/security.rb`). Combined with daily balance materialization and exchange rates, this lets Maybe treat brokerage and crypto accounts as time-series portfolios rather than static balances.

-- API SURFACE
Maybe exposes two overlapping surfaces: a large Rails web app and a smaller JSON API. The web surface in `config/routes.rb` includes accounts, transactions, holdings, trades, valuations, imports, Plaid items, transfers, budgets, rules, settings, subscription/billing, onboarding, MFA, sessions, and webhooks. That breadth suggests the browser UI is still the primary product surface.

The JSON API is more focused. Under `api/v1`, the app exposes mobile-leaning authentication endpoints (`auth/signup`, `auth/login`, `auth/refresh`) plus accounts, transactions, usage, and AI chat resources. `Api::V1::BaseController` forces JSON, skips session auth and CSRF, then authenticates either through Doorkeeper OAuth tokens or API keys. That controller also adds family access checks, scope checks, structured JSON errors, and rate-limit headers for API-key traffic. So the API is intentionally designed for programmatic/mobile use, but it still reuses the same family/account/transaction model as the web app.

The API is not a thin pass-through to Rails models. `Api::V1::AuthController` shows explicit device-aware token issuance: signup/login validate password and device metadata, create or update a `mobile_device`, create a per-device OAuth application, revoke old tokens for that device, and mint new access/refresh tokens. This is a strong hint that the API surface is meant to support persistent mobile clients with controlled token rotation, not just third-party developer access.

Accounts and transactions are the main business API entities. The route structure and tests show list/show/create/update/delete flows for transactions and list access for accounts. Because `BaseController` enforces family scoping, API consumers see a family-local slice of the ledger, not globally addressable records.

The webhook/API edges are equally important. Plaid and Stripe webhook endpoints live under `webhooks/*`, and the model layer contains provider objects and sync/import machinery. That tells you a meaningful portion of Maybe’s “API surface” is inbound system integration rather than only user-initiated REST calls.

-- ROUTING
Maybe’s routing is very domain-oriented and mirrors the product’s user journeys. `config/routes.rb` exposes dedicated flows for onboarding, profile/settings, billing, budgets, categories/tags, transactions, rules, transfers, imports, accounts, subtype-specific account editors, Plaid items, and webhooks. The routes are not overly abstracted; they encode finance-specific actions like account sync, transfer matching, valuation confirmation, import publish/revert/template application, and security lookup.

Accounts show how routing follows the domain model. There is a unified `resources :accounts` block for listing/showing/syncing/toggling activity, but subtype-specific creation/editing happens through `depositories`, `investments`, `properties`, `vehicles`, `credit_cards`, `loans`, `cryptos`, `other_assets`, and `other_liabilities`. That matches the delegated account model: broad account operations stay generic, but type-specific editing gets its own controller surface.

Transactions also expose financial workflows directly in routes. There are bulk update/delete routes, per-transaction transfer matching, category reassignment, and filtered clearing. This means routing is not just CRUD; it encodes operations the product considers first-class financial actions.

Imports and sync routes reveal the ingestion pipeline. Imports have nested upload/configuration/clean/confirm/row/mapping resources, and Plaid items expose `sync` endpoints. Combined with webhook routes for Plaid US/EU and Stripe, the route map makes it clear that Maybe treats ingestion as a staged workflow: fetch raw external data, configure/clean/map it, publish it into internal models, then resync downstream balances.

The API routes sit beside, not beneath, this web routing model. That is important context for any integration work: many of the richest workflows are still web-first and controller-driven, even though some of the same data is exposed through JSON endpoints.

-- AUTH
Maybe uses different auth modes for different surfaces. The browser app relies on regular Rails session authentication plus onboarding/security flows. Routes for `registration`, `sessions`, password reset, email confirmation, and `mfa` show a conventional first-party account system with optional multi-factor auth. The app also uses request-scoped session context for logged-in web flows.

The API uses a more explicit dual-mode model. `Api::V1::BaseController` first attempts OAuth bearer-token auth via Doorkeeper and then falls back to `X-Api-Key` authentication. OAuth tokens must be unexpired and have appropriate scopes (`read` or `read_write`), while API keys must be active and are subject to rate limiting. That means the API supports both first-party session continuation via OAuth-style mobile tokens and long-lived developer/system credentials via API keys.

Scope handling is deliberately hierarchical: `read_write` implies read access, while write operations require `read_write`. `BaseController` also emits consistent JSON for unauthorized, insufficient-scope, not-found, and bad-request cases, which is a sign the team expects real external clients rather than only internal AJAX callers.

Mobile auth is especially opinionated. `AuthController` requires device metadata on signup/login, creates an OAuth application per device, revokes existing tokens for that device, and returns new access/refresh tokens with 30-day lifetime. Combined with refresh-token rotation on the `refresh` endpoint, the design resembles a mobile backend more than a generic Rails API.

Finally, authorization is household-aware. `ensure_current_family_access` verifies that a resource’s `family_id` matches the current resource owner. This is one of the most important domain constraints in the whole app: almost all sensitive access is governed by family ownership, not merely by possession of a valid token.

-- KEY WORKFLOWS
The account creation and synchronization workflow starts with `Account.create_and_sync` in `app/models/account.rb`. It ensures an accountable subtype exists, saves the account, sets an opening balance through `Account::OpeningBalanceManager`, and then schedules a background sync. This shows that even manually created accounts are normalized into the same syncable balance pipeline as imported accounts. The account row is only the seed; the synchronized balance history is the real end state.

The Plaid ingestion workflow is the most important external-data path. `Provider::Plaid` handles link-token creation, public-token exchange, item/account fetches, transaction sync cursors, investment holdings/transactions fetches, liabilities fetches, institution metadata, and webhook verification. `PlaidItem` stores the access token, institution metadata, supported products, and raw snapshots, then delegates to an importer and `PlaidAccount::Processor` to turn fetched payloads into Maybe accounts, transactions, investment transactions, and liabilities. After processing, `schedule_account_syncs` enqueues downstream account syncs so historical balances can be recalculated.

Balance synchronization is intentionally two-stage. `Account::Syncer` first imports market data and then materializes balances, choosing a forward or reverse strategy depending on whether the account is linked. `Account::MarketDataImporter` pulls only the exchange rates and security prices actually needed by the account, based on entry currencies and traded securities. This means Maybe avoids treating market data as a separate product silo; it is supplemental infrastructure used to make account histories and portfolio values analytically coherent.

Investment tracking is therefore not just “store holdings.” Holdings are reconstructed from trades and prices, current holdings are derived from the latest dated record per security, and cost basis/trend calculations are computed from trade history plus exchange rates. For investment and crypto accounts, the account balance is partly the result of security price history imported from providers like Synth, not just imported cash movements.

Transaction and transfer handling form another crucial workflow. Transactions carry classification semantics that affect budgets; transfer-like transactions are grouped by `transfer?`; and the family model includes auto-matching logic for transfers, which account syncers trigger after balance processing. This means Maybe’s sync loop does more than ingest data—it also cleans and reconciles relationships between financial events.

The result is a layered pipeline: external providers fetch data, importer/processor classes map it into internal ledger events, sync services materialize time-series balances and enrich with market data, and family-level automation reconciles transfers and analytics. That architecture is why Maybe can behave like both a daily budgeting app and an investment/net-worth tracker without maintaining completely separate data models for those use cases.

--- END DEEP DOMAIN CONTEXT ---

--- CLUE FILE (File 1) ---
=CC v2.1 maybe@HEAD 91mod 270sym
? How does the documented self-hosting update path work, and what is the recovery flow for a first-time database connection problem?



-- TREE
app/  (50 files)
  javascript/
vendor/  (41 files)
  javascript/
.env.example  README.md  package.json

-- INDEX
app/components/DS/dialog_controller.js           33L  clickOutside, close, connect, extends
app/components/DS/menu_controller.js            117L  addEventListeners, close, connect, disconnect, focusFirstElement
app/components/DS/tabs_controller.js             57L  show, extends
app/components/DS/tooltip_controller.js          87L  addEventListeners, connect, disconnect, removeEventListeners, startAutoUpdate
app/javascript/application.js                     7L  
app/javascript/controllers/app_layout_controller.js    56L  closeMobileSidebar, openMobileSidebar, toggleLeftSidebar, toggleRightSidebar, extends
app/javascript/controllers/application.js        19L  
app/javascript/controllers/auto_submit_form_controller.js    96L  clearTimeout, connect, disconnect, extends
app/javascript/controllers/budget_form_controller.js    25L  toggleAutoFill, extends
app/javascript/controllers/bulk_select_controller.js   165L  bulkEditDrawerHeaderTargetConnected, connect, deselectAll, disconnect, selectedIdsValueChanged
app/javascript/controllers/category_controller.js   262L  autoAdjust, backgroundColor, contrast, darkenColor, handleColorChange
app/javascript/controllers/chat_controller.js    60L  autoResize, connect, disconnect, handleInputKeyDown, submitSampleQuestion
app/javascript/controllers/clipboard_controller.js    28L  copy, showSuccess, extends
app/javascript/controllers/color_avatar_controller.js    28L  connect, disconnect, handleColorChange, extends
app/javascript/controllers/color_select_controller.js    65L  connect, select, selectionValueChanged, extends, hexToRGBA
app/javascript/controllers/confirm_dialog_controller.js    59L  handleConfirm, extends
app/javascript/controllers/deletion_controller.js    28L  chooseSubmitButton, extends
app/javascript/controllers/donut_chart_controller.js   168L  clearTimeout, connect, disconnect, extends
  ...and 73 more modules

-- SYM
extends.backgroundColor             M app/javascript/controllers/category_controller.js:160    method extends.backgroundColor
extends.indexOfLastFocus            M app/javascript/controllers/list_keyboard_navigation_controller.js:26     method extends.indexOfLastFocus
extends.refreshWithParam            M app/javascript/controllers/onboarding_controller.js:21     method extends.refreshWithParam
extends.updateConditionPrefixes     M app/javascript/controllers/rules_controller.js:58     method extends.updateConditionPrefixes
extends.setTheme                    M app/javascript/controllers/theme_controller.js:43     method extends.setTheme
extends.getLinkTargetInDirection    M app/javascript/controllers/list_keyboard_navigation_controller.js:18     method extends.getLinkTargetInDirection
extends.updatePopupPosition         M app/javascript/controllers/category_controller.js:244    method extends.updatePopupPosition
extends.luminance                   M app/javascript/controllers/category_controller.js:173    method extends.luminance
extends.focusLinkTargetInDirection  M app/javascript/controllers/list_keyboard_navigation_controller.js:13     method extends.focusLinkTargetInDirection
extends.findHighlightForField       M app/javascript/controllers/mobile_cell_interaction_controller.js:145    method extends.findHighlightForField
extends.validateRequirementText     M app/javascript/controllers/password_validator_controller.js:37     method extends.validateRequirementText
extends._pluralizedResourceName     M app/javascript/controllers/bulk_select_controller.js:140    method extends._pluralizedResourceName
extends.updateSelectedIconColor     M app/javascript/controllers/category_controller.js:118    method extends.updateSelectedIconColor
extends._resetFormInputs            M app/javascript/controllers/bulk_select_controller.js:97     method extends._resetFormInputs
extends.open                        M app/javascript/controllers/plaid_controller.js:16     method extends.open
extends.showSuccess                 M app/javascript/controllers/clipboard_controller.js:20     method extends.showSuccess
extends.updateAmount                M app/javascript/controllers/money_field_controller.js:14     method extends.updateAmount
extends.scrollToActiveItem          M app/javascript/controllers/scroll_on_connect_controller.js:15     method extends.scrollToActiveItem
extends._d3XScale                   M app/javascript/controllers/time_series_chart_controller.js:503    method extends._d3XScale
extends.close                       M app/components/DS/dialog_controller.js:26     method extends.close
extends.contrast                    M app/javascript/controllers/category_controller.js:183    method extends.contrast
extends.hideAllErrorTooltips        M app/javascript/controllers/mobile_cell_interaction_controller.js:119    method extends.hideAllErrorTooltips
extends._d3YScale                   M app/javascript/controllers/time_series_chart_controller.js:510    method extends._d3YScale
extends.clearTimeout                M app/javascript/controllers/turbo_frame_timeout_controller.js:20     method extends.clearTimeout
extends.handleTimeout               M app/javascript/controllers/turbo_frame_timeout_controller.js:27     method extends.handleTimeout
extends._installTrendlineSplit      M app/javascript/controllers/time_series_chart_controller.js:133    method extends._installTrendlineSplit
extends.validate                    M app/javascript/controllers/password_validator_controller.js:11     method extends.validate
extends.addEventListeners           M app/components/DS/tooltip_controller.js:29     method extends.addEventListeners
extends._getTrendIcon               M app/javascript/controllers/time_series_chart_controller.js:401    method extends._getTrendIcon
extends.hideAllTooltipsExcept       M app/javascript/controllers/mobile_cell_interaction_controller.js:126    method extends.hideAllTooltipsExcept
extends.startSystemThemeListener    M app/javascript/controllers/theme_controller.js:71     method extends.startSystemThemeListener
extends.applyTheme                  M app/javascript/controllers/theme_controller.js:32     method extends.applyTheme
extends.stopSystemThemeListener     M app/javascript/controllers/theme_controller.js:79     method extends.stopSystemThemeListener
extends.showPaletteSection          M app/javascript/controllers/category_controller.js:211    method extends.showPaletteSection
extends._addHiddenFormInputsForSelectedIds M app/javascript/controllers/bulk_select_controller.js:85     method extends._addHiddenFormInputsForSelectedIds
extends.darkenColor                 M app/javascript/controllers/category_controller.js:190    method extends.darkenColor
extends._teardown                   M app/javascript/controllers/time_series_chart_controller.js:39     method extends._teardown
extends._createMainGroup            M app/javascript/controllers/time_series_chart_controller.js:449    method extends._createMainGroup
extends._createMainSvg              M app/javascript/controllers/time_series_chart_controller.js:436    method extends._createMainSvg
extends.initPicker                  M app/javascript/controllers/category_controller.js:52     method extends.initPicker
extends.show                        M app/components/DS/tabs_controller.js:9      method extends.show
extends.toggleAutoFill              M app/javascript/controllers/budget_form_controller.js:5      method extends.toggleAutoFill
extends.handleConfirm               M app/javascript/controllers/confirm_dialog_controller.js:8      method extends.handleConfirm
extends.chooseSubmitButton          M app/javascript/controllers/deletion_controller.js:15     method extends.chooseSubmitButton
extends.remove                      M app/javascript/controllers/element_removal_controller.js:5      method extends.remove
extends.show                        M app/javascript/controllers/intercom_controller.js:5      method extends.show
extends.changeType                  M app/javascript/controllers/trade_form_controller.js:6      async_method extends.changeType
extends.update                      M app/javascript/controllers/transfer_match_controller.js:7      method extends.update
CurrenciesService.get               M app/javascript/services/currencies_service.js:2      method CurrenciesService.get
extends.updateAvatarColors          M app/javascript/controllers/category_controller.js:87     method extends.updateAvatarColors
extends._addToSelection             M app/javascript/controllers/bulk_select_controller.js:108    method extends._addToSelection
extends._removeFromSelection        M app/javascript/controllers/bulk_select_controller.js:114    method extends._removeFromSelection
extends.systemPrefersDark           M app/javascript/controllers/theme_controller.js:51     method extends.systemPrefersDark
extends._drawCenteredCircleEmptyState M app/javascript/controllers/time_series_chart_controller.js:95     method extends._drawCenteredCircleEmptyState
extends._drawDashedLineEmptyState   M app/javascript/controllers/time_series_chart_controller.js:84     method extends._drawDashedLineEmptyState
extends.remove                      M app/javascript/controllers/rule/actions_controller.js:13     method extends.remove
extends.stopAutoUpdate              M app/components/DS/tooltip_controller.js:61     method extends.stopAutoUpdate
extends.toggle                      M app/javascript/controllers/password_visibility_controller.js:11     method extends.toggle
extends._drawChart                  M app/javascript/controllers/time_series_chart_controller.js:105    method extends._drawChart
extends._drawEmpty                  M app/javascript/controllers/time_series_chart_controller.js:76     method extends._drawEmpty
extends.addEventListeners           M app/javascript/controllers/tooltip_controller.js:31     method extends.addEventListeners
extends.removeEventListeners        M app/javascript/controllers/tooltip_controller.js:36     method extends.removeEventListeners
extends.startAutoUpdate             M app/javascript/controllers/tooltip_controller.js:50     method extends.startAutoUpdate
extends.stopAutoUpdate              M app/javascript/controllers/tooltip_controller.js:60     method extends.stopAutoUpdate
extends.removeEventListeners        M app/components/DS/tooltip_controller.js:34     method extends.removeEventListeners
  ...and 205 more symbols

-- FOCUS
extends.updateConditionPrefixes (app/javascript/controllers/rules_controller.js:58-77)
  method extends.updateConditionPrefixes
  behavior: ACCUMULATE(updateConditionPrefix... -> result)
  called_by: addCondition, addConditionGroup, connect, extends
  uses: Array.from, this.conditionsListTarget.children, conditions.forEach, condition.classList.contains

extends._updateGroups (app/javascript/controllers/bulk_select_controller.js:148-158)
  method extends._updateGroups
  behavior: ACCUMULATE(_updateGroups loop -> result)
  called_by: extends
  uses: this.groupTargets.forEach, this.rowTargets.filter, group.contains, row.disabled

extends._updateRows (app/javascript/controllers/bulk_select_controller.js:160-164)
  method extends._updateRows
  behavior: ACCUMULATE(_updateRows loop -> result)
  called_by: extends
  uses: this.rowTargets.forEach, row.checked, this.selectedIdsValue.includes, row.dataset.id

extends.updateBlockLines (app/javascript/controllers/password_validator_controller.js:51-62)
  method extends.updateBlockLines
  sig: extends.updateBlockLines(requirementsMet)
  behavior: ACCUMULATE(updateBlockLines loop -> result)
  called_by: validate, extends
  uses: this.blockLineTargets.forEach, line.classList.remove, line.classList.add

extends.focusFirstElement (app/components/DS/menu_controller.js:78-86)
  method extends.focusFirstElement
  called_by: extends
  uses: this.contentTarget.querySelectorAll, firstFocusableElement.focus

extends.startAutoUpdate (app/components/DS/tooltip_controller.js:50-59)
  method extends.startAutoUpdate
  called_by: extends
  uses: this._cleanup, this.element.querySelector, this.element, this.tooltipTarget

extends.startAutoUpdate (app/javascript/controllers/tooltip_controller.js:50-58)
  method extends.startAutoUpdate
  called_by: connect, extends
  uses: this._cleanup, this.element, this.tooltipTarget, this.boundUpdate

extends.startAutoUpdate (app/components/DS/menu_controller.js:88-96)
  method extends.startAutoUpdate
  called_by: connect, extends
  uses: this._cleanup, this.buttonTarget, this.contentTarget, this.boundUpdate

extends.updateSelectedIconColor (app/javascript/controllers/category_controller.js:118-124)
  method extends.updateSelectedIconColor
  sig: extends.updateSelectedIconColor(color)
  calls: backgroundColor
  called_by: handleColorChange, handleIconColorChange, initPicker, extends
  uses: this.selectedIcon, this.selectedIcon.nextElementSibling, iconWrapper.style.backgroundColor, iconWrapper.style.color

extends.updatePopupPosition (app/javascript/controllers/category_controller.js:244-257)
  method extends.updatePopupPosition
  called_by: initialize, showColorsSection, showPaletteSection, extends
  uses: this.popupTarget, popup.style.top, popup.style.bottom, popup.getBoundingClientRect

extends.updateAvatarColors (app/javascript/controllers/category_controller.js:87-90)
  method extends.updateAvatarColors
  sig: extends.updateAvatarColors(color)
  calls: backgroundColor
  called_by: handleColorChange, initPicker, extends
  uses: this.avatarTarget.style.backgroundColor, this.avatarTarget.style.color

extends.updateTheme (app/javascript/controllers/theme_controller.js:20-29)
  method extends.updateTheme
  sig: extends.updateTheme(event)
  calls: setTheme, systemPrefersDark
  called_by: extends
  uses: event.currentTarget.value, this.setTheme, this.systemPrefersDark

extends._updateSelectionBar (app/javascript/controllers/bulk_select_controller.js:132-138)
  method extends._updateSelectionBar
  calls: _pluralizedResourceName
  called_by: extends
  uses: this.selectedIdsValue.length, this.selectionBarTextTarget.innerText, this._pluralizedResourceName, this.selectionBarTarget.classList.toggle

extends.stopAutoUpdate (app/components/DS/menu_controller.js:98-103)
  method extends.stopAutoUpdate
  called_by: disconnect, extends
  uses: this._cleanup

extends.stopAutoUpdate (app/javascript/controllers/tooltip_controller.js:60-65)
  method extends.stopAutoUpdate
  called_by: disconnect, extends
  uses: this._cleanup

extends.stopAutoUpdate (app/components/DS/tooltip_controller.js:61-66)
  method extends.stopAutoUpdate
  called_by: disconnect, extends
  uses: this._cleanup

extends.update (app/javascript/controllers/transfer_match_controller.js:7-15)
  method extends.update
  sig: extends.update(event)
  called_by: extends
  uses: event.target.value, this.newSelectTarget.classList.remove, this.existingSelectTarget.classList.add, this.newSelectTarget.classList.add

extends.update (app/javascript/controllers/tooltip_controller.js:67-86)
  method extends.update
  called_by: extends
  uses: this.element, this.tooltipTarget, this.placementValue, this.offsetValue

extends.update (app/components/DS/tooltip_controller.js:68-86)
  method extends.update
  called_by: extends
  uses: this.element.querySelector, this.element, this.tooltipTarget, this.placementValue

extends.update (app/components/DS/menu_controller.js:105-116)
  method extends.update
  called_by: extends
  uses: this.buttonTarget, this.contentTarget, this.placementValue, this.offsetValue

extends.updateAmount (app/javascript/controllers/money_field_controller.js:14-26)
  method extends.updateAmount
  sig: extends.updateAmount(currency)
  called_by: handleCurrencyChange, extends
  uses: this.amountTarget.step, currency.step, Number.isFinite, this.amountTarget.value

.env.example (.env.example:1-86)
  Config summary for .env.example: entries: SELF_HOSTED=true, SECRET_KEY_BASE=secret-value, SYNTH_API_KEY=<set>, PORT=3000, SMTP_ADDRESS=<set>, SMTP_PORT=465
  entries: SELF_HOSTED=true, SECRET_KEY_BASE=secret-value, SYNTH_API_KEY=<set>, PORT=3000, SMTP_ADDRESS=<set>

README.md (README.md:1-64)
  Documentation summary for README.md: <img width="1190" alt="maybe_hero" src="https://github.com/user-attachments/assets/5ed08763-a9ee-42b2-a436-e05038fcf5... > [!IMPORTANT]; sections: Maybe: The personal finance app for everyone, Maybe Hosting, Forking and Attribution, Local Development Setup, Requirements
  sections: Maybe: The personal finance app for everyone, Maybe Hosting, Forking and Attribution, Local Development Setup, Requirements

extends (app/components/DS/menu_controller.js:13-117)
  extends: Controller
  methods: addEventListeners, close, connect, disconnect, focusFirstElement, removeEventListeners
  calls: addEventListeners, close, connect, disconnect, focusFirstElement, removeEventListeners, startAutoUpdate, stopAutoUpdate
  uses: this.show, this.showValue, this.boundUpdate, this.update.bind

extends.clearTimeout (app/javascript/controllers/auto_submit_form_controller.js:28-28)
  method extends.clearTimeout
  sig: extends.clearTimeout(this.timeout)
  called_by: extends

extends.clearTimeout (app/javascript/controllers/turbo_frame_timeout_controller.js:20-25)
  method extends.clearTimeout
  called_by: disconnect, extends
  uses: this.timeoutId

extends.clearTimeout (app/javascript/controllers/donut_chart_controller.js:112-112)
  method extends.clearTimeout
  sig: extends.clearTimeout(hoverTimeout)
  called_by: extends

extends.handleTimeout (app/javascript/controllers/turbo_frame_timeout_controller.js:27-41)
  method extends.handleTimeout
  called_by: connect, extends
  uses: this.element.innerHTML, www.w3.org

extends (app/javascript/controllers/bulk_select_controller.js:2-165)
  extends: Controller
  methods: bulkEditDrawerHeaderTargetConnected, connect, deselectAll, disconnect, selectedIdsValueChanged, submitBulkRequest
  calls: _addHiddenFormInputsForSelectedIds, _addToSelection, _pluralizedResourceName, _removeFromSelection, _resetFormInputs, _rowsForGroup, _selectAll, _updateGroups
  uses: document.addEventListener, this._updateView, document.removeEventListener, element.querySelector

extends (app/components/DS/tooltip_controller.js:9-87)
  extends: Controller
  methods: addEventListeners, connect, disconnect, removeEventListeners, startAutoUpdate, stopAutoUpdate
  calls: addEventListeners, connect, disconnect, removeEventListeners, startAutoUpdate, stopAutoUpdate, update
  uses: this._cleanup, this.boundUpdate, this.update.bind, this.addEventListeners

extends (app/javascript/controllers/tooltip_controller.js:9-87)
  extends: Controller
  methods: addEventListeners, connect, disconnect, removeEventListeners, startAutoUpdate, stopAutoUpdate
  calls: addEventListeners, connect, disconnect, removeEventListeners, startAutoUpdate, stopAutoUpdate, update
  uses: this._cleanup, this.boundUpdate, this.update.bind, this.startAutoUpdate

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 12 with behavior annotations
uncovered: extends, extends._drawEmpty, extends._d3Line, extends._draw
drill: app/javascript/controllers/category_controller.js (~6 lines, extends.updateSelectedIconColor)
drill: app/javascript/controllers/rules_controller.js (~18 lines, extends.updateConditionPrefixes)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## extends.updateSelectedIconColor  (app/javascript/controllers/category_controller.js L118-124)
```
  updateSelectedIconColor(color) {
    if (this.selectedIcon) {
      const iconWrapper = this.selectedIcon.nextElementSibling;
      iconWrapper.style.backgroundColor = `${this.#backgroundColor(color)}`;
      iconWrapper.style.color = color;
    }
  }
```

## extends.updateConditionPrefixes  (app/javascript/controllers/rules_controller.js L58-77)
```
  updateConditionPrefixes() {
    const conditions = Array.from(this.conditionsListTarget.children);
    let conditionIndex = 0;

    conditions.forEach((condition) => {
      // Only process visible conditions, this prevents conditions that are marked for removal and hidden
      // from being added to the index. This is important when editing a rule.
      if (!condition.classList.contains('hidden')) {
        const prefixEl = condition.querySelector('[data-condition-prefix]');
        if (prefixEl) {
          if (conditionIndex === 0) {
            prefixEl.classList.add('hidden');
          } else {
            prefixEl.classList.remove('hidden');
          }
          conditionIndex++;
        }
      }
    });
  }
```

## extends.addAction  (app/javascript/controllers/rules_controller.js L35-37)
```
  addAction() {
    this.#appendTemplate(this.actionTemplateTarget, this.actionsListTarget);
  }
```

## extends.addCondition  (app/javascript/controllers/rules_controller.js L27-33)
```
  addCondition() {
    this.#appendTemplate(
      this.conditionTemplateTarget,
      this.conditionsListTarget,
    );
    this.updateConditionPrefixes();
  }
```

## extends.addConditionGroup  (app/javascript/controllers/rules_controller.js L19-25)
```
  addConditionGroup() {
    this.#appendTemplate(
      this.conditionGroupTemplateTarget,
      this.conditionsListTarget,
    );
    this.updateConditionPrefixes();
  }
```

## extends.clearEffectiveDate  (app/javascript/controllers/rules_controller.js L39-41)
```
  clearEffectiveDate() {
    this.effectiveDateInputTarget.value = "";
  }
```

## extends.connect  (app/javascript/controllers/turbo_frame_timeout_controller.js L7-14)
```
  connect() {
    this.timeoutId = setTimeout(() => {
      this.handleTimeout()
    }, this.timeoutValue)

    // Listen for successful frame loads to clear timeout
    this.element.addEventListener("turbo:frame-load", this.clearTimeout.bind(this))
  }
```

## extends  (app/javascript/controllers/turbo_frame_timeout_controller.js L2-42)
```

// Connects to data-controller="turbo-frame-timeout"
export default class extends Controller {
  static values = { timeout: { type: Number, default: 10000 } }

  connect() {
    this.timeoutId = setTimeout(() => {
      this.handleTimeout()
    }, this.timeoutValue)

    // Listen for successful frame loads to clear timeout
    this.element.addEventListener("turbo:frame-load", this.clearTimeout.bind(this))
  }

  disconnect() {
    this.clearTimeout()
  }

  clearTimeout() {
    if (this.timeoutId) {
      clearTimeout(this.timeoutId)
      this.timeoutId = null
    }
  }

  handleTimeout() {
    // Replace loading content with error state
    this.element.innerHTML = `
      <div class="flex items-center justify-end gap-1">
        <div class="w-8 h-4 flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-warning">
            <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>
            <path d="M12 9v4"/>
            <path d="m12 17 .01 0"/>
          </svg>
        </div>
        <p class="font-mono text-right text-xs text-warning">Timeout</p>
      </div>
    `
  }
} 
```

## extends.autoAdjust  (app/javascript/controllers/category_controller.js L147-151)
```
  autoAdjust(e) {
    const currentRGBA = this.picker.getColor();
    const adjustedRGBA = this.darkenColor(currentRGBA).toString();
    this.picker.setColor(adjustedRGBA);
  }
```

## extends.backgroundColor  (app/javascript/controllers/category_controller.js L160-171)
```
  backgroundColor([r, g, b, a], percentage) {
    const mixedR = Math.round(
      r * (percentage / 100) + 255 * (1 - percentage / 100),
    );
    const mixedG = Math.round(
      g * (percentage / 100) + 255 * (1 - percentage / 100),
    );
    const mixedB = Math.round(
      b * (percentage / 100) + 255 * (1 - percentage / 100),
    );
    return [mixedR, mixedG, mixedB];
  }
```

## extends.contrast  (app/javascript/controllers/category_controller.js L183-188)
```
  contrast(foregroundColor, backgroundColor) {
    const fgLum = this.luminance(foregroundColor);
    const bgLum = this.luminance(backgroundColor);
    const [l1, l2] = [Math.max(fgLum, bgLum), Math.min(fgLum, bgLum)];
    return (l1 + 0.05) / (l2 + 0.05);
  }
```

## extends.darkenColor  (app/javascript/controllers/category_controller.js L190-209)
```
  darkenColor(color) {
    let darkened = color.toRGBA();
    const backgroundColor = this.backgroundColor(darkened, 10);
    let contrastRatio = this.contrast(darkened, backgroundColor);

    while (
      contrastRatio < 4.5 &&
      (darkened[0] > 0 || darkened[1] > 0 || darkened[2] > 0)
    ) {
      darkened = [
        Math.max(0, darkened[0] - 10),
        Math.max(0, darkened[1] - 10),
        Math.max(0, darkened[2] - 10),
        darkened[3],
      ];
      contrastRatio = this.contrast(darkened, backgroundColor);
    }

    return `rgba(${darkened.join(", ")})`;
  }
```

## extends.handleColorChange  (app/javascript/controllers/color_avatar_controller.js L22-27)
```
  handleColorChange(e) {
    const color = e.currentTarget.value;
    this.avatarTarget.style.backgroundColor = `color-mix(in srgb, ${color} 10%, transparent)`;
    this.avatarTarget.style.borderColor = `color-mix(in srgb, ${color} 10%, transparent)`;
    this.avatarTarget.style.color = color;
  }
```

## extends.handleContrastValidation  (app/javascript/controllers/category_controller.js L134-145)
```
  handleContrastValidation(contrastRatio) {
    if (contrastRatio < 4.5) {
      this.colorInputTarget.setCustomValidity(
        "Poor contrast, choose darker color or auto-adjust.",
      );

      this.validationMessageTarget.classList.remove("hidden");
    } else {
      this.colorInputTarget.setCustomValidity("");
      this.validationMessageTarget.classList.add("hidden");
    }
  }
```

## extends.handleIconChange  (app/javascript/controllers/category_controller.js L107-116)
```
  handleIconChange(e) {
    const iconSVG = e.currentTarget
      .closest("label")
      .querySelector("svg")
      .cloneNode(true);
    this.avatarTarget.innerHTML = "";
    iconSVG.style.padding = "0px";
    iconSVG.classList.add("w-8", "h-8");
    this.avatarTarget.appendChild(iconSVG);
  }
```

## extends.handleIconColorChange  (app/javascript/controllers/category_controller.js L92-105)
```
  handleIconColorChange(e) {
    const selectedIcon = e.target;
    this.selectedIcon = selectedIcon;

    const currentColor = this.colorInputTarget.value;

    this.iconTargets.forEach((icon) => {
      const iconWrapper = icon.nextElementSibling;
      iconWrapper.style.removeProperty("background-color");
      iconWrapper.style.removeProperty("color");
    });

    this.updateSelectedIconColor(currentColor);
  }
```

## extends.handleParentChange  (app/javascript/controllers/category_controller.js L153-158)
```
  handleParentChange(e) {
    const parent = e.currentTarget.value;
    const display =
      typeof parent === "string" && parent !== "" ? "none" : "flex";
    this.selectionTarget.style.display = display;
  }
```

## extends.initPicker  (app/javascript/controllers/category_controller.js L52-85)
```
  initPicker() {
    const pickerContainer = document.createElement("div");
    pickerContainer.classList.add("pickerContainer");
    this.pickerSectionTarget.append(pickerContainer);

    this.picker = Pickr.create({
      el: this.pickerBtnTarget,
      theme: "monolith",
      container: ".pickerContainer",
      useAsButton: true,
      showAlways: true,
      default: this.colorInputTarget.value,
      components: {
        hue: true,
      },
    });

    this.picker.on("change", (color) => {
      const hexColor = color.toHEXA().toString();
      const rgbacolor = color.toRGBA();

      this.updateAvatarColors(hexColor);
      this.updateSelectedIconColor(hexColor);

      const backgroundColor = this.backgroundColor(rgbacolor, 10);
      const contrastRatio = this.contrast(rgbacolor, backgroundColor);

      this.colorInputTarget.value = hexColor;
      this.colorInputTarget.dataset.colorPickerColorValue = hexColor;
      this.colorPreviewTarget.style.backgroundColor = hexColor;

      this.handleContrastValidation(contrastRatio);
    });
  }
```

## extends.initialize  (app/javascript/controllers/category_controller.js L25-50)
```
  initialize() {
    this.pickerBtnTarget.addEventListener("click", () => {
      this.showPaletteSection();
    });

    this.colorInputTarget.addEventListener("input", (e) => {
      this.picker.setColor(e.target.value);
    });

    this.detailsTarget.addEventListener("toggle", (e) => {
      if (!this.colorInputTarget.checkValidity()) {
        e.preventDefault();
        this.colorInputTarget.reportValidity();
        e.target.open = true;
      }
      this.updatePopupPosition()
    });

    this.selectedIcon = null;

    if (!this.presetColorsValue.includes(this.colorInputTarget.value)) {
      this.colorPickerRadioBtnTarget.checked = true;
    }

    document.addEventListener("mousedown", this.handleOutsideClick);
  }
```

## extends.luminance  (app/javascript/controllers/category_controller.js L173-181)
```
  luminance([r, g, b]) {
    const toLinear = (c) => {
      const scaled = c / 255;
      return scaled <= 0.04045
        ? scaled / 12.92
        : ((scaled + 0.055) / 1.055) ** 2.4;
    };
    return 0.2126 * toLinear(r) + 0.7152 * toLinear(g) + 0.0722 * toLinear(b);
  }
```

## extends.showColorsSection  (app/javascript/controllers/category_controller.js L220-228)
```
  showColorsSection() {
    this.colorsSectionTarget.classList.remove("hidden");
    this.paletteSectionTarget.classList.add("hidden");
    this.pickerSectionTarget.classList.add("hidden");
    this.updatePopupPosition()
    if (this.picker) {
      this.picker.destroyAndRemove();
    }
  }
```

## extends.showPaletteSection  (app/javascript/controllers/category_controller.js L211-218)
```
  showPaletteSection() {
    this.initPicker();
    this.colorsSectionTarget.classList.add("hidden");
    this.paletteSectionTarget.classList.remove("hidden");
    this.pickerSectionTarget.classList.remove("hidden");
    this.updatePopupPosition();
    this.picker.show();
  }
```

## extends.toggleSections  (app/javascript/controllers/category_controller.js L230-236)
```
  toggleSections() {
    if (this.colorsSectionTarget.classList.contains("hidden")) {
      this.showColorsSection();
    } else {
      this.showPaletteSection();
    }
  }
```

## extends.updateAvatarColors  (app/javascript/controllers/category_controller.js L87-90)
```
  updateAvatarColors(color) {
    this.avatarTarget.style.backgroundColor = `${this.#backgroundColor(color)}`;
    this.avatarTarget.style.color = color;
  }
```

## extends.updatePopupPosition  (app/javascript/controllers/category_controller.js L244-257)
```
  updatePopupPosition() {
    const popup = this.popupTarget;
    popup.style.top = "";
    popup.style.bottom = "";

    const rect = popup.getBoundingClientRect();
    const overflow = rect.bottom > window.innerHeight;

    if (overflow) {
      popup.style.bottom = "0px";
    } else {
      popup.style.bottom = "";
    }
  }
```
--- END SOURCE SNIPPETS ---

QUESTION: How does the documented self-hosting update path work, and what is the recovery flow for a first-time database connection problem?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
