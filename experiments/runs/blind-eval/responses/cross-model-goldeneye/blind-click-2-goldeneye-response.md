# Cross-Model (Goldeneye): blind-click-2
Date: 2026-04-16

When a value is not supplied directly on the CLI, Click runs the parameter through `consume_value(ctx, opts)`. The clue explicitly says that, for `Option`, this is where the value can be collected from an interactive prompt. [consume_value, src/click/core.py:3256-3318; Option, src/click/core.py:2646-3335]

After a value is sourced, `process_value(ctx, value)` decides what happens next: it branches on whether the value is still `UNSET`, otherwise type-casts it, and raises `MissingParameter` when a required value is still missing. [process_value, src/click/core.py:2416-2480; MissingParameter, src/click/exceptions.py:137-205]

For arguments, the constructor auto-determines requiredness from defaults and `nargs`: if there is no explicit default and at least one value is expected, the argument becomes required; if a default exists, it is not required. [Argument, src/click/core.py:3338-3413]

The prompt also shows an env-var path for non-CLI values: `split_envvar_value(rv)` exists to split a value coming from an environment variable. [split_envvar_value, src/click/types.py:126-134]

File and path types then do extra conversion work beyond plain type-casting:

- `File` resolves lazy-opening behavior, checks whether the incoming object is already file-like, and fails with `BadParameter` if needed. It relies on `open_file(...)`, which has special behavior for `'-'` and can return `KeepOpenFile` or `LazyFile`. [File, src/click/types.py:754-872; open_file, src/click/utils.py:358-404]
- `LazyFile` defers the actual open and manages closing behavior intelligently, which is additional work compared with simple scalar conversion. [LazyFile, src/click/utils.py:109-194]
- `Path` performs path-specific validation/coercion and calls `coerce_path_result(...)` during conversion, again failing through parameter-validation machinery when necessary. [Path, src/click/types.py:879-1057; coerce_path_result, src/click/types.py:955-966]
