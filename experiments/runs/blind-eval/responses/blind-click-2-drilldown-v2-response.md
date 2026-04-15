# Response: blind-click-2 v2 (with drill-down)
Date: 2026-04-15

When a parameter value is not supplied on the command line, the decision order is explicit in `consume_value`: first check the parsed CLI options, then fall back to the environment variable, then the context default map, then the parameter's declared default; if none of those produce a value, an internal sentinel (`UNSET`) is returned. This precedence is stated in the docstring and implemented by the sequence of checks in `consume_value` (`opts.get(...)`, `value_from_envvar`, `ctx.lookup_default(...)`, `get_default(...)`). [Source snippet: `consume_value` L402-L442]

More concretely:
- A parsed user-provided value is taken from `opts` and marked as `ParameterSource.COMMANDLINE`. [Source snippet: `consume_value` L412-L420]
- If no CLI value is present, `value_from_envvar(ctx)` is tried next, and if it returns a non-`None` value, the source becomes `ParameterSource.ENVIRONMENT`. [Source snippet: `consume_value` L422-L427]
- If that still yields nothing, `ctx.lookup_default(self.name)` is checked, with an additional membership check against `ctx.default_map`, and the source becomes `ParameterSource.DEFAULT_MAP`. [Source snippet: `consume_value` L428-L435]
- If there is still no value, `self.get_default(ctx)` is used, and the source is `ParameterSource.DEFAULT`. [Source snippet: `consume_value` L436-L440]
- If none of the above produce anything, `consume_value` returns `UNSET`. [Source snippet: `consume_value` L408-L442]

After choosing the raw value, Click records where it came from by calling `ctx.set_parameter_source(self.name, source)`. [Source snippet: `handle_parse_result` L344-L347; `set_parameter_source` L569-L576]

Regardless of where the value came from, Click then runs it through the parameter's type conversion logic. This is stated directly: `handle_parse_result` says it will "Always process the value through the Parameter's :attr:\`type\`, wherever it comes from," and then calls `self.process_value(ctx, value)`. [Source snippet: `handle_parse_result` L333-L370]

If type processing fails and `ctx.resilient_parsing` is false, the exception is raised normally. If resilient parsing is enabled, Click suppresses the failure and resets the value to `UNSET`, effectively treating it as missing. [Source snippet: `handle_parse_result` L369-L377] This is relevant because `_resolve_context` enables `resilient_parsing=True` specifically while traversing command contexts for shell completion, and its docstring says this traversal does not trigger input prompts or callbacks. [Source snippet: `_resolve_context` L453-L462]

`handle_parse_result` also shows one more consequence of the source information: deprecation warnings are only emitted when a deprecated parameter has a value that was explicitly set by the user, not when it came from the normal default or default map paths. The condition excludes `ParameterSource.DEFAULT` and `ParameterSource.DEFAULT_MAP`. [Source snippet: `handle_parse_result` L349-L366]

For file and path types, the clues show that conversion does extra work beyond plain "apply a type directly":
- The clue for `Tuple` says the default behavior is to apply a type directly to a value, which implies any special logic in other types is noteworthy. [Clue file, FOCUS `Tuple`]
- `Path` is called out as a dedicated parameter type, "similar to the `File` type," and its implementation specifically calls `coerce_path_result` and `fail`. [Clue file, FOCUS `Path`]
- Because `Path` calls `coerce_path_result`, we can conclude that path conversion includes some additional coercion/normalization step on the path result, plus validation that can raise a `BadParameter` via `fail`. [Clue file, FOCUS `Path`; clue file, `fail` called by `Path`]
- For files, the strongest concrete clue is `open_file`, whose purpose is to "Open a file, with extra behavior to handle `'-'`" and which uses `KeepOpenFile` and `LazyFile`. [Clue file, FOCUS `open_file`]
- Since `fail` is also called by `File`, we can conclude that file conversion, like path conversion, performs validation that can surface as `BadParameter`. [Clue file, `fail` called_by `File`]

What I can determine confidently from the provided material is therefore:
1. Non-command-line values are chosen in this precedence order: environment variable -> default map -> declared default, after first checking whether the parser already produced a command-line value. [Source snippet: `consume_value` L402-L442]
2. The chosen value is tagged with its source and still passed through normal type processing. [Source snippet: `handle_parse_result` L344-L370; `set_parameter_source` L569-L576]
3. `Path` conversion performs extra result coercion via `coerce_path_result` and can fail validation with `BadParameter`. [Clue file, FOCUS `Path`; clue file, `fail`]
4. File handling involves opening files with special handling for `'-'`, and uses `KeepOpenFile` / `LazyFile`, indicating extra file-opening behavior rather than a trivial cast. [Clue file, FOCUS `open_file`]

What I cannot determine from the provided clues/snippets:
- The exact body of `File` conversion, because the `File` class/function implementation is not included in the drill-down snippets or focus bodies shown here.
- The exact semantics of `coerce_path_result` (for example, exactly how it transforms the path), because only the fact that `Path` calls it is given, not its implementation. [Clue file, FOCUS `Path`]

So, in summary: when no direct CLI value exists, Click falls back in a fixed order—environment, then default map, then parameter default—and then still processes that value through the parameter type. File/path types add specialized conversion work: paths perform extra coercion/validation, and files perform file-opening-related handling including special treatment for `'-'`; however, the exact low-level details of those conversions are not fully available in the provided evidence. [Source snippet: `consume_value` L402-L442; `handle_parse_result` L333-L394; clue file, FOCUS `Path`; clue file, FOCUS `open_file`]
