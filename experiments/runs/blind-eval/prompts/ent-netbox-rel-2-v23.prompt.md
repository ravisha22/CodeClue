# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-netbox-rel-2

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 netbox@HEAD 1108mod 11516sym
? How do NetBox permissions and authentication interact across the UI and API?


-- TREE
contrib/  (1 files)
netbox/  (1107 files)
  account/  circuits/  core/  dcim/  extras/  ipam/  netbox/  reports/  scripts/  tenancy/  ...+5

-- INDEX
contrib/gunicorn.py                              20L  
netbox/account/__init__.py                        0L  
netbox/account/migrations/0001_initial.py        27L  Migration
netbox/account/migrations/__init__.py             0L  
netbox/account/models.py                         17L  Meta, get_absolute_url, UserToken
netbox/account/urls.py                           21L  
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
netbox/circuits/constants.py                     11L  
  ...and 1089 more modules

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
get_url_params                      M netbox/netbox/object_actions.py:55     function get_url_params
_get_custom_fields                  M netbox/extras/api/customfields.py:40     Cache CustomFields assigned to this model to av...
VLANGroupSerializer                 C netbox/ipam/api/serializers_/vlans.py:27     class VLANGroupSerializer
filter_device                       M netbox/ipam/graphql/filters.py:166    Helper to standardize logic for device and devi...
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
get_queryset                        M netbox/core/models/object_types.py:43     function get_queryset
generate                            M netbox/users/models/tokens.py:256    Generate and return a random token value of the...
get_clean_data                      M netbox/core/models/change_logging.py:173    Return only the pre-/post-change attributes whi...
get_object                          M netbox/extras/views.py:1642   function get_object
clone                               M netbox/ipam/models/ip.py:991    function clone
to_objectchange                     M netbox/ipam/models/ip.py:1000   function to_objectchange
get_for_model                       M netbox/extras/models/customfields.py:66     Return all CustomFields assigned to the given m...
_get_columns                        M netbox/netbox/tables/tables.py:64     function _get_columns
get_serializer_ref_name             M netbox/core/api/schema.py:208    Get serializer's ref_name
_get_opts                           M netbox/core/models/object_types.py:63     function _get_opts
update                              M netbox/netbox/api/serializers/features.py:65     function update
filter_by_cable_end                 M netbox/dcim/filtersets.py:2651   function filter_by_cable_end
vc_interfaces                       M netbox/dcim/models/devices.py:1087   Return a QuerySet matching all Interfaces assig...
_is_superuser                       M netbox/netbox/authentication/__init__.py:240    function _is_superuser
enqueue                             M netbox/netbox/jobs.py:150    Enqueue a new `Job`.
_load_resource                      M netbox/netbox/plugins/__init__.py:87     function _load_resource
ProviderSerializer                  C netbox/circuits/api/serializers_/providers.py:18     class ProviderSerializer
  ...and 7826 more symbols

-- FOCUS
TokenPermissions (netbox/netbox/api/authentication.py:125-169)
  Custom permissions handler which extends the built-in DjangoModelPermissions to validate a Token's write ability
  extends: DjangoObjectPermissions
  imports: logging, django.conf, django.utils, drf_spectacular.extensions, rest_framework
  calls: __init__, _verify_write_permission, has_object_permission

get_permissions (netbox/extras/api/views.py:243-247)
  behavior: GUARD(self.action == 'render' -> return [TokenWritePermiss...)
  called_by: ConfigTemplateViewSet
  uses: TokenWritePermission (netbox.api.authentication)

get_permissions (netbox/extras/api/mixins.py:70-74)
  behavior: GUARD(self.action == 'render_config' -> return [TokenWritePermiss...)
  called_by: RenderConfigMixin
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

APIRootView (netbox/netbox/api/views.py:20-46)
  This is the root of NetBox's REST API.
  extends: APIView
  imports: platform, django, django.conf, django_rq.queues, drf_spectacular.types

APISelect (netbox/utilities/forms/widgets/apiselect.py:13-169)
  A select widget populated via an API call
  extends: Select
  attrs: template_name='widgets/apiselect.html', option_template_name='widgets/select_option.html'
  imports: django, django.conf, django.utils.translation
  calls: __deepcopy__, __init__, _add_dynamic_params, _add_static_params, _process_query_param, _process_query_params, _serialize_params, add_query_params
  raises: RuntimeError

InstalledPluginsAPIView (netbox/netbox/plugins/views.py:15-42)
  API view for listing all installed plugins
  extends: APIView
  attrs: schema=None
  imports: django.apps, django.urls.exceptions, drf_spectacular.utils, rest_framework.response, rest_framework.reverse
  calls: _get_plugin_data

NetBoxGraphQLView (netbox/netbox/graphql/views.py:13-42)
  Extends strawberry's GraphQLView to support DRF's token-based authentication.
  extends: GraphQLView
  imports: django.conf, django.contrib.auth.views, django.http, django.urls, django.views.decorators.csrf
  calls: dispatch
  uses: HttpResponseNotFound (django.http), TokenAuthentication (netbox.api.authentication), HttpResponseForbidden (django.http)

Token (netbox/users/models/tokens.py:28-305)
  An API token used for user authentication.
  extends: Model
  imports: hashlib, hmac, random, zoneinfo, django.conf
  calls: __init__, clean, generate, generate_key, save, update_digest
  raises: ValueError, ValidationError
  uses: ValidationError (django.core.exceptions)

TokenWritePermission (netbox/netbox/api/authentication.py:172-183)
  Verify the token has write_enabled for unsafe methods, without requiring specific model permissions.
  extends: BasePermission
  imports: logging, django.conf, django.utils, drf_spectacular.extensions, rest_framework
  raises: PermissionDenied

get_serializer_for_model (netbox/utilities/api.py:45-56)
  Return the appropriate REST API serializer for the given model.
  sig: get_serializer_for_model(model, prefix)
  raises: SerializerNotFound
  uses: SerializerNotFound (netbox.api.exceptions)

RenderConfigMixin (netbox/extras/api/mixins.py:65-99)
  Provides a /render-config/ endpoint for REST API views whose model may have a ConfigTemplate assigned.
  extends: ConfigTemplateRenderMixin
  imports: jinja2.exceptions, rest_framework.decorators, rest_framework.renderers, rest_framework.response, rest_framework.status
  calls: render_configtemplate, get_permissions
  uses: ConfigTemplateSerializer (serializers), Response (rest_framework.response), TokenWritePermission (netbox.api.authentication)

BaseViewSet (netbox/netbox/api/viewsets/__init__.py:37-94)
  Base class for all API ViewSets.
  extends: GenericViewSet
  attrs: brief=False
  imports: logging, django.core.exceptions, django.db, django.db.models, django_pglocks
  calls: initial, initialize_request

CircuitsRootView (netbox/circuits/api/views.py:11-16)
  Circuits API root view
  extends: APIRootView
  imports: rest_framework.routers, circuits, circuits.models, dcim.api.views, netbox.api.viewsets

ConfigTemplateRenderMixin (netbox/extras/api/mixins.py:41-62)
  Provides a method to return a rendered ConfigTemplate as REST API data.
  imports: jinja2.exceptions, rest_framework.decorators, rest_framework.renderers, rest_framework.response, rest_framework.status

CoreRootView (netbox/core/api/views.py:30-35)
  Core API root view
  extends: APIRootView
  imports: django.http, django.shortcuts, django.utils.translation, django_rq.queues, django_rq.settings

DCIMRootView (netbox/dcim/api/views.py:29-34)
  DCIM API root view
  extends: APIRootView
  imports: django.contrib.contenttypes.prefetch, django.http, django.shortcuts, drf_spectacular.types, drf_spectacular.utils

ExtrasRootView (netbox/extras/api/views.py:32-37)
  Extras API root view
  extends: APIRootView
  imports: django.http, django.shortcuts, django_rq.queues, drf_spectacular.utils, rest_framework

IPAMRootView (netbox/ipam/api/views.py:31-36)
  IPAM API root view
  extends: APIRootView
  imports: copy, django.contrib.contenttypes.prefetch, django.core.exceptions, django.db, django.shortcuts

MPTTLockedMixin (netbox/netbox/api/viewsets/__init__.py:262-278)
  Puts pglock on objects that derive from MPTTModel for parallel API calling.
  imports: logging, django.core.exceptions, django.db, django.db.models, django_pglocks

TenancyRootView (netbox/tenancy/api/views.py:10-15)
  Tenancy API root view
  extends: APIRootView
  imports: rest_framework.routers, netbox.api.viewsets, tenancy, tenancy.models

-- GAPS
type: RELATIONAL (answerable from L2-L3 structure)
coverage: 80 symbols in L3, 15 with behavior annotations
uncovered: perform_create, SyncedDataMixin, initial, initialize_request

--- CLUE FILE END ---

QUESTION: How do NetBox permissions and authentication interact across the UI and API?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
