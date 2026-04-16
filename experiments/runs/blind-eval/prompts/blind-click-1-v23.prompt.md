# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: blind-click-1

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.

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
_check_nested_chain (src/click/core.py:73-90)
  sig: _check_nested_chain(base_command, cmd_name, cmd, register)
  behavior: GUARD(not base_command.chain or not isinstance(cmd, Group) -> return); BRANCH(register -> f'It is not possible..., else -> f'Found the group {cm...)
  called_by: CommandCollection, add_command, Group
  raises: RuntimeError

ClickException (src/click/exceptions.py:26-53)
  An exception that Click can handle and show to the user.
  extends: Exception
  attrs: exit_code=1
  imports: gettext, globals, utils, core

ComplexCLI (examples/complex/complex/cli.py:31-45)
  extends: Group
  imports: click

cli (examples/completion/completion.py:8-9)
  calls: group

cli (examples/termui/termui.py:9-11)
  This script showcases different terminal UI helpers in Click.

_expand_args (src/click/utils.py:578-628)
  Simulate Unix shell expansion with Python functions.
  sig: _expand_args(args)
  behavior: ACCUMULATE(args loop -> out)

_resolve_incomplete (src/click/shell_completion.py:623-667)
  Find the Click object that will handle the completion of the
  sig: _resolve_incomplete(ctx, args, incomplete)
  behavior: ACCUMULATE(params loop -> result)
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

_match_short_opt (src/click/parser.py:389-427)
  sig: _match_short_opt(arg, state)
  behavior: ACCUMULATE(arg[1:] loop -> i, raises NoSuchOption)
  calls: _get_value_from_state, _normalize_opt
  called_by: _process_opts, _OptionParser
  raises: NoSuchOption
  uses: NoSuchOption (exceptions)

_match_long_opt (src/click/parser.py:359-387)
  sig: _match_long_opt(opt, explicit_value, state)
  behavior: GUARD(opt not in self._long_opt -> raise NoSuchOption(opt, p...)
  calls: _get_value_from_state
  called_by: _process_opts, _OptionParser
  raises: NoSuchOption, BadOptionUsage
  uses: NoSuchOption (exceptions), BadOptionUsage (exceptions)

__next__ (src/click/_termui_impl.py:134-140)
  behavior: DELEGATE(next -> result)

cli (examples/colors/colors.py:25-39)
  This script prints some colors.
  behavior: ACCUMULATE(all_colors loop -> result)

cli (examples/complex/complex/cli.py:56-60)
  A complex command line interface.
  sig: cli(ctx, verbose, home)

cli (examples/inout/inout.py:7-30)
  This script works similar to the Unix `cat` command but it writes
  sig: cli(input, output)
  behavior: ACCUMULATE(input loop -> output)

cli (examples/imagepipe/imagepipe.py:11-20)
  This script processes a bunch of images through pillow in a unix

cli (examples/aliases/aliases.py:97-98)
  An example application that supports aliases.

cli (examples/naval/naval.py:6-12)
  Naval Fate.

cli (examples/complex/complex/commands/cmd_init.py:9-13)
  Initializes a repository.
  sig: cli(ctx, path)

cli (examples/repo/repo.py:44-57)
  Repo is a command line tool that showcases how to build complex
  sig: cli(ctx, repo_home, config, verbose)
  behavior: ACCUMULATE(config loop -> result)
  calls: set_config, Repo

cli (examples/complex/complex/commands/cmd_status.py:8-11)
  Shows file changes in the current working directory.
  sig: cli(ctx)

cli (examples/validation/validation.py:34-48)
  Validation.
  sig: cli(count, foo, url)
  calls: URL
  raises: BadParameter

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

smoothen_cmd (examples/imagepipe/imagepipe.py:229-238)
  Applies a smoothening filter.
  sig: smoothen_cmd(images, iterations)
  behavior: ACCUMULATE(images loop -> result)
  calls: copy_filename

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

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 24 with behavior annotations
uncovered: get_invalid_choice_message, get_parameter_source, handle_parse_result, iter_params_for_processing
drill: src/click/utils.py (~31 lines, _expand_args)
drill: src/click/core.py (~15 lines, _check_nested_chain)

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
        file wrapper.  For instance this will never close stdin.
        """
        if self.should_close:
            self.close()
```

## open  (src/click/utils.py L151-167)
```
    def open(self) -> t.IO[t.Any]:
        """Opens the file if it's not yet open.  This call might fail with
        a :exc:`FileError`.  Not handling this error will produce an error
        that Click shows.
        """
        if self._f is not None:
            return self._f
        try:
            rv, self.should_close = open_stream(
                self.name, self.mode, self.encoding, self.errors, atomic=self.atomic
            )
        except OSError as e:
            from .exceptions import FileError

            raise FileError(self.name, hint=e.strerror) from e
        self._f = rv
        return rv
```

## LazyFile  (src/click/utils.py L109-194)
```
class LazyFile:
    """A lazy file works like a regular file but it does not fully open
    the file but it does perform some basic checks early to see if the
    filename parameter does make sense.  This is useful for safely opening
    files for writing.
    """

    def __init__(
        self,
        filename: str | os.PathLike[str],
        mode: str = "r",
        encoding: str | None = None,
        errors: str | None = "strict",
        atomic: bool = False,
    ):
        self.name: str = os.fspath(filename)
        self.mode = mode
        self.encoding = encoding
        self.errors = errors
        self.atomic = atomic
        self._f: t.IO[t.Any] | None
        self.should_close: bool

        if self.name == "-":
            self._f, self.should_close = open_stream(filename, mode, encoding, errors)
        else:
            if "r" in mode:
                # Open and close the file in case we're opening it for
                # reading so that we can catch at least some errors in
                # some cases early.
                open(filename, mode).close()
            self._f = None
            self.should_close = True

    def __getattr__(self, name: str) -> t.Any:
        return getattr(self.open(), name)

    def __repr__(self) -> str:
        if self._f is not None:
            return repr(self._f)
        return f"<unopened file '{format_filename(self.name)}' {self.mode}>"

    def open(self) -> t.IO[t.Any]:
        """Opens the file if it's not yet open.  This call might fail with
        a :exc:`FileError`.  Not handling this error will produce an error
        that Click shows.
        """
        if self._f is not None:
            return self._f
        try:
            rv, self.should_close = open_stream(
                self.name, self.mode, self.encoding, self.errors, atomic=self.atomic
            )
        except OSError as e:
            from .exceptions import FileError

            raise FileError(self.name, hint=e.strerror) from e
        self._f = rv
        return rv

    def close(self) -> None:
        """Closes the underlying file, no matter what."""
        if self._f is not None:
            self._f.close()

    def close_intelligently(self) -> None:
        """This function only closes the file if it was opened by the lazy
        file wrapper.  For instance this will never close stdin.
        """
        if self.should_close:
            self.close()

    def __enter__(self) -> LazyFile:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close_intelligently()

    def __iter__(self) -> cabc.Iterator[t.AnyStr]:
        self.open()
        return iter(self._f)  # type: ignore
```

## flush  (src/click/utils.py L510-519)
```
    def flush(self) -> None:
        try:
            self.wrapped.flush()
        except OSError as e:
            import errno

            if e.errno != errno.EPIPE:
                raise

    def __getattr__(self, attr: str) -> t.Any:
```

## PacifyFlushWrapper  (src/click/utils.py L498-522)
```
class PacifyFlushWrapper:
    """This wrapper is used to catch and suppress BrokenPipeErrors resulting
    from ``.flush()`` being called on broken pipe during the shutdown/final-GC
    of the Python interpreter. Notably ``.flush()`` is always called on
    ``sys.stdout`` and ``sys.stderr``. So as to have minimal impact on any
    other cleanup code, and the case where the underlying file is not a broken
    pipe, all calls and attributes are proxied.
    """

    def __init__(self, wrapped: t.IO[t.Any]) -> None:
        self.wrapped = wrapped

    def flush(self) -> None:
        try:
            self.wrapped.flush()
        except OSError as e:
            import errno

            if e.errno != errno.EPIPE:
                raise

    def __getattr__(self, attr: str) -> t.Any:
        return getattr(self.wrapped, attr)


```

## _detect_program_name  (src/click/utils.py L523-577)
```
def _detect_program_name(
    path: str | None = None, _main: ModuleType | None = None
) -> str:
    """Determine the command used to run the program, for use in help
    text. If a file or entry point was executed, the file name is
    returned. If ``python -m`` was used to execute a module or package,
    ``python -m name`` is returned.

    This doesn't try to be too precise, the goal is to give a concise
    name for help text. Files are only shown as their name without the
    path. ``python`` is only shown for modules, and the full path to
    ``sys.executable`` is not shown.

    :param path: The Python file being executed. Python puts this in
        ``sys.argv[0]``, which is used by default.
    :param _main: The ``__main__`` module. This should only be passed
        during internal testing.

    .. versionadded:: 8.0
        Based on command args detection in the Werkzeug reloader.

    :meta private:
    """
    if _main is None:
        _main = sys.modules["__main__"]

    if not path:
        path = sys.argv[0]

    # The value of __package__ indicates how Python was called. It may
    # not exist if a setuptools script is installed as an egg. It may be
    # set incorrectly for entry points created with pip on Windows.
    # It is set to "" inside a Shiv or PEX zipapp.
    if getattr(_main, "__package__", None) in {None, ""} or (
        os.name == "nt"
        and _main.__package__ == ""
        and not os.path.exists(path)
        and os.path.exists(f"{path}.exe")
    ):
        # Executed a file, like "python app.py".
        return os.path.basename(path)

    # Executed a module, like "python -m example".
    # Rewritten by Python from "-m script" to "/path/to/script.py".
    # Need to look at main module to determine how it was executed.
    py_module = t.cast(str, _main.__package__)
    name = os.path.splitext(os.path.basename(path))[0]

    # A submodule like "example.cli".
    if name != "__main__":
        py_module = f"{py_module}.{name}"

    return f"python -m {py_module.lstrip('.')}"


```

## _posixify  (src/click/utils.py L32-33)
```
def _posixify(name: str) -> str:
    return "-".join(name.split()).lower()
```

## echo  (tests/test_utils.py L237-241)
```
    def echo():
        for _ in range(3):
            click.echo(click.prompt("", type=int))

    # only provide two lines of input for three prompts
```

## format_filename  (src/click/utils.py L407-448)
```
def format_filename(
    filename: str | bytes | os.PathLike[str] | os.PathLike[bytes],
    shorten: bool = False,
) -> str:
    """Format a filename as a string for display. Ensures the filename can be
    displayed by replacing any invalid bytes or surrogate escapes in the name
    with the replacement character ``�``.

    Invalid bytes or surrogate escapes will raise an error when written to a
    stream with ``errors="strict"``. This will typically happen with ``stdout``
... (truncated)
```
--- END SOURCE SNIPPETS ---

QUESTION: How does Click turn decorated Python functions into a nested CLI and then dispatch the right subcommand at runtime?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
