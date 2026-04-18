# Enterprise v4 (full-stack): ent-saleor-struct-1
Date: 2026-04-18

## Answer
Saleor is split first around a headless core platform: the prompt frames it as an API-only GraphQL service with `/graphql/` as the main public surface, and the README calls it “GraphQL native, API-only,” “GraphQL only,” and “Headless and API only.” [Prompt ARCH/API context; `README.md` 16, 79-81]

That backend is intentionally separate from presentation/admin surfaces. The README explicitly says the Dashboard is a decoupled project in the separate `saleor-dashboard` repository, and it versions Saleor, Dashboard, and Storefront as separate components. That matches the prompt’s description of a backend extended through APIs/webhooks rather than an in-process storefront. [`README.md` 113, 136-140; Prompt ARCH 19-22]

Its commerce model is native multichannel. The README says channels control pricing, currencies, stock, product, and more, while the domain context shows channel-specific state in `ProductChannelListing`, `ProductVariantChannelListing`, shipping-zone/channel links, and warehouse/channel relationships. [`README.md` 87; Prompt DOMAIN MODEL 32, 42]

Its extension surface is API-first and broader than just plugins. The README explicitly lists webhooks, apps, subscription queries, API extensions, and dashboard iframes; the prompt clue then anchors those surfaces in concrete symbols such as `AppExtension`, `AppManifestExtension`, `trigger_webhooks_async`, `_get_webhooks_for_channel_events`, and plugin webhook routes. [`README.md` 91, 125; Prompt clue: `AppExtension` `saleor/graphql/app/types.py`, `trigger_webhooks_async` `saleor/plugins/webhook/plugin.py`, plugin webhook routes in `saleor/urls.py`]

## Synthesis
So the split is: (1) a GraphQL-first backend monolith, (2) a channel-shaped commerce data model, and (3) external extension surfaces for apps/webhooks/subscription-driven integrations and dashboard iframe integrations.

