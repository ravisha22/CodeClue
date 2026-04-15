# Response: blind-click-1 (with drill-down)
2026-04-15

## Bottom line
From the provided material, Click appears to build its CLI in two layers: (1) decorators wrap Python functions into `Command` objects and attach parameter metadata, and (2) `Group` objects register those commands as children, forming a tree of commands and subcommands. At runtime, Click builds a `Context` from argv, descends through group/subcommand boundaries, resolves the matching child command, and then hands execution to the selected command object. The exact final invocation site is not shown in the provided excerpts, so that last step can only be inferred from the command-construction clues. [Clue: `command` in `src/click/decorators.py:168-255`; Clue: `option` in `src/click/decorators.py:352`; Clue: `Group` in `src/click/core.py:1503-1951`; Clue: `make_context` in `src/click/core.py:1182-1217`]

## 1) How decorated Python functions become command objects
The strongest clue is the `command` decorator entry: it "Creates a new :class:`Command` and uses the decorated function as ..." with `sig: command(name, cls)` and `behavior: UNWIND(reversed)`. That tells us the decorator is the mechanism that converts a Python function into a `Command` object, and that decoration order matters enough for Click to unwind something in reverse order. [Clue: `command` in `src/click/decorators.py:168-255`]

The parameter side is hinted by two decorator-related entries: `_param_memo` exists in `src/click/decorators.py`, and `option` is explicitly described as "Attaches an option to the command." Together, those clues support the model that decorators collect parameter definitions while the command object is being built. [Clue: `_param_memo` in `src/click/decorators.py:314`; Clue: `option` in `src/click/decorators.py:352`]

What I can determine confidently:
- a decorated function is wrapped into a `Command`; [Clue: `command` in `src/click/decorators.py:168-255`]
- options are attached during decoration; [Clue: `option` in `src/click/decorators.py:352`]
- decoration order is normalized by a reverse unwind step. [Clue: `command` behavior `UNWIND(reversed)`]

What I cannot determine from the provided material:
- the exact internal storage layout for the callback function;
- the exact body of `_param_memo`;
- the exact order in which argument decorators vs option decorators are materialized, beyond the fact that reverse unwinding occurs. [Clue coverage limitation: only summaries for `command`, `option`, `_param_memo`]

## 2) How nested CLIs are formed
The core structural clue is the `Group` class summary: "A group is a command that nests other commands (or more groups)." It extends `Command`, which means nested CLIs are built by a specialized command type rather than by a separate registry system. `Group` also calls `add_command`, `make_context`, `_make_sub_context`, `format_commands`, and `_process_result`. That combination strongly suggests that a group both owns subcommands and participates in runtime descent into them. [Clue: `Group` in `src/click/core.py:1503-1951`]

`list_commands(ctx)` "Returns a list of subcommand names in the order they should appear" and delegates to `sorted`, which implies groups expose an ordered child-command namespace. [Clue: `list_commands` in `src/click/core.py:1784-1786`]

`_check_nested_chain(base_command, cmd_name, cmd, register)` is called by `CommandCollection`, `add_command`, and `Group`, and can raise `RuntimeError`. That means Click validates some combinations of nesting/chaining when commands are registered, rather than waiting until execution time. [Clue: `_check_nested_chain` in `src/click/core.py:73-90`]

The examples reinforce that this tree is extensible through lookup hooks:
- `ComplexCLI` extends `Group` and defines `get_command` and `list_commands`; [Clue: `ComplexCLI` in `examples/complex/complex/cli.py:31-45`; Index: `examples/complex/complex/cli.py`]
- `AliasedGroup` defines `get_command` and `resolve_command`; [Index: `examples/aliases/aliases.py`]
- the naval, repo, completion, and termui examples each expose a top-level `cli`, showing the pattern of a root command/group object defined in Python source. [Index entries for `examples/naval/naval.py`, `examples/repo/repo.py`, `examples/completion/completion.py`, `examples/termui/termui.py`]

So, based only on the supplied evidence, the nested CLI is formed by:
1. turning Python functions into `Command` objects with decorators; [Clue: `command`; Clue: `option`]
2. registering those command objects under a `Group`; [Clue: `Group` calls `add_command`]
3. allowing a child to itself be a `Group`, which recursively creates a tree. [Clue: `Group` "nests other commands (or more groups)"]

## 3) How parameter typing is derived from Python values/types
The drill-down on `convert_type` shows how Click maps Python type information into CLI parameter types. If no explicit type is supplied but there is a default value, it infers a type from the default. For tuple/list defaults, it looks at the first item; if that item is itself a tuple/list, it builds a tuple of inner Python types. [Source snippet: `convert_type`, lines 361-385]

After inference, `convert_type` maps:
- `tuple` -> `Tuple(ty)`; [Source snippet: `convert_type`, lines 387-389]
- `ParamType` instance -> returned as-is; [Source snippet: `convert_type`, lines 390-391]
- `str` or `None` -> `STRING`; [Source snippet: `convert_type`, lines 393-395]
- `int` -> `INT`; [Source snippet: `convert_type`, lines 396-397]
- `float` -> `FLOAT`; [Source snippet: `convert_type`, lines 399-400]
- `bool` -> `BOOL`; [Source snippet: `convert_type`, lines 402-403]
- other guessed types -> `STRING`; [Source snippet: `convert_type`, lines 405-406]
- other explicit callables/types -> `FuncParamType(ty)`. [Source snippet: `convert_type`, lines 408-418]

That matters to decorated commands because the decorator layer attaches parameters to commands, and these snippets show the concrete machinery that can turn Python-level types/defaults into CLI parsing behavior. The exact call site from decorator code into `convert_type` is not shown, so I can say the type-conversion mechanism exists and is clearly meant for command parameters, but I cannot prove the exact integration point from the supplied excerpts alone. [Clue: `option` attaches option; Clue: `convert_type` summary in File 1; Source snippet: `convert_type`]

The `Tuple` drill-down adds more detail. Its constructor converts each declared element type with `convert_type`, its `arity` is the number of element types, and `convert` rejects inputs whose value count does not match that arity. When counts do match, it converts each element positionally via `ty(x, param, ctx)` and returns a Python tuple. [Source snippet: `Tuple`, lines 437-472]

So for multi-value parameters, Click does not just say "tuple" abstractly; it preserves per-position typing and enforces exact cardinality. [Source snippet: `Tuple`, lines 437-472]

The `BoolParamType` snippet shows a concrete example of what those parameter types do at runtime. It defines a fixed string-to-bool mapping (`"1"`, `"yes"`, `"true"`, etc.), normalizes strings by `strip().lower()`, returns `None` for unknown values, and `convert` raises a typed failure if the input does not match any known boolean state. [Source snippets: `BoolParamType`, `str_to_bool`, `convert`, `__repr__`]

## 4) What runtime dispatch appears to do
The central runtime clue is `make_context(info_name, args, parent)`, which "when given an info name and arguments will kick ..." and has `behavior: ACCUMULATE(loop)`. It calls `scope`, and `scope(cleanup)` is a context helper used by `make_context`, `Command`, and `Group`. This strongly indicates that Click first turns argv into a `Context` object and does so in a loop over input arguments while managing contextual state. [Clue: `make_context` in `src/click/core.py:1182-1217`; Clue: `scope` in `src/click/core.py:496-531`]

For nested CLIs specifically, `Group` calls both `make_context` and `_make_sub_context`. That suggests a parent context is created for the current command/group, and then a child context is created when dispatch descends into a selected subcommand. [Clue: `Group` in `src/click/core.py:1503-1951`]

The clue file does not show the body of `resolve_command`, but two clues make its role clear enough to mention:
- `fail(message)` in `core.py` is called by `Command`, `resolve_command`, and `Group`; [Clue: `fail` in `src/click/core.py:718-724`]
- the aliases example advertises a `resolve_command` symbol and a `get_command` symbol. [Index: `examples/aliases/aliases.py`]

From that, I can determine that runtime selection of the target subcommand involves a resolution step that can fail and that group-like command containers expose hooks such as `get_command`, `list_commands`, and `resolve_command` for turning argv tokens into concrete child command objects. [Clue: core `fail`; Index: `examples/aliases/aliases.py`; Index: `examples/complex/complex/cli.py`; Clue: `list_commands`]

What I cannot determine exactly from the provided material:
- whether name resolution first checks an exact name map, aliases, normalization, or something else;
- the precise algorithm for consuming argv tokens during subcommand descent;
- the exact method that finally invokes the selected callback function. [Coverage limitation: no body for `resolve_command`, `invoke`, or parser integration shown]

## 5) Evidence from shell-completion traversal
The shell-completion clues are not the same as runtime execution, but they are useful because they show Click traversing the same command hierarchy to find the object responsible for the current position.

`ShellComplete` calls `get_completions`, `source_vars`, `_resolve_context`, `_resolve_incomplete`, and `shell_complete`. [Clue: `ShellComplete` in `src/click/shell_completion.py:200-301`]

`get_completions(args, incomplete)` calls `_resolve_context`, `_resolve_incomplete`, and `shell_complete`. [Clue: `get_completions` in `src/click/shell_completion.py:271-281`]

`_resolve_incomplete(ctx, args, incomplete)` "Find[s] the Click object that will handle the completion" and loops over arguments, branching on whether the current token is incomplete, while consulting `_is_incomplete_argument`, `_is_incomplete_option`, and `_start_of_option`. [Clue: `_resolve_incomplete` in `src/click/shell_completion.py:623-667`]

That supports the broader architectural reading: Click keeps a command/parameter object graph, then walks it dynamically based on argv to identify the relevant handler object. Completion does this for suggestions; execution presumably does the analogous thing for actual dispatch. The provided evidence supports the similarity of traversal, but not that both paths share the same exact method bodies. [Clue: `ShellComplete`; Clue: `get_completions`; Clue: `_resolve_incomplete`]

The drill-down `shell_complete` snippet from `types.py` shows what happens once completion reaches a parameter type: this method returns a `CompletionItem` whose `type` is `"dir"` if `dir_okay and not file_okay`, otherwise `"file"`. So once the system has resolved the active parameter, the parameter type itself can produce completions. [Source snippet: `shell_complete`, lines 340-356]

## 6) A careful end-to-end reconstruction
Based only on the clue file and snippets, the most defensible end-to-end flow is:

1. **Definition time:** A Python function is decorated with `command(...)`, which creates a `Command` using that decorated function. Parameter decorators such as `option(...)` attach parameter objects/metadata to that command, with reverse unwinding used to normalize decoration order. [Clue: `command`; Clue: `option`; Clue: `_param_memo`]

2. **Tree construction time:** One or more `Command` objects are registered under a `Group` through `add_command`. Because a `Group` can nest "other commands (or more groups)", this yields a recursive command tree. Ordering/visibility of children is exposed through `list_commands`, and invalid nested-chain combinations are guarded by `_check_nested_chain`. [Clue: `Group`; Clue: `list_commands`; Clue: `_check_nested_chain`]

3. **Parameter normalization:** For command parameters, Python-level type/default information is converted into `ParamType` objects through `convert_type`. Built-in scalar types map to built-in parameter types, tuple signatures become `Tuple(...)`, and other explicit types fall back to `FuncParamType`. `Tuple` enforces positional arity and per-element conversion. [Source snippet: `convert_type`; Source snippet: `Tuple`; Clue: `convert_type` summary]

4. **Invocation setup:** At runtime, `make_context(info_name, args, parent)` builds a `Context` from argv while looping over arguments and using `scope` to manage contextual state. [Clue: `make_context`; Clue: `scope`]

5. **Subcommand descent:** If the current command is a `Group`, it creates subcontexts (`_make_sub_context`) and resolves the next command token to a child command, using group-style lookup hooks evidenced by `get_command`, `list_commands`, and `resolve_command`. If resolution or usage is invalid, `fail(...)` raises a `UsageError`. [Clue: `Group`; Clue: core `fail`; Index: aliases and complex examples]

6. **Final handling:** Once the appropriate leaf command object is selected, execution is handed off to that command object. The exact method that invokes the original Python function is not shown in the provided excerpts, but that linkage is implied by the `command` decorator’s statement that it creates a `Command` from the decorated function. [Clue: `command`]

## 7) What is certain vs uncertain
### Certain from the evidence
- Decorated functions become `Command` objects. [Clue: `command`]
- Decorators attach parameter metadata such as options. [Clue: `option`; Clue: `_param_memo`]
- Nested CLIs are represented by `Group`, which is itself a `Command` and can nest commands or groups. [Clue: `Group`]
- Group registration/structure is tied to `add_command`, `list_commands`, and `_check_nested_chain`. [Clue: `Group`; Clue: `list_commands`; Clue: `_check_nested_chain`]
- Runtime processing builds contexts from argv and uses subcontexts for nested traversal. [Clue: `make_context`; Clue: `scope`; Clue: `Group`]
- Type conversion for parameters is driven by `convert_type`, with explicit handling for tuples and booleans shown in the drill-down. [Source snippet: `convert_type`; Source snippet: `Tuple`; Source snippet: `BoolParamType`]

### Not certain from the evidence
- the exact body of `resolve_command`;
- the exact parser/argv token consumption algorithm used during command dispatch;
- the exact method name/body that invokes the final callback. [Because those bodies are not present in the provided clue/snippet set]

## Final answer
So, using only the supplied clues, Click appears to turn decorated Python functions into a nested CLI by wrapping each function in a `Command` (`command(...)`), attaching parameter definitions like options during decoration (`option(...)`, `_param_memo`), and then registering those commands under `Group` objects, which can recursively contain more commands or groups. At runtime it builds a `Context` from argv (`make_context` + `scope`), descends through group/subcommand boundaries using subcontexts (`_make_sub_context`) and command-resolution hooks (`get_command`, `list_commands`, `resolve_command`), and then dispatches to the selected command object. Parameter values are interpreted through a `ParamType` layer (`convert_type`, `Tuple`, `BoolParamType`) that turns Python-facing type information into CLI parsing and validation behavior. The exact low-level resolution and final callback-invocation bodies are not present in the provided material, so those details cannot be stated more precisely without going beyond the evidence. [Clue: `command`; Clue: `option`; Clue: `_param_memo`; Clue: `Group`; Clue: `make_context`; Clue: `scope`; Clue: `list_commands`; Clue: `_check_nested_chain`; Source snippet: `convert_type`; Source snippet: `Tuple`; Source snippet: `BoolParamType`]
