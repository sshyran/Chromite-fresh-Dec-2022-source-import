# -*- coding: utf-8 -*-
# Copyright 2015 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Helper script to deploy the cq_stats app to our appengine instances."""

from __future__ import print_function

import os
import time

from chromite.lib import commandline
from chromite.lib import cros_build_lib
from chromite.lib import cros_logging as logging
from chromite.lib import osutils


APP_INSTANCE_DEBUG = 'debug'
APP_INSTANCE_PROD = 'prod'

APP_INSTANCE_NAME = {
    APP_INSTANCE_DEBUG: 'google.com:chromiumos-build-annotator-dbg',
    APP_INSTANCE_PROD: 'google.com:chromiumos-build-annotator',
}
APP_INSTANCE_CIDB = {
    APP_INSTANCE_DEBUG: 'debug-cidb',
    APP_INSTANCE_PROD: 'cidb',
}


def _GetParser():
  """Get parser for deploy_app cli.

  Returns:
    commandline.ArgumentParser object to parse the commandline args.
  """
  parser = commandline.ArgumentParser()
  parser.add_argument('instance', type=str,
                      choices=(APP_INSTANCE_DEBUG, APP_INSTANCE_PROD),
                      help='The app instance to deploy to')
  parser.add_argument('--secret-key', type=str, required=True,
                      help='The secret key to sign django cookies.')
  return parser


def _GetDeploySettings(options):
  """The autogenerated part of django settings.

  Returns:
    python "code" as str to be written to the settings file.
  """
  content = [
      '# DO NOT EDIT! Autogenerated by %s.' % os.path.basename(__file__),
      'DEBUG = False',
      'TEMPLATE_DEBUG = False',
      'SECRET_KEY = "%s"' % options.secret_key,
      'CIDB_PROJECT_NAME = "cosmic-strategy-646"',
      'CIDB_INSTANCE_NAME = "%s"' % APP_INSTANCE_CIDB[options.instance],
  ]
  return '\n'.join(content)


def _DeployApp(basedir, options):
  """Deploy the prepared app from basedir.

  Args:
    basedir: The base directory where the app has already been prepped.
    options: The command-line options passed in.
  """
  cros_build_lib.RunCommand(
      ['./ae_shell', 'cq_stats', '--',
       'python', 'cq_stats/manage.py', 'collectstatic', '--noinput'],
      cwd=basedir)

  # Remove sensitive files that are needed to run tools locally to prepare the
  # deploy directory, but that we don't want to push to AE.
  cidb_cred_file = 'annotator_cidb_creds'
  if options.instance == APP_INSTANCE_DEBUG:
    cidb_cred_file += '.debug'
  cidb_cred_path = os.path.join(basedir, 'cq_stats', cidb_cred_file)
  osutils.SafeUnlink(os.path.join(cidb_cred_path, 'client-cert.pem'))
  osutils.SafeUnlink(os.path.join(cidb_cred_path, 'client-key.pem'))
  osutils.SafeUnlink(os.path.join(cidb_cred_path, 'server-ca.pem'))
  cros_build_lib.RunCommand(
      ['./ae_shell', 'cq_stats', '--',
       'appcfg.py', '--oauth2', '--noauth_local_webserver', 'update',
       'cq_stats'],
      cwd=basedir)


def _Hang(tempdir):
  """How else will you ever work on this script?

  Args:
    tempdir: The directory prepared for deploying the app.
  """
  logging.info('All the real stuff\'s done. Tempdir: %s', tempdir)
  while True:
    logging.info('Sleeping... Hit Ctrl-C to exit.')
    time.sleep(30)


def main(argv):
  parser = _GetParser()
  options = parser.parse_args(argv)
  options.Freeze()

  with osutils.TempDir() as tempdir:
    # This is rsync in 'archive' mode, but symlinks are followed to copy actual
    # files/directories.
    rsync_cmd = ['rsync', '-qrLgotD', '--exclude=\'*/*.pyc\'']
    chromite_dir = os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__))))

    cmd = rsync_cmd + [
        'chromite/appengine/', tempdir,
        '--exclude=google_appengine_*',
    ]
    cros_build_lib.RunCommand(cmd, cwd=os.path.dirname(chromite_dir))

    cmd = rsync_cmd + [
        'chromite', os.path.join(tempdir, 'cq_stats'),
        '--exclude=appengine',
        '--exclude=third_party',
        '--exclude=ssh_keys',
        '--exclude=contrib',
        '--exclude=.git',
        '--exclude=venv',
    ]
    cros_build_lib.RunCommand(cmd, cwd=os.path.dirname(chromite_dir))

    osutils.WriteFile(os.path.join(tempdir, 'cq_stats', 'cq_stats',
                                   'deploy_settings.py'),
                      _GetDeploySettings(options))

    # update the instance we're updating.
    # Use absolute path. Let's not update sourcedir by mistake.
    app_yaml_path = os.path.join(tempdir, 'cq_stats', 'app.yaml')
    regex = (r's/^application:[ \t]*[a-zA-Z0-9_-\.:]\+[ \t]*$'
             '/application: %s/')
    cmd = [
        'sed', '-i',
        '-e', regex % APP_INSTANCE_NAME[options.instance],
        app_yaml_path,
    ]
    cros_build_lib.RunCommand(cmd, cwd=tempdir)

    _DeployApp(tempdir, options)
    # _Hang(tempdir)
