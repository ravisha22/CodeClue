You are running the AFTER pass of a CodeClue drill-down evaluation.

Rules:
- Start from the same clue projection below.
- You MAY use the configured CodeClue MCP tools if needed.
- Use tool calls only where the clue is insufficient.
- After any tool usage, produce a revised answer.
- Be explicit about what changed because of the tools.

Task ID: flask-tf2-001
Family: TF2
Operation Family: OF2

Question:
If I change the `push` method in RequestContext (ctx.py) to be async, what other components would be impacted?

Return your answer in this format:

1. Revised answer
2. Tools used:
   - tool name + why you used it
3. What changed after drill-down:
   - ...
4. Remaining uncertainty:
   - ...
5. Final confidence: low|medium|high

## Confidence Block
{
  "code_density_risk": 0.147059,
  "confidence_overall": 0.487395,
  "lookup_decision_hint": "expanded_lookup",
  "operation_family": "OF2",
  "p_context_miss": 0.0,
  "p_dependency_miss": 0.428571,
  "p_hallucination": 0.0,
  "per_edge_confidence": [
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.__call__:1618:symbol:src/flask/app.py:Flask.wsgi_app:1566:1625",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.__init__:310:symbol:src/flask/app.py:Flask.__init__:310:323",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.__init__:310:symbol:src/flask/app.py:Flask.send_static_file:392:362",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.__init_subclass__:254:symbol:src/flask/app.py:add_ctx:97:308",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.__init_subclass__:254:symbol:src/flask/app.py:remove_ctx:85:307",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.dispatch_request:966:symbol:src/flask/app.py:Flask.ensure_sync:1065:990",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.dispatch_request:966:symbol:src/flask/app.py:Flask.make_default_options_response:1053:987",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.dispatch_request:966:symbol:src/flask/app.py:Flask.raise_routing_exception:562:979",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.do_teardown_appcontext:1453:symbol:src/flask/app.py:Flask.ensure_sync:1065:1474",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.do_teardown_request:1420:symbol:src/flask/app.py:Flask.ensure_sync:1065:1446",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.ensure_sync:1065:symbol:src/flask/app.py:Flask.async_to_sync:1079:1075",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.finalize_request:1021:symbol:src/flask/app.py:Flask.make_response:1224:1039",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.finalize_request:1021:symbol:src/flask/app.py:Flask.process_response:1394:1041",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.full_dispatch_request:992:symbol:src/flask/app.py:Flask.dispatch_request:966:1016",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.full_dispatch_request:992:symbol:src/flask/app.py:Flask.finalize_request:1021:1019",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.full_dispatch_request:992:symbol:src/flask/app.py:Flask.handle_user_exception:865:1018",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.full_dispatch_request:992:symbol:src/flask/app.py:Flask.preprocess_request:1366:1014",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_exception:897:symbol:src/flask/app.py:Flask.ensure_sync:1065:946",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_exception:897:symbol:src/flask/app.py:Flask.finalize_request:1021:948",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_exception:897:symbol:src/flask/app.py:Flask.log_exception:950:940",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_http_exception:830:symbol:src/flask/app.py:Flask.ensure_sync:1065:863",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_user_exception:865:symbol:src/flask/app.py:Flask.ensure_sync:1065:895",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_user_exception:865:symbol:src/flask/app.py:Flask.handle_http_exception:830:888",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.preprocess_request:1366:symbol:src/flask/app.py:Flask.ensure_sync:1065:1387",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.process_response:1394:symbol:src/flask/app.py:Flask.ensure_sync:1065:1408",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.process_response:1394:symbol:src/flask/app.py:Flask.ensure_sync:1065:1413",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.send_static_file:392:symbol:src/flask/app.py:Flask.get_send_file_max_age:365:409",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.test_request_context:1517:symbol:src/flask/app.py:Flask.request_context:1501:1564",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.update_template_context:590:symbol:src/flask/app.py:Flask.ensure_sync:1065:616",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.url_for:1102:symbol:src/flask/app.py:Flask.create_url_adapter:509:1182",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.wsgi_app:1566:symbol:src/flask/app.py:Flask.full_dispatch_request:992:1597",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.wsgi_app:1566:symbol:src/flask/app.py:Flask.handle_exception:897:1600",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/app.py:Flask.wsgi_app:1566:symbol:src/flask/app.py:Flask.request_context:1501:1592",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:AppGroup.command:413:symbol:src/flask/cli.py:AppGroup.command:413:425",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:AppGroup.command:413:symbol:src/flask/cli.py:with_appcontext:380:424",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:AppGroup.group:429:symbol:src/flask/cli.py:AppGroup.group:429:437",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.get_command:609:symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600:610",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.get_command:609:symbol:src/flask/cli.py:FlaskGroup.get_command:609:613",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.get_command:609:symbol:src/flask/cli.py:FlaskGroup.get_command:609:634",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.get_command:609:symbol:src/flask/cli.py:ScriptInfo.load_app:333:623",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600:637",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:639",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:645",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:symbol:src/flask/cli.py:ScriptInfo.load_app:333:645",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.make_context:657:symbol:src/flask/cli.py:FlaskGroup.make_context:657:676",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.make_context:657:symbol:src/flask/cli.py:ScriptInfo:293:670",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.parse_args:678:symbol:src/flask/cli.py:FlaskGroup.parse_args:678:688",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:ScriptInfo.load_app:333:symbol:src/flask/cli.py:NoAppException:37:359",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:ScriptInfo.load_app:333:symbol:src/flask/cli.py:prepare_import:200:348",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:ScriptInfo.load_app:333:symbol:src/flask/cli.py:prepare_import:200:352",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:_env_file_callback:493:symbol:src/flask/cli.py:load_dotenv:698:510",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:131",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:142",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:159",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:163",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:170",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:183",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:194",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:_called_with_wrong_args:94:180",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:find_best_app:41:symbol:src/flask/cli.py:NoAppException:37:60",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:find_best_app:41:symbol:src/flask/cli.py:NoAppException:37:80",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:find_best_app:41:symbol:src/flask/cli.py:NoAppException:37:87",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:find_best_app:41:symbol:src/flask/cli.py:_called_with_wrong_args:94:77",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:main:1122:symbol:src/flask/cli.py:main:1122:1123",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:routes_command:1061:symbol:src/flask/cli.py:AppGroup.command:413:1048",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:AppGroup.command:413:882",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:CertParamType:780:887",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:ScriptInfo.load_app:333:955",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:SeparatedPathType:867:918",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:SeparatedPathType:867:927",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:show_server_banner:766:981",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:shell_command:1001:symbol:src/flask/cli.py:AppGroup.command:413:999",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/cli.py:with_appcontext:380:symbol:src/flask/cli.py:ScriptInfo.load_app:333:397",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/ctx.py:AppContext.__enter__:506:symbol:src/flask/ctx.py:AppContext.push:416:507",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/ctx.py:AppContext.push:416:symbol:src/flask/ctx.py:AppContext._get_session:381:439",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/ctx.py:AppContext.push:416:symbol:src/flask/ctx.py:AppContext.match_request:405:444",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/ctx.py:AppContext.session:396:symbol:src/flask/ctx.py:AppContext._get_session:381:401",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:77",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93:symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93:103",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/ctx.py:after_this_request:118:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:139",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/ctx.py:copy_current_request_context:154:symbol:src/flask/ctx.py:AppContext.copy:355:200",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/ctx.py:copy_current_request_context:154:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:192",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/ctx.py:has_app_context:235:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:257",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:src/flask/ctx.py:has_request_context:209:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:232",
      "suggested_actions": []
    }
  ],
  "per_node_confidence": [
    {
      "confidence": 0.85,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 41,
        "fan_out_z_score": 0.581,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:src/flask/app.py",
      "suggested_actions": [
        {
          "args": {
            "depth": 2,
            "node_id": "module:src/flask/app.py"
          },
          "rationale": "12 outgoing edge(s) point to nodes outside this projection; dependency closure is incomplete",
          "tool": "resolve_dependency"
        },
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.85,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 42,
        "fan_out_z_score": 0.609,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:src/flask/cli.py",
      "suggested_actions": [
        {
          "args": {
            "depth": 2,
            "node_id": "module:src/flask/cli.py"
          },
          "rationale": "18 outgoing edge(s) point to nodes outside this projection; dependency closure is incomplete",
          "tool": "resolve_dependency"
        },
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.85,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 30,
        "fan_out_z_score": 0.282,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:src/flask/ctx.py",
      "suggested_actions": [
        {
          "args": {
            "depth": 2,
            "node_id": "module:src/flask/ctx.py"
          },
          "rationale": "18 outgoing edge(s) point to nodes outside this projection; dependency closure is incomplete",
          "tool": "resolve_dependency"
        },
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/ctx.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.__call__:1618",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 2,
        "fan_out_z_score": 1.594,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.__init__:310",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 2,
        "fan_out_z_score": 1.594,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.__init_subclass__:254",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.358,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.async_to_sync:1079",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.358,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.create_url_adapter:509",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.57,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 3,
        "fan_out_z_score": 2.57,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.dispatch_request:966",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.do_teardown_appcontext:1453",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.do_teardown_request:1420",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 2,
        "fan_out_z_score": 1.594,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.finalize_request:1021",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.57,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 4,
        "fan_out_z_score": 3.546,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.full_dispatch_request:992",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.358,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.get_send_file_max_age:365",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.57,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 3,
        "fan_out_z_score": 2.57,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.handle_exception:897",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.handle_http_exception:830",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 2,
        "fan_out_z_score": 1.594,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.handle_user_exception:865",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.358,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.log_exception:950",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.358,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.make_default_options_response:1053",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.358,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.make_response:1224",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.preprocess_request:1366",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 2,
        "fan_out_z_score": 1.594,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.process_response:1394",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.358,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.raise_routing_exception:562",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.358,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.request_context:1501",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.send_static_file:392",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.test_request_context:1517",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.update_template_context:590",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.url_for:1102",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.57,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 3,
        "fan_out_z_score": 2.57,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:Flask.wsgi_app:1566",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.358,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:add_ctx:97",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.358,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/app.py:remove_ctx:85",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/app.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 2,
        "fan_out_z_score": 1.594,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:AppGroup.command:413",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:AppGroup.group:429",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:CertParamType:780",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.358,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.57,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 4,
        "fan_out_z_score": 3.546,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:FlaskGroup.get_command:609",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.57,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 4,
        "fan_out_z_score": 3.546,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 2,
        "fan_out_z_score": 1.594,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:FlaskGroup.make_context:657",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:FlaskGroup.parse_args:678",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:NoAppException:37",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.57,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 3,
        "fan_out_z_score": 2.57,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:ScriptInfo.load_app:333",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:ScriptInfo:293",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:SeparatedPathType:867",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.358,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:_called_with_wrong_args:94",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:_env_file_callback:493",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.57,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 8,
        "fan_out_z_score": 7.451,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:find_app_by_string:120",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.57,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 4,
        "fan_out_z_score": 3.546,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:find_best_app:41",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.358,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:load_dotenv:698",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:main:1122",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.358,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:prepare_import:200",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:routes_command:1061",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.57,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 6,
        "fan_out_z_score": 5.499,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:run_command:935",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:shell_command:1001",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.358,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:show_server_banner:766",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/cli.py:with_appcontext:380",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/cli.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/ctx.py:AppContext.__enter__:506",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/ctx.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.358,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/ctx.py:AppContext._get_session:381",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/ctx.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.358,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/ctx.py:AppContext.copy:355",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/ctx.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.358,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/ctx.py:AppContext.match_request:405",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/ctx.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 2,
        "fan_out_z_score": 1.594,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/ctx.py:AppContext.push:416",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/ctx.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/ctx.py:AppContext.session:396",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/ctx.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/ctx.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/ctx.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/ctx.py:after_this_request:118",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/ctx.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 2,
        "fan_out_z_score": 1.594,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/ctx.py:copy_current_request_context:154",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/ctx.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/ctx.py:has_app_context:235",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/ctx.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.036,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 0.618,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:src/flask/ctx.py:has_request_context:209",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "src/flask/ctx.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    }
  ],
  "threshold": 0.9,
  "tool_call_budget": 15
}

## Projection Stats
{
  "graph_edge_count": 2163,
  "graph_node_count": 1712,
  "initial_seed_count": 20,
  "projected_edge_count": 84,
  "projected_node_count": 68,
  "seed_count": 42
}

## Projected Nodes
[
  {
    "confidence": 1.0,
    "node_id": "module:src/flask/app.py",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "Module-level semantic container",
      "symbol_name": "src/flask/app.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 65423,
      "byte_start": 0,
      "content_hash": "09a3a1a7b3d1f174a4d274da2c329f9377745bbf6f138b17c3187352f7466a15",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 1.0,
    "node_id": "module:src/flask/cli.py",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "Module-level semantic container",
      "symbol_name": "src/flask/cli.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 36808,
      "byte_start": 0,
      "content_hash": "1f2e6624f5a34c86eb0e1928c6acb6b85297b19be0e039791bf0c065d2b2b7af",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 1.0,
    "node_id": "module:src/flask/ctx.py",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "Module-level semantic container",
      "symbol_name": "src/flask/ctx.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 18104,
      "byte_start": 0,
      "content_hash": "fdff186ec6f47fa5a15fe5947c843bbd2ee20ab0be34036ea8dedaaa89c58f9f",
      "file_path": "src/flask/ctx.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.__call__:1618",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.wsgi_app:1566"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function __call__",
      "symbol_name": "__call__",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.__call__",
      "byte_end": 65422,
      "byte_start": 65068,
      "content_hash": "16b710f47ea72347274ceccb21649a5a4ce7b9a941c1d69f39a6109c157cec97",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.__init__:310",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.__init__:310"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.__init__:310"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.send_static_file:392"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function __init__",
      "symbol_name": "__init__",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.__init__",
      "byte_end": 15001,
      "byte_start": 12632,
      "content_hash": "57da7ea2afea8f19b08c324002385c3be9baf0c6407c163a9e8049ec5a9c849b",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.__init_subclass__:254",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:add_ctx:97"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:remove_ctx:85"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function __init_subclass__",
      "symbol_name": "__init_subclass__",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.__init_subclass__",
      "byte_end": 12626,
      "byte_start": 10298,
      "content_hash": "3b2870215f971ca43d2861a3add34b60453e15b3bc67e6dfd92c08468e07e45b",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.async_to_sync:1079",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function async_to_sync",
      "symbol_name": "async_to_sync",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.async_to_sync",
      "byte_end": 44006,
      "byte_start": 43264,
      "content_hash": "84cc58adce4ab6990926b0445c184ef72fce3510204e177b41ccedb54327dedd",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.create_url_adapter:509",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.url_for:1102"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function create_url_adapter",
      "symbol_name": "create_url_adapter",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.create_url_adapter",
      "byte_end": 22649,
      "byte_start": 20375,
      "content_hash": "326d82d2151f3a5db94d71701a097b93b1d963ff195012f28cc5d5aff7af34f3",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.dispatch_request:966",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.full_dispatch_request:992"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.make_default_options_response:1053"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.raise_routing_exception:562"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function dispatch_request",
      "symbol_name": "dispatch_request",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.dispatch_request",
      "byte_end": 39969,
      "byte_start": 38725,
      "content_hash": "f9c7ebf70a162afaa3e706b8d4162e9ff9869b62736df8d163e83a5a97c1ba09",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.do_teardown_appcontext:1453",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function do_teardown_appcontext",
      "symbol_name": "do_teardown_appcontext",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.do_teardown_appcontext",
      "byte_end": 59703,
      "byte_start": 58699,
      "content_hash": "3c740347ee3ada59e3e126a5b9beaaaf97d94d1de8659072b69064bfd2c290e2",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.do_teardown_request:1420",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function do_teardown_request",
      "symbol_name": "do_teardown_request",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.do_teardown_request",
      "byte_end": 58693,
      "byte_start": 57361,
      "content_hash": "041737b4aa090af7eab203e32f8e5fea50ecb08f85041dd094e4f55928e97951",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.dispatch_request:966"
        },
        {
          "source": "symbol:src/flask/app.py:Flask.do_teardown_appcontext:1453"
        },
        {
          "source": "symbol:src/flask/app.py:Flask.do_teardown_request:1420"
        },
        {
          "source": "symbol:src/flask/app.py:Flask.handle_exception:897"
        },
        {
          "source": "symbol:src/flask/app.py:Flask.handle_http_exception:830"
        },
        {
          "source": "symbol:src/flask/app.py:Flask.handle_user_exception:865"
        },
        {
          "source": "symbol:src/flask/app.py:Flask.preprocess_request:1366"
        },
        {
          "source": "symbol:src/flask/app.py:Flask.process_response:1394"
        },
        {
          "source": "symbol:src/flask/app.py:Flask.update_template_context:590"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.async_to_sync:1079"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function ensure_sync",
      "symbol_name": "ensure_sync",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.ensure_sync",
      "byte_end": 43258,
      "byte_start": 42765,
      "content_hash": "6b2a9bda8dd8e46b5098a7f3d631a7cfeda476f534749cb1101e21b18705a1ae",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.finalize_request:1021",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.full_dispatch_request:992"
        },
        {
          "source": "symbol:src/flask/app.py:Flask.handle_exception:897"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.make_response:1224"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.process_response:1394"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function finalize_request",
      "symbol_name": "finalize_request",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.finalize_request",
      "byte_end": 42285,
      "byte_start": 41065,
      "content_hash": "7a66de46aa56116313f6ecb33949c6c7b43a88eec316c09a9a052b2cb946c9ca",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.full_dispatch_request:992",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.wsgi_app:1566"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.dispatch_request:966"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.finalize_request:1021"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.handle_user_exception:865"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.preprocess_request:1366"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function full_dispatch_request",
      "symbol_name": "full_dispatch_request",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.full_dispatch_request",
      "byte_end": 41059,
      "byte_start": 40006,
      "content_hash": "8e19522cc1da2b297a32103626a277c3fc185dcd358b57b6df698d2caf911b62",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.get_send_file_max_age:365",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.send_static_file:392"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function get_send_file_max_age",
      "symbol_name": "get_send_file_max_age",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.get_send_file_max_age",
      "byte_end": 15930,
      "byte_start": 15007,
      "content_hash": "01c9df7cbf2b57c53a553c81d0eebfc02ea31dd964b0ddb5e21178af8b70ed59",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.handle_exception:897",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.wsgi_app:1566"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.finalize_request:1021"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.log_exception:950"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function handle_exception",
      "symbol_name": "handle_exception",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.handle_exception",
      "byte_end": 38144,
      "byte_start": 35936,
      "content_hash": "94fa1a557d158357fa24901a30ed508910248cbd59a954626e771aa0c02f4b6b",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.handle_http_exception:830",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.handle_user_exception:865"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function handle_http_exception",
      "symbol_name": "handle_http_exception",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.handle_http_exception",
      "byte_end": 34696,
      "byte_start": 33366,
      "content_hash": "54f2cc1a7277891f9984d463c16bda67f3a49ccdd57ec93838af07a21370ddd5",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.handle_user_exception:865",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.full_dispatch_request:992"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.handle_http_exception:830"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function handle_user_exception",
      "symbol_name": "handle_user_exception",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.handle_user_exception",
      "byte_end": 35899,
      "byte_start": 34733,
      "content_hash": "65f0f36c19963deafce37ba086efdf0079617dbcc34a99773cb839e4f2a3f42c",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.log_exception:950",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.handle_exception:897"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function log_exception",
      "symbol_name": "log_exception",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.log_exception",
      "byte_end": 38719,
      "byte_start": 38150,
      "content_hash": "5c6d1f2f1c4c9778085f6ed59c1feba42b243771987ea7552ad00c4aff079b15",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.make_default_options_response:1053",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.dispatch_request:966"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function make_default_options_response",
      "symbol_name": "make_default_options_response",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.make_default_options_response",
      "byte_end": 42759,
      "byte_start": 42291,
      "content_hash": "8a2f74eb652357b7559bdbb7f084cc51905249d5b85e3e9d9198b941e35d972c",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.make_response:1224",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.finalize_request:1021"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function make_response",
      "symbol_name": "make_response",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.make_response",
      "byte_end": 55019,
      "byte_start": 49141,
      "content_hash": "0d06b529b46e02f98ab2983ee4c22e3ec5ad669894e21669c941ba539f4a86d5",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.preprocess_request:1366",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.full_dispatch_request:992"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function preprocess_request",
      "symbol_name": "preprocess_request",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.preprocess_request",
      "byte_end": 56181,
      "byte_start": 55025,
      "content_hash": "e8241727e4adceb04aa62dcb3ba158f8fcade2feeb35cf6de5cfa4c2cab2867d",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.process_response:1394",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.finalize_request:1021"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function process_response",
      "symbol_name": "process_response",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.process_response",
      "byte_end": 57355,
      "byte_start": 56187,
      "content_hash": "01df3451a006199a5f04d18eab36b8bca8732d704c72fa60153e37a928bdb205",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.raise_routing_exception:562",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.dispatch_request:966"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function raise_routing_exception",
      "symbol_name": "raise_routing_exception",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.raise_routing_exception",
      "byte_end": 23625,
      "byte_start": 22655,
      "content_hash": "295ced4ad7dbf6e1f2e2ea95eebe4e5ab8d210f48fca8c2df8e994083551724e",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.request_context:1501",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.test_request_context:1517"
        },
        {
          "source": "symbol:src/flask/app.py:Flask.wsgi_app:1566"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function request_context",
      "symbol_name": "request_context",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.request_context",
      "byte_end": 61083,
      "byte_start": 60344,
      "content_hash": "d233642d6405c7af5388bff1ffaeef51efc5feba7d33df39011b66e753588748",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.send_static_file:392",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.__init__:310"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.get_send_file_max_age:365"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function send_static_file",
      "symbol_name": "send_static_file",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.send_static_file",
      "byte_end": 16782,
      "byte_start": 15967,
      "content_hash": "27d2683e2746c869cb91807722d38ff946b71fa05f1a5f77b3bb6267d77abb71",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.test_request_context:1517",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.request_context:1501"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function test_request_context",
      "symbol_name": "test_request_context",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.test_request_context",
      "byte_end": 63177,
      "byte_start": 61089,
      "content_hash": "01b99fd691fc355b938491b41a842566d73cfbe0d595bf74ca24097081c3a556",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.update_template_context:590",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function update_template_context",
      "symbol_name": "update_template_context",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.update_template_context",
      "byte_end": 24895,
      "byte_start": 23631,
      "content_hash": "9605416d8b7e0803328f2aec29c5e5e0964d3eb5c6e6325a767176ee0456d857",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.url_for:1102",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.create_url_adapter:509"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function url_for",
      "symbol_name": "url_for",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.url_for",
      "byte_end": 49135,
      "byte_start": 44012,
      "content_hash": "b476a0dec4c79242e60a8469e83a4cb44b4645c44efe3fd67672d4284fe3239b",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:Flask.wsgi_app:1566",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.__call__:1618"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.full_dispatch_request:992"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.handle_exception:897"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.request_context:1501"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function wsgi_app",
      "symbol_name": "wsgi_app",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:Flask.wsgi_app",
      "byte_end": 65062,
      "byte_start": 63183,
      "content_hash": "efd78a36ec1d79465da93b82553ebef531fd2c598cdd1231b32ebc959f3463e9",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:add_ctx:97",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.__init_subclass__:254"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function add_ctx",
      "symbol_name": "add_ctx",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:add_ctx",
      "byte_end": 3575,
      "byte_start": 3221,
      "content_hash": "6d3df893048dde40a2e8d8ecda5c256d98b3f17c369b01fa7dffafe617fdc8ec",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/app.py:remove_ctx:85",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.__init_subclass__:254"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function remove_ctx",
      "symbol_name": "remove_ctx",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:remove_ctx",
      "byte_end": 3075,
      "byte_start": 2818,
      "content_hash": "5c58ac17b76b3fb185090bf51555c9b39cbb0342f9bf535151347fe2f1826071",
      "file_path": "src/flask/app.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:AppGroup.command:413",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:AppGroup.command:413"
        },
        {
          "source": "symbol:src/flask/cli.py:routes_command:1061"
        },
        {
          "source": "symbol:src/flask/cli.py:run_command:935"
        },
        {
          "source": "symbol:src/flask/cli.py:shell_command:1001"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:AppGroup.command:413"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:with_appcontext:380"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function command",
      "symbol_name": "command",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:AppGroup.command",
      "byte_end": 13759,
      "byte_start": 13060,
      "content_hash": "7cbc7fe2247437eb5981de5bc005d1176e0e2c707a67cff4b2d3fb18f6c1a623",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:AppGroup.group:429",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:AppGroup.group:429"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:AppGroup.group:429"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function group",
      "symbol_name": "group",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:AppGroup.group",
      "byte_end": 14173,
      "byte_start": 13765,
      "content_hash": "56dfb90977bf75433236c3ba6b505a74d878e1c9585b2b5bec395a7e9b514a2d",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:CertParamType:780",
    "node_type": "class",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:run_command:935"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "class CertParamType",
      "symbol_name": "CertParamType",
      "symbol_type": "class",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "class:CertParamType",
      "byte_end": 27959,
      "byte_start": 26527,
      "content_hash": "5a97b025ef493def3d3226a4bb2f57c50062059830724a3b0f77a82a5bc09db0",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:FlaskGroup.get_command:609"
        },
        {
          "source": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _load_plugin_commands",
      "symbol_name": "_load_plugin_commands",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:FlaskGroup._load_plugin_commands",
      "byte_end": 20281,
      "byte_start": 20011,
      "content_hash": "e1a57664073884e8cf7c5c0237ee175695451f125ceaa7b6229d0e0daa044b68",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:FlaskGroup.get_command:609",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:FlaskGroup.get_command:609"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:FlaskGroup.get_command:609"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:ScriptInfo.load_app:333"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function get_command",
      "symbol_name": "get_command",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:FlaskGroup.get_command",
      "byte_end": 21344,
      "byte_start": 20287,
      "content_hash": "cfb4a2ed09a26b0a2b396dbc38117a618b47e6e26c2df25943bf4098c40e42d4",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:ScriptInfo.load_app:333"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function list_commands",
      "symbol_name": "list_commands",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:FlaskGroup.list_commands",
      "byte_end": 22230,
      "byte_start": 21350,
      "content_hash": "db7aa35213f300bcbd95996c0762822d243516cc3715c21cd85a2dbe8f8a6b06",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:FlaskGroup.make_context:657",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:FlaskGroup.make_context:657"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:FlaskGroup.make_context:657"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:ScriptInfo:293"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function make_context",
      "symbol_name": "make_context",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:FlaskGroup.make_context",
      "byte_end": 23032,
      "byte_start": 22236,
      "content_hash": "d5fd541910368dc55fd8ad4dc200c23d2768876ebc1988b2a1ec121e23e2fd56",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:FlaskGroup.parse_args:678",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:FlaskGroup.parse_args:678"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:FlaskGroup.parse_args:678"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function parse_args",
      "symbol_name": "parse_args",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:FlaskGroup.parse_args",
      "byte_end": 23595,
      "byte_start": 23038,
      "content_hash": "d6cefdc254f2eedcbf1b83d1708a912a67f3fe16092180cb1683cd729b27da8c",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:NoAppException:37",
    "node_type": "class",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:ScriptInfo.load_app:333"
        },
        {
          "source": "symbol:src/flask/cli.py:find_app_by_string:120"
        },
        {
          "source": "symbol:src/flask/cli.py:find_best_app:41"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "class NoAppException",
      "symbol_name": "NoAppException",
      "symbol_type": "class",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "class:NoAppException",
      "byte_end": 894,
      "byte_start": 793,
      "content_hash": "9e968dd91274d585a76dc0e384e22c73915368b63eb1b58c2d5b72290ac35a19",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:ScriptInfo.load_app:333",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:FlaskGroup.get_command:609"
        },
        {
          "source": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636"
        },
        {
          "source": "symbol:src/flask/cli.py:run_command:935"
        },
        {
          "source": "symbol:src/flask/cli.py:with_appcontext:380"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:NoAppException:37"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:prepare_import:200"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function load_app",
      "symbol_name": "load_app",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:ScriptInfo.load_app",
      "byte_end": 11724,
      "byte_start": 10203,
      "content_hash": "fcc5e00092c0dcfde838fbfd79d5492ad1ce3415cd57f8c8c088308d920dffb6",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:ScriptInfo:293",
    "node_type": "class",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:FlaskGroup.make_context:657"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "class ScriptInfo",
      "symbol_name": "ScriptInfo",
      "symbol_type": "class",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "class:ScriptInfo",
      "byte_end": 11724,
      "byte_start": 8628,
      "content_hash": "592901e1d1006934831a264b7b30b61fb9fc1075d47bb685d40e4ef31e911431",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:SeparatedPathType:867",
    "node_type": "class",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:run_command:935"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "class SeparatedPathType",
      "symbol_name": "SeparatedPathType",
      "symbol_type": "class",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "class:SeparatedPathType",
      "byte_end": 29677,
      "byte_start": 29098,
      "content_hash": "4e7c63eca412e2011eb711ff409e2fd4fe283745f8dab01fd8475913b13cfe7c",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:_called_with_wrong_args:94",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:find_app_by_string:120"
        },
        {
          "source": "symbol:src/flask/cli.py:find_best_app:41"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _called_with_wrong_args",
      "symbol_name": "_called_with_wrong_args",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:_called_with_wrong_args",
      "byte_end": 3426,
      "byte_start": 2679,
      "content_hash": "5152c1adb4a87c355e684d73ccffa080ae06f81d67a6749406bddc65dae81c69",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:_env_file_callback:493",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:load_dotenv:698"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _env_file_callback",
      "symbol_name": "_env_file_callback",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:_env_file_callback",
      "byte_end": 16666,
      "byte_start": 15909,
      "content_hash": "ae6497dbece96def68c74d214584647fbd8ea5506ecca1e520ae0b70cf0e75a5",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:find_app_by_string:120",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:NoAppException:37"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:_called_with_wrong_args:94"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function find_app_by_string",
      "symbol_name": "find_app_by_string",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:find_app_by_string",
      "byte_end": 6072,
      "byte_start": 3429,
      "content_hash": "9bac2537de80d6198f90f5cb0db6004ffe1eb5ee047b1194b8b8e925bb41620b",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:find_best_app:41",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:NoAppException:37"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:_called_with_wrong_args:94"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function find_best_app",
      "symbol_name": "find_best_app",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:find_best_app",
      "byte_end": 2676,
      "byte_start": 897,
      "content_hash": "31e4877b92dac2e4b30a01ac6de6b33aa9ac352b31f4f3020ce80f924a4f49b2",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:load_dotenv:698",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:_env_file_callback:493"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function load_dotenv",
      "symbol_name": "load_dotenv",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:load_dotenv",
      "byte_end": 26057,
      "byte_start": 23897,
      "content_hash": "2a267c0f6aafc25803425e9ae8180528f049b3052338b96d3aca2680293a7937",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:main:1122",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:main:1122"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:main:1122"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function main",
      "symbol_name": "main",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:main",
      "byte_end": 36767,
      "byte_start": 36733,
      "content_hash": "3ce7e69224f9911d2368576d8d2636e55191585be61b570379a866d7eb8052c7",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:prepare_import:200",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:ScriptInfo.load_app:333"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function prepare_import",
      "symbol_name": "prepare_import",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:prepare_import",
      "byte_end": 6833,
      "byte_start": 6075,
      "content_hash": "6f782cd47ba837652c22c7821a8ed94633d643c42a6d1e73afcfdbe528810040",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:routes_command:1061",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:AppGroup.command:413"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function routes_command",
      "symbol_name": "routes_command",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:routes_command",
      "byte_end": 36462,
      "byte_start": 35041,
      "content_hash": "de54c495f02d2082084e70b33ad58590157df474c65053fbcd2d33db2f21cb33",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:run_command:935",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:AppGroup.command:413"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:CertParamType:780"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:ScriptInfo.load_app:333"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:SeparatedPathType:867"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:show_server_banner:766"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function run_command",
      "symbol_name": "run_command",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:run_command",
      "byte_end": 32873,
      "byte_start": 31221,
      "content_hash": "274ef091406ad22f695821c2424adb1a05b3230349a4c26d2bf2426e32db69ee",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:shell_command:1001",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:AppGroup.command:413"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function shell_command",
      "symbol_name": "shell_command",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:shell_command",
      "byte_end": 34586,
      "byte_start": 33009,
      "content_hash": "38fdf9991c96e369786c2b407f792344c23c3deb4920db80d4b857076589df8d",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:show_server_banner:766",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:run_command:935"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function show_server_banner",
      "symbol_name": "show_server_banner",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:show_server_banner",
      "byte_end": 26524,
      "byte_start": 26104,
      "content_hash": "4cacbd42a7d6bb09208e5d498b4413f2ea05e91a570f49c7a05bb2824babb7f2",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/cli.py:with_appcontext:380",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:AppGroup.command:413"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:ScriptInfo.load_app:333"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function with_appcontext",
      "symbol_name": "with_appcontext",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:with_appcontext",
      "byte_end": 12726,
      "byte_start": 11849,
      "content_hash": "295814aff7ae90b368a4bfe6751cfa9eb672f4d6edd3e32e39da31b5cd858052",
      "file_path": "src/flask/cli.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/ctx.py:AppContext.__enter__:506",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/ctx.py:AppContext.push:416"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function __enter__",
      "symbol_name": "__enter__",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:AppContext.__enter__",
      "byte_end": 17212,
      "byte_start": 17141,
      "content_hash": "49d6e2603d322097fb8af9c91208bb12a9cb537500d3ed7e1510aae36fb00050",
      "file_path": "src/flask/ctx.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/ctx.py:AppContext._get_session:381",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/ctx.py:AppContext.push:416"
        },
        {
          "source": "symbol:src/flask/ctx.py:AppContext.session:396"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _get_session",
      "symbol_name": "_get_session",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:AppContext._get_session",
      "byte_end": 12986,
      "byte_start": 12480,
      "content_hash": "c7002c97308535374aae1e0a5498d7487ec697c65c3313c915895f1be8e8a8af",
      "file_path": "src/flask/ctx.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/ctx.py:AppContext.copy:355",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/ctx.py:copy_current_request_context:154"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function copy",
      "symbol_name": "copy",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:AppContext.copy",
      "byte_end": 12093,
      "byte_start": 11645,
      "content_hash": "567f7d1eba70f4f7ded882364729684643188fed01d229fa7ce27101de211eec",
      "file_path": "src/flask/ctx.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/ctx.py:AppContext.match_request:405",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/ctx.py:AppContext.push:416"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function match_request",
      "symbol_name": "match_request",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:AppContext.match_request",
      "byte_end": 13856,
      "byte_start": 13388,
      "content_hash": "30a3e8e2b7c2766b5f4a4905aa8b3b578b81ff809b295943a096e0091092127e",
      "file_path": "src/flask/ctx.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/ctx.py:AppContext.push:416",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/ctx.py:AppContext.__enter__:506"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/ctx.py:AppContext._get_session:381"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/ctx.py:AppContext.match_request:405"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function push",
      "symbol_name": "push",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:AppContext.push",
      "byte_end": 15072,
      "byte_start": 13890,
      "content_hash": "baea61546581cd071253f636eab7755bb187517fc7ef18792714d8ff15c99ceb",
      "file_path": "src/flask/ctx.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/ctx.py:AppContext.session:396",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/ctx.py:AppContext._get_session:381"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function session",
      "symbol_name": "session",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:AppContext.session",
      "byte_end": 13382,
      "byte_start": 13006,
      "content_hash": "590089f091d3708bc6500e680c2a3c5f5d9f23d40cd1afc1d06956bf353bd989",
      "file_path": "src/flask/ctx.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68"
        },
        {
          "source": "symbol:src/flask/ctx.py:after_this_request:118"
        },
        {
          "source": "symbol:src/flask/ctx.py:copy_current_request_context:154"
        },
        {
          "source": "symbol:src/flask/ctx.py:has_app_context:235"
        },
        {
          "source": "symbol:src/flask/ctx.py:has_request_context:209"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function get",
      "symbol_name": "get",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:_AppCtxGlobals.get",
      "byte_end": 2066,
      "byte_start": 1701,
      "content_hash": "4cf395aed2615680e0cf616b5c5c1c824db38fd29a94ac5e59ed38cb723e5da8",
      "file_path": "src/flask/ctx.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function setdefault",
      "symbol_name": "setdefault",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:_AppCtxGlobals.setdefault",
      "byte_end": 3008,
      "byte_start": 2565,
      "content_hash": "a1b558471d75d55bc52218b7f969c7e3837f8dd415293c498a5fb423acdc8cc1",
      "file_path": "src/flask/ctx.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/ctx.py:after_this_request:118",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function after_this_request",
      "symbol_name": "after_this_request",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:after_this_request",
      "byte_end": 4338,
      "byte_start": 3356,
      "content_hash": "590fe62a7a96a19cbee51dd4bca788f3af64e20de69d6ead3cabd6a43c949c81",
      "file_path": "src/flask/ctx.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/ctx.py:copy_current_request_context:154",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/ctx.py:AppContext.copy:355"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function copy_current_request_context",
      "symbol_name": "copy_current_request_context",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:copy_current_request_context",
      "byte_end": 6364,
      "byte_start": 4392,
      "content_hash": "9504136be71c1a8e4bb30c06be7dac93ce3e790126eeba4b8142319bbe08e413",
      "file_path": "src/flask/ctx.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/ctx.py:has_app_context:235",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function has_app_context",
      "symbol_name": "has_app_context",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:has_app_context",
      "byte_end": 7823,
      "byte_start": 7138,
      "content_hash": "5da5ef672c2c455b670186d0805938dfb0fca798aba4a35efe3d992b4455a99a",
      "file_path": "src/flask/ctx.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:src/flask/ctx.py:has_request_context:209",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function has_request_context",
      "symbol_name": "has_request_context",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:has_request_context",
      "byte_end": 7135,
      "byte_start": 6397,
      "content_hash": "888098922a159d358f8b355821b2f8786bb1d134f4257b8c69d8ca11b4296d02",
      "file_path": "src/flask/ctx.py"
    }
  }
]

## Projected Edges
[
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.__call__:1618:symbol:src/flask/app.py:Flask.wsgi_app:1566:1625",
    "edge_type": "calls",
    "evidence": {
      "line": 1625,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.__call__:1618",
    "to_node": "symbol:src/flask/app.py:Flask.wsgi_app:1566"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.__init__:310:symbol:src/flask/app.py:Flask.__init__:310:323",
    "edge_type": "calls",
    "evidence": {
      "line": 323,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.__init__:310",
    "to_node": "symbol:src/flask/app.py:Flask.__init__:310"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.__init__:310:symbol:src/flask/app.py:Flask.send_static_file:392:362",
    "edge_type": "calls",
    "evidence": {
      "line": 362,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.__init__:310",
    "to_node": "symbol:src/flask/app.py:Flask.send_static_file:392"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.__init_subclass__:254:symbol:src/flask/app.py:add_ctx:97:308",
    "edge_type": "calls",
    "evidence": {
      "line": 308,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.__init_subclass__:254",
    "to_node": "symbol:src/flask/app.py:add_ctx:97"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.__init_subclass__:254:symbol:src/flask/app.py:remove_ctx:85:307",
    "edge_type": "calls",
    "evidence": {
      "line": 307,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.__init_subclass__:254",
    "to_node": "symbol:src/flask/app.py:remove_ctx:85"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.dispatch_request:966:symbol:src/flask/app.py:Flask.ensure_sync:1065:990",
    "edge_type": "calls",
    "evidence": {
      "line": 990,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.dispatch_request:966",
    "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.dispatch_request:966:symbol:src/flask/app.py:Flask.make_default_options_response:1053:987",
    "edge_type": "calls",
    "evidence": {
      "line": 987,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.dispatch_request:966",
    "to_node": "symbol:src/flask/app.py:Flask.make_default_options_response:1053"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.dispatch_request:966:symbol:src/flask/app.py:Flask.raise_routing_exception:562:979",
    "edge_type": "calls",
    "evidence": {
      "line": 979,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.dispatch_request:966",
    "to_node": "symbol:src/flask/app.py:Flask.raise_routing_exception:562"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.do_teardown_appcontext:1453:symbol:src/flask/app.py:Flask.ensure_sync:1065:1474",
    "edge_type": "calls",
    "evidence": {
      "line": 1474,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.do_teardown_appcontext:1453",
    "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.do_teardown_request:1420:symbol:src/flask/app.py:Flask.ensure_sync:1065:1446",
    "edge_type": "calls",
    "evidence": {
      "line": 1446,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.do_teardown_request:1420",
    "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.ensure_sync:1065:symbol:src/flask/app.py:Flask.async_to_sync:1079:1075",
    "edge_type": "calls",
    "evidence": {
      "line": 1075,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
    "to_node": "symbol:src/flask/app.py:Flask.async_to_sync:1079"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.finalize_request:1021:symbol:src/flask/app.py:Flask.make_response:1224:1039",
    "edge_type": "calls",
    "evidence": {
      "line": 1039,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.finalize_request:1021",
    "to_node": "symbol:src/flask/app.py:Flask.make_response:1224"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.finalize_request:1021:symbol:src/flask/app.py:Flask.process_response:1394:1041",
    "edge_type": "calls",
    "evidence": {
      "line": 1041,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.finalize_request:1021",
    "to_node": "symbol:src/flask/app.py:Flask.process_response:1394"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.full_dispatch_request:992:symbol:src/flask/app.py:Flask.dispatch_request:966:1016",
    "edge_type": "calls",
    "evidence": {
      "line": 1016,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.full_dispatch_request:992",
    "to_node": "symbol:src/flask/app.py:Flask.dispatch_request:966"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.full_dispatch_request:992:symbol:src/flask/app.py:Flask.finalize_request:1021:1019",
    "edge_type": "calls",
    "evidence": {
      "line": 1019,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.full_dispatch_request:992",
    "to_node": "symbol:src/flask/app.py:Flask.finalize_request:1021"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.full_dispatch_request:992:symbol:src/flask/app.py:Flask.handle_user_exception:865:1018",
    "edge_type": "calls",
    "evidence": {
      "line": 1018,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.full_dispatch_request:992",
    "to_node": "symbol:src/flask/app.py:Flask.handle_user_exception:865"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.full_dispatch_request:992:symbol:src/flask/app.py:Flask.preprocess_request:1366:1014",
    "edge_type": "calls",
    "evidence": {
      "line": 1014,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.full_dispatch_request:992",
    "to_node": "symbol:src/flask/app.py:Flask.preprocess_request:1366"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_exception:897:symbol:src/flask/app.py:Flask.ensure_sync:1065:946",
    "edge_type": "calls",
    "evidence": {
      "line": 946,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.handle_exception:897",
    "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_exception:897:symbol:src/flask/app.py:Flask.finalize_request:1021:948",
    "edge_type": "calls",
    "evidence": {
      "line": 948,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.handle_exception:897",
    "to_node": "symbol:src/flask/app.py:Flask.finalize_request:1021"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_exception:897:symbol:src/flask/app.py:Flask.log_exception:950:940",
    "edge_type": "calls",
    "evidence": {
      "line": 940,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.handle_exception:897",
    "to_node": "symbol:src/flask/app.py:Flask.log_exception:950"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_http_exception:830:symbol:src/flask/app.py:Flask.ensure_sync:1065:863",
    "edge_type": "calls",
    "evidence": {
      "line": 863,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.handle_http_exception:830",
    "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_user_exception:865:symbol:src/flask/app.py:Flask.ensure_sync:1065:895",
    "edge_type": "calls",
    "evidence": {
      "line": 895,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.handle_user_exception:865",
    "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_user_exception:865:symbol:src/flask/app.py:Flask.handle_http_exception:830:888",
    "edge_type": "calls",
    "evidence": {
      "line": 888,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.handle_user_exception:865",
    "to_node": "symbol:src/flask/app.py:Flask.handle_http_exception:830"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.preprocess_request:1366:symbol:src/flask/app.py:Flask.ensure_sync:1065:1387",
    "edge_type": "calls",
    "evidence": {
      "line": 1387,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.preprocess_request:1366",
    "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.process_response:1394:symbol:src/flask/app.py:Flask.ensure_sync:1065:1408",
    "edge_type": "calls",
    "evidence": {
      "line": 1408,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.process_response:1394",
    "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.process_response:1394:symbol:src/flask/app.py:Flask.ensure_sync:1065:1413",
    "edge_type": "calls",
    "evidence": {
      "line": 1413,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.process_response:1394",
    "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.send_static_file:392:symbol:src/flask/app.py:Flask.get_send_file_max_age:365:409",
    "edge_type": "calls",
    "evidence": {
      "line": 409,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.send_static_file:392",
    "to_node": "symbol:src/flask/app.py:Flask.get_send_file_max_age:365"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.test_request_context:1517:symbol:src/flask/app.py:Flask.request_context:1501:1564",
    "edge_type": "calls",
    "evidence": {
      "line": 1564,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.test_request_context:1517",
    "to_node": "symbol:src/flask/app.py:Flask.request_context:1501"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.update_template_context:590:symbol:src/flask/app.py:Flask.ensure_sync:1065:616",
    "edge_type": "calls",
    "evidence": {
      "line": 616,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.update_template_context:590",
    "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.url_for:1102:symbol:src/flask/app.py:Flask.create_url_adapter:509:1182",
    "edge_type": "calls",
    "evidence": {
      "line": 1182,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.url_for:1102",
    "to_node": "symbol:src/flask/app.py:Flask.create_url_adapter:509"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.wsgi_app:1566:symbol:src/flask/app.py:Flask.full_dispatch_request:992:1597",
    "edge_type": "calls",
    "evidence": {
      "line": 1597,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.wsgi_app:1566",
    "to_node": "symbol:src/flask/app.py:Flask.full_dispatch_request:992"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.wsgi_app:1566:symbol:src/flask/app.py:Flask.handle_exception:897:1600",
    "edge_type": "calls",
    "evidence": {
      "line": 1600,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.wsgi_app:1566",
    "to_node": "symbol:src/flask/app.py:Flask.handle_exception:897"
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.wsgi_app:1566:symbol:src/flask/app.py:Flask.request_context:1501:1592",
    "edge_type": "calls",
    "evidence": {
      "line": 1592,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/app.py:Flask.wsgi_app:1566",
    "to_node": "symbol:src/flask/app.py:Flask.request_context:1501"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:AppGroup.command:413:symbol:src/flask/cli.py:AppGroup.command:413:425",
    "edge_type": "calls",
    "evidence": {
      "line": 425,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:AppGroup.command:413",
    "to_node": "symbol:src/flask/cli.py:AppGroup.command:413"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:AppGroup.command:413:symbol:src/flask/cli.py:with_appcontext:380:424",
    "edge_type": "calls",
    "evidence": {
      "line": 424,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:AppGroup.command:413",
    "to_node": "symbol:src/flask/cli.py:with_appcontext:380"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:AppGroup.group:429:symbol:src/flask/cli.py:AppGroup.group:429:437",
    "edge_type": "calls",
    "evidence": {
      "line": 437,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:AppGroup.group:429",
    "to_node": "symbol:src/flask/cli.py:AppGroup.group:429"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.get_command:609:symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600:610",
    "edge_type": "calls",
    "evidence": {
      "line": 610,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:FlaskGroup.get_command:609",
    "to_node": "symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.get_command:609:symbol:src/flask/cli.py:FlaskGroup.get_command:609:613",
    "edge_type": "calls",
    "evidence": {
      "line": 613,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:FlaskGroup.get_command:609",
    "to_node": "symbol:src/flask/cli.py:FlaskGroup.get_command:609"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.get_command:609:symbol:src/flask/cli.py:FlaskGroup.get_command:609:634",
    "edge_type": "calls",
    "evidence": {
      "line": 634,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:FlaskGroup.get_command:609",
    "to_node": "symbol:src/flask/cli.py:FlaskGroup.get_command:609"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.get_command:609:symbol:src/flask/cli.py:ScriptInfo.load_app:333:623",
    "edge_type": "calls",
    "evidence": {
      "line": 623,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:FlaskGroup.get_command:609",
    "to_node": "symbol:src/flask/cli.py:ScriptInfo.load_app:333"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600:637",
    "edge_type": "calls",
    "evidence": {
      "line": 637,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636",
    "to_node": "symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:639",
    "edge_type": "calls",
    "evidence": {
      "line": 639,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636",
    "to_node": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:645",
    "edge_type": "calls",
    "evidence": {
      "line": 645,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636",
    "to_node": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:symbol:src/flask/cli.py:ScriptInfo.load_app:333:645",
    "edge_type": "calls",
    "evidence": {
      "line": 645,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636",
    "to_node": "symbol:src/flask/cli.py:ScriptInfo.load_app:333"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.make_context:657:symbol:src/flask/cli.py:FlaskGroup.make_context:657:676",
    "edge_type": "calls",
    "evidence": {
      "line": 676,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:FlaskGroup.make_context:657",
    "to_node": "symbol:src/flask/cli.py:FlaskGroup.make_context:657"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.make_context:657:symbol:src/flask/cli.py:ScriptInfo:293:670",
    "edge_type": "calls",
    "evidence": {
      "line": 670,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:FlaskGroup.make_context:657",
    "to_node": "symbol:src/flask/cli.py:ScriptInfo:293"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.parse_args:678:symbol:src/flask/cli.py:FlaskGroup.parse_args:678:688",
    "edge_type": "calls",
    "evidence": {
      "line": 688,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:FlaskGroup.parse_args:678",
    "to_node": "symbol:src/flask/cli.py:FlaskGroup.parse_args:678"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:ScriptInfo.load_app:333:symbol:src/flask/cli.py:NoAppException:37:359",
    "edge_type": "calls",
    "evidence": {
      "line": 359,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:ScriptInfo.load_app:333",
    "to_node": "symbol:src/flask/cli.py:NoAppException:37"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:ScriptInfo.load_app:333:symbol:src/flask/cli.py:prepare_import:200:348",
    "edge_type": "calls",
    "evidence": {
      "line": 348,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:ScriptInfo.load_app:333",
    "to_node": "symbol:src/flask/cli.py:prepare_import:200"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:ScriptInfo.load_app:333:symbol:src/flask/cli.py:prepare_import:200:352",
    "edge_type": "calls",
    "evidence": {
      "line": 352,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:ScriptInfo.load_app:333",
    "to_node": "symbol:src/flask/cli.py:prepare_import:200"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:_env_file_callback:493:symbol:src/flask/cli.py:load_dotenv:698:510",
    "edge_type": "calls",
    "evidence": {
      "line": 510,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:_env_file_callback:493",
    "to_node": "symbol:src/flask/cli.py:load_dotenv:698"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:131",
    "edge_type": "calls",
    "evidence": {
      "line": 131,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
    "to_node": "symbol:src/flask/cli.py:NoAppException:37"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:142",
    "edge_type": "calls",
    "evidence": {
      "line": 142,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
    "to_node": "symbol:src/flask/cli.py:NoAppException:37"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:159",
    "edge_type": "calls",
    "evidence": {
      "line": 159,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
    "to_node": "symbol:src/flask/cli.py:NoAppException:37"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:163",
    "edge_type": "calls",
    "evidence": {
      "line": 163,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
    "to_node": "symbol:src/flask/cli.py:NoAppException:37"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:170",
    "edge_type": "calls",
    "evidence": {
      "line": 170,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
    "to_node": "symbol:src/flask/cli.py:NoAppException:37"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:183",
    "edge_type": "calls",
    "evidence": {
      "line": 183,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
    "to_node": "symbol:src/flask/cli.py:NoAppException:37"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:194",
    "edge_type": "calls",
    "evidence": {
      "line": 194,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
    "to_node": "symbol:src/flask/cli.py:NoAppException:37"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:_called_with_wrong_args:94:180",
    "edge_type": "calls",
    "evidence": {
      "line": 180,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
    "to_node": "symbol:src/flask/cli.py:_called_with_wrong_args:94"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_best_app:41:symbol:src/flask/cli.py:NoAppException:37:60",
    "edge_type": "calls",
    "evidence": {
      "line": 60,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:find_best_app:41",
    "to_node": "symbol:src/flask/cli.py:NoAppException:37"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_best_app:41:symbol:src/flask/cli.py:NoAppException:37:80",
    "edge_type": "calls",
    "evidence": {
      "line": 80,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:find_best_app:41",
    "to_node": "symbol:src/flask/cli.py:NoAppException:37"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_best_app:41:symbol:src/flask/cli.py:NoAppException:37:87",
    "edge_type": "calls",
    "evidence": {
      "line": 87,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:find_best_app:41",
    "to_node": "symbol:src/flask/cli.py:NoAppException:37"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_best_app:41:symbol:src/flask/cli.py:_called_with_wrong_args:94:77",
    "edge_type": "calls",
    "evidence": {
      "line": 77,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:find_best_app:41",
    "to_node": "symbol:src/flask/cli.py:_called_with_wrong_args:94"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:main:1122:symbol:src/flask/cli.py:main:1122:1123",
    "edge_type": "calls",
    "evidence": {
      "line": 1123,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:main:1122",
    "to_node": "symbol:src/flask/cli.py:main:1122"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:routes_command:1061:symbol:src/flask/cli.py:AppGroup.command:413:1048",
    "edge_type": "calls",
    "evidence": {
      "line": 1048,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:routes_command:1061",
    "to_node": "symbol:src/flask/cli.py:AppGroup.command:413"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:AppGroup.command:413:882",
    "edge_type": "calls",
    "evidence": {
      "line": 882,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:run_command:935",
    "to_node": "symbol:src/flask/cli.py:AppGroup.command:413"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:CertParamType:780:887",
    "edge_type": "calls",
    "evidence": {
      "line": 887,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:run_command:935",
    "to_node": "symbol:src/flask/cli.py:CertParamType:780"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:ScriptInfo.load_app:333:955",
    "edge_type": "calls",
    "evidence": {
      "line": 955,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:run_command:935",
    "to_node": "symbol:src/flask/cli.py:ScriptInfo.load_app:333"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:SeparatedPathType:867:918",
    "edge_type": "calls",
    "evidence": {
      "line": 918,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:run_command:935",
    "to_node": "symbol:src/flask/cli.py:SeparatedPathType:867"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:SeparatedPathType:867:927",
    "edge_type": "calls",
    "evidence": {
      "line": 927,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:run_command:935",
    "to_node": "symbol:src/flask/cli.py:SeparatedPathType:867"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:show_server_banner:766:981",
    "edge_type": "calls",
    "evidence": {
      "line": 981,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:run_command:935",
    "to_node": "symbol:src/flask/cli.py:show_server_banner:766"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:shell_command:1001:symbol:src/flask/cli.py:AppGroup.command:413:999",
    "edge_type": "calls",
    "evidence": {
      "line": 999,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:shell_command:1001",
    "to_node": "symbol:src/flask/cli.py:AppGroup.command:413"
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:with_appcontext:380:symbol:src/flask/cli.py:ScriptInfo.load_app:333:397",
    "edge_type": "calls",
    "evidence": {
      "line": 397,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/cli.py:with_appcontext:380",
    "to_node": "symbol:src/flask/cli.py:ScriptInfo.load_app:333"
  },
  {
    "edge_id": "calls:symbol:src/flask/ctx.py:AppContext.__enter__:506:symbol:src/flask/ctx.py:AppContext.push:416:507",
    "edge_type": "calls",
    "evidence": {
      "line": 507,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/ctx.py:AppContext.__enter__:506",
    "to_node": "symbol:src/flask/ctx.py:AppContext.push:416"
  },
  {
    "edge_id": "calls:symbol:src/flask/ctx.py:AppContext.push:416:symbol:src/flask/ctx.py:AppContext._get_session:381:439",
    "edge_type": "calls",
    "evidence": {
      "line": 439,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/ctx.py:AppContext.push:416",
    "to_node": "symbol:src/flask/ctx.py:AppContext._get_session:381"
  },
  {
    "edge_id": "calls:symbol:src/flask/ctx.py:AppContext.push:416:symbol:src/flask/ctx.py:AppContext.match_request:405:444",
    "edge_type": "calls",
    "evidence": {
      "line": 444,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/ctx.py:AppContext.push:416",
    "to_node": "symbol:src/flask/ctx.py:AppContext.match_request:405"
  },
  {
    "edge_id": "calls:symbol:src/flask/ctx.py:AppContext.session:396:symbol:src/flask/ctx.py:AppContext._get_session:381:401",
    "edge_type": "calls",
    "evidence": {
      "line": 401,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/ctx.py:AppContext.session:396",
    "to_node": "symbol:src/flask/ctx.py:AppContext._get_session:381"
  },
  {
    "edge_id": "calls:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:77",
    "edge_type": "calls",
    "evidence": {
      "line": 77,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68",
    "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68"
  },
  {
    "edge_id": "calls:symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93:symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93:103",
    "edge_type": "calls",
    "evidence": {
      "line": 103,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93",
    "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93"
  },
  {
    "edge_id": "calls:symbol:src/flask/ctx.py:after_this_request:118:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:139",
    "edge_type": "calls",
    "evidence": {
      "line": 139,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/ctx.py:after_this_request:118",
    "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68"
  },
  {
    "edge_id": "calls:symbol:src/flask/ctx.py:copy_current_request_context:154:symbol:src/flask/ctx.py:AppContext.copy:355:200",
    "edge_type": "calls",
    "evidence": {
      "line": 200,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/ctx.py:copy_current_request_context:154",
    "to_node": "symbol:src/flask/ctx.py:AppContext.copy:355"
  },
  {
    "edge_id": "calls:symbol:src/flask/ctx.py:copy_current_request_context:154:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:192",
    "edge_type": "calls",
    "evidence": {
      "line": 192,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/ctx.py:copy_current_request_context:154",
    "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68"
  },
  {
    "edge_id": "calls:symbol:src/flask/ctx.py:has_app_context:235:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:257",
    "edge_type": "calls",
    "evidence": {
      "line": 257,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/ctx.py:has_app_context:235",
    "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68"
  },
  {
    "edge_id": "calls:symbol:src/flask/ctx.py:has_request_context:209:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:232",
    "edge_type": "calls",
    "evidence": {
      "line": 232,
      "rel": "ast_call"
    },
    "from_node": "symbol:src/flask/ctx.py:has_request_context:209",
    "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68"
  }
]
