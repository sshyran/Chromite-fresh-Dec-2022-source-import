# Copyright 2015 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Module for instantiating builders.

Typically builder classes/objects are obtained indirectly via the helpers in
this module.  This is because the cbuildbot_config settings can't import this
module (and children directly): it might lead to circular references, and it
would add a lot of overhead to that module.  Generally only the main cbuildbot
module needs to care about the builder classes.

If you're looking for a specific builder implementation, then check out the
*_builders.py modules that are in this same directory.  The cbuildbot_config
has a builder_class_name member that controls the type of builder that is used
for each config.  e.g. builder_class_name='Simple' would look for the class
whose name is 'SimpleBuilder' in all the *_builders.py modules.
"""

from __future__ import print_function

import glob
import os

from chromite.lib import cros_import


def GetBuilderClass(name):
  """Locate the builder class with |name|.

  Examples:
    If you want to create a new SimpleBuilder, you'd do:
    cls = builders.GetBuilderClass('Simple')
    builder = cls(...)

  Args:
    name: The base name of the builder class.

  Returns:
    The class used to instantiate this type of builder.

  Raises:
    AttributeError when |name| could not be found.
  """
  if '.' not in name:
    raise ValueError('name should be "<module>.<builder>" not "%s"' % name)
  mod_name, builder_class_name = name.split('.')

  target = 'chromite.cbuildbot.builders.%s' % mod_name
  module = cros_import.ImportModule(target)

  # See if this module has the builder we care about.
  if hasattr(module, builder_class_name):
    return getattr(module, builder_class_name)

  raise AttributeError('could not locate %s builder' % builder_class_name)


def Builder(builder_run):
  """Given a |builder_run| runtime, return an instantiated builder

  This is a helper wrapper that resolves the builder_class_name field in the
  builder settings (which was declared in cbuildbot_config) to the actual class
  found in the builder modules.

  Args:
    builder_run: A cbuildbot_run.BuilderRun object.

  Returns:
    An object of type generic_builders.Builder.
  """
  cls = GetBuilderClass(builder_run.config.builder_class_name)
  return cls(builder_run)
