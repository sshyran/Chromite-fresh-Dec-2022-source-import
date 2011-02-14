#!/usr/bin/python

# Copyright (c) 2011 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# Copyright (c) 2003-2005 by Peter Astrand <astrand@lysator.liu.se>
# Licensed to PSF under a Contributor Agreement.
# See http://www.python.org/2.4/license for licensing details.

"""Subprocress execution

This module holds a subclass of subprocess.Popen with our own required
features.
"""

import errno
import os
import pty
import select
import subprocess
import sys
import unittest



class Popen(subprocess.Popen):
  """Like subprocess.Popen with ptys and incremental output

  This class deals with running a child process and filtering its output on
  both stdout and stderr while it is running. We do this so we can monitor
  progress, and possibly relay the output to the user if requested.

  The class is similar to subprocess.Popen, the equivalent is something like:

    Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

  But this class has many fewer features, and two enhancement:

  1. Rather than getting the output data only at the end, this class sends it
     to a provided operation as it arrives.
  2. We use pseudo terminals so that the child will hopefully flush its output
     to us as soon as it is produced, rather than waiting for the end of a
     line.

  Use CommunicateFilter() to handle output from the subprocess.

  """
  PIPE_PTY = -3

  def __init__(self, args, stdin=None, stdout=PIPE_PTY, stderr=PIPE_PTY,
      shell=False, cwd=None, env=None, **kwargs):
    """Cut-down constructor

    Args:
      args: Program and arguments for subprocess to execute.
      stdin: See subprocess.Popen()
      stdout: See subprocess.Popen(), except that we support the sentinel
          value of cros_subprocess.Popen.PIPE_PTY.
      stderr: See subprocess.Popen(), except that we support the sentinel
          value of cros_subprocess.Popen.PIPE_PTY.
      shell: See subprocess.Popen()
      cwd: Working directory to change to for subprocess, or None if none.
      env: Environment to use for this subprocess, or None to inherit parent.
      kwargs: No other arguments are supported at the moment.  Passing other
          arguments will cause a ValueError to be raised.
    """
    stdout_pty = None
    stderr_pty = None

    if stdout == Popen.PIPE_PTY:
      stdout_pty = pty.openpty()
      stdout = os.fdopen(stdout_pty[1])
    if stderr == Popen.PIPE_PTY:
      stderr_pty = pty.openpty()
      stderr = os.fdopen(stderr_pty[1])

    super(Popen, self).__init__(args, stdin=stdin,
        stdout=stdout, stderr=stderr, shell=shell, cwd=cwd, env=env,
        **kwargs)

    # If we're on a PTY, we passed the slave half of the PTY to the subprocess.
    # We want to use the master half on our end from now on.  Setting this here
    # does make some assumptions about the implementation of subprocess, but
    # those assumptions are pretty minor.
    if stdout_pty is not None:
      self.stdout = os.fdopen(stdout_pty[0])
    if stderr_pty is not None:
      self.stderr = os.fdopen(stderr_pty[0])

    # Insist that unit tests exist for other arguments we don't support.
    if kwargs:
      raise ValueError("Unit tests do not test extra args - please add tests")

  def CommunicateFilter(self, operation):
    """Interact with process: Read data from stdout and stderr.

    This method runs until end-of-file is reached, then waits for the
    subprocess to terminate.

    The operation object is send all output from the subprocess through its
    Output() method which must be defined like this:

      def Output(self, stream, data)
      Args:
        stream: the stream the output was received on, which will be
            sys.stdout or sys.stderr.
        data: a string containing the data

    Note: The data read is buffered in memory, so do not use this
    method if the data size is large or unlimited.

    Args:
      operation: Operation to use for this subprocess.

    Returns:
      A tuple (stdout, stderr, combined) which is the data received on
      stdout, stderr and the combined data (interleaved stdout and stderr).
    """

    read_set = []
    write_set = []
    stdout = None # Return
    stderr = None # Return

    if self.stdin:
      # Flush stdio buffer.  This might block, if the user has
      # been writing to .stdin in an uncontrolled fashion.
      self.stdin.flush()
      if input:
        write_set.append(self.stdin)
      else:
        self.stdin.close()
    if self.stdout:
      read_set.append(self.stdout)
      stdout = []
    if self.stderr:
      read_set.append(self.stderr)
      stderr = []
    combined = []

    input_offset = 0
    while read_set or write_set:
      try:
        rlist, wlist, _ = select.select(read_set, write_set, [])
      except select.error, e:
        if e.args[0] == errno.EINTR:
          continue
        raise

      if self.stdin in wlist:
        # When select has indicated that the file is writable,
        # we can write up to PIPE_BUF bytes without risk
        # blocking.  POSIX defines PIPE_BUF >= 512
        chunk = input[input_offset : input_offset + 512]
        bytes_written = os.write(self.stdin.fileno(), chunk)
        input_offset += bytes_written
        if input_offset >= len(input):
          self.stdin.close()
          write_set.remove(self.stdin)

      if self.stdout in rlist:
        data = ""
        # We will get an error on read if the pty is closed
        try:
          data = os.read(self.stdout.fileno(), 1024)
        except OSError:
          pass
        if data == "":
          self.stdout.close()
          read_set.remove(self.stdout)
        else:
          stdout.append(data)
          combined.append(data)
          operation.Output(sys.stdout, data)
      if self.stderr in rlist:
        data = ""
        # We will get an error on read if the pty is closed
        try:
          data = os.read(self.stderr.fileno(), 1024)
        except OSError:
          pass
        if data == "":
          self.stderr.close()
          read_set.remove(self.stderr)
        else:
          stderr.append(data)
          combined.append(data)
          operation.Output(sys.stderr, data)

    # All data exchanged.  Translate lists into strings.
    if stdout is not None:
      stdout = ''.join(stdout)
    if stderr is not None:
      stderr = ''.join(stderr)
    combined = ''.join(combined)

    # Translate newlines, if requested.  We cannot let the file
    # object do the translation: It is based on stdio, which is
    # impossible to combine with select (unless forcing no
    # buffering).
    if self.universal_newlines and hasattr(file, 'newlines'):
      if stdout:
        stdout = self._translate_newlines(stdout)
      if stderr:
        stderr = self._translate_newlines(stderr)

    self.wait()
    return (stdout, stderr, combined)


# Just being a unittest.TestCase gives us 14 public methods.  Unless we
# disable this, we can only have 6 tests in a TestCase.  That's not enough.
#
# pylint: disable=R0904

class TestSubprocess(unittest.TestCase):
  """Our simple unit test for this module"""

  class MyOperation:
    """Provides a operation that we can pass to Popen"""
    def __init__(self, input_to_send=None):
      """Constructor to set up the operation and possible input.

      Args:
        input_to_send: a text string to send when we first get input. We will
          add \r\n to the string.
      """
      self.stdout_data = ''
      self.stderr_data = ''
      self.combined_data = ''
      self.stdin_pipe = None
      self._input_to_send = input_to_send
      if input_to_send:
        pipe = os.pipe()
        self.stdin_read_pipe = pipe[0]
        self._stdin_write_pipe = os.fdopen(pipe[1], 'w')

    def Output(self, stream, data):
      """Output handler for Popen. Stores the data for later comparison"""
      if stream == sys.stdout:
        self.stdout_data += data
      if stream == sys.stderr:
        self.stderr_data += data
      self.combined_data += data

      # Output the input string if we have one.
      if self._input_to_send:
        self._stdin_write_pipe.write(self._input_to_send + '\r\n')
        self._stdin_write_pipe.flush()

  def _BasicCheck(self, plist, oper):
    """Basic checks that the output looks sane."""
    self.assertEqual(plist[0], oper.stdout_data)
    self.assertEqual(plist[1], oper.stderr_data)
    self.assertEqual(plist[2], oper.combined_data)

    # The total length of stdout and stderr should equal the combined length
    self.assertEqual(len(plist[0]) + len(plist[1]), len(plist[2]))

  def test_simple(self):
    """Simple redirection: Get process list"""
    oper = TestSubprocess.MyOperation()
    plist = Popen(['ps']).CommunicateFilter(oper)
    self._BasicCheck(plist, oper)

  def test_stderr(self):
    """Check stdout and stderr"""
    oper = TestSubprocess.MyOperation()
    cmd = 'echo fred >/dev/stderr && false || echo bad'
    plist = Popen([cmd], shell=True).CommunicateFilter(oper)
    self._BasicCheck(plist, oper)
    self.assertEqual(plist [0], 'bad\r\n')
    self.assertEqual(plist [1], 'fred\r\n')

  def test_shell(self):
    """Check with and without shell works"""
    oper = TestSubprocess.MyOperation()
    cmd = 'echo test >/dev/stderr'
    self.assertRaises(OSError, Popen, [cmd], shell=False)
    plist = Popen([cmd], shell=True).CommunicateFilter(oper)
    self._BasicCheck(plist, oper)
    self.assertEqual(len(plist [0]), 0)
    self.assertEqual(plist [1], 'test\r\n')

  def test_list_args(self):
    """Check with and without shell works using list arguments"""
    oper = TestSubprocess.MyOperation()
    cmd = ['echo', 'test', '>/dev/stderr']
    plist = Popen(cmd, shell=False).CommunicateFilter(oper)
    self._BasicCheck(plist, oper)
    self.assertEqual(plist [0], ' '.join(cmd[1:]) + '\r\n')
    self.assertEqual(len(plist [1]), 0)

    oper = TestSubprocess.MyOperation()

    # this should be interpreted as 'echo' with the other args dropped
    cmd = ['echo', 'test', '>/dev/stderr']
    plist = Popen(cmd, shell=True).CommunicateFilter(oper)
    self._BasicCheck(plist, oper)
    self.assertEqual(plist [0], '\r\n')

  def test_cwd(self):
    """Check we can change directory"""
    for shell in (False, True):
      oper = TestSubprocess.MyOperation()
      plist = Popen('pwd', shell=shell, cwd='/tmp').CommunicateFilter(oper)
      self._BasicCheck(plist, oper)
      self.assertEqual(plist [0], '/tmp\r\n')

  def test_env(self):
    """Check we can change environment"""
    for add in (False, True):
      oper = TestSubprocess.MyOperation()
      env = os.environ
      if add:
        env ['FRED'] = 'fred'
      cmd = 'echo $FRED'
      plist = Popen(cmd, shell=True, env=env).CommunicateFilter(oper)
      self._BasicCheck(plist, oper)
      self.assertEqual(plist [0], add and 'fred\r\n' or '\r\n')

  def test_extra_args(self):
    """Check we can't add extra arguments"""
    self.assertRaises(ValueError, Popen, 'true', close_fds=False)

  def test_basic_input(self):
    """Check that incremental input works

    We set up a subprocess which will prompt for name. When we see this prompt
    we send the name as input to the process. It should then print the name
    properly to stdout.
    """
    oper = TestSubprocess.MyOperation('Flash')
    prompt = 'What is your name?: '
    cmd = 'echo -n "%s"; read name; echo Hello $name' % prompt
    plist = Popen([cmd], stdin=oper.stdin_read_pipe,
        shell=True).CommunicateFilter(oper)
    self._BasicCheck(plist, oper)
    self.assertEqual(len(plist [1]), 0)
    self.assertEqual(plist [0], prompt + 'Hello Flash\r\r\n')

  #TODO(sjg): Add test for passing PIPE in case underlying subprocess breaks.
  #TODO(sjg): Add test for passing a file handle also.

  def test_isatty(self):
    """Check that ptys appear as terminals to the subprocess"""
    oper = TestSubprocess.MyOperation()
    cmd = ('if [ -t %d ]; then echo "terminal %d" >&%d; '
        'else echo "not %d" >&%d; fi;')
    both_cmds = ''
    for fd in (1, 2):
      both_cmds += cmd % (fd, fd, fd, fd, fd)
    plist = Popen(both_cmds, shell=True).CommunicateFilter(oper)
    self._BasicCheck(plist, oper)
    self.assertEqual(plist [0], 'terminal 1\r\n')
    self.assertEqual(plist [1], 'terminal 2\r\n')

    # Now try with PIPE and make sure it is not a terminal
    oper = TestSubprocess.MyOperation()
    plist = Popen(both_cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        shell=True).CommunicateFilter(oper)
    self._BasicCheck(plist, oper)
    self.assertEqual(plist [0], 'not 1\n')
    self.assertEqual(plist [1], 'not 2\n')

if __name__ == '__main__':
  unittest.main()
