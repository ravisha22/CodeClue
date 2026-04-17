# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-netbox-mech-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 netbox@HEAD 1108mod 11893sym
? How are NetBox background jobs enqueued, scheduled, and executed?


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

is_background_request (netbox/utilities/jobs.py:14-18)
  Return True if the request is being processed as a background job.
  sig: is_background_request(request)
  behavior: DELEGATE(hasattr -> result)
  called_by: process_request_as_job

get_jobs (netbox/extras/models/mixins.py:40-48)
  Returns a list of Jobs associated with this specific script or report module
  sig: get_jobs(name)
  behavior: DELEGATE(jobs.filter -> result)

get_latest_jobs (netbox/netbox/models/features.py:466-470)
  Return a list of the most recent jobs for this instance.
  behavior: DELEGATE(jobs.filter.order_by.defer -> result)

get_rq_jobs (netbox/core/utils.py:28-38)
  Return a list of all RQ jobs.
  behavior: ACCUMULATE(get_queues_list() loop -> jobs queue get jobs)

get_rq_jobs_from_status (netbox/core/utils.py:41-74)
  Return the RQ jobs with the given status.
  sig: get_rq_jobs_from_status(queue, status)
  behavior: BRANCH(status != RQJobStatus.DEFERRED -> get_jobs(queue, job_i..., else -> r...)
  raises: Http404

delete_expired_jobs (netbox/core/jobs.py:143-159)
  Delete any jobs older than the configured retention period (if any).
  called_by: SystemHousekeepingJob
  uses: Config (netbox.config)

BackgroundTaskSerializer (netbox/core/api/serializers_/tasks.py:11-59)
  extends: Serializer
  imports: rest_framework, rest_framework.reverse
  calls: get_position, get_status

get_jobs (netbox/netbox/jobs.py:134-147)
  Get all jobs of this `JobRunner` related to a specific instance.
  sig: get_jobs(cls, instance)
  called_by: enqueue_once, JobRunner

draw_background (netbox/dcim/svg/racks.py:297-325)
  Draw the rack unit placeholders which form the "background" of the rack elevation.
  sig: draw_background(face)
  behavior: ACCUMULATE(range(0, self.rack.u_... -> y offset binop)
  called_by: render, RackElevationSVG
  uses: Hyperlink (svgwrite.container), Rect (svgwrite.shapes), Text (svgwrite.text)

BackgroundJobMixin (netbox/utilities/forms/mixins.py:102-116)
  extends: Form
  imports: decimal, django, django.core.validators, django.utils.translation, netbox.registry

BackgroundQueueListView (netbox/core/views.py:500-509)
  extends: TableMixin, BaseRQView
  imports: platform, copy, django, django.conf, django.contrib

BackgroundQueueSerializer (netbox/core/api/serializers_/tasks.py:62-77)
  extends: Serializer
  imports: rest_framework, rest_framework.reverse

BackgroundQueueTable (netbox/core/tables/tasks.py:10-71)
  extends: BaseTable
  imports: django_tables2, django.utils.translation, django_tables2.utils, core.constants, core.tables.columns

BackgroundTaskDeleteView (netbox/core/views.py:568-592)
  extends: BaseRQView
  imports: platform, copy, django, django.conf, django.contrib

BackgroundTaskEnqueueView (netbox/core/views.py:603-609)
  extends: BaseRQView
  imports: platform, copy, django, django.conf, django.contrib

BackgroundTaskListView (netbox/core/views.py:512-538)
  extends: TableMixin, BaseRQView
  imports: platform, copy, django, django.conf, django.contrib

BackgroundTaskRequeueView (netbox/core/views.py:595-600)
  extends: BaseRQView
  imports: platform, copy, django, django.conf, django.contrib

BackgroundTaskStopView (netbox/core/views.py:612-621)
  extends: BaseRQView
  imports: platform, copy, django, django.conf, django.contrib

BackgroundTaskTable (netbox/core/tables/tasks.py:74-111)
  extends: BaseTable
  imports: django_tables2, django.utils.translation, django_tables2.utils, core.constants, core.tables.columns

BackgroundTaskView (netbox/core/views.py:541-565)
  extends: BaseRQView
  imports: platform, copy, django, django.conf, django.contrib
  raises: Http404

BackgroundWorkerSerializer (netbox/core/api/serializers_/tasks.py:80-97)
  extends: Serializer
  imports: rest_framework, rest_framework.reverse
  calls: get_state

ScriptJobsView (netbox/extras/views.py:1751-1765)
  extends: BaseScriptView
  imports: django.contrib, django.contrib.auth.mixins, django.contrib.contenttypes.models, django.core.paginator, django.db.models
  calls: get_object

convert_reportmodule_jobs (netbox/extras/migrations/0108_convert_reports_to_scripts.py:4-12)
  sig: convert_reportmodule_jobs(apps, schema_editor)

get_jobs (netbox/netbox/views/generic/feature_views.py:209-214)
  sig: get_jobs(instance)
  called_by: ObjectJobsView

path:background-queues/ (netbox/core/urls.py:1-57)
  Django route background-queues/ -> views.BackgroundQueueListView.as_view
  target: views.BackgroundQueueListView.as_view

path:background-queues/<i (netbox/core/urls.py:1-57)
  Django route background-queues/<i -> views.BackgroundTaskListView.as_view
  target: views.BackgroundTaskListView.as_view

path:background-tasks/<st (netbox/core/urls.py:1-57)
  Django route background-tasks/<st -> views.BackgroundTaskDeleteView.as_view
  target: views.BackgroundTaskDeleteView.as_view

path:background-tasks/<st (netbox/core/urls.py:1-57)
  Django route background-tasks/<st -> views.BackgroundTaskRequeueView.as_view
  target: views.BackgroundTaskRequeueView.as_view

path:background-tasks/<st (netbox/core/urls.py:1-57)
  Django route background-tasks/<st -> views.BackgroundTaskEnqueueView.as_view
  target: views.BackgroundTaskEnqueueView.as_view

path:background-tasks/<st (netbox/core/urls.py:1-57)
  Django route background-tasks/<st -> views.BackgroundTaskStopView.as_view
  target: views.BackgroundTaskStopView.as_view

path:background-tasks/<st (netbox/core/urls.py:1-57)
  Django route background-tasks/<st -> views.BackgroundTaskView.as_view
  target: views.BackgroundTaskView.as_view

path:background-workers/< (netbox/core/urls.py:1-57)
  Django route background-workers/< -> views.WorkerListView.as_view
  target: views.WorkerListView.as_view

path:background-workers/< (netbox/core/urls.py:1-57)
  Django route background-workers/< -> views.WorkerView.as_view
  target: views.WorkerView.as_view

path:jobs/ (netbox/core/urls.py:1-57)
  Django route jobs/ -> include
  target: include

path:jobs/<int:pk>/ (netbox/core/urls.py:1-57)
  Django route jobs/<int:pk>/ -> include
  target: include

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 80 symbols in L3, 12 with behavior annotations
uncovered: NetBoxModelFilter, NetBoxModelFilterSet, NetBoxModelFilterSetForm, README.md

--- CLUE FILE END ---

QUESTION: How are NetBox background jobs enqueued, scheduled, and executed?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
