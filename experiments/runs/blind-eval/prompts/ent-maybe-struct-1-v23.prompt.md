# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: ent-maybe-struct-1

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.

--- CLUE FILE (File 1) ---
=CC v2.1 maybe@HEAD 91mod 267sym
? What documented surfaces and usage modes does Maybe expose for users, self-hosters, and developers?


-- TREE
app/  (50 files)
  javascript/
vendor/  (41 files)
  javascript/

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
extends.applyTheme                  M app/javascript/controllers/theme_controller.js:32     method extends.applyTheme
extends.startSystemThemeListener    M app/javascript/controllers/theme_controller.js:71     method extends.startSystemThemeListener
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
  ...and 202 more symbols

-- FOCUS
extends.userPreferenceValueChanged (app/javascript/controllers/theme_controller.js:15-17)
  method extends.userPreferenceValueChanged
  calls: applyTheme
  called_by: extends
  uses: this.applyTheme

extends (app/javascript/controllers/theme_controller.js:2-87)
  extends: Controller
  methods: applyTheme, connect, disconnect, setTheme, startSystemThemeListener, stopSystemThemeListener
  calls: applyTheme, connect, disconnect, setTheme, startSystemThemeListener, stopSystemThemeListener, systemPrefersDark, toggle
  uses: this.startSystemThemeListener, this.stopSystemThemeListener, e.g, this.applyTheme

extends.applyTheme (app/javascript/controllers/theme_controller.js:32-40)
  method extends.applyTheme
  calls: setTheme, systemPrefersDark
  called_by: userPreferenceValueChanged, extends
  uses: this.userPreferenceValue, this.setTheme, this.systemPrefersDark

extends.setTheme (app/javascript/controllers/theme_controller.js:43-49)
  method extends.setTheme
  sig: extends.setTheme(isDark)
  called_by: applyTheme, toggle, updateTheme, extends
  uses: document.documentElement.setAttribute

extends.systemPrefersDark (app/javascript/controllers/theme_controller.js:51-53)
  method extends.systemPrefersDark
  behavior: DELEGATE(window.matchMedia -> result)
  called_by: applyTheme, updateTheme, extends
  uses: window.matchMedia

extends.updateTheme (app/javascript/controllers/theme_controller.js:20-29)
  method extends.updateTheme
  sig: extends.updateTheme(event)
  calls: setTheme, systemPrefersDark
  called_by: extends
  uses: event.currentTarget.value, this.setTheme, this.systemPrefersDark

extends.connect (app/javascript/controllers/theme_controller.js:6-8)
  method extends.connect
  calls: startSystemThemeListener
  called_by: extends
  uses: this.startSystemThemeListener

extends.disconnect (app/javascript/controllers/theme_controller.js:10-12)
  method extends.disconnect
  calls: stopSystemThemeListener
  called_by: extends
  uses: this.stopSystemThemeListener

extends.startSystemThemeListener (app/javascript/controllers/theme_controller.js:71-77)
  method extends.startSystemThemeListener
  called_by: connect, extends
  uses: this.darkMediaQuery, window.matchMedia, this.darkMediaQuery.addEventListener, this.handleSystemThemeChange

extends.stopSystemThemeListener (app/javascript/controllers/theme_controller.js:79-86)
  method extends.stopSystemThemeListener
  called_by: disconnect, extends
  uses: this.darkMediaQuery, this.darkMediaQuery.removeEventListener, this.handleSystemThemeChange

extends.toggle (app/javascript/controllers/theme_controller.js:62-69)
  method extends.toggle
  calls: setTheme
  called_by: extends
  uses: document.documentElement.getAttribute, this.setTheme

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 11 symbols in L3, 1 with behavior annotations
drill: app/javascript/controllers/theme_controller.js (~1 lines, extends.userPreferenceValueChanged)
drill: app/javascript/controllers/theme_controller.js (~4 lines, extends.setTheme)
drill: app/javascript/controllers/theme_controller.js (~6 lines, extends.applyTheme)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## extends.userPreferenceValueChanged  (app/javascript/controllers/theme_controller.js L15-17)
```
  userPreferenceValueChanged() {
    this.applyTheme();
  }
```

## extends.setTheme  (app/javascript/controllers/theme_controller.js L43-49)
```
  setTheme(isDark) {
    if (isDark) {
      document.documentElement.setAttribute("data-theme", "dark");
    } else {
      document.documentElement.setAttribute("data-theme", "light");
    }
  }
```

## extends.applyTheme  (app/javascript/controllers/theme_controller.js L32-40)
```
  applyTheme() {
    if (this.userPreferenceValue === "system") {
      this.setTheme(this.systemPrefersDark());
    } else if (this.userPreferenceValue === "dark") {
      this.setTheme(true);
    } else {
      this.setTheme(false);
    }
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

## extends.disconnect  (app/javascript/controllers/turbo_frame_timeout_controller.js L16-18)
```
  disconnect() {
    this.clearTimeout()
  }
```

## extends.startSystemThemeListener  (app/javascript/controllers/theme_controller.js L71-77)
```
  startSystemThemeListener() {
    this.darkMediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    this.darkMediaQuery.addEventListener(
      "change",
      this.handleSystemThemeChange,
    );
  }
```

## extends.stopSystemThemeListener  (app/javascript/controllers/theme_controller.js L79-86)
```
  stopSystemThemeListener() {
    if (this.darkMediaQuery) {
      this.darkMediaQuery.removeEventListener(
        "change",
        this.handleSystemThemeChange,
      );
    }
  }
```

## extends.systemPrefersDark  (app/javascript/controllers/theme_controller.js L51-53)
```
  systemPrefersDark() {
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  }
```

## extends.toggle  (app/javascript/controllers/theme_controller.js L62-69)
```
  toggle() {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    if (currentTheme === "dark") {
      this.setTheme(false);
    } else {
      this.setTheme(true);
    }
  }
```

## extends.updateTheme  (app/javascript/controllers/theme_controller.js L20-29)
```
  updateTheme(event) {
    const selectedTheme = event.currentTarget.value;
    if (selectedTheme === "system") {
      this.setTheme(this.systemPrefersDark());
    } else if (selectedTheme === "dark") {
      this.setTheme(true);
    } else {
      this.setTheme(false);
    }
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
--- END SOURCE SNIPPETS ---

QUESTION: What documented surfaces and usage modes does Maybe expose for users, self-hosters, and developers?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
