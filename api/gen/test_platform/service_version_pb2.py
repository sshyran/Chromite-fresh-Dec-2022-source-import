# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/service_version.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='test_platform/service_version.proto',
  package='test_platform',
  syntax='proto3',
  serialized_options=_b('Z7go.chromium.org/chromiumos/infra/proto/go/test_platform'),
  serialized_pb=_b('\n#test_platform/service_version.proto\x12\rtest_platform\"K\n\x0eServiceVersion\x12\x13\n\x0bskylab_tool\x18\x02 \x01(\x03\x12\x16\n\x0e\x63rosfleet_tool\x18\x03 \x01(\x03J\x04\x08\x01\x10\x02R\x06globalB9Z7go.chromium.org/chromiumos/infra/proto/go/test_platformb\x06proto3')
)




_SERVICEVERSION = _descriptor.Descriptor(
  name='ServiceVersion',
  full_name='test_platform.ServiceVersion',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='skylab_tool', full_name='test_platform.ServiceVersion.skylab_tool', index=0,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='crosfleet_tool', full_name='test_platform.ServiceVersion.crosfleet_tool', index=1,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=54,
  serialized_end=129,
)

DESCRIPTOR.message_types_by_name['ServiceVersion'] = _SERVICEVERSION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ServiceVersion = _reflection.GeneratedProtocolMessageType('ServiceVersion', (_message.Message,), dict(
  DESCRIPTOR = _SERVICEVERSION,
  __module__ = 'test_platform.service_version_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.ServiceVersion)
  ))
_sym_db.RegisterMessage(ServiceVersion)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
