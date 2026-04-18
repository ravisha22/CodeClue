# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-maybe-rel-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.


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

--- CLUE FILE START ---
=CC v2.1 maybe@HEAD 91mod 270sym
? How are authentication, AI enablement, and endpoint scopes related across Maybe's Chat API?



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
.env.example (.env.example:1-86)
  Config summary for .env.example: entries: SELF_HOSTED=true, SECRET_KEY_BASE=secret-value, SYNTH_API_KEY=<set>, PORT=3000, SMTP_ADDRESS=<set>, SMTP_PORT=465
  entries: SELF_HOSTED=true, SECRET_KEY_BASE=secret-value, SYNTH_API_KEY=<set>, PORT=3000, SMTP_ADDRESS=<set>

README.md (README.md:1-64)
  Documentation summary for README.md: <img width="1190" alt="maybe_hero" src="https://github.com/user-attachments/assets/5ed08763-a9ee-42b2-a436-e05038fcf5... > [!IMPORTANT]; sections: Maybe: The personal finance app for everyone, Maybe Hosting, Forking and Attribution, Local Development Setup, Requirements
  sections: Maybe: The personal finance app for everyone, Maybe Hosting, Forking and Attribution, Local Development Setup, Requirements

extends.submitSampleQuestion (app/javascript/controllers/chat_controller.js:27-35)
  method extends.submitSampleQuestion
  sig: extends.submitSampleQuestion(e)
  called_by: extends
  uses: this.inputTarget.value, e.target.dataset.chatQuestionParam, this.formTarget.requestSubmit

extends (app/javascript/controllers/chat_controller.js:2-61)
  extends: Controller
  methods: autoResize, connect, disconnect, handleInputKeyDown, submitSampleQuestion
  calls: autoResize, connect, disconnect, handleInputKeyDown, submitSampleQuestion
  uses: this.messagesObserver, this.messagesObserver.disconnect, this.inputTarget, input.style.height

extends.autoResize (app/javascript/controllers/chat_controller.js:16-27)
  method extends.autoResize
  called_by: extends
  uses: this.inputTarget, input.style.height, Math.min, input.scrollHeight

extends.connect (app/javascript/controllers/chat_controller.js:6-8)
  method extends.connect
  called_by: extends

extends.disconnect (app/javascript/controllers/chat_controller.js:10-14)
  method extends.disconnect
  called_by: extends
  uses: this.messagesObserver, this.messagesObserver.disconnect

extends.handleInputKeyDown (app/javascript/controllers/chat_controller.js:36-43)
  method extends.handleInputKeyDown
  sig: extends.handleInputKeyDown(e)
  called_by: extends
  uses: e.key, e.shiftKey, e.preventDefault, this.formTarget.requestSubmit

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 8 symbols in L3, 0 with behavior annotations

--- CLUE FILE END ---

QUESTION: How are authentication, AI enablement, and endpoint scopes related across Maybe's Chat API?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
