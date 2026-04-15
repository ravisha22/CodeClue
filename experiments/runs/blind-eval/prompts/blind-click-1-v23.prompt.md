# Blind Evaluation Prompt - MRLF v2.1 with File 2 Drill-Down
# Task: blind-click-1

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

--- CLUE FILE (File 1) ---
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
  behavior: ACCUMULATE(loop -> out)

_check_nested_chain (src/click/core.py:73-90)
  sig: _check_nested_chain(base_command, cmd_name, cmd, register)
  behavior: GUARD(not_base_command.chain_or_not_is -> none); BRANCH(register -> result, else -> result)
  called_by: CommandCollection, add_command, Group
  raises: RuntimeError

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

_resolve_incomplete (src/click/shell_completion.py:623-667)
  Find the Click object that will handle the completion of the
  sig: _resolve_incomplete(ctx, args, incomplete)
  behavior: ACCUMULATE(loop -> result)
  calls: _is_incomplete_argument, _is_incomplete_option, _start_of_option
  called_by: get_completions, ShellComplete

shell_complete (src/click/shell_completion.py:19-54)
  Perform shell completion for the given CLI program.
  sig: shell_complete(cli, ctx_args, prog_name, complete_var, instruction)
  calls: complete, get_completion_class
  called_by: get_completions, ShellComplete

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
  behavior: DELEGATE(sorted -> result)

make_formatter (src/click/core.py:561-573)
  Creates the :class:`~click.HelpFormatter` for the help and
  behavior: DELEGATE(formatter_class -> result)
  called_by: Command

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

FuncParamType (src/click/types.py:171-192)
  extends: ParamType
  imports: enum, stat, gettext, exceptions, utils
  calls: fail
  called_by: convert_type
  uses: BadParameter (exceptions)

_join_param_hints (src/click/exceptions.py:19-23)
  sig: _join_param_hints(param_hint)
  behavior: GUARD(param_hint_and_not_isinstance_st -> /_join)
  called_by: BadParameter, MissingParameter

CommandCollection (src/click/core.py:1961-2014)
  A :class:`Group` that looks up subcommands on other groups.
  extends: Group
  imports: enum, errno, inspect, gettext, itertools
  calls: _check_nested_chain

_is_incomplete_argument (src/click/shell_completion.py:503-525)
  Determine if the given parameter is an argument that can still
  sig: _is_incomplete_argument(ctx, param)
  called_by: _resolve_incomplete

_is_incomplete_option (src/click/shell_completion.py:537-559)
  Determine if the given parameter is an option that needs a value.
  sig: _is_incomplete_option(ctx, args, param)
  behavior: ACCUMULATE(loop -> result); UNWIND(reversed)
  calls: _start_of_option
  called_by: _resolve_incomplete

_start_of_option (src/click/shell_completion.py:528-534)
  Check if the value looks like the start of an option.
  sig: _start_of_option(ctx, value)
  called_by: _is_incomplete_option, _resolve_incomplete

add_command (src/click/core.py:1622-1630)
  Registers another :class:`Command` with this group.
  sig: add_command(cmd, name)
  calls: _check_nested_chain
  called_by: Group
  raises: TypeError

complete (src/click/shell_completion.py:291-301)
  Produce the completion data to send back to the shell.
  calls: get_completions
  called_by: shell_complete

get_completion_class (src/click/shell_completion.py:456-463)
  Look up a registered :class:`ShellComplete` subclass by the name
  sig: get_completion_class(shell)
  behavior: DELEGATE(_available_shells.get -> result)
  called_by: shell_complete

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 17 with behavior annotations
drill: src/click/utils.py (~31 lines, _expand_args)
drill: src/click/core.py (~15 lines, _check_nested_chain)
drill: src/click/shell_completion.py (~49 lines, _resolve_incomplete)
drill: src/click/types.py (~40 lines, convert_type)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## _check_nested_chain  (src/click/core.py L73-90)
```
def _check_nested_chain(
    base_command: Group, cmd_name: str, cmd: Command, register: bool = False
) -> None:
    if not base_command.chain or not isinstance(cmd, Group):
        return

    if register:
        message = (
            f"It is not possible to add the group {cmd_name!r} to another"
            f" group {base_command.name!r} that is in chain mode."
        )
    else:
        message = (
            f"Found the group {cmd_name!r} as subcommand to another group "
            f" {base_command.name!r} that is in chain mode. This is not supported."
        )

    raise RuntimeError(message)
```

## _expand_args  (src/click/utils.py L578-628)
```
def _expand_args(
    args: cabc.Iterable[str],
    *,
    user: bool = True,
    env: bool = True,
    glob_recursive: bool = True,
) -> list[str]:
    """Simulate Unix shell expansion with Python functions.

    See :func:`glob.glob`, :func:`os.path.expanduser`, and
    :func:`os.path.expandvars`.

    This is intended for use on Windows, where the shell does not do any
    expansion. It may not exactly match what a Unix shell would do.

    :param args: List of command line arguments to expand.
    :param user: Expand user home directory.
    :param env: Expand environment variables.
    :param glob_recursive: ``**`` matches directories recursively.

    .. versionchanged:: 8.1
        Invalid glob patterns are treated as empty expansions rather
        than raising an error.

    .. versionadded:: 8.0

    :meta private:
    """
    from glob import glob

    out = []

    for arg in args:
        if user:
            arg = os.path.expanduser(arg)

        if env:
            arg = os.path.expandvars(arg)

        try:
            matches = glob(arg, recursive=glob_recursive)
        except re.error:
            matches = []

        if not matches:
            out.append(arg)
        else:
            out.extend(matches)

    return out
```

## convert_type  (src/click/types.py L1112-1169)
```
def convert_type(ty: t.Any | None, default: t.Any | None = None) -> ParamType:
    """Find the most appropriate :class:`ParamType` for the given Python
    type. If the type isn't provided, it can be inferred from a default
    value.
    """
    guessed_type = False

    if ty is None and default is not None:
        if isinstance(default, (tuple, list)):
            # If the default is empty, ty will remain None and will
            # return STRING.
            if default:
                item = default[0]

                # A tuple of tuples needs to detect the inner types.
                # Can't call convert recursively because that would
                # incorrectly unwind the tuple to a single type.
                if isinstance(item, (tuple, list)):
                    ty = tuple(map(type, item))
                else:
                    ty = type(item)
        else:
            ty = type(default)

        guessed_type = True

    if isinstance(ty, tuple):
        return Tuple(ty)

    if isinstance(ty, ParamType):
        return ty

    if ty is str or ty is None:
        return STRING

    if ty is int:
        return INT

    if ty is float:
        return FLOAT

    if ty is bool:
        return BOOL

    if guessed_type:
        return STRING

    if __debug__:
        try:
            if issubclass(ty, ParamType):
                raise AssertionError(
                    f"Attempted to use an uninstantiated parameter type ({ty})."
                )
        except TypeError:
            # ty is an instance (correct), so issubclass fails.
            pass

    return FuncParamType(ty)
```

## _resolve_incomplete  (src/click/shell_completion.py L623-667)
```
def _resolve_incomplete(
    ctx: Context, args: list[str], incomplete: str
) -> tuple[Command | Parameter, str]:
    """Find the Click object that will handle the completion of the
    incomplete value. Return the object and the incomplete value.

    :param ctx: Invocation context for the command represented by
        the parsed complete args.
    :param args: List of complete args before the incomplete value.
    :param incomplete: Value being completed. May be empty.
    """
    # Different shells treat an "=" between a long option name and
    # value differently. Might keep the value joined, return the "="
    # as a separate item, or return the split name and value. Always
    # split and discard the "=" to make completion easier.
    if incomplete == "=":
        incomplete = ""
    elif "=" in incomplete and _start_of_option(ctx, incomplete):
        name, _, incomplete = incomplete.partition("=")
        args.append(name)

    # The "--" marker tells Click to stop treating values as options
    # even if they start with the option character. If it hasn't been
    # given and the incomplete arg looks like an option, the current
    # command will provide option name completions.
    if "--" not in args and _start_of_option(ctx, incomplete):
        return ctx.command, incomplete

    params = ctx.command.get_params(ctx)

    # If the last complete arg is an option name with an incomplete
    # value, the option will provide value completions.
    for param in params:
        if _is_incomplete_option(ctx, args, param):
            return param, incomplete

    # It's not an option name or value. The first argument without a
    # parsed value will provide value completions.
    for param in params:
        if _is_incomplete_argument(ctx, param):
            return param, incomplete

    # There were no unparsed arguments, the command may be a group that
    # will provide command name completions.
    return ctx.command, incomplete
```

## _is_incomplete_argument  (src/click/shell_completion.py L503-525)
```
def _is_incomplete_argument(ctx: Context, param: Parameter) -> bool:
    """Determine if the given parameter is an argument that can still
    accept values.

    :param ctx: Invocation context for the command represented by the
        parsed complete args.
    :param param: Argument object being checked.
    """
    if not isinstance(param, Argument):
        return False

    assert param.name is not None
    # Will be None if expose_value is False.
    value = ctx.params.get(param.name)
    return (
        param.nargs == -1
        or ctx.get_parameter_source(param.name) is not ParameterSource.COMMANDLINE
        or (
            param.nargs > 1
            and isinstance(value, (tuple, list))
            and len(value) < param.nargs
        )
    )
```

## _is_incomplete_option  (src/click/shell_completion.py L537-559)
```
def _is_incomplete_option(ctx: Context, args: list[str], param: Parameter) -> bool:
    """Determine if the given parameter is an option that needs a value.

    :param args: List of complete args before the incomplete value.
    :param param: Option object being checked.
    """
    if not isinstance(param, Option):
        return False

    if param.is_flag or param.count:
        return False

    last_option = None

    for index, arg in enumerate(reversed(args)):
        if index + 1 > param.nargs:
            break

        if _start_of_option(ctx, arg):
            last_option = arg
            break

    return last_option is not None and last_option in param.opts
```

## _start_of_option  (src/click/shell_completion.py L528-534)
```
def _start_of_option(ctx: Context, value: str) -> bool:
    """Check if the value looks like the start of an option."""
    if not value:
        return False

    c = value[0]
    return c in ctx._opt_prefixes
```

## FuncParamType  (src/click/types.py L171-192)
```
class FuncParamType(ParamType):
    def __init__(self, func: t.Callable[[t.Any], t.Any]) -> None:
        self.name: str = func.__name__
        self.func = func

    def to_info_dict(self) -> dict[str, t.Any]:
        info_dict = super().to_info_dict()
        info_dict["func"] = self.func
        return info_dict

    def convert(
        self, value: t.Any, param: Parameter | None, ctx: Context | None
    ) -> t.Any:
        try:
            return self.func(value)
        except ValueError:
            try:
                value = str(value)
            except UnicodeError:
                value = value.decode("utf-8", "replace")

            self.fail(value, param, ctx)
```

## Tuple  (src/click/types.py L1060-1109)
```
class Tuple(CompositeParamType):
    """The default behavior of Click is to apply a type on a value directly.
    This works well in most cases, except for when `nargs` is set to a fixed
    count and different types should be used for different items.  In this
    case the :class:`Tuple` type can be used.  This type can only be used
    if `nargs` is set to a fixed number.

    For more information see :ref:`tuple-type`.

    This can be selected by using a Python tuple literal as a type.

    :param types: a list of types that should be used for the tuple items.
    """

    def __init__(self, types: cabc.Sequence[type[t.Any] | ParamType]) -> None:
        self.types: cabc.Sequence[ParamType] = [convert_type(ty) for ty in types]

    def to_info_dict(self) -> dict[str, t.Any]:
        info_dict = super().to_info_dict()
        info_dict["types"] = [t.to_info_dict() for t in self.types]
        return info_dict

    @property
    def name(self) -> str:  # type: ignore
        return f"<{' '.join(ty.name for ty in self.types)}>"

    @property
    def arity(self) -> int:  # type: ignore
        return len(self.types)

    def convert(
        self, value: t.Any, param: Parameter | None, ctx: Context | None
    ) -> t.Any:
        len_type = len(self.types)
        len_value = len(value)

        if len_value != len_type:
            self.fail(
                ngettext(
                    "{len_type} values are required, but {len_value} was given.",
                    "{len_type} values are required, but {len_value} were given.",
                    len_value,
                ).format(len_type=len_type, len_value=len_value),
                param=param,
                ctx=ctx,
            )

        return tuple(
            ty(x, param, ctx) for ty, x in zip(self.types, value, strict=False)
        )
```

## __enter__  (tests/test_context.py L602-604)
```
        def __enter__(self) -> list[int]:
            self.val = [self._base_val]
            return self.val
```

## __exit__  (tests/test_context.py L606-617)
```
        def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_value: BaseException | None,
            traceback: TracebackType | None,
        ) -> bool | None:
            if not exc_type:
                self.val[0] = self._base_val - 1
                return None

            self.val[0] = self._base_val + 1
            return self._handle_exception
```

## __getattr__  (src/click/utils.py L519-522)
```
    def __getattr__(self, attr: str) -> t.Any:
        return getattr(self.wrapped, attr)


```

## __init__  (tests/test_utils.py L682-685)
```
    def __init__(self, package_name):
        self.__package__ = package_name


```

## __iter__  (tests/test_termui.py L55-56)
```
        def __iter__(self):
            return self
```

## __repr__  (src/click/utils.py L146-149)
```
    def __repr__(self) -> str:
        if self._f is not None:
            return repr(self._f)
        return f"<unopened file '{format_filename(self.name)}' {self.mode}>"
```

## KeepOpenFile  (src/click/utils.py L197-219)
```
class KeepOpenFile:
    def __init__(self, file: t.IO[t.Any]) -> None:
        self._file: t.IO[t.Any] = file

    def __getattr__(self, name: str) -> t.Any:
        return getattr(self._file, name)

    def __enter__(self) -> KeepOpenFile:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        pass

    def __repr__(self) -> str:
        return repr(self._file)

    def __iter__(self) -> cabc.Iterator[t.AnyStr]:
        return iter(self._file)
```

## close  (src/click/utils.py L169-172)
```
    def close(self) -> None:
        """Closes the underlying file, no matter what."""
        if self._f is not None:
            self._f.close()
```

## close_intelligently  (src/click/utils.py L174-179)
```
    def close_intelligently(self) -> None:
        """This function only closes the file if it was opened by the lazy
... (truncated)
```
--- END SOURCE SNIPPETS ---

QUESTION: How does Click turn decorated Python functions into a nested CLI and then dispatch the right subcommand at runtime?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
