# Response: blind-click-2 (raw-topk baseline)
Date: 2026-04-15

The supplied prompt only contains `src\click\types.py`, so it shows **type conversion**, not the full parameter-resolution order.

What the prompt does show about missing command-line values:

- `ParamType.__call__` only invokes `convert(...)` when the value is not `None` (`src\click\types.py`, lines 93-100). If the resolved value is still `None`, conversion is skipped.
- `ParamType.split_envvar_value` shows how a value coming from an environment variable is split (`lines 136-144`). The class-level docs say the default rule is whitespace splitting, except that files and paths use `os.path.pathsep` (`lines 64-70`).
- The same docstring notes that conversion may run with `ctx` and `param` as `None`, “such as when converting prompt input” (`lines 122-133`).

What the prompt does **not** show is the code that decides the fallback order between command-line input, environment variables, defaults, prompts, etc. That logic would have to live in `Parameter` / `Context` / parser code, but those implementations are not included here.

For the concrete type work:

- **File values:** `File` is a `ParamType` (`lines 764-795`). Its docs say it can map `"-"` to stdin/stdout (`lines 769-770`), auto-close when the context tears down (`lines 765-767`), support encoding/lazy opening/atomic writes (`lines 772-785`), and split env-var lists with `os.path.pathsep` (`line 795`). In `File.convert`, an already-file-like object is returned unchanged (`lines 825-832`); otherwise it resolves whether opening should be lazy via `resolve_lazy_flag` (`lines 816-823`) and then proceeds into lazy/open-stream handling, but that portion is truncated after line 840.
- **Path values:** the question asks about path-specific conversion work, but the `Path` type implementation is not present in this excerpt. The only path-specific behavior visible is the shared env-var splitting rule for “paths and files” in `ParamType`’s documentation (`lines 64-70`).

So, based only on the prompt: Click first resolves some value from outside the type layer, then `ParamType.__call__` converts it only if it is non-`None` (`lines 93-100`); env-var values are split per `split_envvar_value` (`lines 136-144`); `File` adds file-opening behavior (`lines 764-840`); and the actual `Path.convert` logic is not available in the supplied source.
