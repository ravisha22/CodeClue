# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-netbox-rel-2

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.


--- ARCHITECTURAL CONTEXT (LLM-generated, one-time) ---
NetBox
-- ARCH (LLM-generated architectural summary, ~500 tokens)
Framework: Django 5.2.13 (NetBox 4.5.8) with Django REST Framework 3.16.1 and Strawberry GraphQL
Architecture: Modular Django monolith serving server-rendered UI, REST API, and GraphQL from one application. The codebase is split into bounded app areas such as dcim, ipam, circuits, virtualization, tenancy, vpn, wireless, extras, and users. It is not a microservice system; instead, it is a single authoritative “source of truth” platform with strong plugin hooks.
Domain model: NetBox models network infrastructure as interlinked inventory and address-management objects. dcim covers sites, racks, devices, modules, power, cables, and component templates/components; ipam covers VRFs, prefixes, IP addresses, VLANs, services, FHRP groups, and ASNs. Other apps add circuits, virtual machines/clusters, tenants, VPN constructs, and wireless objects. The result is a graph-like operational model: sites contain racks, racks hold devices, devices connect by cables and interfaces, interfaces/IPs live inside VRFs/VLANs/prefixes, and tenancy overlays ownership and access boundaries.
Data layer: PostgreSQL via Django ORM, configured through a separate Python configuration module rather than hardcoding in settings. Standard Django migrations are used per app. Redis is a required companion service and is split logically for task queues and caching. This gives NetBox a classic relational core with sidecar queue/cache infrastructure.
API surface: Multi-surface API. netbox.urls mounts app UIs, app-specific REST endpoints under /api/, an OpenAPI schema via drf-spectacular, and a /graphql/ endpoint backed by NetBoxGraphQLView. Routes are composed by Django include() from each domain app, so the URL tree mirrors the modular app structure. This is a richer surface than AST extraction alone suggests: HTML UI, REST, GraphQL, schema docs, plugin routes, and HTMX endpoints all coexist.
Auth/permissions: Session auth for the web UI and token auth for the API. DRF uses a custom TokenAuthentication class plus TokenPermissions, enforcing object/model permissions, token validity, expiration, and optional source-IP restrictions. AUTHENTICATION_BACKENDS layers remote/SSO backends with ObjectPermissionBackend, and README/settings emphasize granular role-style permissions plus optional remote auth.
Key workflows: (1) Build the network source of truth by modeling sites, racks, devices, components, and cabling. (2) Perform IPAM by allocating VRFs, prefixes, VLANs, IPs, and services with validation. (3) Expose intended-state data to automation through REST/GraphQL, config rendering, and exported docs. (4) Run custom scripts, webhooks, and event-driven automations when infrastructure data changes. (5) Extend behavior via plugins, custom fields, tags, validation rules, and change logging.
Config: Configuration is loaded from a Python module (default netbox.configuration, overridable with NETBOX_CONFIGURATION). Required parameters include ALLOWED_HOSTS, SECRET_KEY, REDIS, and DATABASE/DATABASES. Operators tune auth, plugins, metrics, CORS, base path, remote auth, and many deployment behaviors in that config module rather than only environment variables.
Dependencies: PostgreSQL, Redis for both tasks and caching, django-rq for background work, social auth/remote auth integrations, drf-spectacular for API schema/docs, Prometheus middleware for metrics, and plugin/webhook/script extension points.
Test approach: Django TestCase-style testing with substantial reusable helpers in utilities.testing. There are specialized base classes for model, view, API, table, and GraphQL tests, using DRF APIClient and shared assertion patterns to keep app-level tests consistent.
--- END ARCHITECTURAL CONTEXT ---

--- CLUE FILE START ---
=CC v2.1 netbox@HEAD 1108mod 11893sym
? How do NetBox permissions and authentication interact across the UI and API?


-- README
<div align="center"> <img src="https://raw.githubusercontent.com/netbox-community/netbox/main/docs/netbox_logo_light.svg" width="400" alt=...
sections: NetBox's Role, Why NetBox?, Comprehensive Data Model, Focused Development, Extensible and Customizable

-- TREE
contrib/  (1 files)
docs/  (1 files)
netbox/  (1109 files)
  account/  circuits/  core/  dcim/  extras/  ipam/  netbox/  project-static/  reports/  scripts/  ...+6
README.md  mkdocs.yml

-- INDEX
contrib/gunicorn.py                              20L  
netbox/account/__init__.py                        0L  
netbox/account/migrations/0001_initial.py        27L  Migration
netbox/account/migrations/__init__.py             0L  
netbox/account/models.py                         17L  Meta, get_absolute_url, UserToken
netbox/account/urls.py                           21L  path:api-tokens/, path:api-tokens/<int:pk>/, path:api-tokens/add/, path:bookmarks/, path:notifications/
netbox/account/views.py                         380L  get_extra_context, get_queryset, BookmarkListView, get, post
netbox/circuits/__init__.py                       0L  
netbox/circuits/api/__init__.py                   0L  
netbox/circuits/api/serializers.py                2L  
netbox/circuits/api/serializers_/__init__.py      0L  
netbox/circuits/api/serializers_/circuits.py    207L  Meta, CircuitCircuitTerminationSerializer, Meta, CircuitGroupAssignmentSerializer, Meta
netbox/circuits/api/serializers_/nested.py       13L  Meta, NestedProviderAccountSerializer
netbox/circuits/api/serializers_/providers.py    67L  Meta, ProviderAccountSerializer, Meta, ProviderNetworkSerializer, Meta
netbox/circuits/api/urls.py                      26L  
netbox/circuits/api/views.py                    126L  CircuitGroupAssignmentViewSet, CircuitGroupViewSet, CircuitTerminationViewSet, CircuitTypeViewSet, CircuitViewSet
netbox/circuits/apps.py                          26L  ready, CircuitsConfig
netbox/circuits/choices.py                      110L  CircuitCommitRateChoices, CircuitPriorityChoices, CircuitStatusChoices, CircuitTerminationPortSpeedChoices, CircuitTerminationSideChoices
  ...and 1090 more modules

-- SYM
IPAddress                           C netbox/ipam/models/ip.py:750    An IPAddress represents an individual IPv4 or I...
filter_by_termination_object        M netbox/dcim/filtersets.py:2675   function filter_by_termination_object
multivalue_field_factory            M netbox/utilities/filters.py:31     Given a form field class, return a subclass cap...
run                                 M netbox/extras/jobs.py:100    Run the script.
save                                M netbox/extras/models/scripts.py:186    function save
IPRange                             C netbox/ipam/models/ip.py:516    A range of IP addresses, defined by start and e...
run_script                          M netbox/extras/jobs.py:30     Core script execution task.
delete                              M netbox/extras/models/scripts.py:77     function delete
sync_classes                        M netbox/extras/models/scripts.py:153    Syncs the file-based module to the database, ad...
_get_registered_content             M netbox/utilities/templatetags/plugins.py:11     Given an object and a PluginTemplateExtension m...
get                                 M netbox/ipam/views.py:1130   function get
process_lhs                         M netbox/ipam/lookups.py:6      function process_lhs
get_next_available_ip               M netbox/ipam/models/ip.py:864    Return the next available IP address within thi...
_log                                M netbox/extras/scripts.py:525    Log a message.
_check_permission                   M netbox/utilities/templatetags/perms.py:17     function _check_permission
create                              M netbox/core/models/object_types.py:26     function create
_save_tags                          M netbox/netbox/api/serializers/features.py:77     function _save_tags
update                              M netbox/ipam/api/views.py:126    function update
_populate_from_cache                M netbox/netbox/config/__init__.py:69     Populate config data from Redis cache
serialize_for_event                 M netbox/extras/events.py:79     Return a serialized representation of the given...
resolve_name                        M netbox/dcim/models/device_component_templates.py:169    function resolve_name
RIRSerializer                       C netbox/ipam/api/serializers_/asns.py:18     class RIRSerializer
resolve_label                       M netbox/dcim/models/device_component_templates.py:174    function resolve_label
_serialize_params                   M netbox/utilities/forms/widgets/apiselect.py:105    Serialize dynamic or static query params to JSO...
ObjectTypeQuerySet                  C netbox/core/models/object_types.py:24     class ObjectTypeQuerySet
_get_filter_lookup_dict             M netbox/netbox/filtersets.py:129    function _get_filter_lookup_dict
run_validators                      M netbox/utilities/filters.py:48     function run_validators
to_python                           M netbox/utilities/filters.py:39     function to_python
validate                            M netbox/utilities/filters.py:52     function validate
get_limit                           M netbox/netbox/api/pagination.py:45     function get_limit
_get_terminations                   M netbox/dcim/tables/cables.py:29     function _get_terminations
_populate_count_for_type            M netbox/dcim/migrations/0219_devicetype_device_count.py:7      Update a CounterCache field on the specified mo...
_get_custom_fields                  M netbox/extras/api/customfields.py:40     Cache CustomFields assigned to this model to av...
VLANGroupSerializer                 C netbox/ipam/api/serializers_/vlans.py:27     class VLANGroupSerializer
filter_device                       M netbox/ipam/graphql/filters.py:166    Helper to standardize logic for device and devi...
get_url_params                      M netbox/netbox/object_actions.py:55     function get_url_params
get_queryset                        M netbox/users/api/views.py:118    function get_queryset
cache_templates                     M netbox/utilities/jinja2.py:44     function cache_templates
_draw_device                        M netbox/dcim/svg/racks.py:177    function _draw_device
profile_class                       M netbox/dcim/models/cables.py:139    function profile_class
_get_protocol_from_url              M netbox/utilities/proxy.py:17     Determine the applicable protocol (e.g.
collect                             M netbox/netbox/models/deletion.py:15     function collect
unpack_grouped_choices              M netbox/utilities/choices.py:86     Unpack a grouped choices hierarchy into a flat ...
to_python                           M netbox/ipam/fields.py:33     function to_python
serialize_object                    M netbox/netbox/models/features.py:82     Return a JSON representation of the instance.
_compile_form_errors                M netbox/netbox/views/generic/bulk_views.py:362    function _compile_form_errors
Config                              C netbox/netbox/config/__init__.py:42     Fetch and store in memory the current NetBox co...
get_viewname                        M netbox/utilities/views.py:293    Return the view name for the given model and ac...
_clean_side                         M netbox/dcim/forms/bulk_import.py:1539   Derive a Cable's A/B termination objects.
_get_script                         M netbox/extras/api/views.py:294    function _get_script
get_additional_lookups              M netbox/netbox/filtersets.py:167    function get_additional_lookups
generate                            M netbox/users/models/tokens.py:256    Generate and return a random token value of the...
get_queryset                        M netbox/core/models/object_types.py:43     function get_queryset
get_object                          M netbox/extras/views.py:1642   function get_object
get_clean_data                      M netbox/core/models/change_logging.py:173    Return only the pre-/post-change attributes whi...
clone                               M netbox/ipam/models/ip.py:991    function clone
to_objectchange                     M netbox/ipam/models/ip.py:1000   function to_objectchange
get_for_model                       M netbox/extras/models/customfields.py:66     Return all CustomFields assigned to the given m...
_get_columns                        M netbox/netbox/tables/tables.py:64     function _get_columns
  ...and 8206 more symbols

-- FOCUS
netbox/netbox/settings.py (netbox/netbox/settings.py:1-981)
  Config summary for netbox/netbox/settings.py: entries: RELEASE=load_release_data(), VERSION=RELEASE.full_version, BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ADMINS=getattr(configuration, 'ADMINS', []), ALLOWED_HOSTS=getattr(configuration, 'ALLOWED_HOSTS'), API_TOKEN_PEPPERS=getattr(configuration, 'API_TOKEN_PEPPERS', {})
  entries: RELEASE=load_release_data(), VERSION=RELEASE.full_version, BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ADMINS=getattr(configuration, 'ADMINS', []), ALLOWED_HOSTS=getattr(configuration, 'ALLOWED_HOSTS')

netbox/core/tables/config.py (netbox/core/tables/config.py:1-36)
  Config summary for netbox/core/tables/config.py: entries: REVISION_BUTTONS='\n{% if not record.is_active %}\n<a href="{% url \'core:configrevision_restore\' pk=record.pk %}...
  entries: REVISION_BUTTONS='\n{% if not record.is_active %}\n<a href="{% url \'core:configrevision_restore\' pk=record.pk %}...

netbox/project-static/netbox-graphiql/package.json (netbox/project-static/netbox-graphiql/package.json:1-17)
  Config summary for netbox/project-static/netbox-graphiql/package.json: deps: @graphiql/plugin-explorer, graphiql, graphql, js-cookie, react, react-dom
  deps: @graphiql/plugin-explorer, graphiql, graphql, js-cookie, react, react-dom

path:api/authentication-c (netbox/netbox/urls.py:1-97)
  Django route api/authentication-c -> AuthenticationCheckView.as_view
  target: AuthenticationCheckView.as_view

TokenPermissions (netbox/netbox/api/authentication.py:125-169)
  Custom permissions handler which extends the built-in DjangoModelPermissions to validate a Token's write ability
  extends: DjangoObjectPermissions
  imports: logging, django.conf, django.utils, drf_spectacular.extensions, rest_framework
  calls: __init__, _verify_write_permission, has_object_permission

get_permissions (netbox/extras/api/mixins.py:70-74)
  behavior: GUARD(self.action == 'render_config' -> return [TokenWritePermiss...)
  called_by: RenderConfigMixin
  uses: TokenWritePermission (netbox.api.authentication)

get_permissions (netbox/extras/api/views.py:243-247)
  behavior: GUARD(self.action == 'render' -> return [TokenWritePermiss...)
  called_by: ConfigTemplateViewSet
  uses: TokenWritePermission (netbox.api.authentication)

TokenAuthentication (netbox/netbox/api/authentication.py:19-122)
  A custom authentication scheme which enforces Token expiration times and source IP restrictions.
  extends: BaseAuthentication
  imports: logging, django.conf, django.utils, drf_spectacular.extensions, rest_framework
  raises: AuthenticationFailed, DoesNotExist

get_all_permissions (netbox/netbox/authentication/__init__.py:73-78)
  sig: get_all_permissions(user_obj, obj)
  behavior: GUARD(not user_obj.is_active or user_obj.is_anonymous -> return dict())
  calls: get_object_permissions
  called_by: ObjectPermissionMixin

get_object_permissions (netbox/netbox/authentication/__init__.py:83-112)
  Return all permissions granted to the user by an ObjectPermission.
  sig: get_object_permissions(user_obj)
  behavior: ACCUMULATE(settings.DEFAULT_PERM... -> perms constraints, raises ImproperlyC...)
  called_by: get_all_permissions, ObjectPermissionMixin
  raises: ImproperlyConfigured
  uses: ImproperlyConfigured (django.core.exceptions)

AuthenticationAlgorithmChoices (netbox/vpn/choices.py:139-152)
  extends: ChoiceSet
  attrs: AUTH_HMAC_SHA1='hmac-sha1', AUTH_HMAC_SHA256='hmac-sha256', AUTH_HMAC_SHA384='hmac-sha384', AUTH_HMAC_SHA512='hmac-sha512'
  imports: django.utils.translation, utilities.choices

AuthenticationMethodChoices (netbox/vpn/choices.py:93-104)
  extends: ChoiceSet
  attrs: PRESHARED_KEYS='preshared-keys', CERTIFICATES='certificates', RSA_SIGNATURES='rsa-signatures', DSA_SIGNATURES='dsa-signatures'
  imports: django.utils.translation, utilities.choices

WirelessAuthenticationBase (netbox/wireless/models.py:21-46)
  Abstract model for attaching attributes related to wireless authentication.
  extends: Model
  imports: django.core.exceptions, django.db, django.utils.translation, dcim.choices, dcim.constants

WirelessAuthenticationFilterMixin (netbox/wireless/graphql/filter_mixins.py:17-24)
  imports: strawberry, strawberry_django, enums

WirelessAuthenticationPanel (netbox/wireless/ui/panels.py:20-25)
  extends: ObjectAttributesPanel
  imports: django.utils.translation, netbox.ui

get_rest_api_endpoint (netbox/core/api/serializers_/object_types.py:35-41)
  sig: get_rest_api_endpoint(obj)
  behavior: GUARD(not (model := obj.model_class()) -> return None)

handle_rest_api_exception (netbox/utilities/error_handlers.py:48-59)
  Handle exceptions and return a useful error message for REST API requests.
  sig: handle_rest_api_exception(request)
  uses: JsonResponse (django.http)

is_api_request (netbox/utilities/api.py:71-75)
  Return True of the request is being made via the REST API.
  sig: is_api_request(request)
  behavior: DELEGATE(request.path_info.startswith -> result)

path:api-tokens/ (netbox/account/urls.py:1-22)
  Django route api-tokens/ -> views.UserTokenListView.as_view
  target: views.UserTokenListView.as_view

path:api-tokens/<int:pk>/ (netbox/account/urls.py:1-22)
  Django route api-tokens/<int:pk>/ -> include
  target: include

path:api-tokens/add/ (netbox/account/urls.py:1-22)
  Django route api-tokens/add/ -> views.UserTokenEditView.as_view
  target: views.UserTokenEditView.as_view

path:api/ (netbox/netbox/urls.py:1-97)
  Django route api/ -> APIRootView.as_view
  target: APIRootView.as_view

path:api/circuits/ (netbox/netbox/urls.py:1-97)
  Django route api/circuits/ -> include
  target: include

path:api/core/ (netbox/netbox/urls.py:1-97)
  Django route api/core/ -> include
  target: include

path:api/dcim/ (netbox/netbox/urls.py:1-97)
  Django route api/dcim/ -> include
  target: include

path:api/extras/ (netbox/netbox/urls.py:1-97)
  Django route api/extras/ -> include
  target: include

path:api/ipam/ (netbox/netbox/urls.py:1-97)
  Django route api/ipam/ -> include
  target: include

path:api/plugins/ (netbox/netbox/urls.py:1-97)
  Django route api/plugins/ -> include
  target: include

path:api/schema/ (netbox/netbox/urls.py:1-97)
  Django route api/schema/ -> cache_page
  target: cache_page

path:api/schema/redoc/ (netbox/netbox/urls.py:1-97)
  Django route api/schema/redoc/ -> SpectacularRedocView.as_view
  target: SpectacularRedocView.as_view

path:api/schema/swagger-u (netbox/netbox/urls.py:1-97)
  Django route api/schema/swagger-u -> SpectacularSwaggerView.as_view
  target: SpectacularSwaggerView.as_view

path:api/status/ (netbox/netbox/urls.py:1-97)
  Django route api/status/ -> StatusView.as_view
  target: StatusView.as_view

path:api/tenancy/ (netbox/netbox/urls.py:1-97)
  Django route api/tenancy/ -> include
  target: include

path:api/users/ (netbox/netbox/urls.py:1-97)
  Django route api/users/ -> include
  target: include

path:api/virtualization/ (netbox/netbox/urls.py:1-97)
  Django route api/virtualization/ -> include
  target: include

path:api/vpn/ (netbox/netbox/urls.py:1-97)
  Django route api/vpn/ -> include
  target: include

path:api/wireless/ (netbox/netbox/urls.py:1-97)
  Django route api/wireless/ -> include
  target: include

path:permissions/ (netbox/users/urls.py:1-29)
  Django route permissions/ -> include
  target: include

-- GAPS
type: RELATIONAL (answerable from L2-L3 structure)
coverage: 80 symbols in L3, 11 with behavior annotations
uncovered: AuthenticationCheckView, PermissionsViolation, get_api_root_view, ObjectPermissionSerializer

--- CLUE FILE END ---

QUESTION: How do NetBox permissions and authentication interact across the UI and API?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
