# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/execution/param.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import message as _message
from chromite.third_party.google.protobuf import reflection as _reflection
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.chromiumos.build.api import container_metadata_pb2 as chromiumos_dot_build_dot_api_dot_container__metadata__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='test_platform/execution/param.proto',
  package='test_platform.execution',
  syntax='proto3',
  serialized_options=b'ZAgo.chromium.org/chromiumos/infra/proto/go/test_platform/execution',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n#test_platform/execution/param.proto\x12\x17test_platform.execution\x1a-chromiumos/build/api/container_metadata.proto\"\xac\x01\n\x05Param\x12\x16\n\x0eupload_crashes\x18\x01 \x01(\x08\x12\x43\n\x12\x63ontainer_metadata\x18\x02 \x01(\x0b\x32\'.chromiumos.build.api.ContainerMetadata\x12\x46\n\x14\x63ontainer_image_info\x18\x08 \x01(\x0b\x32(.chromiumos.build.api.ContainerImageInfoBCZAgo.chromium.org/chromiumos/infra/proto/go/test_platform/executionb\x06proto3'
  ,
  dependencies=[chromiumos_dot_build_dot_api_dot_container__metadata__pb2.DESCRIPTOR,])




_PARAM = _descriptor.Descriptor(
  name='Param',
  full_name='test_platform.execution.Param',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='upload_crashes', full_name='test_platform.execution.Param.upload_crashes', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='container_metadata', full_name='test_platform.execution.Param.container_metadata', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='container_image_info', full_name='test_platform.execution.Param.container_image_info', index=2,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=112,
  serialized_end=284,
)

_PARAM.fields_by_name['container_metadata'].message_type = chromiumos_dot_build_dot_api_dot_container__metadata__pb2._CONTAINERMETADATA
_PARAM.fields_by_name['container_image_info'].message_type = chromiumos_dot_build_dot_api_dot_container__metadata__pb2._CONTAINERIMAGEINFO
DESCRIPTOR.message_types_by_name['Param'] = _PARAM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Param = _reflection.GeneratedProtocolMessageType('Param', (_message.Message,), {
  'DESCRIPTOR' : _PARAM,
  '__module__' : 'test_platform.execution.param_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.execution.Param)
  })
_sym_db.RegisterMessage(Param)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
