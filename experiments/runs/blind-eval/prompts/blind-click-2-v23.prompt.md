# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: blind-click-2

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.

--- CLUE FILE (File 1) ---
=CC v2.1 click@HEAD 63mod 1620sym
? When an option or argument value is not provided directly on the command line, how does Click decide what value to use, and what extra work do file and path types perform during conversion?


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
_is_incomplete_option (src/click/shell_completion.py:537-559)
  Determine if the given parameter is an option that needs a value.
  sig: _is_incomplete_option(ctx, args, param)
  behavior: ACCUMULATE(enumerate(reversed(ar... -> result); UNWIND(reversed)
  calls: _start_of_option
  called_by: _resolve_incomplete

_start_of_option (src/click/shell_completion.py:528-534)
  Check if the value looks like the start of an option.
  sig: _start_of_option(ctx, value)
  called_by: _is_incomplete_option, _resolve_incomplete

coerce_path_result (src/click/types.py:955-966)
  sig: coerce_path_result(value)
  called_by: Path

get_help_option (src/click/core.py:1054-1079)
  Returns the help option object.
  sig: get_help_option(ctx)
  calls: get_help_option_names
  called_by: get_params, Command

get_help_option_names (src/click/core.py:1046-1052)
  Returns the names for the help option.
  sig: get_help_option_names(ctx)
  behavior: ACCUMULATE(self.params loop -> result)
  called_by: get_help_option, Command

get_help_extra (src/click/core.py:3052-3134)
  sig: get_help_extra(ctx)
  called_by: Option

OptionHelpExtra (src/click/types.py:1205-1209)
  extends: TypedDict
  imports: enum, stat, gettext, exceptions, utils

Path (src/click/types.py:879-1057)
  The ``Path`` type is similar to the :class:`File` type, but
  extends: ParamType
  imports: enum, stat, gettext, exceptions, utils
  calls: fail, coerce_path_result
  uses: BadParameter (exceptions)

command_path (src/click/core.py:642-658)
  The computed command path.
  calls: get_params

Command (src/click/core.py:873-1485)
  Commands are the basic building block of command line interfaces in
  attrs: allow_extra_args=False, allow_interspersed_args=True, ignore_unknown_options=False
  imports: enum, errno, inspect, gettext, itertools
  calls: _main_shell_completion, format_epilog, format_help, format_help_text, format_usage, get_help_option, get_help_option_names, get_params
  raises: NoArgsIsHelpError, Abort
  uses: Exit (exceptions), UsageError (exceptions)

option (src/click/decorators.py:352-377)
  Attaches an option to the command.
  calls: _param_memo
  called_by: confirmation_option, help_option, password_option, version_option

open_file (src/click/utils.py:358-404)
  Open a file, with extra behavior to handle ``'-'`` to indicate
  sig: open_file(filename, mode, encoding, errors, lazy...)
  calls: KeepOpenFile, LazyFile

Option (src/click/core.py:2646-3335)
  Options are usually optional values on the command line and
  extends: Parameter
  attrs: param_type_name='option'
  imports: enum, errno, inspect, gettext, itertools
  calls: get_help_extra, _write_opts, prompt_for_value, batch
  raises: TypeError, ValueError

BadArgumentUsage (src/click/exceptions.py:259-265)
  Raised if an argument is generally supplied but the use of the argument
  extends: UsageError
  imports: gettext, globals, utils, core

BadOptionUsage (src/click/exceptions.py:242-256)
  Raised if an option is generally supplied but the use of the option
  extends: UsageError
  imports: gettext, globals, utils, core

NoSuchOption (src/click/exceptions.py:208-239)
  Raised if click attempted to handle an option that does not
  extends: UsageError
  imports: gettext, globals, utils, core

argument (src/click/decorators.py:324-349)
  Attaches an argument to the command.
  calls: _param_memo

consume_value (src/click/core.py:3256-3318)
  For :class:`Option`, the value can be collected from an interactive prompt
  sig: consume_value(ctx, opts)

File (src/click/types.py:754-872)
  Declares a parameter to be a file for reading or writing.
  extends: ParamType
  attrs: name='filename'
  imports: enum, stat, gettext, exceptions, utils
  calls: resolve_lazy_flag, fail, _is_file_like
  uses: BadParameter (exceptions)

_is_file_like (src/click/types.py:875-876)
  sig: _is_file_like(value)
  called_by: File

split_envvar_value (src/click/types.py:126-134)
  Given a value from an environment variable this splits it up
  sig: split_envvar_value(rv)
  behavior: DELEGATE(boolop.split -> result)

add_option (src/click/parser.py:261-284)
  Adds a new option named `dest` to the parser.
  sig: add_option(obj, opts, dest, action, nargs...)
  behavior: ACCUMULATE(option._short_opts loop -> result)
  calls: _Option, _normalize_opt

process_value (src/click/core.py:2416-2480)
  Process the value of this parameter:
  sig: process_value(ctx, value)
  behavior: BRANCH(value is UNSET -> result, else -> self.type_cast_value(...)
  raises: MissingParameter
  uses: MissingParameter (exceptions)

_get_value_from_state (src/click/parser.py:429-467)
  sig: _get_value_from_state(option_name, option, state)
  called_by: _match_long_opt, _match_short_opt, _OptionParser
  raises: BadOptionUsage
  uses: BadOptionUsage (exceptions)

LazyFile (src/click/utils.py:109-194)
  A lazy file works like a regular file but it does not fully open
  imports: types, globals, typing_extensions, glob, exceptions
  calls: close, close_intelligently, open, format_filename
  called_by: open_file
  raises: FileError
  uses: FileError (exceptions)

_OptionParser (src/click/parser.py:220-499)
  The option parser is an internal class that is ultimately used to
  imports: gettext, exceptions, core, warnings, shell_completion
  calls: _Argument, _Option, _get_value_from_state, _match_long_opt, _match_short_opt, _process_args_for_args, _process_args_for_options, _process_opts
  raises: NoSuchOption, BadOptionUsage
  uses: BadOptionUsage (exceptions), NoSuchOption (exceptions)

type_cast_value (src/click/core.py:2342-2396)
  Convert and validate a value against the parameter's
  sig: type_cast_value(ctx, value)
  calls: check_iter, _check_iter
  called_by: Context, Parameter
  raises: BadParameter
  uses: BadParameter (exceptions)

_Argument (src/click/parser.py:181-209)
  imports: gettext, exceptions, core, warnings, shell_completion
  called_by: add_argument, _OptionParser
  raises: BadArgumentUsage

_Option (src/click/parser.py:127-178)
  imports: gettext, exceptions, core, warnings, shell_completion
  calls: _split_opt
  called_by: add_option, _OptionParser
  raises: ValueError

KeepOpenFile (src/click/utils.py:197-219)
  imports: types, globals, typing_extensions, glob, exceptions
  called_by: open_file

_is_incomplete_argument (src/click/shell_completion.py:503-525)
  Determine if the given parameter is an argument that can still
  sig: _is_incomplete_argument(ctx, param)
  called_by: _resolve_incomplete

add_argument (src/click/parser.py:286-292)
  Adds a positional argument named `dest` to the parser.
  sig: add_argument(obj, dest, nargs)
  calls: _Argument

add_command (src/click/core.py:1622-1630)
  Registers another :class:`Command` with this group.
  sig: add_command(cmd, name)
  calls: _check_nested_chain
  called_by: Group
  raises: TypeError

confirmation_option (src/click/decorators.py:380-401)
  Add a ``--yes`` option which shows a prompt before continuing if
  calls: option

help_option (src/click/decorators.py:527-551)
  Pre-configured ``--help`` option which immediately prints the help page
  calls: option

password_option (src/click/decorators.py:404-418)
  Add a ``--password`` option which prompts for a password, hiding
  calls: option

resolve_command (src/click/core.py:1907-1932)
  sig: resolve_command(ctx, args)
  calls: fail
  called_by: Group

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 15 with behavior annotations
uncovered: _process_args_for_options, _find_binary_reader, _WindowsConsoleReader, _force_correct_text_reader
drill: src/click/core.py (~18 lines, command_path)
drill: src/click/decorators.py (~24 lines, option)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## command_path  (src/click/core.py L642-658)
```
    def command_path(self) -> str:
        """The computed command path.  This is used for the ``usage``
        information on the help page.  It's automatically created by
        combining the info names of the chain of contexts to the root.
        """
        rv = ""
        if self.info_name is not None:
            rv = self.info_name
        if self.parent is not None:
            parent_command_path = [self.parent.command_path]

            if isinstance(self.parent.command, Command):
                for param in self.parent.command.get_params(self):
                    parent_command_path.extend(param.get_usage_pieces(self))

            rv = f"{' '.join(parent_command_path)} {rv}"
        return rv.lstrip()
```

## option  (src/click/decorators.py L352-377)
```
def option(
    *param_decls: str, cls: type[Option] | None = None, **attrs: t.Any
) -> t.Callable[[FC], FC]:
    """Attaches an option to the command.  All positional arguments are
    passed as parameter declarations to :class:`Option`; all keyword
    arguments are forwarded unchanged (except ``cls``).
    This is equivalent to creating an :class:`Option` instance manually
    and attaching it to the :attr:`Command.params` list.

    For the default option class, refer to :class:`Option` and
    :class:`Parameter` for descriptions of parameters.

    :param cls: the option class to instantiate.  This defaults to
                :class:`Option`.
    :param param_decls: Passed as positional arguments to the constructor of
        ``cls``.
    :param attrs: Passed as keyword arguments to the constructor of ``cls``.
    """
    if cls is None:
        cls = Option

    def decorator(f: FC) -> FC:
        _param_memo(f, cls(param_decls, **attrs))
        return f

    return decorator
```

## get_params  (src/click/core.py L1002-1025)
```
    def get_params(self, ctx: Context) -> list[Parameter]:
        params = self.params
        help_option = self.get_help_option(ctx)

        if help_option is not None:
            params = [*params, help_option]

        if __debug__:
            import warnings

            opts = [opt for param in params for opt in param.opts]
            opts_counter = Counter(opts)
            duplicate_opts = (opt for opt, count in opts_counter.items() if count > 1)

            for duplicate_opt in duplicate_opts:
                warnings.warn(
                    (
                        f"The parameter {duplicate_opt} is used more than once. "
                        "Remove its duplicate as parameters should be unique."
                    ),
                    stacklevel=3,
                )

        return params
```

## _param_memo  (src/click/decorators.py L314-321)
```
def _param_memo(f: t.Callable[..., t.Any], param: Parameter) -> None:
    if isinstance(f, Command):
        f.params.append(param)
    else:
        if not hasattr(f, "__click_params__"):
            f.__click_params__ = []  # type: ignore

        f.__click_params__.append(param)  # type: ignore
```

## decorator  (src/click/decorators.py L115-121)
```
    def decorator(f: t.Callable[te.Concatenate[T, P], R]) -> t.Callable[P, R]:
        def new_func(*args: P.args, **kwargs: P.kwargs) -> R:
            ctx = get_current_context()
            obj = ctx.meta[key]
            return ctx.invoke(f, obj, *args, **kwargs)

        return update_wrapper(new_func, f)
```

## argument  (src/click/decorators.py L324-349)
```
def argument(
    *param_decls: str, cls: type[Argument] | None = None, **attrs: t.Any
) -> t.Callable[[FC], FC]:
    """Attaches an argument to the command.  All positional arguments are
    passed as parameter declarations to :class:`Argument`; all keyword
    arguments are forwarded unchanged (except ``cls``).
    This is equivalent to creating an :class:`Argument` instance manually
    and attaching it to the :attr:`Command.params` list.

    For the default argument class, refer to :class:`Argument` and
    :class:`Parameter` for descriptions of parameters.

    :param cls: the argument class to instantiate.  This defaults to
                :class:`Argument`.
    :param param_decls: Passed as positional arguments to the constructor of
        ``cls``.
    :param attrs: Passed as keyword arguments to the constructor of ``cls``.
    """
    if cls is None:
        cls = Argument

    def decorator(f: FC) -> FC:
        _param_memo(f, cls(param_decls, **attrs))
        return f

    return decorator
```

## command  (tests/test_formatting.py L68-69)
```
    def command():
        """A command."""
```

## callback  (tests/test_context.py L116-117)
```
        def callback():
            called.append(True)
```

## confirmation_option  (src/click/decorators.py L380-401)
```
def confirmation_option(*param_decls: str, **kwargs: t.Any) -> t.Callable[[FC], FC]:
    """Add a ``--yes`` option which shows a prompt before continuing if
    not passed. If the prompt is declined, the program will exit.

    :param param_decls: One or more option names. Defaults to the single
        value ``"--yes"``.
    :param kwargs: Extra arguments are passed to :func:`option`.
    """

    def callback(ctx: Context, param: Parameter, value: bool) -> None:
        if not value:
            ctx.abort()

    if not param_decls:
        param_decls = ("--yes",)

    kwargs.setdefault("is_flag", True)
    kwargs.setdefault("callback", callback)
    kwargs.setdefault("expose_value", False)
    kwargs.setdefault("prompt", "Do you want to continue?")
    kwargs.setdefault("help", "Confirm the action without prompting.")
    return option(*param_decls, **kwargs)
```

## group  (tests/test_commands.py L523-524)
```
    def group(t):
        pass
```

## show_help  (src/click/decorators.py L536-540)
```
    def show_help(ctx: Context, param: Parameter, value: bool) -> None:
        """Callback that print the help page on ``<stdout>`` and exits."""
        if value and not ctx.resilient_parsing:
            echo(ctx.get_help(), color=ctx.color)
            ctx.exit()
```

## help_option  (src/click/decorators.py L527-551)
```
def help_option(*param_decls: str, **kwargs: t.Any) -> t.Callable[[FC], FC]:
    """Pre-configured ``--help`` option which immediately prints the help page
    and exits the program.

    :param param_decls: One or more option names. Defaults to the single
        value ``"--help"``.
    :param kwargs: Extra arguments are passed to :func:`option`.
    """

    def show_help(ctx: Context, param: Parameter, value: bool) -> None:
        """Callback that print the help page on ``<stdout>`` and exits."""
        if value and not ctx.resilient_parsing:
            echo(ctx.get_help(), color=ctx.color)
            ctx.exit()

    if not param_decls:
        param_decls = ("--help",)

    kwargs.setdefault("is_flag", True)
    kwargs.setdefault("expose_value", False)
    kwargs.setdefault("is_eager", True)
    kwargs.setdefault("help", _("Show this message and exit."))
    kwargs.setdefault("callback", show_help)

    return option(*param_decls, **kwargs)
```

## new_func  (src/click/decorators.py L45-46)
```
    def new_func(*args: P.args, **kwargs: P.kwargs) -> R:
        return f(get_current_context().obj, *args, **kwargs)
```

## make_pass_decorator  (src/click/decorators.py L51-97)
```
def make_pass_decorator(
    object_type: type[T], ensure: bool = False
) -> t.Callable[[t.Callable[te.Concatenate[T, P], R]], t.Callable[P, R]]:
    """Given an object type this creates a decorator that will work
    similar to :func:`pass_obj` but instead of passing the object of the
    current context, it will find the innermost context of type
    :func:`object_type`.

    This generates a decorator that works roughly like this::

        from functools import update_wrapper

        def decorator(f):
            @pass_context
            def new_func(ctx, *args, **kwargs):
                obj = ctx.find_object(object_type)
                return ctx.invoke(f, obj, *args, **kwargs)
            return update_wrapper(new_func, f)
        return decorator

    :param object_type: the type of the object to pass.
    :param ensure: if set to `True`, a new object will be created and
                   remembered on the context if it's not there yet.
    """

    def decorator(f: t.Callable[te.Concatenate[T, P], R]) -> t.Callable[P, R]:
        def new_func(*args: P.args, **kwargs: P.kwargs) -> R:
            ctx = get_current_context()

            obj: T | None
            if ensure:
                obj = ctx.ensure_object(object_type)
            else:
                obj = ctx.find_object(object_type)

            if obj is None:
                raise RuntimeError(
                    "Managed to invoke callback without a context"
                    f" object of type {object_type.__name__!r}"
                    " existing."
                )

            return ctx.invoke(f, obj, *args, **kwargs)

        return update_wrapper(new_func, f)

    return decorator
```

## pass_context  (src/click/decorators.py L28-36)
```
def pass_context(f: t.Callable[te.Concatenate[Context, P], R]) -> t.Callable[P, R]:
    """Marks a callback as wanting to receive the current context
    object as first argument.
    """

    def new_func(*args: P.args, **kwargs: P.kwargs) -> R:
        return f(get_current_context(), *args, **kwargs)

    return update_wrapper(new_func, f)
```

## pass_meta_key  (src/click/decorators.py L100-130)
```
def pass_meta_key(
    key: str, *, doc_description: str | None = None
) -> t.Callable[[t.Callable[te.Concatenate[T, P], R]], t.Callable[P, R]]:
    """Create a decorator that passes a key from
    :attr:`click.Context.meta` as the first argument to the decorated
    function.

    :param key: Key in ``Context.meta`` to pass.
    :param doc_description: Description of the object being passed,
        inserted into the decorator's docstring. Defaults to "the 'key'
        key from Context.meta".

    .. versionadded:: 8.0
    """

    def decorator(f: t.Callable[te.Concatenate[T, P], R]) -> t.Callable[P, R]:
        def new_func(*args: P.args, **kwargs: P.kwargs) -> R:
            ctx = get_current_context()
            obj = ctx.meta[key]
            return ctx.invoke(f, obj, *args, **kwargs)

        return update_wrapper(new_func, f)

    if doc_description is None:
        doc_description = f"the {key!r} key from :attr:`click.Context.meta`"

    decorator.__doc__ = (
        f"Decorator that passes {doc_description} as the first argument"
        " to the decorated function."
    )
    return decorator
```

## pass_obj  (src/click/decorators.py L39-48)
```
def pass_obj(f: t.Callable[te.Concatenate[T, P], R]) -> t.Callable[P, R]:
    """Similar to :func:`pass_context`, but only pass the object on the
    context onwards (:attr:`Context.obj`).  This is useful if that object
    represents the state of a nested system.
    """

    def new_func(*args: P.args, **kwargs: P.kwargs) -> R:
        return f(get_current_context().obj, *args, **kwargs)

    return update_wrapper(new_func, f)
```

## password_option  (src/click/decorators.py L404-418)
```
def password_option(*param_decls: str, **kwargs: t.Any) -> t.Callable[[FC], FC]:
    """Add a ``--password`` option which prompts for a password, hiding
    input and asking to enter the value again for confirmation.

    :param param_decls: One or more option names. Defaults to the single
        value ``"--password"``.
    :param kwargs: Extra arguments are passed to :func:`option`.
    """
    if not param_decls:
        param_decls = ("--password",)

    kwargs.setdefault("prompt", True)
    kwargs.setdefault("confirmation_prompt", True)
    kwargs.setdefault("hide_input", True)
    return option(*param_decls, **kwargs)
```

## version_option  (src/click/decorators.py L421-524)
```
def version_option(
    version: str | None = None,
    *param_decls: str,
    package_name: str | None = None,
    prog_name: str | None = None,
    message: str | None = None,
    **kwargs: t.Any,
) -> t.Callable[[FC], FC]:
    """Add a ``--version`` option which immediately prints the version
    number and exits the program.

    If ``version`` is not provided, Click will try to detect it using
... (truncated)
```
--- END SOURCE SNIPPETS ---

QUESTION: When an option or argument value is not provided directly on the command line, how does Click decide what value to use, and what extra work do file and path types perform during conversion?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
