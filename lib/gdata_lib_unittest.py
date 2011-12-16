#!/usr/bin/python2.6
# Copyright (c) 2011 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unit tests for the gdata_lib module."""

import getpass
import os
import shutil
import tempfile
import unittest

import mox

import cros_test_lib as test_lib
import gdata_lib

# pylint: disable=W0201
class GdataLibTest(test_lib.TestCase):

  def setUp(self):
    pass

  def testPrepColNameForSS(self):
    tests = {
      'foo': 'foo',
      'Foo': 'foo',
      'FOO': 'foo',
      'foo bar': 'foobar',
      'Foo Bar': 'foobar',
      'F O O B A R': 'foobar',
      'Foo/Bar': 'foobar',
      'Foo Bar/Dude': 'foobardude',
      'foo/bar': 'foobar',
      }

    for col in tests:
      expected = tests[col]
      self.assertEquals(expected, gdata_lib.PrepColNameForSS(col))
      self.assertEquals(expected, gdata_lib.PrepColNameForSS(expected))

  def testPrepValForSS(self):
    tests = {
      None: None,
      '': '',
      'foo': 'foo',
      'foo123': 'foo123',
      '123': "'123",
      '1.2': "'1.2",
      }

    for val in tests:
      expected = tests[val]
      self.assertEquals(expected, gdata_lib.PrepValForSS(val))

  def testPrepRowForSS(self):
    vals = {
      None: None,
      '': '',
      'foo': 'foo',
      'foo123': 'foo123',
      '123': "'123",
      '1.2': "'1.2",
      }

    # Create before and after rows (rowIn, rowOut).
    rowIn = {}
    rowOut = {}
    col = 'a' # Column names not important.
    for valIn in vals:
      valOut = vals[valIn]
      rowIn[col] = valIn
      rowOut[col] = valOut

      col = chr(ord(col) + 1) # Change column name.

    self.assertEquals(rowOut, gdata_lib.PrepRowForSS(rowIn))

  def testScrubValFromSS(self):
    tests = {
      None: None,
      'foo': 'foo',
      '123': '123',
      "'123": '123',
      }

    for val in tests:
      expected = tests[val]
      self.assertEquals(expected, gdata_lib.ScrubValFromSS(val))

class CredsTest(test_lib.MoxTestCase):

  USER = 'somedude@chromium.org'
  PASSWORD = 'worldsbestpassword'
  TMPFILE_NAME = 'creds.txt'

  def setUp(self):
    mox.MoxTestBase.setUp(self)

  @test_lib.tempfile_decorator
  def testStoreLoadCreds(self):
    # Replay script
    mocked_creds = self.mox.CreateMock(gdata_lib.Creds)
    self.mox.ReplayAll()

    # Verify
    gdata_lib.Creds.__init__(mocked_creds, user=self.USER,
                             password=self.PASSWORD)
    self.assertEquals(self.USER, mocked_creds.user)
    self.assertEquals(self.PASSWORD, mocked_creds.password)

    gdata_lib.Creds.StoreCreds(mocked_creds, self.tempfile)
    self.assertEquals(self.USER, mocked_creds.user)
    self.assertEquals(self.PASSWORD, mocked_creds.password)

    # Clear user/password before loading from just-created file.
    mocked_creds.user = None
    mocked_creds.password = None
    self.assertEquals(None, mocked_creds.user)
    self.assertEquals(None, mocked_creds.password)

    gdata_lib.Creds.LoadCreds(mocked_creds, self.tempfile)
    self.assertEquals(self.USER, mocked_creds.user)
    self.assertEquals(self.PASSWORD, mocked_creds.password)
    self.mox.VerifyAll()

  @test_lib.tempfile_decorator
  def testCredsInitFromFile(self):
    open(self.tempfile, 'w').close()

    # Replay script
    mocked_creds = self.mox.CreateMock(gdata_lib.Creds)
    mocked_creds.LoadCreds(self.tempfile)
    self.mox.ReplayAll()

    # Verify
    gdata_lib.Creds.__init__(mocked_creds, cred_file=self.tempfile)
    self.mox.VerifyAll()

  def testCredsInitFromUserPassword(self):
    # Replay script
    mocked_creds = self.mox.CreateMock(gdata_lib.Creds)
    self.mox.ReplayAll()

    # Verify
    gdata_lib.Creds.__init__(mocked_creds, user=self.USER,
                             password=self.PASSWORD)
    self.mox.VerifyAll()
    self.assertEquals(self.USER, mocked_creds.user)
    self.assertEquals(self.PASSWORD, mocked_creds.password)

  def testCredsInitFromUser(self):
    # Add test-specific mocks/stubs
    self.mox.StubOutWithMock(getpass, 'getpass')

    # Replay script
    mocked_creds = self.mox.CreateMock(gdata_lib.Creds)
    getpass.getpass(mox.IgnoreArg()).AndReturn(self.PASSWORD)
    self.mox.ReplayAll()

    # Verify
    gdata_lib.Creds.__init__(mocked_creds, user=self.USER)
    self.mox.VerifyAll()
    self.assertEquals(self.USER, mocked_creds.user)
    self.assertEquals(self.PASSWORD, mocked_creds.password)

if __name__ == '__main__':
  unittest.main()
