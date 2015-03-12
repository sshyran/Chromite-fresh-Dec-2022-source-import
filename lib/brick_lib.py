# Copyright 2015 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Common brick related utilities."""

from __future__ import print_function

import json
import os

from chromite.cbuildbot import constants
from chromite.lib import osutils
from chromite.lib import portage_util
from chromite.lib import workspace_lib

_DEFAULT_LAYOUT_CONF = {'profile-formats': 'portage-2',
                        'thin-manifests': 'true',
                        'use-manifests': 'true'}

_CONFIG_JSON = 'config.json'


_BOARD_PREFIX = 'board:'
_WORKSPACE_PREFIX = '//'

_IGNORED_OVERLAYS = ('portage-stable', 'chromiumos', 'eclass-overlay')


class BrickCreationFailed(Exception):
  """The brick creation failed."""


class BrickNotFound(Exception):
  """The brick does not exist."""


class BrickFeatureNotSupported(Exception):
  """Attempted feature not supported for this brick."""


class Brick(object):
  """Encapsulates the interaction with a brick."""

  def __init__(self, brick_loc, initial_config=None, allow_legacy=True):
    """Instantiates a brick object.

    Args:
      brick_loc: brick locator. This can be a relative path to CWD, an absolute
        path, a public board name prefix with 'board:' or a relative path to the
        root of the workspace, prefixed with '//').
      initial_config: The initial configuration as a python dictionary.
        If not None, creates a brick with this configuration.
      allow_legacy: Allow board overlays, simulating a basic read-only config.
        Ignored if |initial_config| is not None.

    Raises:
      BrickNotFound: when |brick_loc| is not a brick and no initial
        configuration was provided.
      BrickCreationFailed: when the brick could not be created successfully.
    """
    if IsLocator(brick_loc):
      self.brick_dir = _LocatorToPath(brick_loc)
      self.brick_locator = brick_loc
    else:
      self.brick_dir = brick_loc
      self.brick_locator = _PathToLocator(brick_loc)

    self.config = None
    self.legacy = False
    config_json = os.path.join(self.brick_dir, _CONFIG_JSON)

    if not os.path.exists(config_json):
      if initial_config:
        if os.path.exists(self.brick_dir):
          raise BrickCreationFailed('directory %s already exists.'
                                    % self.brick_dir)
        success = False
        try:
          self.UpdateConfig(initial_config)
          success = True
        except BrickNotFound as e:
          # If BrickNotFound was raised, the dependencies contain a missing
          # brick.
          raise BrickCreationFailed('dependency not found %s' % e)
        finally:
          if not success:
            # If the brick creation failed for any reason, cleanup the partially
            # created brick.
            osutils.RmDir(self.brick_dir, ignore_missing=True)

      elif allow_legacy:
        self.legacy = True
        try:
          masters = self._ReadLayoutConf().get('masters')
          masters_list = masters.split() if masters else []

          # Keep general Chromium OS overlays out of this list as they are
          # handled separately by the build system.
          deps = ['board:' + d for d in masters_list
                  if d not in _IGNORED_OVERLAYS]
          self.config = {'name': self._ReadLayoutConf()['repo-name'],
                         'dependencies': deps}
        except (IOError, KeyError):
          pass

      if self.config is None:
        raise BrickNotFound(self.brick_dir)
    elif initial_config is None:
      self.config = json.loads(osutils.ReadFile(config_json))
    else:
      raise BrickCreationFailed('brick %s already exists.' % self.brick_dir)

  def _LayoutConfPath(self):
    """Returns the path to the layout.conf file."""
    return os.path.join(self.OverlayDir(), 'metadata', 'layout.conf')

  def _WriteLayoutConf(self, content):
    """Writes layout.conf.

    Sets unset fields to a sensible default and write |content| in layout.conf
    in the right format.

    Args:
      content: dictionary containing the set fields in layout.conf.
    """
    for k, v in _DEFAULT_LAYOUT_CONF.iteritems():
      content.setdefault(k, v)

    content_str = ''.join(['%s = %s\n' % (k, v)
                           for k, v in content.iteritems()])
    osutils.WriteFile(self._LayoutConfPath(), content_str, makedirs=True)

  def _ReadLayoutConf(self):
    """Returns the content of layout.conf as a Python dictionary."""
    def ParseConfLine(line):
      k, _, v = line.partition('=')
      return k.strip(), v.strip() or None

    content_str = osutils.ReadFile(self._LayoutConfPath())
    return dict(ParseConfLine(line) for line in content_str.splitlines())

  def _WriteParents(self, parents):
    """Writes the parents profile.

    Args:
      parents: list of overlay names
    """
    if self.legacy:
      raise BrickFeatureNotSupported()

    osutils.WriteFile(os.path.join(self.OverlayDir(), 'profiles', 'base',
                                   'parent'),
                      ''.join([p + '\n' for p in parents]), makedirs=True)

  def UpdateConfig(self, config, regenerate=True):
    """Updates the brick's configuration.

    Write the json representation of |config| in config.json.
    If |regenerate| is true, regenerate the portage configuration files in
    this brick to match the new config.json.

    Args:
      config: brick configuration as a python dict
      regenerate: if True, regenerate autogenerated brick files
    """
    if self.legacy:
      raise BrickFeatureNotSupported(
          'Cannot update configuration of legacy brick %s' % self.brick_dir)

    self.config = config
    # All objects must be unambiguously referenced. Normalize all the
    # dependencies according to the workspace.
    self.config['dependencies'] = [d if IsLocator(d) else _PathToLocator(d)
                                   for d in self.config.get('dependencies', [])]

    formatted_config = json.dumps(config, sort_keys=True, indent=4,
                                  separators=(',', ': '))
    osutils.WriteFile(os.path.join(self.brick_dir, _CONFIG_JSON),
                      formatted_config, makedirs=True)

    if regenerate:
      self.GeneratePortageConfig()

  def GeneratePortageConfig(self):
    """Generates all autogenerated brick files."""
    # We don't generate anything in legacy brick so everything is up-to-date.
    if self.legacy:
      return

    deps = [b.config['name'] for b in self.Dependencies()]

    self._WriteLayoutConf(
        {'masters': ' '.join(['portage-stable', 'chromiumos'] + deps),
         'repo-name': self.config['name']})

    self._WriteParents([m + ':base' for m in deps])

  def Dependencies(self):
    """Returns the dependent bricks."""
    return [Brick(d) for d in self.config.get('dependencies', [])]

  def Inherits(self, brick_name):
    """Checks whether this brick contains |brick_name|.

    Args:
      brick_name: The name of the brick to check containment.

    Returns:
      Whether |brick_name| is contained in this brick.
    """
    return bool('name' in self.config and
                _FindBrickInOverlays(brick_name, self.config['name']))

  def MainPackages(self):
    """Returns the brick's main package(s).

    This finds the 'main_package' property.  It nevertheless returns a (single
    element) list as it is easier to work with.

    Returns:
      A list of main packages; empty if no main package configured.
    """
    main_package = self.config.get('main_package')
    return [main_package] if main_package else []

  def OverlayDir(self):
    """Returns the brick's overlay directory."""
    if self.legacy:
      return self.brick_dir

    return os.path.join(self.brick_dir, 'packages')

  def SourceDir(self):
    """Returns the project's source directory."""
    return os.path.join(self.brick_dir, 'src')

  def FriendlyName(self):
    """Return the friendly name for this brick.

    This name is used as the board name for legacy commands (--board).
    """
    if self.legacy:
      raise BrickFeatureNotSupported()
    return self.brick_locator[len(_WORKSPACE_PREFIX):].replace('/', '.')

  def BrickStack(self):
    """Returns the brick stack for this brick.

    Returns:
      A list of bricks, respecting the partial ordering of bricks as defined by
      dependencies, ordered from the lowest priority to the highest priority.
    """
    seen = set()
    def _stack(brick):
      seen.add(brick.brick_dir)
      l = []
      for dep in brick.Dependencies():
        if dep.brick_dir not in seen:
          l.extend(_stack(dep))
      l.append(brick)
      return l

    return _stack(self)


def IsLocator(name):
  """Returns True if name is a specific locator."""
  return name.startswith(_WORKSPACE_PREFIX) or name.startswith(_BOARD_PREFIX)


def _LocatorToPath(locator):
  """Returns the absolute path for this locator.

  Args:
    locator: a brick/overlay locator.

  Returns:
    The absolute path to the brick.

  Raises:
    ValueError if the locator is invalid.
  """
  if locator.startswith(_WORKSPACE_PREFIX):
    return os.path.join(workspace_lib.WorkspacePath(),
                        locator[len(_WORKSPACE_PREFIX):])
  if locator.startswith(_BOARD_PREFIX):
    return os.path.join(constants.SOURCE_ROOT, 'src', 'overlays',
                        'overlay-%s' % locator[len(_BOARD_PREFIX):])
  raise ValueError('Invalid brick locator %s' % locator)


def _PathToLocator(path):
  """Converts a path to a brick locator.

  This does not raise error if the path does not map to a locator. Some valid
  (legacy) brick path do not map to any locator: chromiumos-overlay,
  private board overlays, etc...

  Args:
    path: absolute or relative to CWD path to a brick or overlay.

  Returns:
    The locator for this brick if it exists, None otherwise.
  """
  workspace_path = workspace_lib.WorkspacePath()
  path = os.path.abspath(path)

  if workspace_path is None:
    return None

  # If path is in the current workspace, return the relative path prefixed with
  # //.
  if os.path.commonprefix([path, workspace_path]) == workspace_path:
    return _WORKSPACE_PREFIX + os.path.relpath(path, workspace_path)

  # If path is in the src directory of the checkout, this is a board overlay.
  # Return board:board_name
  src_path = os.path.join(constants.SOURCE_ROOT, 'src')
  if os.path.commonprefix([path, src_path]) == src_path:
    parts = os.path.split(os.path.relpath(path, src_path))
    if parts[0] == 'overlays':
      board_name = '-'.join(parts[1].split('-')[1:])
      return _BOARD_PREFIX + board_name

  return None


def _FindBrickInOverlays(name, base=None):
  """Returns the parent brick of |base| that matches |name|.

  Will prefer an exact match, but if one does not exist then it would settle
  for the private repo name. This is needed for backward compatibility with
  Chrome OS repo naming convention and should be adapted accordingly.

  Args:
    name: Overlay/brick name to look for.
    base: Base brick/overlay name to scan from; if None, uses |name|.

  Returns:
    The brick associated to |name| if one exists, otherwise None.
  """
  if not name:
    return None
  if base is None:
    base = name

  private_proj = None
  try:
    for overlay in portage_util.FindOverlays('both', base):
      try:
        try:
          # portage_util.FindOverlay will return an overlay list instead of a
          # brick list.
          # Use the parent directory if it is a Brick.
          proj = Brick(os.path.dirname(overlay), allow_legacy=False)
        except BrickNotFound:
          proj = Brick(overlay)
        proj_name = proj.config.get('name')
        if proj_name == name:
          return proj
        if proj_name == name + '-private':
          private_proj = proj
      except BrickNotFound:
        pass
  except portage_util.MissingOverlayException:
    pass

  return private_proj


def FindBrickInPath(path=None):
  """Returns the root directory of the brick containing a path.

  Return the first parent directory of |path| that is the root of a brick.
  This method is used for brick auto-detection and does not consider legacy.

  Args:
    path: path to a directory. If |path| is None, |path| will be set to CWD.

  Returns:
    The path to the first parent that is a brick directory if one exist.
    Otherwise return None.
  """
  for p in osutils.IteratePathParents(path or os.getcwd()):
    try:
      return Brick(p, allow_legacy=False)
    except BrickNotFound:
      pass

  return None


def FindBrickByName(name):
  """Returns the brick associated to |name|.

  Args:
    name: A brick name.

  Returns:
    The brick associated to |name| if one exists, otherwise None.
  """
  return _FindBrickInOverlays(name)
