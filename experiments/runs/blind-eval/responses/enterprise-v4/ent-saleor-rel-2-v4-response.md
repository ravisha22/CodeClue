# Enterprise v4 (full-stack): ent-saleor-rel-2
Date: 2026-04-18

## Answer
Saleor treats several external-facing surfaces as breaking-change contracts. The contributing guide’s breaking-change list explicitly includes deleting or renaming a GraphQL schema field, deleting or renaming a webhook payload field, and changing plugin-function signatures in `PluginsManager` (for existing plugins). [`CONTRIBUTING.md` 657-663]

The prompt’s full-stack context shows why those three surfaces are linked. GraphQL is the main public API surface; webhook payloads are generated from subscription payload machinery and processed by webhook transport; and plugin/webhook behavior flows through `WebhookPlugin` plus plugin-manager dispatch such as `__run_method_on_plugins`, `get_plugins`, and `_load_plugin`. [Prompt ARCH/API context 22, 45-54; Prompt clue `generate_pre_save_payloads`, `process_webhook_payloads`, `WebhookPlugin`, `__run_method_on_plugins`, `get_plugins`, `_load_plugin`]

Saleor’s removal policy is deprecate-first. The API guidance says fields should first be marked `DEPRECATED` (or use `deprecation_reason`; mutation inputs use `DEPRECATED_IN_X_INPUT` in descriptions). The prompt clue directly exposes `deprecation_reason(enum)` for webhook GraphQL enums, which matches that repo-wide rule. [`CONTRIBUTING.md` 420-428; Prompt clue `deprecation_reason` in `saleor/graphql/webhook/enums.py`]

`PREVIEW_FEATURE` is the exception with a shorter runway, not a free pass. Saleor says preview-feature API fields still go through deprecation, but deprecated preview fields may be removed in the next minor release, and those changes must be recorded in the changelog’s “Breaking changes” section. [`CONTRIBUTING.md` 422-444, 650-663]

## Synthesis
GraphQL fields, webhook payload fields, and `PluginsManager` signatures are all treated as compatibility surfaces; deprecate before removal, and document breaking/preview-feature removals in the changelog.

