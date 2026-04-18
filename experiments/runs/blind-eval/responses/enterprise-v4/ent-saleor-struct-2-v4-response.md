# Enterprise v4 (full-stack): ent-saleor-struct-2
Date: 2026-04-18

## Answer
Saleor’s repository follows a standard Django app layout. The contributing guide says each app has its own directory containing migrations, management, models, utils, error codes, and tests, and the prompt’s `saleor/account/...` index shows that pattern concretely via `management/commands`, `migrations`, `error_codes.py`, and other app-local files. [`CONTRIBUTING.md` 144-153; Prompt INDEX `saleor/account/...`]

The GraphQL API lives under `saleor/graphql/`. Both the prompt and contributing guide place the API there, and the prompt shows domain files such as `saleor/graphql/app/schema.py`, `saleor/graphql/app/types.py`, `saleor/graphql/page/filters.py`, `saleor/graphql/app/dataloaders/app.py`, and domain mutation modules. [Prompt ARCH/API context 22, 45-51; `CONTRIBUTING.md` 155-167]

Saleor also documents a standard per-module GraphQL file pattern: `schema.py`, `sorters.py`, `filters.py`, `types.py`, `enums.py`, `dataloaders.py`, a mutations file or directory, and a tests directory. The guide further says each module should prefer a `mutations/` directory with one file per mutation, with checkout shown as the example. [`CONTRIBUTING.md` 155-180]

Tests are organized alongside those GraphQL modules. Saleor says tests live in a module-local `tests` directory, split into `queries` and `mutations`, with one file per query or mutation. The prompt’s test harness (`conftest.py`, `saleor/tests/settings.py`) supplies the repo-wide test environment around that convention. [`CONTRIBUTING.md` 182-203; Prompt FOCUS `saleor/tests/settings.py`, root `conftest.py`]

## Synthesis
So the organization is: Django domain apps at `saleor/<app>/...`, GraphQL modules at `saleor/graphql/<domain>/...`, and GraphQL tests nested per module under `tests/queries` and `tests/mutations`.

