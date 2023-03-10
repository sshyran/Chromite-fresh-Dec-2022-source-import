# Copyright (c) 2012 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Run lint checks on the specified files."""

import fnmatch
import functools
import json
import logging
import multiprocessing
import os
import re
import sys

from chromite.cli import command
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import git
from chromite.lib import osutils
from chromite.lib import parallel


# Extract a script's shebang.
SHEBANG_RE = re.compile(br'^#!\s*([^\s]+)(\s+([^\s]+))?')


def _GetProjectPath(path):
  """Find the absolute path of the git checkout that contains |path|."""
  ret = git.FindGitTopLevel(path)
  if ret:
    return ret
  else:
    # Maybe they're running on a file outside of a checkout.
    # e.g. cros lint ~/foo.py /tmp/test.py
    return os.path.dirname(path)


def _GetPylintrc(path):
  """Locate pylintrc or .pylintrc file that applies to |path|.

  If not found - use the default.
  """
  path = os.path.realpath(path)
  parent = os.path.dirname(path)
  project_path = _GetProjectPath(parent)
  while project_path and parent.startswith(project_path):
    pylintrc = os.path.join(parent, 'pylintrc')
    dotpylintrc = os.path.join(parent, '.pylintrc')
    # Only allow one of these to exist to avoid confusing which one is used.
    if os.path.isfile(pylintrc) and os.path.isfile(dotpylintrc):
      cros_build_lib.Die('%s: Only one of "pylintrc" or ".pylintrc" is allowed',
                         parent)
    if os.path.isfile(pylintrc):
      return pylintrc
    if os.path.isfile(dotpylintrc):
      return dotpylintrc

    parent = os.path.dirname(parent)

  return os.path.join(constants.SOURCE_ROOT, 'chromite', 'pylintrc')


def _GetPylintGroups(paths):
  """Return a dictionary mapping pylintrc files to lists of paths."""
  groups = {}
  for path in paths:
    pylintrc = _GetPylintrc(path)
    if pylintrc:
      groups.setdefault(pylintrc, []).append(path)
  return groups


def _GetPythonPath(paths):
  """Return the set of Python library paths to use."""
  # Carry through custom PYTHONPATH that the host env has set.
  return os.environ.get('PYTHONPATH', '').split(os.pathsep) + [
      # Add the Portage installation inside the chroot to the Python path.
      # This ensures that scripts that need to import portage can do so.
      os.path.join(constants.SOURCE_ROOT, 'chroot', 'usr', 'lib', 'portage',
                   'pym'),

      # Allow platform projects to be imported by name (e.g. crostestutils).
      os.path.join(constants.SOURCE_ROOT, 'src', 'platform'),

      # Ideally we'd modify meta_path in pylint to handle our virtual chromite
      # module, but that's not possible currently.  We'll have to deal with
      # that at some point if we want `cros lint` to work when the dir is not
      # named 'chromite'.
      constants.SOURCE_ROOT,

      # Also allow scripts to import from their current directory.
  ] + list(set(os.path.dirname(x) for x in paths))


# The mapping between the "cros lint" --output-format flag and cpplint.py
# --output flag.
CPPLINT_OUTPUT_FORMAT_MAP = {
    'colorized': 'emacs',
    'msvs': 'vs7',
    'parseable': 'emacs',
}

# Default category filters to pass to cpplint.py when invoked via `cros lint`.
#
# `-foo/bar` means "don't show any lints from category foo/bar".
# See `cpplint.py --help` for more explanation of category filters.
CPPLINT_DEFAULT_FILTERS = (
    '-runtime/references',
)


# The mapping between the "cros lint" --output-format flag and shellcheck
# flags.
# Note that the msvs mapping here isn't quite VS format, but it's closer than
# the default output.
SHLINT_OUTPUT_FORMAT_MAP = {
    'colorized': ['--color=always'],
    'msvs': ['--format=gcc'],
    'parseable': ['--format=gcc'],
}


def _LinterRunCommand(cmd, debug, **kwargs):
  """Run the linter with common run args set as higher levels expect."""
  return cros_build_lib.run(cmd, check=False, print_cmd=debug,
                            debug_level=logging.NOTICE, **kwargs)


def _WhiteSpaceLintData(path, data):
  """Run basic whitespace checks on |data|.

  Args:
    path: The name of the file (for diagnostics).
    data: The file content to lint.

  Returns:
    True if everything passed.
  """
  ret = True

  # Make sure files all have a trailing newline.
  if not data.endswith('\n'):
    ret = False
    logging.warning('%s: file needs a trailing newline', path)

  # Disallow leading & trailing blank lines.
  if data.startswith('\n'):
    ret = False
    logging.warning('%s: delete leading blank lines', path)
  if data.endswith('\n\n'):
    ret = False
    logging.warning('%s: delete trailing blank lines', path)

  for i, line in enumerate(data.splitlines(), start=1):
    if line.rstrip() != line:
      ret = False
      logging.warning('%s:%i: trim trailing whitespace: %s', path, i, line)

  return ret


def _CpplintFile(path, output_format, debug):
  """Returns result of running cpplint on |path|."""
  cmd = [os.path.join(constants.DEPOT_TOOLS_DIR, 'cpplint.py')]
  cmd.append('--filter=%s' % ','.join(CPPLINT_DEFAULT_FILTERS))
  if output_format != 'default':
    cmd.append('--output=%s' % CPPLINT_OUTPUT_FORMAT_MAP[output_format])
  cmd.append(path)
  return _LinterRunCommand(cmd, debug)


def _PylintFile(path, output_format, debug):
  """Returns result of running pylint on |path|."""
  pylint = os.path.join(constants.CHROMITE_DIR, 'cli', 'cros', 'pylint-2')
  pylintrc = _GetPylintrc(path)
  cmd = [pylint, '--rcfile=%s' % pylintrc]
  if output_format != 'default':
    cmd.append('--output-format=%s' % output_format)
  cmd.append(path)
  extra_env = {
      'PYTHONPATH': ':'.join(_GetPythonPath([path])),
  }
  return _LinterRunCommand(cmd, debug, extra_env=extra_env)


def _GolintFile(path, _, debug):
  """Returns result of running golint on |path|."""
  # Try using golint if it exists.
  try:
    cmd = ['golint', '-set_exit_status', path]
    return _LinterRunCommand(cmd, debug)
  except cros_build_lib.RunCommandError:
    logging.notice('Install golint for additional go linting.')
    return cros_build_lib.CommandResult('gofmt "%s"' % path,
                                        returncode=0)


def _JsonLintFile(path, _output_format, _debug):
  """Returns result of running json lint checks on |path|."""
  result = cros_build_lib.CommandResult('python -mjson.tool "%s"' % path,
                                        returncode=0)

  data = osutils.ReadFile(path)

  # Strip off leading UTF-8 BOM if it exists.
  if data.startswith(u'\ufeff'):
    data = data[1:]

  # Strip out comments for JSON parsing.
  stripped_data = re.sub(r'^\s*#.*', '', data, flags=re.M)

  # See if it validates.
  try:
    json.loads(stripped_data)
  except ValueError as e:
    result.returncode = 1
    logging.notice('%s: %s', path, e)

  # Check whitespace.
  if not _WhiteSpaceLintData(path, data):
    result.returncode = 1

  return result


def _MarkdownLintFile(path, _output_format, _debug):
  """Returns result of running lint checks on |path|."""
  result = cros_build_lib.CommandResult('mdlint(internal) "%s"' % path,
                                        returncode=0)

  data = osutils.ReadFile(path)

  # Check whitespace.
  if not _WhiteSpaceLintData(path, data):
    result.returncode = 1

  return result


def _ShellLintFile(path, output_format, debug, gentoo_format=False):
  """Returns result of running lint checks on |path|.

  Args:
    path: The path to the script on which to run the linter.
    output_format: The format of the output that the linter should emit. See
                   |SHLINT_OUTPUT_FORMAT_MAP|.
    debug: Whether to print out the linter command.
    gentoo_format: Whether to treat this file as an ebuild style script.

  Returns:
    A CommandResult object.
  """
  # TODO: Try using `checkbashisms`.
  syntax_check = _LinterRunCommand(['bash', '-n', path], debug)
  if syntax_check.returncode != 0:
    return syntax_check

  # Try using shellcheck if it exists, with a preference towards finding it
  # inside the chroot. This is OK as it is statically linked.
  shellcheck = (
      osutils.Which('shellcheck', path='/usr/bin',
                    root=os.path.join(constants.SOURCE_ROOT, 'chroot'))
      or osutils.Which('shellcheck'))

  if not shellcheck:
    logging.notice('Install shellcheck for additional shell linting.')
    return syntax_check

  # Instruct shellcheck to run itself from the shell script's dir. Note that
  # 'SCRIPTDIR' is a special string that shellcheck rewrites to the dirname of
  # the given path.
  extra_checks = [
      'avoid-nullary-conditions',     # SC2244
      'check-unassigned-uppercase',   # Include uppercase in SC2154
      'require-variable-braces',      # SC2250
  ]
  if not gentoo_format:
    extra_checks.append('quote-safe-variables')  # SC2248

  cmd = [shellcheck, '--source-path=SCRIPTDIR',
         '--enable=%s' % ','.join(extra_checks)]
  if output_format != 'default':
    cmd.extend(SHLINT_OUTPUT_FORMAT_MAP[output_format])
  cmd.append('-x')
  # No warning for using local with /bin/sh.
  cmd.append('--exclude=SC3043')
  if gentoo_format:
    # ebuilds don't explicitly export variables or contain a shebang.
    cmd.append('--exclude=SC2148')
    # ebuilds always use bash.
    cmd.append('--shell=bash')
  cmd.append(path)

  lint_result = _LinterRunCommand(cmd, debug)

  # Check whitespace.
  if not _WhiteSpaceLintData(path, osutils.ReadFile(path)):
    lint_result.returncode = 1

  return lint_result


def _GentooShellLintFile(path, output_format, debug):
  """Run shell checks with Gentoo rules."""
  return _ShellLintFile(path, output_format, debug, gentoo_format=True)


def _SeccompPolicyLintFile(path, _output_format, debug):
  """Run the seccomp policy linter."""
  dangerous_syscalls = {'bpf', 'setns', 'execveat', 'ptrace', 'swapoff',
                        'swapon'}
  return _LinterRunCommand(
      [os.path.join(constants.SOURCE_ROOT, 'src', 'aosp', 'external',
                    'minijail', 'tools', 'seccomp_policy_lint.py'),
       '--dangerous-syscalls', ','.join(dangerous_syscalls),
       path],
      debug)


def _DirMdLintFile(path, _output_format, debug):
  """Run the dirmd linter."""
  return _LinterRunCommand(
      [os.path.join(constants.DEPOT_TOOLS_DIR, 'dirmd'), 'validate', path],
      debug, capture_output=not debug)


def _BreakoutDataByLinter(map_to_return, path):
  """Maps a linter method to the content of the |path|."""
  # Detect by content of the file itself.
  try:
    with open(path, 'rb') as fp:
      # We read 128 bytes because that's the Linux kernel's current limit.
      # Look for BINPRM_BUF_SIZE in fs/binfmt_script.c.
      data = fp.read(128)

      if not data.startswith(b'#!'):
        # If the file doesn't have a shebang, nothing to do.
        return

      m = SHEBANG_RE.match(data)
      if m:
        prog = m.group(1)
        if prog == b'/usr/bin/env':
          prog = m.group(3)
        basename = os.path.basename(prog)
        if basename.startswith(b'python'):
          pylint_list = map_to_return.setdefault(_PylintFile, [])
          pylint_list.append(path)
        elif basename in (b'sh', b'dash', b'bash'):
          shlint_list = map_to_return.setdefault(_ShellLintFile, [])
          shlint_list.append(path)
  except IOError as e:
    logging.debug('%s: reading initial data failed: %s', path, e)


# Map file extensions to a linter function.
_EXT_TO_LINTER_MAP = {
    # Note these are defined to keep in line with cpplint.py. Technically, we
    # could include additional ones, but cpplint.py would just filter them out.
    frozenset({'.cc', '.cpp', '.h'}): _CpplintFile,
    frozenset({'.json'}): _JsonLintFile,
    frozenset({'.py'}): _PylintFile,
    frozenset({'.go'}): _GolintFile,
    frozenset({'.sh'}): _ShellLintFile,
    frozenset({'.ebuild', '.eclass', '.bashrc'}): _GentooShellLintFile,
    frozenset({'.md'}): _MarkdownLintFile,
    frozenset({'.policy'}): _SeccompPolicyLintFile,
}

# Map known filenames to a linter function.
_FILENAME_PATTERNS_TO_LINTER_MAP = {
    frozenset({'DIR_METADATA'}): _DirMdLintFile,
}


def _BreakoutFilesByLinter(files):
  """Maps a linter method to the list of files to lint."""
  map_to_return = {}
  for f in files:
    extension = os.path.splitext(f)[1]
    for extensions, linter in _EXT_TO_LINTER_MAP.items():
      if extension in extensions:
        map_to_return.setdefault(linter, []).append(f)
        break
    else:
      name = os.path.basename(f)
      for patterns, linter in _FILENAME_PATTERNS_TO_LINTER_MAP.items():
        if any(fnmatch.fnmatch(name, x) for x in patterns):
          map_to_return.setdefault(linter, []).append(f)
          break
      else:
        if os.path.isfile(f):
          _BreakoutDataByLinter(map_to_return, f)

  return map_to_return


def _Dispatcher(errors, output_format, debug, linter, path):
  """Call |linter| on |path| and take care of coalescing exit codes/output."""
  result = linter(path, output_format, debug)
  if result.returncode:
    with errors.get_lock():
      errors.value += 1


@command.command_decorator('lint')
class LintCommand(command.CliCommand):
  """Run lint checks on the specified files."""

  EPILOG = """
Right now, only supports cpplint and pylint. We may also in the future
run other checks (e.g. pyflakes, etc.)
"""

  # The output formats supported by cros lint.
  OUTPUT_FORMATS = ('default', 'colorized', 'msvs', 'parseable')

  @classmethod
  def AddParser(cls, parser):
    super(LintCommand, cls).AddParser(parser)
    parser.add_argument('files', help='Files to lint', nargs='*')
    parser.add_argument('--output', default='default',
                        choices=LintCommand.OUTPUT_FORMATS,
                        help='Output format to pass to the linters. Supported '
                        'formats are: default (no option is passed to the '
                        'linter), colorized, msvs (Visual Studio) and '
                        'parseable.')

  def Run(self):
    files = self.options.files
    if not files:
      # Running with no arguments is allowed to make the repo upload hook
      # simple, but print a warning so that if someone runs this manually
      # they are aware that nothing was linted.
      logging.warning('No files provided to lint.  Doing nothing.')

    errors = parallel.WrapMultiprocessing(multiprocessing.Value, 'i')
    linter_map = _BreakoutFilesByLinter(files)
    dispatcher = functools.partial(_Dispatcher, errors,
                                   self.options.output, self.options.debug)

    # Special case one file as it's common -- faster to avoid parallel startup.
    if not linter_map:
      return 0
    elif sum(len(x) for x in linter_map.values()) == 1:
      linter, files = next(iter(linter_map.items()))
      dispatcher(linter, files[0])
    else:
      # Run the linter in parallel on the files.
      with parallel.BackgroundTaskRunner(dispatcher) as q:
        for linter, files in linter_map.items():
          for path in files:
            q.put([linter, path])

    if errors.value:
      logging.error('Found lint errors in %i files.', errors.value)
      sys.exit(1)
