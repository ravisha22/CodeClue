# Answer

Based on the clue file alone, Click appears to build the CLI in two phases: **decoration/registration** and **runtime context/dispatch**.

## 1) Decoration turns Python functions into command objects

- `option(...)` is described as attaching an option to a command, so option decorators contribute command metadata before the final command object exists. [`option`, `src/click/decorators.py:352`]
- The nearby helper `_param_memo` strongly suggests that decorator-produced parameter metadata is memoized on the decorated function until command construction happens. [`_param_memo`, `src/click/decorators.py:314`; `option`, `src/click/decorators.py:352`]
- `command(name, cls)` "Creates a new `Command` and uses the decorated function as ..." and is annotated with `behavior: UNWIND(reversed)`. The safest reading is that `@command` converts the decorated Python function into a `Command` object and replays previously attached decorator metadata in reverse decorator order while doing so. [`command`, `src/click/decorators.py:168-255`]
- `Command` is the "basic building block of command line interfaces," so the result of decoration is a tree node representing one CLI command. [`Command`, `src/click/core.py:873-1485`]

## 2) Nested CLIs are represented by groups containing child commands

- `Group` "is a command that nests other commands (or more groups)," so nesting is modeled explicitly by `Group` nodes that can contain other `Command` or `Group` nodes. [`Group`, `src/click/core.py:1503-1951`]
- `Group` calls `add_command`, which indicates that child commands are registered onto a group. [`Group`, `src/click/core.py:1503-1951`]
- `_check_nested_chain` is called by `Group` and `add_command` and raises `RuntimeError`, so Click validates some illegal nesting / chaining combinations at registration time. [`_check_nested_chain`, `src/click/core.py:73-90`]
- `list_commands(ctx)` returns subcommand names in display order, which confirms that a group maintains a named set of child commands. [`list_commands`, `src/click/core.py:1784-1786`]
- The examples show that this child-command lookup can be customized: `ComplexCLI` extends `Group`, and the examples expose `get_command`, `list_commands`, and `resolve_command`; `AliasedGroup` in the aliases example also exposes `get_command` and `resolve_command`. That supports the idea that dispatch walks a group tree by resolving a subcommand name to a child command object. [`ComplexCLI`, `examples/complex/complex/cli.py:31-45`; `get_command`, `list_commands`, `examples/complex/complex/cli.py:60L summary`; `AliasedGroup`, `get_command`, `resolve_command`, `examples/aliases/aliases.py:143L summary`]

## 3) Runtime dispatch starts by building a context from argv

- `make_context(info_name, args, parent)` says that, given a command name and argument list, it will "kick ..." execution, and both `Command` and `Group` call it. That means dispatch begins by turning argv into a `Context` associated with the current command node. [`make_context`, `src/click/core.py:1182-1217`; `Command`, `src/click/core.py:873-1485`; `Group`, `src/click/core.py:1503-1951`]
- `scope(cleanup)` is called by `make_context`, `Command`, and `Group`, so context creation and command execution run inside an explicit context-management scope. [`scope`, `src/click/core.py:496-531`]

## 4) Groups appear to parse their own args, then hand remaining args to a child command

- `Command` has `allow_extra_args=False` and `allow_interspersed_args=True`, while `Group` has `allow_extra_args=True` and `allow_interspersed_args=False`. Based only on those attributes, a group is configured differently from a leaf command in a way that is consistent with preserving leftover argv tokens for subcommands. [`Command`, `src/click/core.py:873-1485`; `Group`, `src/click/core.py:1503-1951`]
- `Group` calls `_make_sub_context` and `_process_result`, which supports a runtime sequence of: parse at the current group level, identify a child command, create a child context, then process the child command's result. [`Group`, `src/click/core.py:1503-1951`]
- `Group` also calls `fail`, and `fail(message)` raises `UsageError`, giving the error path if command resolution or invocation is invalid. [`Group`, `src/click/core.py:1503-1951`; `fail`, `src/click/core.py:718-724`]

## 5) Most likely end-to-end flow, limited to what the clue supports

From the clue alone, the most defensible reconstruction is:

1. Parameter decorators such as `option(...)` attach metadata to a Python function, likely via `_param_memo`. [`option`, `src/click/decorators.py:352`; `_param_memo`, `src/click/decorators.py:314`]
2. `@command(...)` converts that decorated function into a `Command` object, replaying the accumulated decorators in reverse order (`UNWIND(reversed)`). [`command`, `src/click/decorators.py:168-255`]
3. If the command should contain subcommands, a `Group` object is used instead; child commands are registered onto it with `add_command`, and invalid nesting patterns are checked by `_check_nested_chain`. [`Group`, `src/click/core.py:1503-1951`; `_check_nested_chain`, `src/click/core.py:73-90`]
4. At runtime, Click starts from the top-level command/group and calls `make_context(info_name, args, parent)` to turn argv into a `Context`. [`make_context`, `src/click/core.py:1182-1217`]
5. For a `Group`, the remaining argv appears to be used to select a child command name from the group's registered commands, then `Group` creates a sub-context (`_make_sub_context`) for that child and processes the result (`_process_result`). [`Group`, `src/click/core.py:1503-1951`; `list_commands`, `src/click/core.py:1784-1786`]
6. The lookup step is probably overrideable, because the examples expose `get_command` / `resolve_command` on `Group` subclasses. [`get_command`, `resolve_command`, `examples/aliases/aliases.py:143L summary`; `get_command`, `list_commands`, `examples/complex/complex/cli.py:60L summary`]

## 6) What the clue does **not** let me state confidently

- I **can** say that Click turns decorated functions into `Command` objects, uses `Group` to build a nested command tree, and uses `make_context` plus group-specific sub-context handling at runtime. [`command`, `src/click/decorators.py:168-255`; `Command`, `src/click/core.py:873-1485`; `Group`, `src/click/core.py:1503-1951`; `make_context`, `src/click/core.py:1182-1217`]
- I **cannot** give the exact internal body-level algorithm for subcommand lookup or the exact final callback-invocation function, because the clue explicitly flags mechanistic gaps and does not show the bodies of `add_command`, `_make_sub_context`, `_process_result`, or the callback execution path. [`Group`, `src/click/core.py:1503-1951`; `command`, `src/click/decorators.py:168-255`]

So, in one sentence: Click appears to collect decorator metadata on a Python function, convert that function into a `Command`, assemble commands into a tree of `Group` objects, then at runtime build a `Context` from argv, resolve the next subcommand within the current group, create a sub-context for it, and process that subcommand's result. [`_param_memo`, `src/click/decorators.py:314`; `command`, `src/click/decorators.py:168-255`; `Group`, `src/click/core.py:1503-1951`; `make_context`, `src/click/core.py:1182-1217`]

