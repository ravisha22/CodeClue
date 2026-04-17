# Enterprise v2: ent-mattermost-struct-1
Date: 2026-04-17

## Reasoning Scaffold

### 1. Relevant Clue Entries

The question asks about Mattermost's core runtime and deployment profile as described in the top-level README.

**README** (README.md:1-97): States that Mattermost is "an open core, self-hosted collaboration platform that offers chat, workflow a…" and provides links to "Deploy Mattermost on-premises" as well as "try i…" (likely a cloud trial). The FOCUS entry for README.md confirms sections include "Install Mattermost", "Native mobile and desktop apps", "Get security bulletins", and "Get involved".

**TREE**: The repository root contains `server/` (1309 files), `webapp/` (1 file), `api/` (2 files), `e2e-tests/` (1 file), and `tools/` (37 files). Under `server/` we see `build/`, `config/`, `einterfaces/`, `enterprise/`, `fips/`.

**INDEX**: The largest modules are Go files — `server/public/model/client4.go` (8269L), `server/channels/store/retrylayer/retrylayer.go` (18248L), `server/channels/app/user.go` (3208L) — confirming Go as the server language.

**FOCUS – docker-compose.yml** (server/build/docker-compose.yml:1-73): Lists infrastructure services: `postgres`, `minio`, `inbucket`, `openldap`, `elasticsearch`, `opensearch` — all extending from `docker-compose.common.yml`.

**SYM**: `SqlStore.GetMaster` (server/channels/store/sqlstore/store.go:428), `SqlStore.GetReplica` (server/channels/store/sqlstore/store.go:462) confirm a SQL-backed persistence layer with master/replica topology. `LRU.Remove` (server/platform/services/cache/lru.go:88) confirms an in-memory LRU caching layer.

### 2. Tracing Through the Clue

- **Language/Runtime**: All server source files reside under `server/` and are `.go` files. Symbols use Go conventions (capitalized exported names, `func` signatures, `*model.User` pointer types). The tools directory includes `mattermost-govet/` (TREE), a Go vet tool. This collectively establishes **Go** as the core runtime.

- **Deployment model**: The README explicitly describes Mattermost as "self-hosted" and offers "Deploy Mattermost on-premises" (README, FOCUS README.md). The docker-compose.yml (FOCUS server/build/docker-compose.yml) provides a container-based local deployment stack with Postgres, MinIO (object storage), Inbucket (email testing), OpenLDAP (directory services), and Elasticsearch/OpenSearch (search).

- **Data tier**: `SqlStore.GetMaster` and `SqlStore.GetReplica` (server/channels/store/sqlstore/store.go:428, 462) show a master-replica SQL architecture. The docker-compose services list `postgres` as the database (FOCUS server/build/docker-compose.yml).

- **Webapp**: The `webapp/` directory (TREE) holds 1 file, indicating the web frontend is tracked here but likely built separately. The `e2e-tests/cypress/package.json` (FOCUS) lists `@mattermost/client` as a dependency, confirming a JavaScript/TypeScript web client exists.

- **Enterprise/FIPS**: The `server/enterprise/` and `server/fips/` directories (TREE) indicate enterprise and FIPS-compliance modules are part of the codebase. `SqlStore.hasLicense` (server/channels/store/sqlstore/store.go:966) confirms license-gated functionality.

### 3. GAPS — What Cannot Be Determined

The GAPS section states:
- **Type**: STRUCTURAL (answerable from L0-L2)
- **Coverage**: 83 symbols in L3, 25 with behavior annotations
- **Uncovered**: `PlatformService.getGoroutineProfile`, `PlatformService.getHeapProfile`, `PluginAPI.LogAuditRecWithLevel`, `ProfileImageBytes`

From the clue alone, we **cannot determine**:
- The specific Go version required
- Exact supported OS/architecture targets for deployment
- Whether the "try i…" link refers to a managed cloud offering or a demo
- Full details of the FIPS compliance scope
- Runtime configuration specifics (e.g., how many replicas, clustering mode)

### 4. Synthesis

**Core runtime**: Mattermost's server is a **Go application** (`server/` directory with Go source files, `mattermost-govet/` tooling in TREE, Go-style symbol signatures throughout SYM and INDEX).

**Deployment profile**: The README describes Mattermost as a **"self-hosted collaboration platform"** with an explicit **"Deploy Mattermost on-premises"** option (README.md, FOCUS README.md). The development/deployment infrastructure uses **Docker Compose** (FOCUS server/build/docker-compose.yml) orchestrating:
- **PostgreSQL** as the primary relational database, backed by a master/replica `SqlStore` architecture (`SqlStore.GetMaster` at store.go:428, `SqlStore.GetReplica` at store.go:462)
- **MinIO** for S3-compatible object storage
- **Inbucket** for email/SMTP testing
- **OpenLDAP** for directory/authentication integration
- **Elasticsearch / OpenSearch** for full-text search

The platform additionally supports **enterprise and FIPS-compliant** deployment configurations (`server/enterprise/`, `server/fips/` in TREE), gated by a license system (`SqlStore.hasLicense` at store.go:966).

A **web application** frontend exists (`webapp/` in TREE) with a JavaScript/TypeScript client (`@mattermost/client` in e2e-tests/cypress/package.json), and the README notes **"Native mobile and desktop apps"** are available.

In summary: Mattermost is a Go-based, self-hosted, on-premises collaboration server with a Postgres-backed SQL store, Docker Compose deployment tooling, and optional enterprise/FIPS modules.
