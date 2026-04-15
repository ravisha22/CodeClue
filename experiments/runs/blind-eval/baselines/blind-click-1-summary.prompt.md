# Baseline Evaluation: Plain Summary
# Task: blind-click-1

You are a senior software engineer. You have been given a brief summary
of a repository's structure. Answer the question using ONLY this summary.
Do not use any external knowledge about the framework.

--- REPOSITORY SUMMARY ---
Repository: click

Directory structure:
  CHANGES.rst
  docs/ (39 files)
  examples/ (39 files)
  LICENSE.txt
  pyproject.toml
  README.md
  src/ (18 files)
  tests/ (31 files)
  uv.lock

Source files (42 python files):
  docs\conf.py (1KB)
  examples\aliases\aliases.py (3KB)
  examples\colors\colors.py (0KB)
  examples\completion\completion.py (1KB)
  examples\complex\complex\__init__.py (0KB)
  examples\complex\complex\cli.py (1KB)
  examples\complex\complex\commands\__init__.py (0KB)
  examples\complex\complex\commands\cmd_init.py (0KB)
  examples\complex\complex\commands\cmd_status.py (0KB)
  examples\imagepipe\imagepipe.py (8KB)
  examples\inout\inout.py (0KB)
  examples\naval\naval.py (1KB)
  examples\repo\repo.py (4KB)
  examples\termui\termui.py (4KB)
  examples\validation\validation.py (1KB)
  src\click\__init__.py (4KB)
  src\click\_compat.py (18KB)
  src\click\_termui_impl.py (26KB)
  src\click\_textwrap.py (1KB)
  src\click\_utils.py (0KB)
  src\click\_winconsole.py (8KB)
  src\click\core.py (129KB)
  src\click\decorators.py (18KB)
  src\click\exceptions.py (9KB)
  src\click\formatting.py (9KB)
  src\click\globals.py (1KB)
  src\click\parser.py (18KB)
  src\click\shell_completion.py (20KB)
  src\click\termui.py (30KB)
  src\click\testing.py (18KB)
  ... and 12 more files
--- END SUMMARY ---

QUESTION: How does Click turn decorated Python functions into a nested CLI and then dispatch the right subcommand at runtime?

Provide a detailed answer based solely on the summary above.
If the summary doesn't contain enough information, say what you CAN and CANNOT determine.
