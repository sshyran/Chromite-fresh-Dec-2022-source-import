# Copyright (c) 2012 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Run lint checks on the specified files."""

import fnmatch
import functools
import itertools
import json
import logging
import os
from pathlib import Path
import re
from typing import Union

from chromite.cli import command
from chromite.lib import commandline
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import git
from chromite.lib import osutils
from chromite.lib import parallel
from chromite.lint.linters import owners
from chromite.lint.linters import upstart
from chromite.lint.linters import whitespace
from chromite.utils import timer


# Extract a script's shebang.
SHEBANG_RE = re.compile(br'^#!\s*([^\s]+)(\s+([^\s]+))?')


def _GetProjectPath(path: Path) -> Path:
  """Find the absolute path of the git checkout that contains |path|."""
  ret = git.FindGitTopLevel(path)
  if ret:
    return Path(ret)
  else:
    # Maybe they're running on a file outside of a checkout.
    # e.g. cros lint ~/foo.py /tmp/test.py
    return path.parent


def _GetPylintrc(path: Union[str, os.PathLike]) -> Path:
  """Locate pylintrc or .pylintrc file that applies to |path|.

  If not found - use the default.
  """
  def _test_func(pylintrc):
    dotpylintrc = pylintrc.with_name('.pylintrc')
    # Only allow one of these to exist to avoid confusing which one is used.
    if pylintrc.exists() and dotpylintrc.exists():
      cros_build_lib.Die('%s: Only one of "pylintrc" or ".pylintrc" is allowed',
                         pylintrc.parent)
    return pylintrc.exists() or dotpylintrc.exists()

  path = Path(path)
  end_path = _GetProjectPath(path.parent).parent
  ret = osutils.FindInPathParents(
      'pylintrc', path.parent, test_func=_test_func, end_path=end_path)
  if ret:
    return ret if ret.exists() else ret.with_name('.pylintrc')
  return Path(constants.CHROMITE_DIR) / 'pylintrc'


def _GetPylintGroups(paths):
  """Return a dictionary mapping pylintrc files to lists of paths."""
  groups = {}
  for path in paths:
    pylintrc = _GetPylintrc(path)
    if pylintrc:
      groups.setdefault(pylintrc, []).append(path)
  return groups


def _GetIsortCfg(path: Union[str, os.PathLike]) -> Path:
  """Locate isort.cfg file that applies to |path|.

  If not found - use the default.
  """
  path = Path(path)
  end_path = _GetProjectPath(path.parent).parent
  ret = osutils.FindInPathParents('.isort.cfg', path.parent, end_path=end_path)
  return ret if ret else Path(constants.CHROMITE_DIR) / '.isort.cfg'


def _GetPythonPath():
  """Return the set of Python library paths to use."""
  # Carry through custom PYTHONPATH that the host env has set.
  return os.environ.get('PYTHONPATH', '').split(os.pathsep) + [
      # Ideally we'd modify meta_path in pylint to handle our virtual chromite
      # module, but that's not possible currently.  We'll have to deal with
      # that at some point if we want `cros lint` to work when the dir is not
      # named 'chromite'.
      constants.SOURCE_ROOT,
  ]


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


def _ToolRunCommand(cmd, debug, **kwargs):
  """Run the linter with common run args set as higher levels expect."""
  return cros_build_lib.run(cmd, check=False, print_cmd=debug,
                            debug_level=logging.NOTICE, **kwargs)


def _ConfLintFile(path, output_format, debug, relaxed: bool):
  """Determine the applicable .conf syntax and call the appropriate handler."""
  ret = cros_build_lib.CommandResult(f'cros lint "{path}"', returncode=0)
  if not os.path.isfile(path):
    return ret

  # .conf files are used by more than upstart, so use the parent dirname
  # to filter them.
  parent_name = os.path.basename(os.path.dirname(os.path.realpath(path)))
  if parent_name in {'init', 'upstart'}:
    return _UpstartLintFile(path, output_format, debug, relaxed)

  # Check for the description and author lines present in upstart configs.
  with open(path, 'rb') as file:
    tokens_to_find = {b'author', b'description'}
    for line in file:
      try:
        token = line.split()[0]
      except IndexError:
        continue

      try:
        tokens_to_find.remove(token)
      except KeyError:
        continue

      if not tokens_to_find:
        logging.warning(
            'Found upstart .conf in a directory other than init or upstart.')
        return _UpstartLintFile(path, output_format, debug, relaxed)
  return ret


def _CpplintFile(path, output_format, debug, _relaxed: bool):
  """Returns result of running cpplint on |path|."""
  cmd = [os.path.join(constants.DEPOT_TOOLS_DIR, 'cpplint.py')]
  cmd.append('--filter=%s' % ','.join(CPPLINT_DEFAULT_FILTERS))
  if output_format != 'default':
    cmd.append('--output=%s' % CPPLINT_OUTPUT_FORMAT_MAP[output_format])
  cmd.append(path)
  return _ToolRunCommand(cmd, debug)


def _PylintFile(path, output_format, debug, _relaxed: bool):
  """Returns result of running pylint on |path|."""
  pylint = os.path.join(constants.CHROMITE_SCRIPTS_DIR, 'pylint')
  pylintrc = _GetPylintrc(path)
  cmd = [pylint, '--rcfile=%s' % pylintrc]
  if output_format != 'default':
    cmd.append('--output-format=%s' % output_format)
  cmd.append(path)
  extra_env = {
      'PYTHONPATH': ':'.join(_GetPythonPath()),
  }
  return _ToolRunCommand(cmd, debug, extra_env=extra_env)


def _PyisortFile(path, _output_format, debug, _relaxed: bool):
  """Returns result of running isort on |path|."""
  isort = os.path.join(constants.CHROMITE_SCRIPTS_DIR, 'isort')
  cfg = _GetIsortCfg(path)
  base_cmd = [isort, f'--settings-file={cfg}']
  cmd = base_cmd + ['--diff', '--check']
  cmd.append(path)
  base_cmd.append(path)
  result = _ToolRunCommand(cmd, debug)
  if result.returncode:
    logging.notice('To fix, run:\n%s', cros_build_lib.CmdToStr(base_cmd))
  return result


def _GolintFile(path, _, debug, _relaxed: bool):
  """Returns result of running golint on |path|."""
  # Try using golint if it exists.
  try:
    cmd = ['golint', '-set_exit_status', path]
    return _ToolRunCommand(cmd, debug)
  except cros_build_lib.RunCommandError:
    logging.notice('Install golint for additional go linting.')
    return cros_build_lib.CommandResult('gofmt "%s"' % path,
                                        returncode=0)


def _JsonLintFile(path, _output_format, _debug, _relaxed: bool):
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
  if not whitespace.LintData(path, data):
    result.returncode = 1

  return result


def _MarkdownLintFile(path, _output_format, _debug, _relaxed: bool):
  """Returns result of running lint checks on |path|."""
  result = cros_build_lib.CommandResult('mdlint(internal) "%s"' % path,
                                        returncode=0)

  data = osutils.ReadFile(path)

  # Check whitespace.
  if not whitespace.LintData(path, data):
    result.returncode = 1

  return result


def _ShellLintFile(path, output_format, debug, _relaxed: bool,
                   gentoo_format=False):
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
  syntax_check = _ToolRunCommand(['bash', '-n', path], debug)
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

  lint_result = _ToolRunCommand(cmd, debug)

  # Check whitespace.
  if not whitespace.LintData(path, osutils.ReadFile(path)):
    lint_result.returncode = 1

  return lint_result


def _GentooShellLintFile(path, output_format, debug, relaxed: bool):
  """Run shell checks with Gentoo rules."""
  return _ShellLintFile(path, output_format, debug, relaxed,
                        gentoo_format=True)


def _SeccompPolicyLintFile(path, _output_format, debug, _relaxed: bool):
  """Run the seccomp policy linter."""
  dangerous_syscalls = {'bpf', 'setns', 'execveat', 'ptrace', 'swapoff',
                        'swapon'}
  return _ToolRunCommand(
      [os.path.join(constants.SOURCE_ROOT, 'src', 'aosp', 'external',
                    'minijail', 'tools', 'seccomp_policy_lint.py'),
       '--dangerous-syscalls', ','.join(dangerous_syscalls),
       path],
      debug)


def _UpstartLintFile(path, _output_format, _debug, relaxed: bool):
  """Run lints on upstart configs."""
  # Skip .conf files that aren't in an init parent directory.
  ret = cros_build_lib.CommandResult(f'cros lint "{path}"', returncode=0)
  if not upstart.CheckInitConf(Path(path), relaxed):
    ret.returncode = 1
  return ret


def _DirMdLintFile(path, _output_format, debug, _relaxed: bool):
  """Run the dirmd linter."""
  return _ToolRunCommand(
      [os.path.join(constants.DEPOT_TOOLS_DIR, 'dirmd'), 'validate', path],
      debug, capture_output=not debug)


def _OwnersLintFile(path, _output_format, _debug, _relaxed: bool):
  """Run lints on OWNERS files."""
  ret = cros_build_lib.CommandResult(f'cros lint "{path}"', returncode=0)
  if not owners.lint_path(Path(path)):
    ret.returncode = 1
  return ret


def _BreakoutDataByTool(map_to_return, path):
  """Maps a tool method to the content of the |path|."""
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
        if basename.startswith(b'python') or basename.startswith(b'vpython'):
          for tool in _EXT_TOOL_MAP[frozenset({'.py'})]:
            map_to_return.setdefault(tool, []).append(path)
        elif basename in (b'sh', b'dash', b'bash'):
          for tool in _EXT_TOOL_MAP[frozenset({'.sh'})]:
            map_to_return.setdefault(tool, []).append(path)
  except IOError as e:
    logging.debug('%s: reading initial data failed: %s', path, e)


# Map file extensions to a tool function.
_EXT_TOOL_MAP = {
    # Note these are defined to keep in line with cpplint.py. Technically, we
    # could include additional ones, but cpplint.py would just filter them out.
    frozenset({'.cc', '.cpp', '.h'}): (_CpplintFile,),
    frozenset({'.conf', '.conf.in'}): (_ConfLintFile,),
    frozenset({'.json'}): (_JsonLintFile,),
    frozenset({'.py'}): (_PylintFile, _PyisortFile),
    frozenset({'.go'}): (_GolintFile,),
    frozenset({'.sh'}): (_ShellLintFile,),
    frozenset({'.ebuild', '.eclass', '.bashrc'}): (_GentooShellLintFile,),
    frozenset({'.md'}): (_MarkdownLintFile,),
    frozenset({'.policy'}): (_SeccompPolicyLintFile,),
}

# Map known filenames to a tool function.
_FILENAME_PATTERNS_TOOL_MAP = {
    frozenset({'DIR_METADATA'}): (_DirMdLintFile,),
    frozenset({'OWNERS*'}): (_OwnersLintFile,),
}


def _BreakoutFilesByTool(files):
  """Maps a tool method to the list of files to process."""
  map_to_return = {}

  for f in files:
    extension = os.path.splitext(f)[1]
    for extensions, tools in _EXT_TOOL_MAP.items():
      if extension in extensions:
        for tool in tools:
          map_to_return.setdefault(tool, []).append(f)
        break
    else:
      name = os.path.basename(f)
      for patterns, tools in _FILENAME_PATTERNS_TOOL_MAP.items():
        if any(fnmatch.fnmatch(name, x) for x in patterns):
          for tool in tools:
            map_to_return.setdefault(tool, []).append(f)
          break
      else:
        if os.path.isfile(f):
          _BreakoutDataByTool(map_to_return, f)

  return map_to_return


def _Dispatcher(output_format, debug, relaxed: bool, tool, path):
  """Call |tool| on |path| and take care of coalescing exit codes/output."""
  result = tool(path, output_format, debug, relaxed)
  return 1 if result.returncode else 0


@command.command_decorator('lint')
class LintCommand(command.CliCommand):
  """Run lint checks on the specified files."""

  EPILOG = """
Supported file formats: %s
Supported file names: %s
""" % (' '.join(sorted(itertools.chain(*_EXT_TOOL_MAP))),
       ' '.join(sorted(itertools.chain(*_FILENAME_PATTERNS_TOOL_MAP))))

  # The output formats supported by cros lint.
  OUTPUT_FORMATS = ('default', 'colorized', 'msvs', 'parseable')

  @classmethod
  def AddParser(cls, parser: commandline.ArgumentParser):
    super().AddParser(parser)
    parser.add_argument('files', help='Files to lint', nargs='*')
    parser.add_argument('--output', default='default',
                        choices=LintCommand.OUTPUT_FORMATS,
                        help='Output format to pass to the linters. Supported '
                        'formats are: default (no option is passed to the '
                        'linter), colorized, msvs (Visual Studio) and '
                        'parseable.')
    parser.add_argument('--relaxed', default=False, action='store_true',
                        help='Disable some strict checks. This is used for '
                             'cases like builds where a more permissive '
                             'behavior is desired.')

  def _Run(self):
    files = self.options.files
    if not files:
      # Running with no arguments is allowed to make the repo upload hook
      # simple, but print a warning so that if someone runs this manually
      # they are aware that nothing was linted.
      logging.warning('No files provided to lint.  Doing nothing.')
      return 0

    # Ignore generated files.  Some tools can do this for us, but not all, and
    # it'd be faster if we just never spawned the tools in the first place.
    files = [x for x in self.options.files if not x.endswith('_pb2.py')]

    tool_map = _BreakoutFilesByTool(files)
    dispatcher = functools.partial(_Dispatcher,
                                   self.options.output, self.options.debug,
                                   self.options.relaxed)

    # If we filtered out all files, do nothing.
    # Special case one file (or fewer) as it's common -- faster to avoid the
    # parallel startup penalty.
    tasks = []
    for tool, files in tool_map.items():
      tasks.extend([tool, x] for x in files)
    if not tasks:
      return 0
    elif len(tasks) == 1:
      tool, files = next(iter(tool_map.items()))
      return dispatcher(tool, files[0])
    else:
      # Run the tool in parallel on the files.
      return sum(parallel.RunTasksInProcessPool(dispatcher, tasks))

  def Run(self):
    with timer.Timer() as t:
      ret = self._Run()
    if ret:
      logging.error('Found lint errors in %i files in %s.', ret, t)

    return 1 if ret else 0
