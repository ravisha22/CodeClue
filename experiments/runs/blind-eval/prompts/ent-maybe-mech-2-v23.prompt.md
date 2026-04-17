# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: ent-maybe-mech-2

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.

--- CLUE FILE (File 1) ---
=CC v2.1 maybe@HEAD 91mod 267sym
? How does the documented self-hosting update path work, and what is the recovery flow for a first-time database connection problem?


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

extends.startAutoUpdate (app/components/DS/menu_controller.js:88-96)
  method extends.startAutoUpdate
  called_by: connect, extends
  uses: this._cleanup, this.buttonTarget, this.contentTarget, this.boundUpdate

extends.startAutoUpdate (app/javascript/controllers/tooltip_controller.js:50-58)
  method extends.startAutoUpdate
  called_by: connect, extends
  uses: this._cleanup, this.element, this.tooltipTarget, this.boundUpdate

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

extends.stopAutoUpdate (app/components/DS/tooltip_controller.js:61-66)
  method extends.stopAutoUpdate
  called_by: disconnect, extends
  uses: this._cleanup

extends.stopAutoUpdate (app/components/DS/menu_controller.js:98-103)
  method extends.stopAutoUpdate
  called_by: disconnect, extends
  uses: this._cleanup

extends.stopAutoUpdate (app/javascript/controllers/tooltip_controller.js:60-65)
  method extends.stopAutoUpdate
  called_by: disconnect, extends
  uses: this._cleanup

extends.update (app/javascript/controllers/tooltip_controller.js:67-86)
  method extends.update
  called_by: extends
  uses: this.element, this.tooltipTarget, this.placementValue, this.offsetValue

extends.update (app/javascript/controllers/transfer_match_controller.js:7-15)
  method extends.update
  sig: extends.update(event)
  called_by: extends
  uses: event.target.value, this.newSelectTarget.classList.remove, this.existingSelectTarget.classList.add, this.newSelectTarget.classList.add

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

extends (app/components/DS/menu_controller.js:13-117)
  extends: Controller
  methods: addEventListeners, close, connect, disconnect, focusFirstElement, removeEventListeners
  calls: addEventListeners, close, connect, disconnect, focusFirstElement, removeEventListeners, startAutoUpdate, stopAutoUpdate
  uses: this.show, this.showValue, this.boundUpdate, this.update.bind

extends.clearTimeout (app/javascript/controllers/donut_chart_controller.js:112-112)
  method extends.clearTimeout
  sig: extends.clearTimeout(hoverTimeout)
  called_by: extends

extends.clearTimeout (app/javascript/controllers/auto_submit_form_controller.js:28-28)
  method extends.clearTimeout
  sig: extends.clearTimeout(this.timeout)
  called_by: extends

extends.clearTimeout (app/javascript/controllers/turbo_frame_timeout_controller.js:20-25)
  method extends.clearTimeout
  called_by: disconnect, extends
  uses: this.timeoutId

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

extends (app/javascript/controllers/category_controller.js:3-262)
  extends: Controller
  methods: autoAdjust, backgroundColor, contrast, darkenColor, handleColorChange, handleContrastValidation
  calls: autoAdjust, backgroundColor, contrast, darkenColor, handleColorChange, handleContrastValidation, handleIconChange, handleIconColorChange
  uses: this.pickerBtnTarget.addEventListener, this.showPaletteSection, this.colorInputTarget.addEventListener, this.picker.setColor

extends (app/javascript/controllers/rules_controller.js:2-78)
  extends: Controller
  methods: addAction, addCondition, addConditionGroup, clearEffectiveDate, connect, updateConditionPrefixes
  calls: addAction, addCondition, addConditionGroup, clearEffectiveDate, connect, updateConditionPrefixes
  uses: this.updateConditionPrefixes, this.conditionGroupTemplateTarget, this.conditionsListTarget, this.conditionTemplateTarget

extends.showPaletteSection (app/javascript/controllers/category_controller.js:211-218)
  method extends.showPaletteSection
  calls: initPicker, updatePopupPosition
  called_by: initialize, toggleSections, extends
  uses: this.initPicker, this.colorsSectionTarget.classList.add, this.paletteSectionTarget.classList.remove, this.pickerSectionTarget.classList.remove

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
