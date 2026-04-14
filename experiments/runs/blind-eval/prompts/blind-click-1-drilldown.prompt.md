# Blind Evaluation Prompt - MRLF v2.1
# Task: blind-click-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

--- CLUE FILE START ---
=CC v2.1 click@HEAD 63mod 1620sym
? How does Click turn decorated Python functions into a nested CLI and then dispatch the right subcommand at runtime?


-- TREE
docs/  (1 files)
examples/  (14 files)
  aliases/  colors/  completion/  imagepipe/  inout/  naval/  repo/  termui/  validation/
src/  (17 files)
  click/
tests/  (31 files)
  typing/

-- INDEX
docs/conf.py                                     57L  
examples/aliases/aliases.py                     143L  get_command, resolve_command, AliasedGroup, add_alias, read_config
examples/colors/colors.py                        39L  cli
examples/completion/completion.py                56L  cli, get_env_vars, group, list_users, ls
examples/complex/complex/__init__.py              0L  
examples/complex/complex/cli.py                  60L  get_command, list_commands, ComplexCLI, log, vlog
examples/complex/complex/commands/__init__.py     0L  
examples/complex/complex/commands/cmd_init.py    13L  cli
examples/complex/complex/commands/cmd_status.py    11L  cli
examples/imagepipe/imagepipe.py                 288L  blur_cmd, cli, convert_flip, convert_rotation, copy_filename
examples/inout/inout.py                          30L  cli
examples/naval/naval.py                          72L  cli, mine, mine_remove, mine_set, ship
examples/repo/repo.py                           166L  set_config, Repo, cli, clone, commit
examples/termui/termui.py                       169L  clear, cli, colordemo, edit, locate
examples/validation/validation.py                48L  convert, URL, cli, validate_count
src/click/__init__.py                           123L  
src/click/_compat.py                            622L  close, name, read1, readable, seekable
src/click/_termui_impl.py                       852L  edit, edit, edit, edit_files, get_editor
src/click/_textwrap.py                           51L  extra_indent, indent_only, TextWrapper
src/click/_utils.py                              36L  Sentinel
  ...and 43 more modules

-- SYM
_close_with_exception_info          M src/click/core.py:623    Unwind the exit stack by calling its :meth:`__e...
__exit__                            M src/click/core.py:481    function __exit__
fail                                M src/click/types.py:136    Helper method to fail with an invalid value mes...
copy_filename                       M examples/imagepipe/imagepipe.py:69     function copy_filename
_param_memo                         M src/click/decorators.py:314    function _param_memo
write                               M src/click/formatting.py:135    Writes a unicode string into the internal buffer.
_split_opt                          M src/click/parser.py:111    function _split_opt
format_progress_line                M src/click/_termui_impl.py:209    function format_progress_line
option                              M src/click/decorators.py:352    Attaches an option to the command.
is_ascii_encoding                   M src/click/_compat.py:40     Checks if a given encoding is ascii.
Py_buffer                           C src/click/_winconsole.py:87     class Py_buffer
render_progress                     M src/click/_termui_impl.py:236    function render_progress
get_help_option_names               M src/click/core.py:1046   Returns the names for the help option.
_force_correct_text_stream          M src/click/_compat.py:238    function _force_correct_text_stream
get_buffer                          M src/click/_winconsole.py:105    function get_buffer
get_help_option                     M src/click/core.py:1054   Returns the help option object.
_is_binary_writer                   M src/click/_compat.py:160    function _is_binary_writer
_get_value_from_state               M src/click/parser.py:429    function _get_value_from_state
normalize_choice                    M src/click/types.py:288    Normalize a choice value, used to map a passed ...
_check_iter                         M src/click/core.py:2017   Check if the value is iterable but not a string.
split_arg_string                    M src/click/shell_completion.py:466    Split an argument string as with :func:`shlex.s...
_start_of_option                    M src/click/shell_completion.py:528    Check if the value looks like the start of an o...
get_params                          M src/click/core.py:1002   function get_params
_normalize_opt                      M src/click/parser.py:120    function _normalize_opt
_format_default                     M src/click/termui.py:76     function _format_default
_fetch                              M src/click/parser.py:68     function _fetch
_check_nested_chain                 M src/click/core.py:73     function _check_nested_chain
close                               M src/click/core.py:616    Invoke all close callbacks registered with
close                               M src/click/_compat.py:463    function close
_find_binary_writer                 M src/click/_compat.py:191    function _find_binary_writer
_is_compat_stream_attr              M src/click/_compat.py:218    A stream attribute is compatible if it is equal...
get_completions                     M src/click/shell_completion.py:271    Determine the context and last complete command...
log                                 M examples/complex/complex/cli.py:15     Logs a message to stderr.
_join_param_hints                   M src/click/exceptions.py:19     function _join_param_hints
flush                               M src/click/utils.py:510    function flush
_is_binary_reader                   M src/click/_compat.py:151    function _is_binary_reader
_FixupStream                        C src/click/_compat.py:82     The new io interface needs more from streams th...
_is_jupyter_kernel_output           M src/click/_compat.py:492    function _is_jupyter_kernel_output
_interpret_color                    M src/click/termui.py:507    function _interpret_color
_flush_par                          M src/click/formatting.py:72     function _flush_par
close                               M src/click/utils.py:169    Closes the underlying file, no matter what.
_get_windows_console_stream         M src/click/_compat.py:562    function _get_windows_console_stream
_normalized_mapping                 M src/click/types.py:270    Returns mapping where keys are the original cho...
set_config                          M examples/repo/repo.py:14     function set_config
ConsoleStream                       C src/click/_winconsole.py:194    class ConsoleStream
_build_prompt                       M src/click/termui.py:60     function _build_prompt
_process_opts                       M src/click/parser.py:469    function _process_opts
_unpack_args                        M src/click/parser.py:51     Given an iterable of arguments and an iterable ...
update                              M src/click/_termui_impl.py:304    Update the progress bar by advancing a specifie...
_is_compatible_text_stream          M src/click/_compat.py:227    Check if a stream's encoding and errors attribu...
_make_text_stream                   M src/click/_compat.py:19     function _make_text_stream
_stream_is_misconfigured            M src/click/_compat.py:209    A stream is misconfigured if its encoding is AS...
check_iter                          M src/click/core.py:2352   function check_iter
fail                                M src/click/core.py:718    Aborts the execution of the program with a spec...
exit                                M src/click/core.py:730    Exits the application with a given exit code.
format_bar                          M src/click/_termui_impl.py:190    function format_bar
format_eta                          M src/click/_termui_impl.py:166    function format_eta
format_pct                          M src/click/_termui_impl.py:187    function format_pct
format_pos                          M src/click/_termui_impl.py:181    function format_pos
scope                               M src/click/core.py:496    This helper method can be used with the context...
get_short_help_str                  M src/click/core.py:1097   Gets short help for the command or makes it by ...
make_step                           M src/click/_termui_impl.py:282    function make_step
_find_binary_reader                 M src/click/_compat.py:173    function _find_binary_reader
find_object                         M src/click/core.py:667    Finds the closest object of a given type.
_resolve_context                    M src/click/shell_completion.py:562    Produce the context hierarchy starting with the...
_resolve_incomplete                 M src/click/shell_completion.py:623    Find the Click object that will handle the comp...
shell_complete                      M src/click/shell_completion.py:19     Perform shell completion for the given CLI prog...
_Argument                           C src/click/parser.py:181    class _Argument
render_finish                       M src/click/_termui_impl.py:142    function render_finish
_force_correct_text_writer          M src/click/_compat.py:300    function _force_correct_text_writer
_NonClosingTextIOWrapper            C src/click/_compat.py:56     class _NonClosingTextIOWrapper
get_best_encoding                   M src/click/_compat.py:48     Returns the default stream encoding if not found.
  ...and 579 more symbols

-- FOCUS
_expand_args (src/click/utils.py:578-628)
  Simulate Unix shell expansion with Python functions.
  sig: _expand_args(args)
  behavior: ACCUMULATE(loop)

_check_nested_chain (src/click/core.py:73-90)
  sig: _check_nested_chain(base_command, cmd_name, cmd, register)
  behavior: GUARD(chain_base_command_isinstance); BRANCH(register)
  called_by: CommandCollection, add_command, Group
  raises: RuntimeError

_resolve_incomplete (src/click/shell_completion.py:623-667)
  Find the Click object that will handle the completion of the
  sig: _resolve_incomplete(ctx, args, incomplete)
  behavior: ACCUMULATE(loop); BRANCH(incomplete)
  calls: _is_incomplete_argument, _is_incomplete_option, _start_of_option
  called_by: get_completions, ShellComplete

shell_complete (src/click/shell_completion.py:19-54)
  Perform shell completion for the given CLI program.
  sig: shell_complete(cli, ctx_args, prog_name, complete_var, instruction)
  calls: complete, get_completion_class
  called_by: get_completions, ShellComplete

convert_type (src/click/types.py:1112-1169)
  Find the most appropriate :class:`ParamType` for the given Python
  sig: convert_type(ty, default)
  calls: FuncParamType, Tuple
  called_by: Choice, Tuple
  raises: AssertionError

Tuple (src/click/types.py:1060-1109)
  The default behavior of Click is to apply a type on a value directly.
  extends: CompositeParamType
  imports: enum, stat, gettext, exceptions, utils
  calls: fail, convert_type
  called_by: convert_type
  uses: BadParameter (exceptions)

Abort (src/click/exceptions.py:294-295)
  An internal signalling exception that signals Click to abort.
  extends: RuntimeError
  imports: gettext, globals, utils, core

ClickException (src/click/exceptions.py:26-53)
  An exception that Click can handle and show to the user.
  extends: Exception
  attrs: exit_code=1
  imports: gettext, globals, utils, core

ComplexCLI (examples/complex/complex/cli.py:31-45)
  extends: Group
  imports: click

FloatRange (src/click/types.py:618-658)
  Restrict a :data:`click.FLOAT` value to a range of accepted
  extends: _NumberRangeBase, FloatParamType
  attrs: name='float range'
  imports: enum, stat, gettext, exceptions, utils
  raises: RuntimeError, TypeError

IntRange (src/click/types.py:584-607)
  Restrict an :data:`click.INT` value to a range of accepted
  extends: _NumberRangeBase, IntParamType
  attrs: name='integer range'
  imports: enum, stat, gettext, exceptions, utils

MissingParameter (src/click/exceptions.py:137-205)
  Raised if click required an option or argument but it was not
  extends: BadParameter
  imports: gettext, globals, utils, core
  calls: _join_param_hints

NoSuchOption (src/click/exceptions.py:208-239)
  Raised if click attempted to handle an option that does not
  extends: UsageError
  imports: gettext, globals, utils, core

cli (examples/termui/termui.py:9-11)
  This script showcases different terminal UI helpers in Click.

cli (examples/completion/completion.py:8-9)
  calls: group

command (src/click/decorators.py:168-255)
  Creates a new :class:`Command` and uses the decorated function as
  sig: command(name, cls)
  behavior: UNWIND(reversed)
  raises: TypeError

get_current_context (src/click/globals.py:20-41)
  Returns the current click context.
  sig: get_current_context(silent)
  raises: RuntimeError

list_commands (src/click/core.py:1784-1786)
  Returns a list of subcommand names in the order they should appear.
  sig: list_commands(ctx)
  behavior: DELEGATE(sorted)

make_formatter (src/click/core.py:561-573)
  Creates the :class:`~click.HelpFormatter` for the help and
  behavior: DELEGATE(formatter_class)
  called_by: Command

Command (src/click/core.py:873-1485)
  Commands are the basic building block of command line interfaces in
  attrs: allow_extra_args=False, allow_interspersed_args=True, ignore_unknown_options=False
  imports: enum, errno, inspect, gettext, itertools
  calls: _main_shell_completion, format_epilog, format_help, format_help_text, format_usage, get_help_option, get_help_option_names, get_params
  raises: NoArgsIsHelpError, Abort
  uses: Exit (exceptions), UsageError (exceptions)

Group (src/click/core.py:1503-1951)
  A group is a command that nests other commands (or more groups).
  extends: Command
  attrs: allow_extra_args=True, allow_interspersed_args=False
  imports: enum, errno, inspect, gettext, itertools
  calls: get_short_help_str, make_context, _make_sub_context, fail, scope, add_command, format_commands, _process_result
  raises: TypeError, NoArgsIsHelpError, RuntimeError
  uses: UsageError (exceptions)

fail (src/click/types.py:136-143)
  Helper method to fail with an invalid value message.
  sig: fail(message, param, ctx)
  called_by: BoolParamType, Choice, DateTime, File, FuncParamType, Path, Tuple, UUIDParameterType
  raises: BadParameter
  uses: BadParameter (exceptions)

Choice (src/click/types.py:233-398)
  The choice type allows a value to be checked against a fixed set
  extends: ParamType
  attrs: name='choice'
  imports: enum, stat, gettext, exceptions, utils
  calls: _normalized_mapping, get_invalid_choice_message, normalize_choice, fail, convert_type
  uses: BadParameter (exceptions)

fail (src/click/core.py:718-724)
  Aborts the execution of the program with a specific error
  sig: fail(message)
  called_by: Command, resolve_command, Group
  raises: UsageError
  uses: UsageError (exceptions)

get_short_help_str (src/click/core.py:1097-1118)
  Gets short help for the command or makes it by shortening the
  sig: get_short_help_str(limit)
  behavior: BRANCH(short_help_self)
  called_by: Command, format_commands, Group

_complete_visible_commands (src/click/core.py:54-70)
  List all the subcommands of a group that start with the
  sig: _complete_visible_commands(ctx, incomplete)
  behavior: ACCUMULATE(loop)
  called_by: Command, Group

make_context (src/click/core.py:1182-1217)
  This function when given an info name and arguments will kick
  sig: make_context(info_name, args, parent)
  behavior: ACCUMULATE(loop)
  calls: scope
  called_by: Command, Group

scope (src/click/core.py:496-531)
  This helper method can be used with the context object to promote
  sig: scope(cleanup)
  called_by: make_context, Command, Group

ShellComplete (src/click/shell_completion.py:200-301)
  Base class for providing shell completion support.
  imports: gettext, core, utils, shlex, shutil
  calls: get_completions, source_vars, _resolve_context, _resolve_incomplete, shell_complete
  raises: NotImplementedError

get_completions (src/click/shell_completion.py:271-281)
  Determine the context and last complete command or parameter
  sig: get_completions(args, incomplete)
  calls: _resolve_context, _resolve_incomplete, shell_complete
  called_by: complete, ShellComplete

FuncParamType (src/click/types.py:171-192)
  extends: ParamType
  imports: enum, stat, gettext, exceptions, utils
  calls: fail
  called_by: convert_type
  uses: BadParameter (exceptions)

format_help (src/click/core.py:1120-1135)
  Writes the help into the formatter if it exists.
  sig: format_help(ctx, formatter)
  calls: format_epilog, format_help_text, format_usage
  called_by: Command

_join_param_hints (src/click/exceptions.py:19-23)
  sig: _join_param_hints(param_hint)
  behavior: GUARD(param_hint_isinstance_str)
  called_by: BadParameter, MissingParameter

_normalized_mapping (src/click/types.py:270-286)
  Returns mapping where keys are the original choices and the values are
  sig: _normalized_mapping(ctx)
  calls: normalize_choice
  called_by: get_invalid_choice_message, Choice

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 70 symbols in L3, 17 with behavior annotations
drill: src/click/shell_completion.py (~26 lines, shell_complete)
drill: src/click/types.py (~40 lines, convert_type)
drill: src/click/types.py (~45 lines, Tuple)

--- CLUE FILE END ---

QUESTION: How does Click turn decorated Python functions into a nested CLI and then dispatch the right subcommand at runtime?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
