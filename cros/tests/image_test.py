# Copyright 2014 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Collection of tests to run on the rootfs of a built image."""

import itertools
import logging
import magic
import mimetypes
import os
import re
import stat
import unittest

from chromite.lib import cros_build_lib
from chromite.lib import osutils
from chromite.lib import perf_uploader


# File extension for file containing performance values.
PERF_EXTENSION = '.perf'
# Symlinks to mounted partitions.
ROOT_A = 'dir-ROOT-A'
STATEFUL = 'dir-STATE'


def IsPerfFile(file_name):
  """Return True if |file_name| may contain perf values."""
  return file_name.endswith(PERF_EXTENSION)


class BoardAndDirectoryMixin(object):
  """A mixin to hold image test's specific info."""

  _board = None
  _result_dir = None

  def SetBoard(self, board):
    self._board = board

  def SetResultDir(self, result_dir):
    self._result_dir = result_dir


class ImageTestCase(unittest.TestCase, BoardAndDirectoryMixin):
  """Subclass unittest.TestCase to provide utility methods for image tests.

  Tests should not directly inherit this class. They should instead inherit
  from ForgivingImageTestCase, or NonForgivingImageTestCase.

  Tests MUST use prefix "Test" (e.g.: TestLinkage, TestDiskSpace), not "test"
  prefix, in order to be picked up by the test runner.

  Tests are run outside chroot.

  The current working directory is set up so that "ROOT_A", and "STATEFUL"
  constants refer to the mounted partitions. The partitions are mounted
  readonly.

    current working directory
      + ROOT_A
        + /
          + bin
          + etc
          + usr
          ...
      + STATEFUL
        + var_overlay
        ...
  """

  def IsForgiving(self):
    """Indicate if this test is forgiving.

    The test runner will classify tests into two buckets, forgiving and non-
    forgiving. Forgiving tests DO NOT affect the result of the test runner;
    non-forgiving tests do. In either case, test runner will still output the
    result of each individual test.
    """
    raise NotImplementedError()

  def _GeneratePerfFileName(self):
    """Return a perf file name for this test.

    The file name is formatted as:

      image_test.<test_class><PERF_EXTENSION>

    e.g.:

      image_test.DiskSpaceTest.perf
    """
    test_name = 'image_test.%s' % self.__class__.__name__
    file_name = '%s%s' % (test_name, PERF_EXTENSION)
    file_name = os.path.join(self._result_dir, file_name)
    return file_name

  @staticmethod
  def GetTestName(file_name):
    """Return the test name from a perf |file_name|.

    Args:
      file_name: A path to the perf file as generated by _GeneratePerfFileName.

    Returns:
      The qualified test name part of the file name.
    """
    file_name = os.path.basename(file_name)
    pos = file_name.rindex('.')
    return file_name[:pos]

  def OutputPerfValue(self, description, value, units,
                      higher_is_better=True, graph=None):
    """Record a perf value.

    If graph name is not provided, the test method name will be used as the
    graph name.

    Args:
      description: A string description of the value such as "partition-0". A
        special description "ref" is taken as the reference.
      value: A float value.
      units: A string describing the unit of measurement such as "KB", "meter".
      higher_is_better: A boolean indicating if higher value means better
        performance.
      graph: A string name of the graph this value will be plotted on. If not
        provided, the graph name will take the test method name.
    """
    if not self._result_dir:
      logging.warning('Result directory is not set. Ignore OutputPerfValue.')
      return
    if graph is None:
      graph = self._testMethodName
    file_name = self._GeneratePerfFileName()
    perf_uploader.OutputPerfValue(file_name, description, value, units,
                                  higher_is_better, graph)


class ForgivingImageTestCase(ImageTestCase):
  """Concrete base class of forgiving tests."""

  def IsForgiving(self):
    return True


class NonForgivingImageTestCase(ImageTestCase):
  """Concrete base class of non forgiving tests."""

  def IsForgiving(self):
    return False


class ImageTestSuite(unittest.TestSuite, BoardAndDirectoryMixin):
  """Wrap around unittest.TestSuite to pass more info to the actual tests."""

  def GetTests(self):
    return self._tests

  def run(self, result, debug=False):
    for t in self._tests:
      t.SetResultDir(self._result_dir)
      t.SetBoard(self._board)
    return super(ImageTestSuite, self).run(result)


class ImageTestRunner(unittest.TextTestRunner, BoardAndDirectoryMixin):
  """Wrap around unittest.TextTestRunner to pass more info down the chain."""

  def run(self, test):
    test.SetResultDir(self._result_dir)
    test.SetBoard(self._board)
    return super(ImageTestRunner, self).run(test)


#####################
# Here go the tests
#####################


class LocaltimeTest(NonForgivingImageTestCase):
  """Verify that /etc/localtime is a symlink to /var/lib/timezone/localtime.

  This is an example of an image test. The image is already mounted. The
  test can access rootfs via ROOT_A constant.
  """

  def TestLocaltimeIsSymlink(self):
    localtime_path = os.path.join(ROOT_A, 'etc', 'localtime')
    self.assertTrue(os.path.islink(localtime_path))

  def TestLocaltimeLinkIsCorrect(self):
    localtime_path = os.path.join(ROOT_A, 'etc', 'localtime')
    self.assertEqual('/var/lib/timezone/localtime',
                     os.readlink(localtime_path))


def _GuessMimeType(magic_obj, file_name):
  """Guess a file's mimetype base on its extension and content.

  File extension is favored over file content to reduce noise.

  Args:
    magic_obj: A loaded magic instance.
    file_name: A path to the file.

  Returns:
    A mime type of |file_name|.
  """
  mime_type, _ = mimetypes.guess_type(file_name)
  if not mime_type:
    mime_type = magic_obj.file(file_name)
  return mime_type


class BlacklistTest(NonForgivingImageTestCase):
  """Verify that rootfs does not contain blacklisted items."""

  def TestBlacklistedDirectories(self):
    dirs = [os.path.join(ROOT_A, 'usr', 'share', 'locale')]
    for d in dirs:
      self.assertFalse(os.path.isdir(d), 'Directory %s is blacklisted.' % d)

  def TestBlacklistedFileTypes(self):
    """Fail if there are files of prohibited types (such as C++ source code).

    The whitelist has higher precedence than the blacklist.
    """
    blacklisted_patterns = [re.compile(x) for x in [
        r'text/x-c\+\+',
        r'text/x-c',
    ]]
    whitelisted_patterns = [re.compile(x) for x in [
        r'.*/braille/.*',
        r'.*/brltty/.*',
        r'.*/etc/sudoers$',
        r'.*/dump_vpd_log$',
        r'.*\.conf$',
        r'.*/libnl/classid$',
        r'.*/locale/',
        r'.*/X11/xkb/',
        r'.*/chromeos-assets/',
        r'.*/udev/rules.d/',
        r'.*/firmware/ar3k/.*pst$',
        r'.*/etc/services',
        r'.*/usr/share/dev-install/portage',
    ]]

    failures = []

    magic_obj = magic.open(magic.MAGIC_MIME_TYPE)
    magic_obj.load()
    for root, _, file_names in os.walk(ROOT_A):
      for file_name in file_names:
        full_name = os.path.join(root, file_name)
        if os.path.islink(full_name) or not os.path.isfile(full_name):
          continue

        mime_type = _GuessMimeType(magic_obj, full_name)
        if (any(x.match(mime_type) for x in blacklisted_patterns) and not
            any(x.match(full_name) for x in whitelisted_patterns)):
          failures.append('File %s has blacklisted type %s.' %
                          (full_name, mime_type))
    magic_obj.close()

    self.assertFalse(failures, '\n'.join(failures))

  def TestValidInterpreter(self):
    """Fail if a script's interpreter is not found, or not executable.

    A script interpreter is anything after the #! sign, up to the end of line
    or the first space.
    """
    failures = []

    for root, _, file_names in os.walk(ROOT_A):
      for file_name in file_names:
        full_name = os.path.join(root, file_name)
        file_stat = os.lstat(full_name)
        if (not stat.S_ISREG(file_stat.st_mode) or
            (file_stat.st_mode & 0111) == 0):
          continue

        with open(full_name, 'rb') as f:
          if f.read(2) != '#!':
            continue
          line = f.readline().strip()

        # Ignore arguments to the interpreter.
        interp = line.split(' ', 1)[0]
        if interp.startswith('/'):
          # Absolute path to the interpreter.
          interp = os.path.join(ROOT_A, interp.lstrip('/'))
          # Interpreter could be a symlink. Resolve it.
          interp = osutils.ResolveSymlink(interp, ROOT_A)
          if not os.path.isfile(interp):
            failures.append('File %s uses non-existing interpreter %s.' %
                            (full_name, interp))
          elif (os.stat(interp).st_mode & 0111) == 0:
            failures.append('Interpreter %s is not executable.' % interp)
        else:
          failures.append('File %s uses non-absolute interpreter path %s.' %
                          (full_name, interp))

    self.assertFalse(failures, '\n'.join(failures))


class LinkageTest(NonForgivingImageTestCase):
  """Verify that all binaries and libraries have proper linkage."""

  def setUp(self):
    self._outside_chroot = os.getcwd()
    try:
      self._inside_chroot = cros_build_lib.ToChrootPath(self._outside_chroot)
    except ValueError:
      self._inside_chroot = self._outside_chroot

    osutils.MountDir(
        os.path.join(self._outside_chroot, STATEFUL, 'var_overlay'),
        os.path.join(self._outside_chroot, ROOT_A, 'var'),
        mount_opts=('bind', ),
    )

  def tearDown(self):
    osutils.UmountDir(
        os.path.join(self._outside_chroot, ROOT_A, 'var'),
        cleanup=False,
    )

  def _IsPackageMerged(self, package_name):
    cmd = [
        'portageq-%s' % self._board,
        'has_version',
        os.path.join(self._inside_chroot, ROOT_A),
        package_name
    ]
    ret = cros_build_lib.RunCommand(cmd, error_code_ok=True,
                                    enter_chroot=True)
    return ret.returncode == 0

  def TestLinkage(self):
    """Find main executable binaries and check their linkage."""
    binaries = [
        'boot/vmlinuz',
        'bin/sed',
    ]

    if self._IsPackageMerged('chromeos-base/chromeos-login'):
      binaries.append('sbin/session_manager')

    if self._IsPackageMerged('x11-base/xorg-server'):
      binaries.append('usr/bin/Xorg')

    # When chrome is built with USE="pgo_generate", rootfs chrome is actually a
    # symlink to a real binary which is in the stateful partition. So we do not
    # check for a valid chrome binary in that case.
    if (not self._IsPackageMerged('chromeos-base/chromeos-chrome[pgo_generate]')
        and self._IsPackageMerged('chromeos-base/chromeos-chrome')):
      binaries.append('opt/google/chrome/chrome')

    binaries = [os.path.join(ROOT_A, x) for x in binaries]

    # Grab all .so files
    libraries = []
    for root, _, files in os.walk(ROOT_A):
      for name in files:
        filename = os.path.join(root, name)
        if '.so' in filename:
          libraries.append(filename)

    # lddtree is only available in the chroot but this image_test module
    # is imported by test_stages outside of the chroot too. So we dynamically
    # import lddtree here, where it actually is used.
    import lddtree
    ldpaths = lddtree.LoadLdpaths(ROOT_A)
    for to_test in itertools.chain(binaries, libraries):
      # to_test could be a symlink, we need to resolve it relative to ROOT_A.
      while os.path.islink(to_test):
        link = os.readlink(to_test)
        if link.startswith('/'):
          to_test = os.path.join(ROOT_A, link[1:])
        else:
          to_test = os.path.join(os.path.dirname(to_test), link)
      try:
        lddtree.ParseELF(to_test, root=ROOT_A, ldpaths=ldpaths)
      except lddtree.exceptions.ELFError:
        continue
      except IOError as e:
        self.fail('Fail linkage test for %s: %s' % (to_test, e))


class FileSystemMetaDataTest(ForgivingImageTestCase):
  """A test class to gather file system stats such as free inodes, blocks."""

  def TestStats(self):
    """Collect inodes and blocks usage."""
    # Find the loopback device that was mounted to ROOT_A.
    loop_device = None
    root_path = os.path.abspath(os.readlink(ROOT_A))
    for mtab in osutils.IterateMountPoints():
      if mtab.destination == root_path:
        loop_device = mtab.source
        break
    self.assertTrue(loop_device, 'Cannot find loopback device for ROOT_A.')

    # Gather file system stats with tune2fs.
    cmd = [
        'tune2fs',
        '-l',
        loop_device
    ]
    # tune2fs produces output like this:
    #
    # tune2fs 1.42 (29-Nov-2011)
    # Filesystem volume name:   ROOT-A
    # Last mounted on:          <not available>
    # Filesystem UUID:          <none>
    # Filesystem magic number:  0xEF53
    # Filesystem revision #:    1 (dynamic)
    # ...
    #
    # So we need to ignore the first line.
    ret = cros_build_lib.SudoRunCommand(cmd, capture_output=True,
                                        extra_env={'LC_ALL': 'C'})
    fs_stat = dict(line.split(':', 1) for line in ret.output.splitlines()
                   if ':' in line)
    free_inodes = int(fs_stat['Free inodes'])
    free_blocks = int(fs_stat['Free blocks'])
    inode_count = int(fs_stat['Inode count'])
    block_count = int(fs_stat['Block count'])
    block_size = int(fs_stat['Block size'])

    sum_file_size = 0
    for root, _, filenames in os.walk(ROOT_A):
      for file_name in filenames:
        full_name = os.path.join(root, file_name)
        file_stat = os.lstat(full_name)
        sum_file_size += file_stat.st_size

    metadata_size = (block_count - free_blocks) * block_size - sum_file_size

    self.OutputPerfValue('free_inodes_over_inode_count',
                         free_inodes * 100.0 / inode_count, 'percent',
                         graph='free_over_used_ratio')
    self.OutputPerfValue('free_blocks_over_block_count',
                         free_blocks * 100.0 / block_count, 'percent',
                         graph='free_over_used_ratio')
    self.OutputPerfValue('apparent_size', sum_file_size, 'bytes',
                         higher_is_better=False, graph='filesystem_stats')
    self.OutputPerfValue('metadata_size', metadata_size, 'bytes',
                         higher_is_better=False, graph='filesystem_stats')
