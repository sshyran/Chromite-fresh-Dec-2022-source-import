# Copyright 2021 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unit tests for xz_auto.py."""

import os
from pathlib import Path
import unittest

from chromite.lib import cros_build_lib
from chromite.lib import cros_test_lib
from chromite.lib import osutils
from chromite.scripts import xz_auto


DIR = Path(__file__).resolve().parent


def FindXzAutoLocation():
  """Figures out where the xz_auto binary is."""
  return DIR / 'xz_auto'


class XzAutoTests(cros_test_lib.MockTempDirTestCase):
  """Various tests for xz_auto."""

  def DisablePixzForCurrentTest(self):
    """Disables the use of pixz for the current test."""
    # This will be cleaned up by cros_test_lib, so no need to addCleanup.
    os.environ[xz_auto.PIXZ_DISABLE_VAR] = '1'

  def testPixzCompressedFileNameDeterminationSeemsToWork(self):
    """Tests our detection of file names in pixz commandlines."""
    self.assertEqual(
        xz_auto.DetermineFilesPassedToPixz(['to_compress.txt']),
        ('to_compress.txt', None),
    )
    self.assertEqual(
        xz_auto.DetermineFilesPassedToPixz(
            ['to_compress.txt', 'compressed.txt']),
        ('to_compress.txt', 'compressed.txt'),
    )
    self.assertEqual(
        xz_auto.DetermineFilesPassedToPixz(
            ['to_compress.txt', '-c', 'compressed.txt', '-9']),
        ('to_compress.txt', 'compressed.txt'),
    )
    self.assertEqual(
        xz_auto.DetermineFilesPassedToPixz(
            ['-t', 'to_compress.txt', '-c', 'compressed.txt', '-p', '2']),
        ('to_compress.txt', 'compressed.txt'),
    )
    self.assertEqual(
        xz_auto.DetermineFilesPassedToPixz(
            ['-tcp2', 'to_compress.txt', 'compressed.txt']),
        ('to_compress.txt', 'compressed.txt'),
    )

  @unittest.skipIf(not xz_auto.HasPixz(), 'need pixz for this test')
  def testPixzCommandCreationSelectsPixzIfAvailable(self):
    """Tests that we actually execute pixz when we intend to."""
    compress_command = xz_auto.GetCompressCommand(
        stdout=False,
        jobs=1,
        argv=['file_to_compress.txt'],
    )
    self.assertEqual(compress_command[0], 'pixz')

    decompress_command = xz_auto.GetDecompressCommand(
        stdout=False,
        jobs=1,
        argv=[],
    )
    self.assertEqual(decompress_command[0], 'pixz')

  def _TestFileCompressionImpl(self):
    """Tests that compressing a file with xz_auto WAI."""
    file_contents = b'some random file contents'
    file_location = os.path.join(self.tempdir, 'file.txt')
    osutils.WriteFile(file_location, file_contents, mode='wb')

    xz_auto_script = str(FindXzAutoLocation())
    cros_build_lib.run(
        [
            xz_auto_script,
            file_location,
        ],
        check=True,
    )

    xz_location = file_location + '.xz'
    self.assertExists(xz_location)
    self.assertNotExists(file_location)
    cros_build_lib.run([
        xz_auto_script,
        '--decompress',
        xz_location,
    ])
    self.assertNotExists(xz_location)
    self.assertExists(file_location)
    self.assertEqual(
        osutils.ReadFile(file_location, mode='rb'),
        file_contents,
    )

  def _TestStdoutCompressionImpl(self):
    """Tests that compressing stdstreams with xz_auto WAI."""
    file_contents = b'some random file contents'
    xz_auto_script = str(FindXzAutoLocation())

    run_result = cros_build_lib.run(
        [
            xz_auto_script,
            '-c',
        ],
        capture_output=True,
        input=file_contents,
    )

    compressed_file = run_result.stdout
    self.assertNotEqual(compressed_file, file_contents)

    run_result = cros_build_lib.run(
        [
            xz_auto_script,
            '--decompress',
            '-c',
        ],
        input=compressed_file,
        capture_output=True,
    )
    uncompressed_file = run_result.stdout
    self.assertEqual(file_contents, uncompressed_file)

  @unittest.skipIf(not xz_auto.HasPixz(), 'need pixz for this test')
  def testFileCompressionWithPixzWorks(self):
    """Tests that compressing a file with pixz WAI."""
    self._TestFileCompressionImpl()

  @unittest.skipIf(not xz_auto.HasPixz(), 'need pixz for this test')
  def testStdoutCompressionWithPixzWorks(self):
    """Tests that compressing `stdout` with pixz WAI."""
    self._TestStdoutCompressionImpl()

  def testFileCompressionWithXzWorks(self):
    """Tests that compressing a file with pixz WAI."""
    self.DisablePixzForCurrentTest()
    self._TestFileCompressionImpl()

  def testStdoutCompressionWithXzWorks(self):
    """Tests that compressing `stdout` with pixz WAI."""
    self.DisablePixzForCurrentTest()
    self._TestStdoutCompressionImpl()
