# Copyright 2015 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Common project related utilities."""

from __future__ import print_function

import json
import os

from chromite.lib import cros_build_lib
from chromite.lib import osutils
from chromite.lib import portage_util

_DEFAULT_LAYOUT_CONF = {'profile-formats': 'portage-2',
                        'thin-manifests': 'true',
                        'use-manifests': 'true'}

_PROJECT_JSON = 'project.json'


class ProjectAlreadyExists(Exception):
  """The project already exists."""


class ProjectNotFound(Exception):
  """The project does not exist."""

class ProjectFeatureNotSupported(Exception):
  """Attempted feature not supported for this project."""

class Project(object):
  """Encapsulates the interaction with a project."""

  def __init__(self, project_dir, initial_config=None, allow_legacy=True):
    """Instantiates a project object.

    Args:
      project_dir: The root directory of the project.
      initial_config: The initial configuration as a python dictionary.
        If not None, creates a project with this configuration.
      allow_legacy: Allow board overlays, simulating a basic read-only config.
        Ignored if |initial_config| is not None.

    Raises:
      ProjectNotFound: when |project_dir| is not a project and no initial
        configuration was provided.
      ProjectAlreadyExists: when trying to create a project but |project_dir|
        already contains one.
    """
    self.project_dir = project_dir
    self.config = None
    self.legacy = False
    project_json = os.path.join(project_dir, _PROJECT_JSON)

    if not os.path.exists(project_json):
      if initial_config:
        self.UpdateConfig(initial_config)
      elif allow_legacy:
        self.legacy = True
        try:
          self.config = {'name': self._ReadLayoutConf()['repo-name']}
        except (IOError, KeyError):
          pass

      if self.config is None:
        raise ProjectNotFound(self.project_dir)
    elif initial_config is None:
      self.config = json.loads(osutils.ReadFile(project_json))
    else:
      raise ProjectAlreadyExists(self.project_dir)

  def _LayoutConfPath(self):
    """Returns the path to the layout.conf file."""
    return os.path.join(self.project_dir, 'metadata', 'layout.conf')

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
    osutils.WriteFile(
        os.path.join(self.project_dir, 'profiles', 'base', 'parent'),
        ''.join([p + '\n' for p in parents]), makedirs=True)

  def UpdateConfig(self, config, regenerate=True):
    """Updates the project's configuration.

    Write the json representation of |config| in project.json.
    If |regenerate| is true, regenerate the portage configuration files in
    this project to match the new project.json.

    Args:
      config: project configuration as a python dict
      regenerate: if True, regenerate autogenerated project files
    """
    if self.legacy:
      raise ProjectFeatureNotSupported(
          'Cannot update configuration of legacy project %s' % self.project_dir)

    self.config = config
    formatted_config = json.dumps(config, sort_keys=True, indent=4,
                                  separators=(',', ': '))
    osutils.WriteFile(os.path.join(self.project_dir, _PROJECT_JSON),
                      formatted_config, makedirs=True)

    if regenerate:
      self.GeneratePortageConfig()

  def GeneratePortageConfig(self):
    """Generates all autogenerated project files."""
    deps = [d.get('name', None) for d in self.config.get('dependencies', [])]
    if None in deps:
      cros_build_lib.Die('Invalid dependency name')

    self._WriteLayoutConf(
        {'masters': ' '.join(['portage-stable', 'chromiumos'] + deps),
         'repo-name': self.config['name']})

    self._WriteParents([m + ':base' for m in deps])

  def Inherits(self, project_name):
    """Checks whether this project contains |project_name|.

    Args:
      project_name: The name of the project to check containment.

    Returns:
      Whether |project_name| is contained in this project.
    """
    return bool('name' in self.config and
                _FindProjectInOverlays(project_name, self.config['name']))

  def MainPackages(self):
    """Returns the project's main package(s).

    This finds the 'main_package' property.  It nevertheless returns a (single
    element) list as it is easier to work with.

    Returns:
      A list of main packages; empty if no main package configured.
    """
    main_package = self.config.get('main_package')
    return [main_package] if main_package else []


def _FindProjectInOverlays(name, base=None):
  """Returns the parent project of |base| that matches |name|.

  Will prefer an exact match, but if one does not exist then it would settle
  for the private repo name. This is needed for backward compatibility with
  Chrome OS repo naming convention and should be adapted accordingly.

  Args:
    name: Overlay/project name to look for.
    base: Base project/overlay name to scan from; if None, uses |name|.

  Returns:
    The project associated to |name| if one exists, otherwise None.
  """
  if not name:
    return None
  if base is None:
    base = name

  private_proj = None
  try:
    for overlay in portage_util.FindOverlays('both', base):
      try:
        proj = Project(overlay)
        proj_name = proj.config.get('name')
        if proj_name == name:
          return proj
        if proj_name.rstrip('-private') == name:
          private_proj = proj
      except ProjectNotFound:
        pass
  except portage_util.MissingOverlayException:
    pass

  return private_proj


def FindProjectInPath(path=None):
  """Returns the root directory of the project containing a path.

  Return the first parent directory of |path| that is the root of a project.
  This method is used for project auto-detection and does not consider legacy.

  Args:
    path: path to a directory. If |path| is None, |path| will be set to CWD.

  Returns:
    The path to the first parent that is a project directory if one exist.
    Otherwise return None.
  """
  for p in osutils.IteratePathParents(path or os.getcwd()):
    try:
      return Project(p, allow_legacy=False)
    except ProjectNotFound:
      pass

  return None


def FindProjectByName(name):
  """Returns the project associated to |name|.

  Args:
    name: A project name.

  Returns:
    The project associated to |name| if one exists, otherwise None.
  """
  return _FindProjectInOverlays(name)
