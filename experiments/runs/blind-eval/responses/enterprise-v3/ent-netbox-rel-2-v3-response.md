# Enterprise v3 (arch-enhanced): ent-netbox-rel-2
Date: 2026-04-18

## Answer
NetBox splits authentication by surface: the architectural summary says the web UI uses session auth, while the API uses token auth (ARCH, ent-netbox-rel-2-v3.prompt.md:23). The clue matches that with API-token UI routes under `account/urls.py`, a REST API root under `/api/`, and a custom `TokenAuthentication` class that enforces token expiration and source-IP restrictions (path:api-tokens/, netbox/account/urls.py:1-22; path:api/, netbox/netbox/urls.py:1-97; TokenAuthentication, netbox/netbox/api/authentication.py:19-122).

Permissions are layered on top of that auth model. `TokenPermissions` extends DRF’s object permissions to validate a token’s write ability, and API mixins/views can request `TokenWritePermission` for specific write-style actions such as `render_config` and `render` (TokenPermissions, netbox/netbox/api/authentication.py:125-169; get_permissions, netbox/extras/api/mixins.py:70-74; get_permissions, netbox/extras/api/views.py:243-247).

For permission aggregation, `get_all_permissions(user_obj, obj)` immediately returns no permissions for inactive or anonymous users, otherwise it calls `get_object_permissions(user_obj)`; and `get_object_permissions()` accumulates from `settings.DEFAULT_PERM...` while processing object-permission data (get_all_permissions, netbox/netbox/authentication/__init__.py:73-78; get_object_permissions, netbox/netbox/authentication/__init__.py:83-112). That means active authenticated users pick up a baseline permissions set from settings in addition to object-permission logic.

At the broader deployment layer, the architectural summary also says `AUTHENTICATION_BACKENDS` layers remote/SSO backends with `ObjectPermissionBackend`, so UI/API access can be tied to the same user account and permission model even when remote auth is enabled (ARCH, ent-netbox-rel-2-v3.prompt.md:23).

## Gaps
The prompt does not expose the full object-permission schema from the gold fact (object type + users/groups + allowed actions + JSON constraints), and it does not mention `EXEMPT_VIEW_PERMISSIONS` or anonymous read exemptions. Those parts cannot be confirmed here (GAPS, ent-netbox-rel-2-v3.prompt.md:298-301).
