# Enterprise Eval: ent-maybe-struct-2
Date: 2026-04-17

## Question
What files and setup artifacts are documented for getting a self-hosted Maybe deployment running with Docker?

---

## Reasoning Trace

### 1. Relevant Symbols from FOCUS, SYM, and INDEX

The clue file header states `=CC v2.1 maybe@HEAD 91mod 267sym`, covering 91 modules and 267 symbols. The TREE section reveals the entire documented codebase consists of:
- `app/` (50 files) → `javascript/`
- `vendor/` (41 files) → `javascript/`

Every module in the INDEX is a `.js` file under `app/javascript/controllers/`, `app/components/DS/`, `app/javascript/services/`, or `vendor/javascript/`. No other file types or directories are documented.

### 2. Searching for Docker/Deployment Evidence

Scanning all documented symbols and modules for any reference to Docker, deployment, or self-hosting:

- **INDEX**: Lists controllers such as `dialog_controller.js`, `menu_controller.js`, `chat_controller.js`, `time_series_chart_controller.js`, `file_upload_controller.js`, etc. — all are client-side UI controllers (INDEX lines 25–43+).
- **SYM**: 267 symbols, all are JavaScript methods on classes extending Controller (e.g., `extends.setTheme`, `extends.submitSampleQuestion`, `CurrenciesService.get`). No symbols reference Docker, containers, environment variables, database connections, or deployment configuration (SYM lines 46–111+).
- **FOCUS**: Detailed analysis of `time_series_chart_controller.js` (D3 charting) and `file_upload_controller.js` (file upload UI). Neither relates to deployment (FOCUS lines 114–200).
- **Source snippets**: Include `_setupResizeObserver`, `fileSelected`, `formSubmitting`, D3 chart rendering methods, and `turbo_frame_timeout_controller.js`. All are frontend UI logic (SOURCE SNIPPETS lines 282–665).

### 3. What GAPS Says Cannot Be Determined

The GAPS section states:
- **type: MECHANISTIC** — body logic needed for full answer (GAPS line 273).
- **coverage: 42 symbols in L3, 4 with behavior annotations** (GAPS line 274).
- Drill targets are in `time_series_chart_controller.js` and `file_upload_controller.js` (GAPS lines 275–277).

The GAPS section does **not** mention any uncovered Docker, deployment, or infrastructure files — because these files are entirely outside the scope of what this clue file documents.

### 4. Synthesis

**Supported conclusion:**
The clue file documents **zero files or setup artifacts** related to self-hosted Docker deployment. The entire documented codebase consists exclusively of client-side JavaScript: controllers for UI interactions (chat, charts, theming, forms, tooltips, etc.), a currency service, and Design System components (TREE; INDEX lines 25–43+).

**What cannot be determined from the evidence:**
- Whether Maybe has a Dockerfile, docker-compose.yml, .env.example, or any Docker-related configuration — **none of these file types appear anywhere** in the TREE, INDEX, SYM, or FOCUS sections.
- Database connection setup, migration scripts, or environment variable configuration for self-hosting.
- Any server-side application code (e.g., Rails controllers, models, routes).
- README instructions, deployment guides, or infrastructure-as-code files.

**The fundamental limitation is that this clue file's scope (91 JavaScript modules) does not include the backend, DevOps, or infrastructure layers where Docker deployment artifacts would reside.** The question cannot be answered from this evidence.
