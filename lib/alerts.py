# Copyright (c) 2012 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Chromite email utility functions."""

from __future__ import print_function

import base64
import cStringIO
import gzip
import os
import smtplib
import socket
import sys
import traceback

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from chromite.lib import cros_logging as logging
from chromite.lib import retry_util

try:
  import httplib2
  from apiclient.discovery import build as apiclient_build
  from apiclient import errors as apiclient_errors
  from oauth2client import file as oauth_client_fileio
except ImportError as e:
  apiclient_build = None
  oauth_client_fileio = None


class MailServer(object):
  """Base class for servers."""

  def Send(self, message):
    """Send the message.

    Override by sub-classes.

    Args:
      message: A MIMEMultipart() object containing the body of the message.

    Returns:
      True if the email was sent, else False.
    """
    raise NotImplementedError('Should be implemented by sub-classes.')


class GmailServer(MailServer):
  """Gmail server."""

  DEFAULT_CREDENTIALS = os.path.expanduser('~/.gmail_credentials')

  def __init__(self, credentials=None):
    """Initialize GmailServer.

    Args:
      credentials: Absolute path to gmail credential file.
    """
    self._creds_file = credentials or self.DEFAULT_CREDENTIALS

  def Send(self, message):
    """Send an e-mail via Gmail API.

    Args:
      message: A MIMEMultipart() object containing the body of the message.

    Returns:
      True if the email was sent, else False.
    """
    if not apiclient_build:
      logging.warning('Could not send email: Google API client not installed.')
      return False

    if not os.path.isfile(self._creds_file):
      logging.warning('Could not send email: %s not exist.', self._creds_file)
      return False

    storage = oauth_client_fileio.Storage(self._creds_file)
    credentials = storage.get()
    if not credentials or credentials.invalid:
      logging.warning('Could not send email: Invalid credentials.')
      return False

    http = credentials.authorize(httplib2.Http())
    service = apiclient_build('gmail', 'v1', http=http)
    try:
      # 'me' represents the default authorized user.
      payload = {'raw': base64.urlsafe_b64encode(message.as_string())}
      service.users().messages().send(userId='me', body=payload).execute()
      return True
    except apiclient_errors.HttpError as error:
      logging.warning('Could not send email: %s', error)
      return False


class SmtpServer(MailServer):
  """Smtp server."""

  # Note: When importing this module from cbuildbot code that will run on
  # a builder in the golo, set this to constants.GOLO_SMTP_SERVER
  DEFAULT_SERVER = 'localhost'
  # Retry parameters for the actual smtp connection.
  SMTP_RETRY_COUNT = 3
  SMTP_RETRY_DELAY = 30

  def __init__(self, smtp_server=None):
    """Initialize SmtpServer.

    Args:
      smtp_server: The server with which to send the message.
    """
    self._smtp_server = smtp_server or self.DEFAULT_SERVER

  def Send(self, message):
    """Send an email via SMTP

    If we get a socket error (e.g. the SMTP server is not listening or
    timesout), we will retry a few times.  All socket errors will be
    caught here.

    Args:
      message: A MIMEMultipart() object containing the body of the message.

    Returns:
      True if the email was sent, else False.
    """
    def _Send():
      smtp_client = smtplib.SMTP(self._smtp_server)
      recipients = [s.strip() for s in message['To'].split(',')]
      smtp_client.sendmail(message['From'], recipients, message.as_string())
      smtp_client.quit()

    try:
      retry_util.RetryException(socket.error, self.SMTP_RETRY_COUNT, _Send,
                                sleep=self.SMTP_RETRY_DELAY)
      return True
    except socket.error as e:
      logging.warning('Could not send e-mail from %s to %s via %r: %s',
                      message['From'], message['To'], self._smtp_server, e)
      return False


def CreateEmail(subject, recipients, message='', attachment=None,
                extra_fields=None):
  """Create an email message object.

  Args:
    subject: E-mail subject.
    recipients: List of e-mail recipients.
    message: (optional) Message to put in the e-mail body.
    attachment: (optional) text to attach.
    extra_fields: (optional) A dictionary of additional message header fields
                  to be added to the message. Custom field names should begin
                  with the prefix 'X-'.

  Returns:
    A MIMEMultipart object, or None if recipients is empty.
  """
  # Ignore if the list of recipients is empty.
  if not recipients:
    logging.warning('Could not create email: recipient list is emtpy.')
    return None

  extra_fields = extra_fields or {}
  sender = socket.getfqdn()
  msg = MIMEMultipart()
  for key, val in extra_fields.iteritems():
    msg[key] = val
  msg['From'] = sender
  msg['Subject'] = subject
  msg['To'] = ', '.join(recipients)

  msg.attach(MIMEText(message))
  if attachment:
    s = cStringIO.StringIO()
    with gzip.GzipFile(fileobj=s, mode='w') as f:
      f.write(attachment)
    part = MIMEApplication(s.getvalue(), _subtype='x-gzip')
    s.close()
    part.add_header('Content-Disposition', 'attachment', filename='logs.txt.gz')
    msg.attach(part)

  return msg


def SendEmail(subject, recipients, server=SmtpServer(), message='',
              attachment=None, extra_fields=None):
  """Send an e-mail job notification with the given message in the body.

  Args:
    subject: E-mail subject.
    recipients: List of e-mail recipients.
    server: A MailServer instance. Default to local SmtpServer.
    message: Message to put in the e-mail body.
    attachment: Text to attach.
    extra_fields: A dictionary of additional message header fields
                  to be added to the message. Custom field names should begin
                  with the prefix 'X-'.
  """
  msg = CreateEmail(subject, recipients, message, attachment, extra_fields)
  if not msg:
    return
  server.Send(msg)


def SendEmailLog(subject, recipients, server=SmtpServer(), message='',
                 inc_trace=True, log=None, extra_fields=None):
  """Send an e-mail with a stack trace and log snippets.

  Args:
    subject: E-mail subject.
    recipients: list of e-mail recipients.
    server: A MailServer instance. Default to local SmtpServer.
    inc_trace: Append a backtrace of the current stack.
    message: Message to put at the top of the e-mail body.
    log: List of lines (log data) to include in the notice.
    extra_fields: (optional) A dictionary of additional message header fields
                  to be added to the message. Custom fields names should begin
                  with the prefix 'X-'.
  """
  if not message:
    message = subject
  message = message[:]

  if inc_trace:
    if sys.exc_info() != (None, None, None):
      trace = traceback.format_exc()
      message += '\n\n' + trace

  attachment = None
  if log:
    message += ('\n\n' +
                '***************************\n' +
                'Last log messages:\n' +
                '***************************\n' +
                ''.join(log[-50:]))
    attachment = ''.join(log)

  SendEmail(subject, recipients, server, message=message,
            attachment=attachment, extra_fields=extra_fields)
