# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/test/dut/device_stability.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen_sdk.chromiumos.test.api import dut_attribute_pb2 as chromiumos_dot_test_dot_api_dot_dut__attribute__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromiumos/test/dut/device_stability.proto',
  package='chromiumos.test.dut',
  syntax='proto3',
  serialized_options=b'Z-go.chromium.org/chromiumos/config/go/test/dut',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n*chromiumos/test/dut/device_stability.proto\x12\x13\x63hromiumos.test.dut\x1a\'chromiumos/test/api/dut_attribute.proto\"\xcb\x01\n\x0f\x44\x65viceStability\x12\x37\n\x0c\x64ut_criteria\x18\x01 \x03(\x0b\x32!.chromiumos.test.api.DutCriterion\x12\x41\n\tstability\x18\x02 \x01(\x0e\x32..chromiumos.test.dut.DeviceStability.Stability\"<\n\tStability\x12\x15\n\x11STABILITY_UNKNOWN\x10\x00\x12\n\n\x06STABLE\x10\x01\x12\x0c\n\x08UNSTABLE\x10\x02\"K\n\x13\x44\x65viceStabilityList\x12\x34\n\x06values\x18\x01 \x03(\x0b\x32$.chromiumos.test.dut.DeviceStabilityB/Z-go.chromium.org/chromiumos/config/go/test/dutb\x06proto3'
  ,
  dependencies=[chromiumos_dot_test_dot_api_dot_dut__attribute__pb2.DESCRIPTOR,])



_DEVICESTABILITY_STABILITY = _descriptor.EnumDescriptor(
  name='Stability',
  full_name='chromiumos.test.dut.DeviceStability.Stability',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='STABILITY_UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STABLE', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNSTABLE', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=252,
  serialized_end=312,
)
_sym_db.RegisterEnumDescriptor(_DEVICESTABILITY_STABILITY)


_DEVICESTABILITY = _descriptor.Descriptor(
  name='DeviceStability',
  full_name='chromiumos.test.dut.DeviceStability',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='dut_criteria', full_name='chromiumos.test.dut.DeviceStability.dut_criteria', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stability', full_name='chromiumos.test.dut.DeviceStability.stability', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _DEVICESTABILITY_STABILITY,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=109,
  serialized_end=312,
)


_DEVICESTABILITYLIST = _descriptor.Descriptor(
  name='DeviceStabilityList',
  full_name='chromiumos.test.dut.DeviceStabilityList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='values', full_name='chromiumos.test.dut.DeviceStabilityList.values', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=314,
  serialized_end=389,
)

_DEVICESTABILITY.fields_by_name['dut_criteria'].message_type = chromiumos_dot_test_dot_api_dot_dut__attribute__pb2._DUTCRITERION
_DEVICESTABILITY.fields_by_name['stability'].enum_type = _DEVICESTABILITY_STABILITY
_DEVICESTABILITY_STABILITY.containing_type = _DEVICESTABILITY
_DEVICESTABILITYLIST.fields_by_name['values'].message_type = _DEVICESTABILITY
DESCRIPTOR.message_types_by_name['DeviceStability'] = _DEVICESTABILITY
DESCRIPTOR.message_types_by_name['DeviceStabilityList'] = _DEVICESTABILITYLIST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DeviceStability = _reflection.GeneratedProtocolMessageType('DeviceStability', (_message.Message,), {
  'DESCRIPTOR' : _DEVICESTABILITY,
  '__module__' : 'chromiumos.test.dut.device_stability_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.dut.DeviceStability)
  })
_sym_db.RegisterMessage(DeviceStability)

DeviceStabilityList = _reflection.GeneratedProtocolMessageType('DeviceStabilityList', (_message.Message,), {
  'DESCRIPTOR' : _DEVICESTABILITYLIST,
  '__module__' : 'chromiumos.test.dut.device_stability_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.dut.DeviceStabilityList)
  })
_sym_db.RegisterMessage(DeviceStabilityList)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
