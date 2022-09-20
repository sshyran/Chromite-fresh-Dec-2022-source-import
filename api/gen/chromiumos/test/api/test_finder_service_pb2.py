# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/test/api/test_finder_service.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import message as _message
from chromite.third_party.google.protobuf import reflection as _reflection
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.chromiumos.test.api import cros_test_finder_cli_pb2 as chromiumos_dot_test_dot_api_dot_cros__test__finder__cli__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromiumos/test/api/test_finder_service.proto',
  package='chromiumos.test.api',
  syntax='proto3',
  serialized_options=b'Z-go.chromium.org/chromiumos/config/go/test/api',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n-chromiumos/test/api/test_finder_service.proto\x12\x13\x63hromiumos.test.api\x1a.chromiumos/test/api/cros_test_finder_cli.proto2y\n\x11TestFinderService\x12\x64\n\tFindTests\x12*.chromiumos.test.api.CrosTestFinderRequest\x1a+.chromiumos.test.api.CrosTestFinderResponseB/Z-go.chromium.org/chromiumos/config/go/test/apib\x06proto3'
  ,
  dependencies=[chromiumos_dot_test_dot_api_dot_cros__test__finder__cli__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None

_TESTFINDERSERVICE = _descriptor.ServiceDescriptor(
  name='TestFinderService',
  full_name='chromiumos.test.api.TestFinderService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=118,
  serialized_end=239,
  methods=[
  _descriptor.MethodDescriptor(
    name='FindTests',
    full_name='chromiumos.test.api.TestFinderService.FindTests',
    index=0,
    containing_service=None,
    input_type=chromiumos_dot_test_dot_api_dot_cros__test__finder__cli__pb2._CROSTESTFINDERREQUEST,
    output_type=chromiumos_dot_test_dot_api_dot_cros__test__finder__cli__pb2._CROSTESTFINDERRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_TESTFINDERSERVICE)

DESCRIPTOR.services_by_name['TestFinderService'] = _TESTFINDERSERVICE

# @@protoc_insertion_point(module_scope)
