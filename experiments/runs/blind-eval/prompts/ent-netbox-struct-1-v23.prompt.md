# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-netbox-struct-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 netbox@HEAD 1108mod 11893sym
? What is NetBox's overall architectural role and data scope?


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

data_as_string (netbox/core/models/data.py:341-347)
  behavior: GUARD(not self.data -> return None)

get_role_color (netbox/ipam/models/ip.py:1043-1044)
  behavior: DELEGATE(IPAddressRoleChoices.colors.get -> result)

get_role_color (netbox/vpn/models/tunnels.py:157-158)
  behavior: DELEGATE(TunnelTerminationRoleChoices.colors.get -> result)

get_role_color (netbox/circuits/models/virtual_circuits.py:162-163)
  behavior: DELEGATE(VirtualCircuitTerminationRoleChoices.colors.get -> result)

oc_cluster_scope (netbox/virtualization/migrations/0044_cluster_scope.py:49-58)
  sig: oc_cluster_scope(objectchange, reverting)
  behavior: ACCUMULATE((objectchange.prechan... -> data value)

oc_prefix_scope (netbox/ipam/migrations/0071_prefix_scope.py:50-59)
  sig: oc_prefix_scope(objectchange, reverting)
  behavior: ACCUMULATE((objectchange.prechan... -> data value)

postchange_data_clean (netbox/core/models/change_logging.py:189-190)
  behavior: DELEGATE(get_clean_data -> result)
  calls: get_clean_data

prechange_data_clean (netbox/core/models/change_logging.py:185-186)
  behavior: DELEGATE(get_clean_data -> result)
  calls: get_clean_data

prep_object_data (netbox/ipam/api/views.py:422-431)
  sig: prep_object_data(requested_objects, available_objects, parent)
  behavior: ACCUMULATE(enumerate(requested_o... -> request data value)

prep_object_data (netbox/ipam/api/views.py:373-386)
  sig: prep_object_data(requested_objects, available_objects, parent)
  behavior: ACCUMULATE(enumerate(requested_o... -> request data value, raises Validation...)
  raises: ValidationError
  uses: IPSet (netaddr), ValidationError (rest_framework.exceptions)

prep_object_data (netbox/ipam/api/views.py:475-482)
  sig: prep_object_data(requested_objects, available_objects, parent)
  behavior: ACCUMULATE(enumerate(requested_o... -> request data value)

prep_object_data (netbox/ipam/api/views.py:325-333)
  sig: prep_object_data(requested_objects, available_objects, parent)
  behavior: ACCUMULATE(enumerate(requested_o... -> request data value)

value_omitted_from_data (netbox/utilities/forms/fields/csv.py:26-32)
  sig: value_omitted_from_data(data, files, name)
  behavior: GUARD(super().value_omitted_from_data(data, files, name) -> return True)
  called_by: CSVSelectWidget

DataSource (netbox/core/models/data.py:35-278)
  A remote source, such as a git repository, from which DataFiles are synchronized.
  extends: JobsMixin, PrimaryModel
  imports: hashlib, logging, fnmatch, urllib.parse, yaml
  calls: refresh_from_disk, DataFile, _ignore, _walk, backend_class, clean, get_backend, save
  raises: ValidationError, SyncError
  uses: ValidationError (django.core.exceptions)

DataFile (netbox/core/models/data.py:281-373)
  The database representation of a remote file fetched from a remote DataSource.
  extends: Model
  imports: hashlib, logging, fnmatch, urllib.parse, yaml
  called_by: sync, DataSource

Role (netbox/ipam/models/ip.py:191-207)
  A Role represents the functional role of a Prefix or VLAN; for example, "Customer," "Infrastructure," or
  extends: OrganizationalModel
  imports: netaddr, django.contrib.contenttypes.fields, django.contrib.contenttypes.models, django.contrib.postgres.indexes, django.core.exceptions

SyncedDataMixin (netbox/netbox/models/features.py:511-638)
  Enables population of local data from a DataFile object, synchronized from a remote DataSource.
  extends: Model
  imports: django.contrib.contenttypes.fields, django.contrib.contenttypes.models, django.core.validators, django.db, django.db.models
  calls: delete, sync, sync_data
  raises: NotImplementedError

BulkSyncDataView (netbox/netbox/views/generic/feature_views.py:262-284)
  Synchronize multiple instances of a model inheriting from SyncedDataMixin.
  extends: GetReturnURLMixin, BaseMultiObjectView
  imports: django.contrib, django.contrib.auth.mixins, django.contrib.contenttypes.models, django.db, django.db.models

CachedScopeMixin (netbox/dcim/models/mixins.py:41-122)
  Mixin for adding a GenericForeignKey scope to a model that can point to a Region, SiteGroup, Site, or Location.
  extends: Model
  imports: django.apps, django.contrib.contenttypes.fields, django.core.exceptions, django.db, django.utils.translation
  calls: cache_related_objects, save
  raises: ValidationError

ConfigContextBulkSyncDataView (netbox/extras/views.py:1126-1127)
  extends: BulkSyncDataView
  imports: django.contrib, django.contrib.auth.mixins, django.contrib.contenttypes.models, django.core.paginator, django.db.models

ConfigContextProfileBulkSyncDataView (netbox/extras/views.py:1027-1028)
  extends: BulkSyncDataView
  imports: django.contrib, django.contrib.auth.mixins, django.contrib.contenttypes.models, django.core.paginator, django.db.models

ConfigTemplateBulkSyncDataView (netbox/extras/views.py:1230-1231)
  extends: BulkSyncDataView
  imports: django.contrib, django.contrib.auth.mixins, django.contrib.contenttypes.models, django.core.paginator, django.db.models

ContactRole (netbox/tenancy/models/contacts.py:64-71)
  Functional role for a Contact assigned to an object.
  extends: OrganizationalModel
  imports: django.contrib.contenttypes.fields, django.core.exceptions, django.db, django.db.models.expressions, django.urls

ContactRoleBulkDeleteView (netbox/tenancy/views.py:362-365)
  extends: BulkDeleteView
  imports: django.contrib.contenttypes.models, django.shortcuts, django.utils.translation, extras.ui.panels, netbox.object_actions

ContactRoleBulkEditForm (netbox/tenancy/forms/bulk_edit.py:74-79)
  extends: OrganizationalModelBulkEditForm
  imports: django, django.utils.translation, netbox.forms, utilities.forms, utilities.forms.fields

ContactRoleBulkEditView (netbox/tenancy/views.py:348-352)
  extends: BulkEditView
  imports: django.contrib.contenttypes.models, django.shortcuts, django.utils.translation, extras.ui.panels, netbox.object_actions

ContactRoleBulkImportView (netbox/tenancy/views.py:342-344)
  extends: BulkImportView
  imports: django.contrib.contenttypes.models, django.shortcuts, django.utils.translation, extras.ui.panels, netbox.object_actions

ContactRoleBulkRenameView (netbox/tenancy/views.py:356-358)
  extends: BulkRenameView
  imports: django.contrib.contenttypes.models, django.shortcuts, django.utils.translation, extras.ui.panels, netbox.object_actions

ContactRoleDeleteView (netbox/tenancy/views.py:337-338)
  extends: ObjectDeleteView
  imports: django.contrib.contenttypes.models, django.shortcuts, django.utils.translation, extras.ui.panels, netbox.object_actions

ContactRoleEditView (netbox/tenancy/views.py:331-333)
  extends: ObjectEditView
  imports: django.contrib.contenttypes.models, django.shortcuts, django.utils.translation, extras.ui.panels, netbox.object_actions

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 82 symbols in L3, 13 with behavior annotations
uncovered: DataSourceType, DataSourceView, DataSourceViewSet, DeviceRole

--- CLUE FILE END ---

QUESTION: What is NetBox's overall architectural role and data scope?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
