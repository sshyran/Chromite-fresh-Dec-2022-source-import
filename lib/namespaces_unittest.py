# Copyright 2014 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unittests for the namespaces.py module."""

import errno
import os
import unittest

from chromite.lib import commandline
from chromite.lib import cros_test_lib
from chromite.lib import namespaces


class SetNSTests(cros_test_lib.TestCase):
  """Tests for SetNS()"""

  def testBasic(self):
    """Simple functionality test."""
    NS_PATH = '/proc/self/ns/mnt'
    if not os.path.exists(NS_PATH):
      raise unittest.SkipTest('kernel too old (missing %s)' % NS_PATH)

    with open(NS_PATH) as f:
      try:
        namespaces.SetNS(f.fileno(), 0)
      except OSError as e:
        if e.errno != errno.EPERM:
          # Running as non-root will fail, so ignore it.  We ran most
          # of the code in the process which is all we really wanted.
          raise


class UnshareTests(cros_test_lib.TestCase):
  """Tests for Unshare()"""

  def testBasic(self):
    """Simple functionality test."""
    try:
      namespaces.Unshare(namespaces.CLONE_NEWNS)
    except OSError as e:
      if e.errno != errno.EPERM:
        # Running as non-root will fail, so ignore it.  We ran most
        # of the code in the process which is all we really wanted.
        raise

class ReExecuteWithNamespaceTests(cros_test_lib.MockTestCase):
  """Tests for ReExecuteWithNamespace()."""

  def testReExecuteWithNamespace(self):
    """Test that SimpleUnshare is called and the non-root user is restored."""
    self.PatchObject(commandline, 'RunAsRootUser')
    self.PatchDict(os.environ, {
        'SUDO_GID': '123',
        'SUDO_UID': '456',
        'SUDO_USER': 'testuser',
    })
    simple_unshare_mock = self.PatchObject(namespaces, 'SimpleUnshare')
    os_initgroups_mock = self.PatchObject(os, 'initgroups')
    os_setresgid_mock = self.PatchObject(os, 'setresgid')
    os_setresuid_mock = self.PatchObject(os, 'setresuid')

    namespaces.ReExecuteWithNamespace([])

    simple_unshare_mock.assert_called_once_with(net=True, pid=True)
    os_initgroups_mock.assert_called_once_with('testuser', 123)
    os_setresgid_mock.assert_called_once_with(123, 123, 123)
    os_setresuid_mock.assert_called_once_with(456, 456, 456)
    self.assertEqual('testuser', os.environ['USER'])
