# v2.4 Ablation (File 1 Only): blind-click-1
Date: 2026-04-16

Click turns a decorated Python function into a CLI command with the `command` decorator: that entry “creates a new `Command` and uses the decorated function as” the command, and its `UNWIND(reversed)` behavior strongly suggests it finalizes previously attached parameter metadata in reverse decoration order. [command (src/click/decorators.py:168-255)]

Options and arguments are attached earlier as metadata. The `option` decorator “attaches an option to the command” by calling `_param_memo`, and the `argument` decorator also calls `_param_memo`. [option (src/click/decorators.py:352-377); argument (src/click/decorators.py:324-349); _param_memo (src/click/decorators.py:314)]

Nested CLIs are represented by `Group`, which is a `Command` subclass whose purpose is to “nest other commands (or more groups).” At runtime it manages command execution by calling `make_context`, `_make_sub_context`, `add_command`, and `_process_result`. [Group (src/click/core.py:1503-1951)]

Subcommands are registered with `add_command`, and Click validates chaining constraints with `_check_nested_chain`; if chain mode conflicts with nested groups, `_check_nested_chain` raises `RuntimeError`. `CommandCollection` is a specialized `Group` that looks up subcommands on other groups and also uses `_check_nested_chain`. [add_command (src/click/core.py:1622-1630); _check_nested_chain (src/click/core.py:73-90); CommandCollection (src/click/core.py:1961-2014)]

For discovery/selection, `list_commands` returns subcommand names in sorted order. [list_commands (src/click/core.py:1784-1786)]

What I cannot determine from this clue file: the exact runtime argv-to-subcommand resolution algorithm, because the clue does not expose the body of `resolve_command` in this prompt. I can see that `Group` creates contexts/subcontexts and processes results, but not the full dispatch branch logic. [Group (src/click/core.py:1503-1951); GAPS]
