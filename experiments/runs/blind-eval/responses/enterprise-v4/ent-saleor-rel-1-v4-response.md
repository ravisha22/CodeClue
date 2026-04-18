# Enterprise v4 (full-stack): ent-saleor-rel-1
Date: 2026-04-18

## Answer
Saleor attaches permission checks to GraphQL queries primarily through decorators. The contributing guide says queries should use `permission_required` or `one_of_permissions_required`, and the prompt clue includes the concrete `permission_required` decorator plus the broader permission combinators in `permission/utils.py` (`one_of_permissions_or_auth_filter_required`, `has_one_of_permissions`). [`CONTRIBUTING.md` 429-432; Prompt clue `permission_required` in `saleor/graphql/decorators.py`, permission utils at Prompt 59]

Mutations attach permissions differently: Saleor documents that mutation permissions are declared in `Meta.permissions`. The prompt then shows the runtime side of that design, with mutation flows such as `_requestor_has_permission`, `PermissionGroupCreate`, and `PermissionGroupDelete` calling `check_permissions(...)` during `perform_mutation`. [`CONTRIBUTING.md` 433; Prompt clue `_requestor_has_permission` `saleor/graphql/notifications/mutations/external_notification_trigger.py`, `PermissionGroupCreate`, `PermissionGroupDelete`]

`AuthorizationFilters` is the bridge for non-codename checks. Saleor defines it as the enum used when permission decisions are function-based rather than named admin permission scopes; that matches the prompt’s repeated imports of `permission.auth_filters` in GraphQL query modules. [`CONTRIBUTING.md` 434; Prompt clue `AccountQueries` and `AppQueries` imports of `permission.auth_filters`]

Saleor also couples error reporting and schema docs to the same permission contract. The guide says a raised `PermissionDenied` should state which permissions are required, and those required permissions should also be named in the GraphQL description. The prompt clue shows `PermissionDenied` being raised by permission helpers and guarded GraphQL paths, while `core.descriptions` is part of the GraphQL description system. [`CONTRIBUTING.md` 420-439; Prompt clue `_user_has_perm`, `permission_required`, `has_required_permission`, and `DiscountQueries` import of `core.descriptions`]

## Synthesis
Queries use decorators, mutations declare `Meta.permissions`, `AuthorizationFilters` covers function-based checks, and both runtime errors and schema descriptions are expected to surface the required permissions.

