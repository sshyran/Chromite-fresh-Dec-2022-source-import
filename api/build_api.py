# -*- coding: utf-8 -*-
# Copyright 2018 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""The build API entry point."""

from __future__ import print_function

import importlib

from google.protobuf import json_format
from google.protobuf import symbol_database

from chromite.api import service
from chromite.api.gen import build_api_pb2
from chromite.api.gen import autotest_pb2
from chromite.api.gen import image_pb2
from chromite.lib import commandline
from chromite.lib import cros_build_lib
from chromite.lib import osutils


class Error(Exception):
  """Base error class for the module."""


class InvalidInputFormatError(Error):
  """Raised when the passed input protobuf can't be parsed."""


# API Service Errors.
class UnknownServiceError(Error):
  """Error raised when the requested service has not been registered."""


class ServiceModuleNotDefinedError(Error):
  """Error class for when no module is defined for a service."""


class ServiceModuleNotFoundError(Error):
  """Error raised when the service cannot be imported."""


# API Method Errors.
class UnknownMethodError(Error):
  """The requested service exists but does not have the requested method."""


class MethodNotFoundError(Error):
  """Error raised when the method cannot be found in the service module."""


def GetParser():
  """Build the argument parser.

  The API parser comprises a subparser hierarchy. The general form is:
  `script service method`, e.g. `build_api image test`.
  """
  parser = commandline.ArgumentParser(description=__doc__)

  parser.add_argument('service_method',
                      help='The "chromite.api.Service/Method" that is being '
                           'called.')

  parser.add_argument(
      '--input-json', type='path', required=True,
      help='Path to the JSON serialized input argument protobuf message.')
  parser.add_argument(
      '--output-json', type='path', required=True,
      help='The path to which the result protobuf message should be written.')

  return parser


def _ParseArgs(argv):
  """Parse and validate arguments."""
  parser = GetParser()
  opts = parser.parse_args(argv)

  parts = opts.service_method.split('/')

  if len(parts) != 2:
    parser.error('Must pass "Service/Method".')

  opts.service = parts[0]
  opts.method = parts[1]

  opts.Freeze()
  return opts


class Router(object):
  """Encapsulates the request dispatching logic."""

  def __init__(self):
    self._services = {}
    self._aliases = {}
    # All imported generated messages get added to this symbol db.
    self._sym_db = symbol_database.Default()

    extensions = build_api_pb2.DESCRIPTOR.extensions_by_name
    self._service_options = extensions['service_options']
    self._method_options = extensions['method_options']

  def Register(self, proto_module):
    """Register the services from a generated proto module.

    Args:
      proto_module (module): The generated proto module whose service is being
        registered.

    Raises:
      ServiceModuleNotDefinedError when the service cannot be found in the
        provided module.
    """
    services = proto_module.DESCRIPTOR.services_by_name
    for service_name, svc in services.items():
      module_name = svc.GetOptions().Extensions[self._service_options].module

      if not module_name:
        raise ServiceModuleNotDefinedError(
            'The module must be defined in the service definition: %s.%s' %
            (proto_module, service_name))

      self._services[svc.full_name] = (svc, module_name)

  def Route(self, service_name, method_name, input_json):
    """Dispatch the request.

    Args:
      service_name (str): The fully qualified service name.
      method_name (str): The name of the method being called.
      input_json (str): The JSON encoded input message data.

    Returns:
      google.protobuf.message.Message: An instance of the method's output
        message class.

    Raises:
      ServiceModuleNotFoundError when the service module cannot be imported.
      MethodNotFoundError when the method cannot be retrieved from the module.
    """
    try:
      svc, module_name = self._services[service_name]
    except KeyError:
      raise UnknownServiceError('The %s service has not been registered.'
                                % service_name)

    try:
      method_desc = svc.methods_by_name[method_name]
    except KeyError:
      raise UnknownMethodError('The %s method has not been defined in the %s '
                               'service.' % (method_name, service_name))

    # Parse the input file to build an instance of the input message.
    input_msg = self._sym_db.GetPrototype(method_desc.input_type)()
    try:
      json_format.Parse(input_json, input_msg, ignore_unknown_fields=True)
    except json_format.ParseError as e:
      raise InvalidInputFormatError(
          'Unable to parse the input json: %s' % e.message)

    # Get an empty output message instance.
    output_msg = self._sym_db.GetPrototype(method_desc.output_type)()

    # Allow proto-based method name override.
    method_options = method_desc.GetOptions().Extensions[self._method_options]
    if method_options.HasField('implementation_name'):
      method_name = method_options.implementation_name

    # Check the chroot assertion settings before running.
    service_options = svc.GetOptions().Extensions[self._service_options]
    self._HandleChrootAssert(service_options, method_options)

    # Import the module and get the method.
    method_impl = self._GetMethod(module_name, method_name)

    # Successfully located; call and return.
    method_impl(input_msg, output_msg)
    return output_msg

  def _HandleChrootAssert(self, service_options, method_options):
    """Check the chroot assert options and execute assertion as needed.

    Args:
      service_options (google.protobuf.Message): The service options.
      method_options (google.protobuf.Message): The method options.
    """
    chroot_assert = build_api_pb2.NO_ASSERTION
    if method_options.HasField('method_chroot_assert'):
      # Prefer the method option when set.
      chroot_assert = method_options.method_chroot_assert
    elif service_options.HasField('service_chroot_assert'):
      # Fall back to the service option.
      chroot_assert = service_options.service_chroot_assert

    # Execute appropriate assertion if set.
    if chroot_assert == build_api_pb2.INSIDE:
      cros_build_lib.AssertInsideChroot()
    elif chroot_assert == build_api_pb2.OUTSIDE:
      cros_build_lib.AssertOutsideChroot()

  def _GetMethod(self, module_name, method_name):
    """Get the implementation of the method for the service module.

    Args:
      module_name (str): The name of the service module.
      method_name (str): The name of the method.

    Returns:
      callable - The method.

    Raises:
      MethodNotFoundError when the method cannot be found in the module.
      ServiceModuleNotFoundError when the service module cannot be imported.
    """
    try:
      module = importlib.import_module(service.IMPORT_PATTERN % module_name)
    except ImportError as e:
      raise ServiceModuleNotFoundError(e.message)
    try:
      return getattr(module, method_name)
    except AttributeError as e:
      raise MethodNotFoundError(e.message)


def RegisterServices(router):
  """Register all the services.

  Args:
    router (Router): The router.
  """
  router.Register(autotest_pb2)
  router.Register(image_pb2)


def main(argv):
  opts = _ParseArgs(argv)

  router = Router()
  RegisterServices(router)

  try:
    input_proto = osutils.ReadFile(opts.input_json)
  except IOError as e:
    cros_build_lib.Die('Unable to read input file: %s' % e.message)

  try:
    output_msg = router.Route(opts.service, opts.method, input_proto)
  except Error as e:
    # Error derivatives are handled nicely, but let anything else bubble up.
    cros_build_lib.Die(e.message)

  output_content = json_format.MessageToJson(output_msg)
  try:
    osutils.WriteFile(opts.output_json, output_content)
  except IOError as e:
    cros_build_lib.Die('Unable to write output file: %s' % e.message)
