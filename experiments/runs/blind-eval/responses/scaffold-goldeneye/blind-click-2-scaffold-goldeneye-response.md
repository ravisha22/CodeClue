# Scaffold (Goldeneye): blind-click-2
Date: 2026-04-16

## Relevant symbols traced
- Parameters are attached by `option()` / `argument()` via `_param_memo`, and surfaced through `Command.get_params()`. [option (src/click/decorators.py:352-377); argument (src/click/decorators.py:324-349); _param_memo (src/click/decorators.py:314-321); Command (src/click/core.py:873-1485); get_params (src/click/core.py:1002-1025)]
- Option value collection is handled by `consume_value()`, and `Option` can prompt. [consume_value (src/click/core.py:3256-3318); Option (src/click/core.py:2646-3335)]
- Conversion/validation is performed in `process_value()` and `type_cast_value()`. [process_value (src/click/core.py:2416-2480); type_cast_value (src/click/core.py:2342-2396)]
- File/path specifics are handled by `File`, `Path`, `open_file`, `LazyFile`, and `coerce_path_result`. [File (src/click/types.py:754-872); Path (src/click/types.py:879-1057); open_file (src/click/utils.py:358-404); LazyFile (src/click/utils.py:109-194); KeepOpenFile (src/click/utils.py:197-219); coerce_path_result (src/click/types.py:955-966)]

## Answer
Based on the clue, Click's fallback path for missing values is:

1. **Options and arguments are first-class `Parameter` objects on the command.** The decorators attach them via `_param_memo`, and `Command.get_params()` returns the active list, including the help option when appropriate. [option (src/click/decorators.py:352-377); argument (src/click/decorators.py:324-349); _param_memo (src/click/decorators.py:314-321); get_params (src/click/core.py:1002-1025)]
2. **If a value is not present directly on the command line, `consume_value()` is the collection hook for options.** The clue explicitly says that, for `Option`, the value can be collected from an interactive prompt, and the `Option` type itself calls `prompt_for_value`. [consume_value (src/click/core.py:3256-3318); Option (src/click/core.py:2646-3335)]
3. **After collection, Click validates/converts what it got.** `process_value()` branches on whether the value is still `UNSET`; otherwise it passes the value through `self.type_cast_value(...)`, and it can raise `MissingParameter` if a required value is still absent. [process_value (src/click/core.py:2416-2480); type_cast_value (src/click/core.py:2342-2396)]
4. **Environment-variable sourced values also exist in the pipeline.** The presence of `split_envvar_value()` shows that values coming from an env var may be split into multiple pieces, which confirms envvar-based sourcing is part of the design. [split_envvar_value (src/click/types.py:126-134)]
5. **File conversion does extra I/O-aware work.** `File` resolves lazy-opening behavior, checks whether a value is already file-like, and uses `open_file()`, which has special handling for `"-"` and can return `KeepOpenFile` or `LazyFile`. [File (src/click/types.py:754-872); _is_file_like (src/click/types.py:875-876); open_file (src/click/utils.py:358-404); LazyFile (src/click/utils.py:109-194); KeepOpenFile (src/click/utils.py:197-219)]
6. **Path conversion does extra coercion/validation work.** `Path` calls `coerce_path_result()` and can fail with `BadParameter`, so it is not just a raw string pass-through. [Path (src/click/types.py:879-1057); coerce_path_result (src/click/types.py:955-966)]

## Gaps / uncertainty
The exact precedence among prompting, envvar input, and any other fallback source is **not fully recoverable** from the provided evidence because `consume_value()`'s full body is not shown and the GAPS section says body logic is needed. So the safe conclusion is that Click can fall back to prompting and envvar-aware processing, then validates through `process_value()`, but the precise ordering is unresolved here. [consume_value (src/click/core.py:3256-3318); split_envvar_value (src/click/types.py:126-134); GAPS]
