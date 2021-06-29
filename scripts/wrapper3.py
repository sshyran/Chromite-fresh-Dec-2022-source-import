#!/usr/bin/env python3
# Copyright 2020 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Wrapper around chromite executable scripts.

This takes care of creating a consistent environment for chromite scripts
(like setting up import paths) so we don't have to duplicate the logic in
lots of places.
"""

import importlib
import importlib.abc
import os
import sys


# Assert some minimum Python versions as we don't test or support any others.
# We only support Python 3.6+.
if sys.version_info < (3, 6):
  print('%s: chromite: error: Python-3.6+ is required, but "%s" is "%s"' %
        (sys.argv[0], sys.executable, sys.version.replace('\n', ' ')),
        file=sys.stderr)
  sys.exit(1)


CHROMITE_PATH = os.path.dirname(os.path.realpath(__file__))
while not os.path.exists(os.path.join(CHROMITE_PATH, 'PRESUBMIT.cfg')):
  CHROMITE_PATH = os.path.dirname(CHROMITE_PATH)
  assert str(CHROMITE_PATH) != '/', 'Unable to locate chromite dir'
CHROMITE_PATH += '/'


# module_repr triggers an abstract warning, but it's deprecated in Python 3.+,
# so we don't want to bother implementing it.
# pylint: disable=abstract-method
class ChromiteLoader(importlib.abc.Loader):
  """Virtual chromite module

  If the checkout is not named 'chromite', trying to do 'from chromite.xxx'
  to import modules fails horribly.  Instead, manually locate the chromite
  directory (whatever it is named), load & return it whenever someone tries
  to import it.  This lets us use the stable name 'chromite' regardless of
  how things are structured on disk.

  This also lets us keep the sys.path search clean.  Otherwise we'd have to
  worry about what other dirs chromite were checked out near to as doing an
  import would also search those for .py modules.
  """

  def __init__(self):
    # When trying to load the chromite dir from disk, we'll get called again,
    # so make sure to disable our logic to avoid an infinite loop.
    self.loading = False

  # pylint: disable=unused-argument
  def create_module(self, spec):
    """Load the current dir."""
    if self.loading:
      return None
    path, mod = os.path.split(CHROMITE_PATH[:-1])
    sys.path.insert(0, path)
    self.loading = True
    try:
      return importlib.import_module(mod)
    finally:
      # We can't pop by index as the import might have changed sys.path.
      sys.path.remove(path)
      self.loading = False

  # pylint: disable=unused-argument
  def exec_module(self, module):
    """Required stub as a loader."""


class ChromiteFinder(importlib.abc.MetaPathFinder):
  """Virtual chromite finder.

  We'll route any requests for the 'chromite' module.
  """

  def __init__(self, loader):
    self._loader = loader

  # pylint: disable=unused-argument
  def find_spec(self, fullname, path=None, target=None):
    if fullname != 'chromite' or self._loader.loading:
      return None
    return importlib.machinery.ModuleSpec(fullname, self._loader)


sys.meta_path.insert(0, ChromiteFinder(ChromiteLoader()))


# We have to put these imports after our meta-importer above.
# pylint: disable=wrong-import-position
from chromite.lib import commandline


def FindTarget(target):
  """Turn the path into something we can import from the chromite tree.

  This supports a variety of ways of running chromite programs:
  # Loaded via depot_tools in $PATH.
  $ cros_sdk --help
  # Loaded via .../chromite/bin in $PATH.
  $ cros --help
  # No $PATH needed.
  $ ./bin/cros --help
  # Loaded via ~/bin in $PATH to chromite bin/ subdir.
  $ ln -s $PWD/bin/cros ~/bin; cros --help
  # No $PATH needed.
  $ ./cbuildbot/cbuildbot --help
  # No $PATH needed, but symlink inside of chromite dir.
  $ ln -s ./cbuildbot/cbuildbot; ./cbuildbot --help
  # Loaded via ~/bin in $PATH to non-chromite bin/ subdir.
  $ ln -s $PWD/cbuildbot/cbuildbot ~/bin/; cbuildbot --help
  # No $PATH needed, but a relative symlink to a symlink to the chromite dir.
  $ cd ~; ln -s bin/cbuildbot ./; ./cbuildbot --help
  # External chromite module
  $ ln -s ../chromite/scripts/wrapper.py foo; ./foo

  Args:
    target: Path to the script we're trying to run.

  Returns:
    The module main functor.
  """
  # We assume/require the script we're wrapping ends in a .py.
  full_path = target + '.py'
  while True:
    # Walk back one symlink at a time until we get into the chromite dir.
    parent, base = os.path.split(target)
    parent = os.path.realpath(parent)
    if parent.startswith(CHROMITE_PATH):
      target = base
      break
    target = os.path.join(os.path.dirname(target), os.readlink(target))

  # If we walked all the way back to wrapper.py, it means we're trying to run
  # an external module.  So we have to import it by filepath and not via the
  # chromite.xxx.yyy namespace.
  if target != 'wrapper3.py':
    assert parent.startswith(CHROMITE_PATH), (
        'could not figure out leading path\n'
        '\tparent: %s\n'
        '\tCHROMITE_PATH: %s' % (parent, CHROMITE_PATH))
    parent = parent[len(CHROMITE_PATH):].split(os.sep)
    target = ['chromite'] + parent + [target.replace('-', '_')]

    if target[1] == 'bin':
      # Convert chromite/bin/foo -> chromite/scripts/foo.
      # Since chromite/bin/ is in $PATH, we want to keep it clean.
      target[1] = 'scripts'

    try:
      module = importlib.import_module('.'.join(target))
    except ImportError as e:
      print(
          '%s: could not import chromite module: %s: %s' % (sys.argv[0],
                                                            full_path, e),
          file=sys.stderr)
      raise
  else:
    import types
    try:
      loader = importlib.machinery.SourceFileLoader('main', full_path)
      module = types.ModuleType(loader.name)
      loader.exec_module(module)
    except IOError as e:
      print(
          '%s: could not import external module: %s: %s' % (sys.argv[0],
                                                            full_path, e),
          file=sys.stderr)
      raise

  # Run the module's main func if it has one.
  main = getattr(module, 'main', None)
  if main:
    return main

  # Is this a unittest?
  if target[-1].rsplit('_', 1)[-1] in ('test', 'unittest'):
    from chromite.lib import cros_test_lib
    return lambda _argv: cros_test_lib.main(module=module)

  # Is this a package?  Import it like `python -m...` does.
  if target != 'wrapper3.py':
    mod_name = '.'.join(target + ['__main__'])
    try:
      module = importlib.import_module(mod_name)
    except ImportError:
      module = None
    if module:
      spec = importlib.util.find_spec(mod_name)
      loader = spec.loader
      code = loader.get_code(mod_name)
      # pylint: disable=exec-used
      return lambda _argv: exec(code, {**globals(), '__name__': '__main__'})


def DoMain():
  commandline.ScriptWrapperMain(FindTarget)


if __name__ == '__main__':
  DoMain()
