# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: ent-maybe-struct-2

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.

--- CLUE FILE (File 1) ---
=CC v2.1 maybe@HEAD 91mod 267sym
? What files and setup artifacts are documented for getting a self-hosted Maybe deployment running with Docker?


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
extends._setupResizeObserver (app/javascript/controllers/time_series_chart_controller.js:564-569)
  method extends._setupResizeObserver
  called_by: connect, extends
  uses: this._resizeObserver, this._reinstall, this._resizeObserver.observe, this.element

extends (app/javascript/controllers/time_series_chart_controller.js:5-570)
  extends: Controller
  methods: connect, disconnect
  calls: _createMainGroup, _createMainSvg, _d3Container, _d3ContainerHeight, _d3ContainerWidth, _d3Group, _d3Line, _d3Svg
  uses: this._install, document.addEventListener, this._reinstall, this._setupResizeObserver

extends.fileSelected (app/javascript/controllers/file_upload_controller.js:34-54)
  method extends.fileSelected
  called_by: extends
  uses: this.hasInputTarget, this.inputTarget.files.length, this.inputTarget.files, this.hasFileNameTarget

extends.connect (app/javascript/controllers/time_series_chart_controller.js:22-26)
  method extends.connect
  calls: _install, _setupResizeObserver
  called_by: extends
  uses: this._install, document.addEventListener, this._reinstall, this._setupResizeObserver

extends._drawChart (app/javascript/controllers/time_series_chart_controller.js:105-117)
  method extends._drawChart
  calls: _drawGradientBelowTrendline, _drawTooltip, _drawTrendline, _drawXAxisLabels, _trackMouseForShowingTooltip
  called_by: _draw, extends
  uses: this._drawTrendline, this.useLabelsValue, this._drawXAxisLabels, this._drawGradientBelowTrendline

extends._trackMouseForShowingTooltip (app/javascript/controllers/time_series_chart_controller.js:284-373)
  method extends._trackMouseForShowingTooltip
  calls: _d3XScale, _d3YScale, _setTrendlineSplitAt, _tooltipTemplate
  called_by: _drawChart, extends
  uses: d3.bisector, d.date, this._d3Group, this._d3ContainerWidth

extends._install (app/javascript/controllers/time_series_chart_controller.js:48-52)
  method extends._install
  calls: _draw, _normalizeDataPoints, _rememberInitialContainerSize
  called_by: connect, extends
  uses: this._normalizeDataPoints, this._rememberInitialContainerSize, this._draw

extends._draw (app/javascript/controllers/time_series_chart_controller.js:68-74)
  method extends._draw
  calls: _drawChart, _drawEmpty
  called_by: _install, extends
  uses: this._normalDataPoints.length, this._drawEmpty, this._drawChart

extends._drawEmpty (app/javascript/controllers/time_series_chart_controller.js:76-82)
  method extends._drawEmpty
  calls: _drawCenteredCircleEmptyState, _drawDashedLineEmptyState
  called_by: _draw, extends
  uses: this._d3Svg.selectAll, this._drawDashedLineEmptyState, this._drawCenteredCircleEmptyState

extends._drawGradientBelowTrendline (app/javascript/controllers/time_series_chart_controller.js:222-272)
  method extends._drawGradientBelowTrendline
  calls: _d3XScale, _d3YScale
  called_by: _drawChart, extends
  uses: this._d3Group, this.element.id, this._d3YScale, d3.max

extends._d3XScale (app/javascript/controllers/time_series_chart_controller.js:503-508)
  method extends._d3XScale
  called_by: _d3Line, _drawGradientBelowTrendline, _trackMouseForShowingTooltip, extends
  uses: this._d3ContainerWidth, d3.extent, this._normalDataPoints, d.date

extends._d3YScale (app/javascript/controllers/time_series_chart_controller.js:510-562)
  method extends._d3YScale
  behavior: GUARD(dataMin === dataMax -> const padding = dat...); PRECEDENCE(dataMin -> relativeChange -> useLabelsValue -> default)
  called_by: _d3Line, _drawGradientBelowTrendline, _trackMouseForShowingTooltip, extends
  uses: d3.min, this._normalDataPoints, this._getDatumValue, d3.max

extends._drawTrendline (app/javascript/controllers/time_series_chart_controller.js:119-131)
  method extends._drawTrendline
  calls: _installTrendlineSplit
  called_by: _drawChart, extends
  uses: this._installTrendlineSplit, this._d3Group, this._normalDataPoints, this.element.id

extends._tooltipTemplate (app/javascript/controllers/time_series_chart_controller.js:375-399)
  method extends._tooltipTemplate
  sig: extends._tooltipTemplate(datum)
  calls: _getTrendIcon
  called_by: _trackMouseForShowingTooltip, extends
  uses: datum.date_formatted, this._getTrendIcon, this._extractFormattedValue, datum.trend.current

extends._d3Line (app/javascript/controllers/time_series_chart_controller.js:496-501)
  method extends._d3Line
  calls: _d3XScale, _d3YScale
  called_by: extends
  uses: this._d3XScale, d.date, this._d3YScale, this._getDatumValue

extends._createMainGroup (app/javascript/controllers/time_series_chart_controller.js:449-453)
  method extends._createMainGroup
  called_by: _d3Group, extends
  uses: this._d3Svg, this._margin.left, this._margin.top

extends._createMainSvg (app/javascript/controllers/time_series_chart_controller.js:436-447)
  method extends._createMainSvg
  called_by: _d3Svg, extends
  uses: this._d3Container, this._d3InitialContainerWidth, this._d3InitialContainerHeight

extends._d3Container (app/javascript/controllers/time_series_chart_controller.js:488-490)
  method extends._d3Container
  behavior: DELEGATE(d3.select -> result)
  called_by: extends
  uses: d3.select, this.element

extends._d3ContainerHeight (app/javascript/controllers/time_series_chart_controller.js:482-486)
  method extends._d3ContainerHeight
  called_by: extends
  uses: this._d3InitialContainerHeight, this._margin.top, this._margin.bottom

extends._d3ContainerWidth (app/javascript/controllers/time_series_chart_controller.js:476-480)
  method extends._d3ContainerWidth
  called_by: extends
  uses: this._d3InitialContainerWidth, this._margin.left, this._margin.right

extends._d3Group (app/javascript/controllers/time_series_chart_controller.js:462-467)
  method extends._d3Group
  calls: _createMainGroup
  called_by: extends
  uses: this._d3GroupMemo, this._createMainGroup

extends._d3Svg (app/javascript/controllers/time_series_chart_controller.js:455-460)
  method extends._d3Svg
  calls: _createMainSvg
  called_by: extends
  uses: this._d3SvgMemo, this._createMainSvg

extends._drawCenteredCircleEmptyState (app/javascript/controllers/time_series_chart_controller.js:95-103)
  method extends._drawCenteredCircleEmptyState
  called_by: _drawEmpty, extends
  uses: this._d3Svg, this._d3InitialContainerWidth, this._d3InitialContainerHeight

extends._drawDashedLineEmptyState (app/javascript/controllers/time_series_chart_controller.js:84-93)
  method extends._drawDashedLineEmptyState
  called_by: _drawEmpty, extends
  uses: this._d3Svg, this._d3InitialContainerWidth, this._d3InitialContainerHeight

extends._drawTooltip (app/javascript/controllers/time_series_chart_controller.js:274-282)
  method extends._drawTooltip
  called_by: _drawChart, extends
  uses: this._d3Tooltip, this.element.id

extends._drawXAxisLabels (app/javascript/controllers/time_series_chart_controller.js:190-220)
  method extends._drawXAxisLabels
  called_by: _drawChart, extends
  uses: this._d3Group, this._d3ContainerHeight, this._d3XScale, this._normalDataPoints

extends._getTrendIcon (app/javascript/controllers/time_series_chart_controller.js:401-416)
  method extends._getTrendIcon
  sig: extends._getTrendIcon(datum)
  behavior: PRECEDENCE(isIncrease -> isDecrease)
  called_by: _tooltipTemplate, extends
  uses: datum.trend.previous.amount, datum.trend.current.amount, www.w3.org, datum.trend.color

extends._installTrendlineSplit (app/javascript/controllers/time_series_chart_controller.js:133-169)
  method extends._installTrendlineSplit
  called_by: _drawTrendline, extends
  uses: this._d3Svg, this.element.id, this._d3XScale.range, this.dataValue.trend.color

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 42 symbols in L3, 4 with behavior annotations
drill: app/javascript/controllers/time_series_chart_controller.js (~4 lines, extends._setupResizeObserver)
drill: app/javascript/controllers/file_upload_controller.js (~15 lines, extends.formSubmitting)
drill: app/javascript/controllers/file_upload_controller.js (~14 lines, extends.fileSelected)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## extends._setupResizeObserver  (app/javascript/controllers/time_series_chart_controller.js L564-569)
```
  _setupResizeObserver() {
    this._resizeObserver = new ResizeObserver(() => {
      this._reinstall();
    });
    this._resizeObserver.observe(this.element);
  }
```

## extends.fileSelected  (app/javascript/controllers/file_upload_controller.js L34-54)
```
  fileSelected() {
    if (this.hasInputTarget && this.inputTarget.files.length > 0) {
      const fileName = this.inputTarget.files[0].name
      
      if (this.hasFileNameTarget) {
        // Find the paragraph element inside the fileName target
        const fileNameText = this.fileNameTarget.querySelector('p')
        if (fileNameText) {
          fileNameText.textContent = fileName
        }
        
        this.fileNameTarget.classList.remove("hidden")
      }
      
      if (this.hasUploadTextTarget) {
        this.uploadTextTarget.classList.add("hidden")
      }
      
    
    }
  }
```

## extends.formSubmitting  (app/javascript/controllers/file_upload_controller.js L56-73)
```
  formSubmitting() {
    if (this.hasFileNameTarget && this.hasInputTarget && this.inputTarget.files.length > 0) {
      const fileNameText = this.fileNameTarget.querySelector('p')
      if (fileNameText) {
        fileNameText.textContent = `Uploading ${this.inputTarget.files[0].name}...`
      }
      
      // Change the icon to a loader
      const iconContainer = this.fileNameTarget.querySelector('.lucide-file-text')
      if (iconContainer) {
        iconContainer.classList.add('animate-pulse')
      }
    }
    
    if (this.hasUploadAreaTarget) {
      this.uploadAreaTarget.classList.add("opacity-70")
    }
  }
```

## extends._createMainGroup  (app/javascript/controllers/time_series_chart_controller.js L449-453)
```
  _createMainGroup() {
    return this._d3Svg
      .append("g")
      .attr("transform", `translate(${this._margin.left},${this._margin.top})`);
  }
```

## extends._createMainSvg  (app/javascript/controllers/time_series_chart_controller.js L436-447)
```
  _createMainSvg() {
    return this._d3Container
      .append("svg")
      .attr("width", this._d3InitialContainerWidth)
      .attr("height", this._d3InitialContainerHeight)
      .attr("viewBox", [
        0,
        0,
        this._d3InitialContainerWidth,
        this._d3InitialContainerHeight,
      ]);
  }
```

## extends._d3Container  (app/javascript/controllers/time_series_chart_controller.js L488-490)
```
  get _d3Container() {
    return d3.select(this.element);
  }
```

## extends._d3ContainerHeight  (app/javascript/controllers/time_series_chart_controller.js L482-486)
```
  get _d3ContainerHeight() {
    return (
      this._d3InitialContainerHeight - this._margin.top - this._margin.bottom
    );
  }
```

## extends._d3ContainerWidth  (app/javascript/controllers/time_series_chart_controller.js L476-480)
```
  get _d3ContainerWidth() {
    return (
      this._d3InitialContainerWidth - this._margin.left - this._margin.right
    );
  }
```

## extends._d3Group  (app/javascript/controllers/time_series_chart_controller.js L462-467)
```
  get _d3Group() {
    if (!this._d3GroupMemo) {
      this._d3GroupMemo = this._createMainGroup();
    }
    return this._d3GroupMemo;
  }
```

## extends._d3Line  (app/javascript/controllers/time_series_chart_controller.js L496-501)
```
  get _d3Line() {
    return d3
      .line()
      .x((d) => this._d3XScale(d.date))
      .y((d) => this._d3YScale(this._getDatumValue(d)));
  }
```

## extends._d3Svg  (app/javascript/controllers/time_series_chart_controller.js L455-460)
```
  get _d3Svg() {
    if (!this._d3SvgMemo) {
      this._d3SvgMemo = this._createMainSvg();
    }
    return this._d3SvgMemo;
  }
```

## extends._d3XScale  (app/javascript/controllers/time_series_chart_controller.js L503-508)
```
  get _d3XScale() {
    return d3
      .scaleTime()
      .rangeRound([0, this._d3ContainerWidth])
      .domain(d3.extent(this._normalDataPoints, (d) => d.date));
  }
```

## extends._d3YScale  (app/javascript/controllers/time_series_chart_controller.js L510-562)
```
  get _d3YScale() {
    const dataMin = d3.min(this._normalDataPoints, this._getDatumValue);
    const dataMax = d3.max(this._normalDataPoints, this._getDatumValue);

    // Handle edge case where all values are the same
    if (dataMin === dataMax) {
      const padding = dataMax === 0 ? 100 : Math.abs(dataMax) * 0.5;
      return d3
        .scaleLinear()
        .rangeRound([this._d3ContainerHeight, 0])
        .domain([dataMin - padding, dataMax + padding]);
    }

    const dataRange = dataMax - dataMin;
    const avgValue = (dataMax + dataMin) / 2;

    // Calculate relative change as a percentage
    const relativeChange = avgValue !== 0 ? dataRange / Math.abs(avgValue) : 1;

    // Dynamic baseline calculation
    let yMin;
    let yMax;

    // For small relative changes (< 10%), use a tighter scale
    if (relativeChange < 0.1 && dataMin > 0) {
      // Start axis at a percentage below the minimum, not at 0
      const baselinePadding = dataRange * 2; // Show 2x the data range below min
      yMin = Math.max(0, dataMin - baselinePadding);
      yMax = dataMax + dataRange * 0.5; // Add 50% padding above
    } else {
      // For larger changes or when data crosses zero, use more context
      // Always include 0 when data is negative or close to 0
      if (dataMin < 0 || (dataMin >= 0 && dataMin < avgValue * 0.1)) {
        yMin = Math.min(0, dataMin * 1.1);
      } else {
        // Otherwise use dynamic baseline
        yMin = dataMin - dataRange * 0.3;
      }
      yMax = dataMax + dataRange * 0.1;
    }

    // Adjust padding for labels if needed
    if (this.useLabelsValue) {
      const extraPadding = (yMax - yMin) * 0.1;
      yMin -= extraPadding;
      yMax += extraPadding;
    }

    return d3
      .scaleLinear()
      .rangeRound([this._d3ContainerHeight, 0])
      .domain([yMin, yMax]);
  }
```

## extends._draw  (app/javascript/controllers/time_series_chart_controller.js L68-74)
```
  _draw() {
    if (this._normalDataPoints.length < 2) {
      this._drawEmpty();
    } else {
      this._drawChart();
    }
  }
```

## extends._drawCenteredCircleEmptyState  (app/javascript/controllers/time_series_chart_controller.js L95-103)
```
  _drawCenteredCircleEmptyState() {
    this._d3Svg
      .append("circle")
      .attr("cx", this._d3InitialContainerWidth / 2)
      .attr("cy", this._d3InitialContainerHeight / 2)
      .attr("r", 4)
      .attr("class", "fg-subdued")
      .style("fill", "currentColor");
  }
```

## extends._drawChart  (app/javascript/controllers/time_series_chart_controller.js L105-117)
```
  _drawChart() {
    this._drawTrendline();

    if (this.useLabelsValue) {
      this._drawXAxisLabels();
      this._drawGradientBelowTrendline();
    }

    if (this.useTooltipValue) {
      this._drawTooltip();
      this._trackMouseForShowingTooltip();
    }
  }
```

## extends._drawDashedLineEmptyState  (app/javascript/controllers/time_series_chart_controller.js L84-93)
```
  _drawDashedLineEmptyState() {
    this._d3Svg
      .append("line")
      .attr("x1", this._d3InitialContainerWidth / 2)
      .attr("y1", 0)
      .attr("x2", this._d3InitialContainerWidth / 2)
      .attr("y2", this._d3InitialContainerHeight)
      .attr("stroke", "var(--color-gray-300)")
      .attr("stroke-dasharray", "4, 4");
  }
```

## extends._drawEmpty  (app/javascript/controllers/time_series_chart_controller.js L76-82)
```
  _drawEmpty() {
    this._d3Svg.selectAll(".tick").remove();
    this._d3Svg.selectAll(".domain").remove();

    this._drawDashedLineEmptyState();
    this._drawCenteredCircleEmptyState();
  }
```

## extends._drawGradientBelowTrendline  (app/javascript/controllers/time_series_chart_controller.js L222-272)
```
  _drawGradientBelowTrendline() {
    // Define gradient
    const gradient = this._d3Group
      .append("defs")
      .append("linearGradient")
      .attr("id", `${this.element.id}-trendline-gradient`)
      .attr("gradientUnits", "userSpaceOnUse")
      .attr("x1", 0)
      .attr("x2", 0)
      .attr(
        "y1",
        this._d3YScale(d3.max(this._normalDataPoints, this._getDatumValue)),
      )
      .attr("y2", this._d3ContainerHeight);

    gradient
      .append("stop")
      .attr("offset", 0)
      .attr("stop-color", this._trendColor)
      .attr("stop-opacity", 0.06);

    gradient
      .append("stop")
      .attr("offset", 0.5)
      .attr("stop-color", this._trendColor)
      .attr("stop-opacity", 0);

    // Clip path makes gradient start at the trendline
    this._d3Group
      .append("clipPath")
      .attr("id", `${this.element.id}-clip-below-trendline`)
      .append("path")
      .datum(this._normalDataPoints)
      .attr(
        "d",
        d3
          .area()
          .x((d) => this._d3XScale(d.date))
          .y0(this._d3ContainerHeight)
          .y1((d) => this._d3YScale(this._getDatumValue(d))),
      );

    // Apply the gradient + clip path
    this._d3Group
      .append("rect")
      .attr("id", `${this.element.id}-trendline-gradient-rect`)
      .attr("width", this._d3ContainerWidth)
      .attr("height", this._d3ContainerHeight)
      .attr("clip-path", `url(#${this.element.id}-clip-below-trendline)`)
      .style("fill", `url(#${this.element.id}-trendline-gradient)`);
  }
```

## extends._drawTooltip  (app/javascript/controllers/time_series_chart_controller.js L274-282)
```
  _drawTooltip() {
    this._d3Tooltip = d3
      .select(`#${this.element.id}`)
      .append("div")
      .attr(
        "class",
        "bg-container text-sm font-sans absolute p-2 border border-secondary rounded-lg pointer-events-none opacity-0",
      );
  }
```

## extends._drawTrendline  (app/javascript/controllers/time_series_chart_controller.js L119-131)
```
  _drawTrendline() {
    this._installTrendlineSplit();

    this._d3Group
      .append("path")
      .datum(this._normalDataPoints)
      .attr("fill", "none")
      .attr("stroke", `url(#${this.element.id}-split-gradient)`)
      .attr("d", this._d3Line)
      .attr("stroke-linejoin", "round")
      .attr("stroke-linecap", "round")
      .attr("stroke-width", this.strokeWidthValue);
  }
```

## extends._drawXAxisLabels  (app/javascript/controllers/time_series_chart_controller.js L190-220)
```
  _drawXAxisLabels() {
    // Add ticks
    this._d3Group
      .append("g")
      .attr("transform", `translate(0,${this._d3ContainerHeight})`)
      .call(
        d3
          .axisBottom(this._d3XScale)
          .tickValues([
            this._normalDataPoints[0].date,
            this._normalDataPoints[this._normalDataPoints.length - 1].date,
          ])
          .tickSize(0)
          .tickFormat(d3.timeFormat("%b %d, %Y")),
      )
      .select(".domain")
      .remove();

    // Style ticks
    this._d3Group
      .selectAll(".tick text")
      .attr("class", "fg-gray")
      .style("font-size", "12px")
      .style("font-weight", "500")
      .attr("text-anchor", "middle")
... (truncated)
```
--- END SOURCE SNIPPETS ---

QUESTION: What files and setup artifacts are documented for getting a self-hosted Maybe deployment running with Docker?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
