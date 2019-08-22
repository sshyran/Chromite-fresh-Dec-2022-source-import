# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/steps/enumeration.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.chromite.api import test_metadata_pb2 as chromite_dot_api_dot_test__metadata__pb2
from chromite.api.gen.test_platform import request_pb2 as test__platform_dot_request__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='test_platform/steps/enumeration.proto',
  package='test_platform.steps',
  syntax='proto3',
  serialized_options=_b('Z=go.chromium.org/chromiumos/infra/proto/go/test_platform/steps'),
  serialized_pb=_b('\n%test_platform/steps/enumeration.proto\x12\x13test_platform.steps\x1a chromite/api/test_metadata.proto\x1a\x1btest_platform/request.proto\"\x82\x01\n\x12\x45numerationRequest\x12\x38\n\x08metadata\x18\x01 \x01(\x0b\x32&.test_platform.Request.Params.Metadata\x12\x32\n\ttest_plan\x18\x04 \x01(\x0b\x32\x1f.test_platform.Request.TestPlan\"\xd9\x01\n\x13\x45numerationResponse\x12Y\n\x14\x61utotest_invocations\x18\x02 \x03(\x0b\x32;.test_platform.steps.EnumerationResponse.AutotestInvocation\x1ag\n\x12\x41utotestInvocation\x12(\n\x04test\x18\x01 \x01(\x0b\x32\x1a.chromite.api.AutotestTest\x12\x11\n\ttest_args\x18\x02 \x01(\t\x12\x14\n\x0c\x64isplay_name\x18\x03 \x01(\tB?Z=go.chromium.org/chromiumos/infra/proto/go/test_platform/stepsb\x06proto3')
  ,
  dependencies=[chromite_dot_api_dot_test__metadata__pb2.DESCRIPTOR,test__platform_dot_request__pb2.DESCRIPTOR,])




_ENUMERATIONREQUEST = _descriptor.Descriptor(
  name='EnumerationRequest',
  full_name='test_platform.steps.EnumerationRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='metadata', full_name='test_platform.steps.EnumerationRequest.metadata', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='test_plan', full_name='test_platform.steps.EnumerationRequest.test_plan', index=1,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=126,
  serialized_end=256,
)


_ENUMERATIONRESPONSE_AUTOTESTINVOCATION = _descriptor.Descriptor(
  name='AutotestInvocation',
  full_name='test_platform.steps.EnumerationResponse.AutotestInvocation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='test', full_name='test_platform.steps.EnumerationResponse.AutotestInvocation.test', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='test_args', full_name='test_platform.steps.EnumerationResponse.AutotestInvocation.test_args', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='display_name', full_name='test_platform.steps.EnumerationResponse.AutotestInvocation.display_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=373,
  serialized_end=476,
)

_ENUMERATIONRESPONSE = _descriptor.Descriptor(
  name='EnumerationResponse',
  full_name='test_platform.steps.EnumerationResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='autotest_invocations', full_name='test_platform.steps.EnumerationResponse.autotest_invocations', index=0,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_ENUMERATIONRESPONSE_AUTOTESTINVOCATION, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=259,
  serialized_end=476,
)

_ENUMERATIONREQUEST.fields_by_name['metadata'].message_type = test__platform_dot_request__pb2._REQUEST_PARAMS_METADATA
_ENUMERATIONREQUEST.fields_by_name['test_plan'].message_type = test__platform_dot_request__pb2._REQUEST_TESTPLAN
_ENUMERATIONRESPONSE_AUTOTESTINVOCATION.fields_by_name['test'].message_type = chromite_dot_api_dot_test__metadata__pb2._AUTOTESTTEST
_ENUMERATIONRESPONSE_AUTOTESTINVOCATION.containing_type = _ENUMERATIONRESPONSE
_ENUMERATIONRESPONSE.fields_by_name['autotest_invocations'].message_type = _ENUMERATIONRESPONSE_AUTOTESTINVOCATION
DESCRIPTOR.message_types_by_name['EnumerationRequest'] = _ENUMERATIONREQUEST
DESCRIPTOR.message_types_by_name['EnumerationResponse'] = _ENUMERATIONRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

EnumerationRequest = _reflection.GeneratedProtocolMessageType('EnumerationRequest', (_message.Message,), dict(
  DESCRIPTOR = _ENUMERATIONREQUEST,
  __module__ = 'test_platform.steps.enumeration_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.steps.EnumerationRequest)
  ))
_sym_db.RegisterMessage(EnumerationRequest)

EnumerationResponse = _reflection.GeneratedProtocolMessageType('EnumerationResponse', (_message.Message,), dict(

  AutotestInvocation = _reflection.GeneratedProtocolMessageType('AutotestInvocation', (_message.Message,), dict(
    DESCRIPTOR = _ENUMERATIONRESPONSE_AUTOTESTINVOCATION,
    __module__ = 'test_platform.steps.enumeration_pb2'
    # @@protoc_insertion_point(class_scope:test_platform.steps.EnumerationResponse.AutotestInvocation)
    ))
  ,
  DESCRIPTOR = _ENUMERATIONRESPONSE,
  __module__ = 'test_platform.steps.enumeration_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.steps.EnumerationResponse)
  ))
_sym_db.RegisterMessage(EnumerationResponse)
_sym_db.RegisterMessage(EnumerationResponse.AutotestInvocation)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
