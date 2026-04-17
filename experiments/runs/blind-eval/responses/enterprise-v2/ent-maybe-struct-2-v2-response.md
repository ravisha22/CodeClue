# Enterprise v2: ent-maybe-struct-2
Date: 2026-04-17

## Question
What files and setup artifacts are documented for getting a self-hosted Maybe deployment running with Docker?

## Answer

### 1. Documented Files and Artifacts

Based solely on the clue file, the following files and setup artifacts are documented that relate to self-hosted deployment:

#### .env.example (.env.example:1-86)
The primary configuration artifact for self-hosting is `.env.example`, located at the repository root (TREE; FOCUS, .env.example:1-86). It contains environment variable entries that configure a self-hosted deployment:

- `SELF_HOSTED=true` — a flag explicitly enabling self-hosted mode (FOCUS, .env.example Config summary).
- `SECRET_KEY_BASE=secret-value` — a secret key placeholder that must be set for the application (FOCUS, .env.example Config summary).
- `SYNTH_API_KEY=<set>` — an API key for an external service called "Synth", marked as needing user configuration (FOCUS, .env.example Config summary).
- `PORT=3000` — the application port (FOCUS, .env.example Config summary).
- `SMTP_ADDRESS=<set>` — SMTP server address for email, requiring user configuration (FOCUS, .env.example Config summary).
- `SMTP_PORT=465` — SMTP port, defaulting to 465 (SSL) (FOCUS, .env.example Config summary).

The `.env.example` file is 86 lines long, suggesting additional configuration entries beyond the six summarized in the clue.

#### README.md (README.md:1-64)
The `README.md` (64 lines) documents key sections relevant to self-hosted deployment (FOCUS, README.md:1-64):

- **"Maybe Hosting"** — a section presumably covering hosting options, which may include self-hosting with Docker (FOCUS, README.md sections).
- **"Local Development Setup"** — setup guidance for running the application locally (FOCUS, README.md sections).
- **"Requirements"** — prerequisites for running Maybe (FOCUS, README.md sections).
- **"Forking and Attribution"** — guidance for those forking the repository (FOCUS, README.md sections).

The README also contains an `[!IMPORTANT]` callout, indicating critical setup information (FOCUS, README.md documentation summary).

#### package.json (package.json)
Present at the repository root (TREE), though its contents are not expanded in the FOCUS for this clue instance.

### 2. Repository Structure

The TREE shows the repository contains:
- `app/` — 50 files, with JavaScript controllers and components (TREE).
- `vendor/` — 41 files of vendored JavaScript (TREE).
- Root files: `.env.example`, `README.md`, `package.json` (TREE).

### 3. What the Clue Reveals About Docker

The clue **does not explicitly mention Docker, Dockerfile, docker-compose.yml, or any container-related configuration files** in the TREE, INDEX, SYM, or FOCUS sections. The TREE listing shows only `app/`, `vendor/`, `.env.example`, `README.md`, and `package.json` at the top level. However, this TREE is a compressed representation showing only a subset of files (the clue header says "91mod 270sym"), so Docker-related files may exist in the repository but are not captured in this clue artifact.

The README.md section titled "Maybe Hosting" may contain Docker instructions, but the clue only provides a summary of section headings, not the full text (FOCUS, README.md:1-64).

### 4. Time Series Chart Controller (Supplementary FOCUS)

The clue's FOCUS section also documents `time_series_chart_controller.js` in detail (FOCUS, extends at time_series_chart_controller.js:5-570), including its full call chain from `connect` → `_install` → `_draw` → `_drawChart`/`_drawEmpty`, with D3-based rendering methods. This is not directly relevant to Docker deployment but shows the application is a data-visualization-heavy finance app. The `_d3YScale` method has a `behavior: GUARD(dataMin === dataMax -> ...)` annotation and `PRECEDENCE(dataMin -> relativeChange -> useLabelsValue -> default)` (FOCUS, extends._d3YScale at time_series_chart_controller.js:510-562), confirming non-trivial front-end logic.

### 5. Gaps and Uncertainties

- **GAPS states:** "type: STRUCTURAL (answerable from L0-L2), coverage: 44 symbols in L3, 4 with behavior annotations" (GAPS). This means 44 symbols have body-level detail but the clue does not fully cover all of them.
- **Docker-specific files** (Dockerfile, docker-compose.yml, etc.) are **not documented** in this clue. The clue cannot confirm whether they exist in the repository.
- The **full text of README.md** is not available — only section headings and a brief summary are provided. Docker setup steps, if documented, would be in the "Maybe Hosting" or "Local Development Setup" sections, but their content is not visible.
- The `.env.example` file has 86 lines but only 6 entries are summarized; additional environment variables relevant to Docker (e.g., database connection strings, Redis URLs) may exist but are not shown.
