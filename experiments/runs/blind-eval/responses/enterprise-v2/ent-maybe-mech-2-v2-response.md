# Enterprise v2: ent-maybe-mech-2
Date: 2026-04-17

## Question
How does the documented self-hosting update path work, and what is the recovery flow for a first-time database connection problem?

## Answer

### 1. Relevant Symbols and Evidence

The clue and source snippets contain the following entries most relevant to self-hosting updates and database connection recovery:

- **.env.example:** Config summary with `SELF_HOSTED=true`, `SECRET_KEY_BASE=secret-value`, `SYNTH_API_KEY=<set>`, `PORT=3000`, `SMTP_ADDRESS=<set>`, `SMTP_PORT=465` (FOCUS, .env.example:1-86).
- **README.md:** Sections: "Maybe: The personal finance app for everyone", "Maybe Hosting", "Forking and Attribution", "Local Development Setup", "Requirements" (FOCUS, README.md:1-64).
- **turbo_frame_timeout_controller.js:** A controller that provides timeout-based error handling for Turbo frame loads (FOCUS, `extends.clearTimeout` at `app/javascript/controllers/turbo_frame_timeout_controller.js:20-25`; FOCUS, `extends.handleTimeout` at `app/javascript/controllers/turbo_frame_timeout_controller.js:27-41`; SOURCE SNIPPET, `turbo_frame_timeout_controller.js` L2-42).
- **Various UI controllers:** Category, bulk select, rules, tooltip, and menu controllers with update/connect/disconnect lifecycles (FOCUS and SOURCE SNIPPETS).

### 2. Self-Hosting Update Path

#### What Is Documented

The clue explicitly confirms a self-hosting mode via the `SELF_HOSTED=true` entry in `.env.example` (FOCUS, .env.example:1-86). The README.md documents a "Maybe Hosting" section and a "Local Development Setup" section (FOCUS, README.md:1-64), which likely contain hosting and update instructions.

However, the clue **does not document a self-hosting update path**. Specifically:
- No update script, migration command, or version-check mechanism appears in the TREE, INDEX, SYM, or FOCUS sections.
- No Dockerfile, docker-compose.yml, or container orchestration configuration is documented in the clue's TREE (which shows only `app/`, `vendor/`, `.env.example`, `README.md`, `package.json`).
- The README.md content is summarized only by section headings — the actual update instructions, if they exist in "Maybe Hosting" or "Local Development Setup", are not visible.
- No symbols related to database migrations, schema updates, or version management appear in the INDEX or SYM.

The `.env.example` documents configuration for a self-hosted deployment (FOCUS, `.env.example:1-86`), but the clue does not expose any concrete update steps. Even the full 86-line file is summarized only by a few entries, so additional update-related settings cannot be confirmed from this artifact alone.

### 3. Recovery Flow for Database Connection Problems

#### What Is Documented

The clue documents **no database-specific recovery flow**. There are no symbols, modules, or FOCUS entries referencing database connections, connection pools, health checks, retry logic, or migration runners.

The closest documented recovery mechanism is the **Turbo Frame Timeout Controller** (SOURCE SNIPPET, extends at turbo_frame_timeout_controller.js L2-42):

```javascript
export default class extends Controller {
  static values = { timeout: { type: Number, default: 10000 } }

  connect() {
    this.timeoutId = setTimeout(() => {
      this.handleTimeout()
    }, this.timeoutValue)
    this.element.addEventListener("turbo:frame-load", this.clearTimeout.bind(this))
  }

  disconnect() { this.clearTimeout() }

  clearTimeout() {
    if (this.timeoutId) {
      clearTimeout(this.timeoutId)
      this.timeoutId = null
    }
  }

  handleTimeout() {
    this.element.innerHTML = `
      <div class="flex items-center justify-end gap-1">
        ...
        <p class="font-mono text-right text-xs text-warning">Timeout</p>
      </div>
    `
  }
}
```

This controller's lifecycle is:
1. **connect:** Sets a timeout (default 10,000ms) and listens for `turbo:frame-load` events (SOURCE SNIPPET, extends.connect at turbo_frame_timeout_controller.js L7-14).
2. **Success path:** If the Turbo frame loads before the timeout, the `turbo:frame-load` event fires, calling `clearTimeout()` to cancel the timer (FOCUS, extends.clearTimeout at turbo_frame_timeout_controller.js:20-25; SOURCE SNIPPET).
3. **Failure path:** If the timeout expires, `handleTimeout()` replaces the element's HTML with a warning icon and "Timeout" text (FOCUS, extends.handleTimeout at turbo_frame_timeout_controller.js:27-41; SOURCE SNIPPET).
4. **disconnect:** Clears any pending timeout on controller teardown (SOURCE SNIPPET, extends.disconnect at turbo_frame_timeout_controller.js L16-18).

This is a **client-side UI recovery mechanism** — it handles the user experience when a server-rendered frame fails to load in time, which could occur if the database is unreachable and the server cannot generate a response. However, it is a generic timeout handler, not specifically tied to database connection problems.

### 4. Other Update/Change Patterns in the Codebase

The source snippets document several UI-level update mechanisms that show the application's general approach to state changes, though none are related to self-hosting updates or database recovery:

- **Rules controller — updateConditionPrefixes:** Iterates visible conditions and toggles prefix element visibility based on position (SOURCE SNIPPET, extends.updateConditionPrefixes at rules_controller.js L58-77). Uses `ACCUMULATE` behavior pattern (FOCUS, extends.updateConditionPrefixes — `behavior: ACCUMULATE(...)`).

- **Category controller — updateSelectedIconColor:** Updates icon wrapper background and text color (SOURCE SNIPPET, extends.updateSelectedIconColor at category_controller.js L118-124). Called by `handleColorChange`, `handleIconColorChange`, `initPicker` (FOCUS, extends.updateSelectedIconColor at category_controller.js:118-124).

- **Category controller — darkenColor:** Iteratively darkens a color until WCAG AA contrast ratio (4.5:1) is met (SOURCE SNIPPET, extends.darkenColor at category_controller.js L190-209). Uses `luminance` and `contrast` helper methods (SOURCE SNIPPET, extends.luminance at category_controller.js L173-181; extends.contrast at category_controller.js L183-188).

- **Bulk select controller — _updateGroups and _updateRows:** Uses `ACCUMULATE` loop patterns to iterate over groups and rows for selection state management (FOCUS, extends._updateGroups at bulk_select_controller.js:148-158; extends._updateRows at bulk_select_controller.js:160-164).

- **Theme controller — updateTheme:** Handles theme switching based on user preference, calling `setTheme` and `systemPrefersDark` (FOCUS, extends.updateTheme at theme_controller.js:20-29).

These demonstrate repeated front-end controller patterns with connect/disconnect lifecycles, DOM mutation, and event-driven updates, but they are all UI patterns rather than deployment or infrastructure patterns.

### 5. Gaps and Uncertainties

- **GAPS states:** "type: MECHANISTIC (body logic needed for full answer), coverage: 80 symbols in L3, 12 with behavior annotations" (GAPS).
- **Uncovered symbols:** `extends`, `extends._drawEmpty`, `extends._d3Line`, `extends._draw` (GAPS uncovered).
- **Drill targets:** `category_controller.js` (~6 lines, `updateSelectedIconColor`), `rules_controller.js` (~18 lines, `updateConditionPrefixes`) (GAPS drill). Both were provided and analyzed above.
- **Self-hosting update path:** Not documented in the clue. The README.md "Maybe Hosting" and "Local Development Setup" sections may contain this information, but their content is not available — only section headings are summarized.
- **Database connection recovery:** Not documented. No database configuration variables (connection string, host, port, database name) are visible in the 6 summarized `.env.example` entries (though they may exist in the remaining ~80 lines).
- **Server-side code:** Entirely absent from the clue. The clue covers only 91 JavaScript front-end modules. Backend infrastructure (database adapters, migration runners, health check endpoints, deployment scripts) is not represented.
- **Docker/container configuration:** Not documented in the clue's TREE or INDEX.

### 6. Conclusion

The clue confirms that Maybe supports self-hosting via the `SELF_HOSTED=true` flag in `.env.example` (FOCUS, .env.example:1-86) and documents hosting-related README sections (FOCUS, README.md:1-64). However, the **specific self-hosting update path** and **database connection recovery flow** are not documented in this clue artifact. The only documented recovery-adjacent mechanism is the `turbo_frame_timeout_controller.js` (SOURCE SNIPPET, extends at turbo_frame_timeout_controller.js L2-42), which provides a 10-second client-side timeout with a visual "Timeout" error state — a generic UI fallback that could surface during database connection failures but is not specific to them. A complete answer to this question would require access to server-side code, deployment scripts, and the full README content, none of which are in the clue.
