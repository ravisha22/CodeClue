# Enterprise v4 (full-stack): ent-netbox-rel-2
Date: 2026-04-18

## Answer
The prompt’s auth/permissions context and clue material show a layered model. Object-based permissions can be scoped to object types, users or groups, allowed actions, and optional JSON constraints, so access is both role-like and data-filtered. On top of explicit permission rows, default permissions are automatically granted to any authenticated user, and `EXEMPT_VIEW_PERMISSIONS` can open selected models for read access to everyone, including anonymous users. The UI and APIs then sit on the same identity model: the REST and GraphQL surfaces use token-based authentication that maps back to user accounts and their assigned permissions, while LDAP and SSO are also supported as upstream identity providers.

## Synthesis
The key relationship is that authentication decides who the caller is, while NetBox’s object-permission layer decides which objects and actions that caller can actually reach across UI, REST, and GraphQL.
