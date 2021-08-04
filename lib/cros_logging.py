# Copyright 2015 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Logging module to be used by all scripts.

cros_logging is a wrapper around logging with additional support for NOTICE
level. This is to be used instead of the default logging module. The new
logging level can only be used from here.

The log levels should be used as follows:

DEBUG: Enabled on the CLI with --debug. This is the noisiest logging level.
Often, as the name suggests, it may contain debugging information you wouldn't
otherwise need.

INFO: Enabled on the CLI with --verbose. Logging at this level should contain
relatively fine-grained info about the steps the process is performing, but
should be light on details (which should be in debug).

NOTICE: The default log level. It should relay a high level overview of what
the process is doing. It should NOT be a noisy output.

WARNING: Unexpected scenarios that are well handled and do not interrupt the
process, things like retrying an operation or missing optional information
needed to complete a portion of a process.

ERROR: Problems that are fatal to a specific operation or script, e.g.
unable to read a file or invalid arguments.

CRITICAL/FATAL: Rarely needed. These should reflect an extraordinary error that
might require the shutdown of an application or lead to data loss.

WARNING, ERROR, CRITICAL/FATAL: These levels are always included in the above
levels as one would expect. Limiting the output of a script to just these log
levels is rarely desirable, but the --log-level argument can be used to do so.
"""

import os
# pylint: disable=unused-wildcard-import, wildcard-import
from logging import *
# pylint: enable=unused-wildcard-import, wildcard-import

# Have to import shutdown explicitly from logging because it is not included
# in logging's __all__.
# pylint: disable=unused-import
from logging import shutdown
# pylint: enable=unused-import

# Remove deprecated APIs to force use of new ones.
del WARN
del warn


# Notice Level.
NOTICE = 25
addLevelName(NOTICE, 'NOTICE')


def _SetupCloudLogging():
  """If appropriate environment variables are set, enable cloud logging.

  Cloud logging is only enabled when the environment has
   CHROMITE_CLOUD_LOGGING=1 and GOOGLE_APPLICATION_CREDENTIALS=<local.json>.
  If these are set, then cloud logging is enable, see
  https://cloud.google.com/docs/authentication/getting-started#cloud-console
  """
  try:
    import google.cloud.logging as cloud_logging  # pylint: disable=import-error,no-name-in-module
  except ImportError as e:
    # TODO(mmortensen): Change to python3's ModuleNotFoundError when this
    # code is only used by python3. Beware though with branches and bisection
    # this could need to be ImportError for a long time. ImportError is the
    # parent class of ModuleNotFoundError and works on both python2 and python3.
    log(ERROR, 'Could not import google.cloud.logging %s', e)
    return

  client = cloud_logging.Client()
  # Retrieves a Cloud Logging handler based on the environment
  # you're running in and integrates the handler with the
  # Python logging module. By default this captures all logs
  # at INFO level and higher
  client.get_default_handler()
  client.setup_logging()


def _CloudLoggingEnvVariablesAreDefined():
  """Check for cloud-logging ENV variables."""
  cloud_logging_env_value = os.environ.get('CHROMITE_CLOUD_LOGGING')
  google_app_creds_env_value = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
  # If both variables are set, log their values and return True.
  if cloud_logging_env_value == '1' and google_app_creds_env_value:
    log(INFO, 'CHROMITE_CLOUD_LOGGING is %s', cloud_logging_env_value)
    return True
  if cloud_logging_env_value == '1' and not google_app_creds_env_value:
    log(WARNING,
        'CHROMITE_CLOUD_LOGGING is set, GOOGLE_APPLICATION_CREDENTIALS is not.')
  return False


if _CloudLoggingEnvVariablesAreDefined():
  _SetupCloudLogging()


# Notice implementation.
def notice(message, *args, **kwargs):
  """Log 'msg % args' with severity 'NOTICE'."""
  log(NOTICE, message, *args, **kwargs)
