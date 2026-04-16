# v2.4 Ablation (File 1 Only): blind-click-2
Date: 2026-04-16

When a value is missing from the command line, Click eventually runs parameter processing through `process_value`, which explicitly branches on whether the incoming value is `UNSET` or should be type-cast, and it can raise `MissingParameter`. That shows “no direct CLI value” is a first-class case in the conversion pipeline. [process_value (src/click/core.py:2416-2480); MissingParameter (src/click/exceptions.py:137-205)]

For options specifically, `consume_value` says the value can be collected from an interactive prompt. So prompting is one of the non-command-line fallback sources. [consume_value (src/click/core.py:3256-3318)]

Environment-variable input is also visible: `split_envvar_value` exists specifically to split a value that came from an environment variable. [split_envvar_value (src/click/types.py:126-134)]

File conversion does extra work beyond ordinary type casting. `File` is a dedicated `ParamType` for reading/writing files; it calls `resolve_lazy_flag`, validates file-likeness with `_is_file_like`, and can fail with `BadParameter`. `open_file` also has special handling for `'-'` and uses `KeepOpenFile` / `LazyFile`. [File (src/click/types.py:754-872); _is_file_like (src/click/types.py:875-876); open_file (src/click/utils.py:358-404); LazyFile (src/click/utils.py:109-194); KeepOpenFile (src/click/utils.py:197-219)]

Path conversion also has extra post-processing: `Path` calls `coerce_path_result` and can fail with `BadParameter`. [Path (src/click/types.py:879-1057); coerce_path_result (src/click/types.py:955-966)]

What I cannot determine from this clue file: the full precedence order among prompt, environment variable, defaults, and any context/default-map source, because the clue names the mechanisms but does not expose `consume_value`’s body or any explicit precedence annotation for those sources. [consume_value (src/click/core.py:3256-3318); GAPS]
