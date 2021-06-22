# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/v2/request.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import message as _message
from chromite.third_party.google.protobuf import reflection as _reflection
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.chromiumos.test.api import coverage_rule_pb2 as chromiumos_dot_test_dot_api_dot_coverage__rule__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='test_platform/v2/request.proto',
  package='test_platform.v2',
  syntax='proto3',
  serialized_options=b'Z:go.chromium.org/chromiumos/infra/proto/go/test_platform_v2',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1etest_platform/v2/request.proto\x12\x10test_platform.v2\x1a\'chromiumos/test/api/coverage_rule.proto\"\xb4\x01\n\x07Request\x12\x39\n\x0e\x63overage_rules\x18\x01 \x03(\x0b\x32!.chromiumos.test.api.CoverageRule\x12\x35\n\tartifacts\x18\x02 \x03(\x0b\x32\".test_platform.v2.Request.Artifact\x1a\x37\n\x08\x41rtifact\x12\x11\n\tbuild_url\x18\x01 \x01(\t\x12\x18\n\x10\x63hromeos_version\x18\x02 \x01(\tB<Z:go.chromium.org/chromiumos/infra/proto/go/test_platform_v2b\x06proto3'
  ,
  dependencies=[chromiumos_dot_test_dot_api_dot_coverage__rule__pb2.DESCRIPTOR,])




_REQUEST_ARTIFACT = _descriptor.Descriptor(
  name='Artifact',
  full_name='test_platform.v2.Request.Artifact',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='build_url', full_name='test_platform.v2.Request.Artifact.build_url', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='chromeos_version', full_name='test_platform.v2.Request.Artifact.chromeos_version', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=219,
  serialized_end=274,
)

_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='test_platform.v2.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='coverage_rules', full_name='test_platform.v2.Request.coverage_rules', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='artifacts', full_name='test_platform.v2.Request.artifacts', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_REQUEST_ARTIFACT, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=94,
  serialized_end=274,
)

_REQUEST_ARTIFACT.containing_type = _REQUEST
_REQUEST.fields_by_name['coverage_rules'].message_type = chromiumos_dot_test_dot_api_dot_coverage__rule__pb2._COVERAGERULE
_REQUEST.fields_by_name['artifacts'].message_type = _REQUEST_ARTIFACT
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), {

  'Artifact' : _reflection.GeneratedProtocolMessageType('Artifact', (_message.Message,), {
    'DESCRIPTOR' : _REQUEST_ARTIFACT,
    '__module__' : 'test_platform.v2.request_pb2'
    # @@protoc_insertion_point(class_scope:test_platform.v2.Request.Artifact)
    })
  ,
  'DESCRIPTOR' : _REQUEST,
  '__module__' : 'test_platform.v2.request_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.v2.Request)
  })
_sym_db.RegisterMessage(Request)
_sym_db.RegisterMessage(Request.Artifact)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
