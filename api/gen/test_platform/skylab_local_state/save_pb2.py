# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/skylab_local_state/save.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import message as _message
from chromite.third_party.google.protobuf import reflection as _reflection
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.test_platform.skylab_local_state import common_pb2 as test__platform_dot_skylab__local__state_dot_common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='test_platform/skylab_local_state/save.proto',
  package='test_platform.skylab_local_state',
  syntax='proto3',
  serialized_options=b'ZJgo.chromium.org/chromiumos/infra/proto/go/test_platform/skylab_local_state',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n+test_platform/skylab_local_state/save.proto\x12 test_platform.skylab_local_state\x1a-test_platform/skylab_local_state/common.proto\"\xbe\x01\n\x0bSaveRequest\x12\x38\n\x06\x63onfig\x18\x01 \x01(\x0b\x32(.test_platform.skylab_local_state.Config\x12\x13\n\x0bresults_dir\x18\x02 \x01(\t\x12\x10\n\x08\x64ut_name\x18\x03 \x01(\t\x12\x0e\n\x06\x64ut_id\x18\x04 \x01(\t\x12\x11\n\tdut_state\x18\x05 \x01(\t\x12\x18\n\x10seal_results_dir\x18\x06 \x01(\x08\x12\x11\n\tpeer_duts\x18\x07 \x03(\tBLZJgo.chromium.org/chromiumos/infra/proto/go/test_platform/skylab_local_stateb\x06proto3'
  ,
  dependencies=[test__platform_dot_skylab__local__state_dot_common__pb2.DESCRIPTOR,])




_SAVEREQUEST = _descriptor.Descriptor(
  name='SaveRequest',
  full_name='test_platform.skylab_local_state.SaveRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='config', full_name='test_platform.skylab_local_state.SaveRequest.config', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='results_dir', full_name='test_platform.skylab_local_state.SaveRequest.results_dir', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dut_name', full_name='test_platform.skylab_local_state.SaveRequest.dut_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dut_id', full_name='test_platform.skylab_local_state.SaveRequest.dut_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dut_state', full_name='test_platform.skylab_local_state.SaveRequest.dut_state', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='seal_results_dir', full_name='test_platform.skylab_local_state.SaveRequest.seal_results_dir', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='peer_duts', full_name='test_platform.skylab_local_state.SaveRequest.peer_duts', index=6,
      number=7, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=129,
  serialized_end=319,
)

_SAVEREQUEST.fields_by_name['config'].message_type = test__platform_dot_skylab__local__state_dot_common__pb2._CONFIG
DESCRIPTOR.message_types_by_name['SaveRequest'] = _SAVEREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SaveRequest = _reflection.GeneratedProtocolMessageType('SaveRequest', (_message.Message,), {
  'DESCRIPTOR' : _SAVEREQUEST,
  '__module__' : 'test_platform.skylab_local_state.save_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.skylab_local_state.SaveRequest)
  })
_sym_db.RegisterMessage(SaveRequest)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
