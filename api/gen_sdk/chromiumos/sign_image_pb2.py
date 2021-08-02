# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/sign_image.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromiumos/sign_image.proto',
  package='chromiumos',
  syntax='proto3',
  serialized_options=b'\n!com.google.chrome.crosinfra.protoZ4go.chromium.org/chromiumos/infra/proto/go/chromiumos',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1b\x63hromiumos/sign_image.proto\x12\nchromiumos\"\xbe\x01\n\x10\x43r50Instructions\x12\x33\n\x06target\x18\x01 \x01(\x0e\x32#.chromiumos.Cr50Instructions.Target\x12\x11\n\tdevice_id\x18\x02 \x01(\t\"b\n\x06Target\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\n\n\x06PREPVT\x10\x01\x12\x15\n\x11RELEASE_CANDIDATE\x10\x02\x12\x0f\n\x0bNODE_LOCKED\x10\x03\x12\x13\n\x0fGENERAL_RELEASE\x10\x04\"\xbc\x01\n\x0fGscInstructions\x12\x32\n\x06target\x18\x01 \x01(\x0e\x32\".chromiumos.GscInstructions.Target\x12\x11\n\tdevice_id\x18\x02 \x01(\t\"b\n\x06Target\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\n\n\x06PREPVT\x10\x01\x12\x15\n\x11RELEASE_CANDIDATE\x10\x02\x12\x0f\n\x0bNODE_LOCKED\x10\x03\x12\x13\n\x0fGENERAL_RELEASE\x10\x04*_\n\nSignerType\x12\x16\n\x12SIGNER_UNSPECIFIED\x10\x00\x12\x15\n\x11SIGNER_PRODUCTION\x10\x01\x12\x12\n\x0eSIGNER_STAGING\x10\x02\x12\x0e\n\nSIGNER_DEV\x10\x03\x42Y\n!com.google.chrome.crosinfra.protoZ4go.chromium.org/chromiumos/infra/proto/go/chromiumosb\x06proto3'
)

_SIGNERTYPE = _descriptor.EnumDescriptor(
  name='SignerType',
  full_name='chromiumos.SignerType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SIGNER_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SIGNER_PRODUCTION', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SIGNER_STAGING', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SIGNER_DEV', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=427,
  serialized_end=522,
)
_sym_db.RegisterEnumDescriptor(_SIGNERTYPE)

SignerType = enum_type_wrapper.EnumTypeWrapper(_SIGNERTYPE)
SIGNER_UNSPECIFIED = 0
SIGNER_PRODUCTION = 1
SIGNER_STAGING = 2
SIGNER_DEV = 3


_CR50INSTRUCTIONS_TARGET = _descriptor.EnumDescriptor(
  name='Target',
  full_name='chromiumos.Cr50Instructions.Target',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PREPVT', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RELEASE_CANDIDATE', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NODE_LOCKED', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GENERAL_RELEASE', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=136,
  serialized_end=234,
)
_sym_db.RegisterEnumDescriptor(_CR50INSTRUCTIONS_TARGET)

_GSCINSTRUCTIONS_TARGET = _descriptor.EnumDescriptor(
  name='Target',
  full_name='chromiumos.GscInstructions.Target',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PREPVT', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RELEASE_CANDIDATE', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NODE_LOCKED', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GENERAL_RELEASE', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=136,
  serialized_end=234,
)
_sym_db.RegisterEnumDescriptor(_GSCINSTRUCTIONS_TARGET)


_CR50INSTRUCTIONS = _descriptor.Descriptor(
  name='Cr50Instructions',
  full_name='chromiumos.Cr50Instructions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='target', full_name='chromiumos.Cr50Instructions.target', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='device_id', full_name='chromiumos.Cr50Instructions.device_id', index=1,
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
    _CR50INSTRUCTIONS_TARGET,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=44,
  serialized_end=234,
)


_GSCINSTRUCTIONS = _descriptor.Descriptor(
  name='GscInstructions',
  full_name='chromiumos.GscInstructions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='target', full_name='chromiumos.GscInstructions.target', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='device_id', full_name='chromiumos.GscInstructions.device_id', index=1,
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
    _GSCINSTRUCTIONS_TARGET,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=237,
  serialized_end=425,
)

_CR50INSTRUCTIONS.fields_by_name['target'].enum_type = _CR50INSTRUCTIONS_TARGET
_CR50INSTRUCTIONS_TARGET.containing_type = _CR50INSTRUCTIONS
_GSCINSTRUCTIONS.fields_by_name['target'].enum_type = _GSCINSTRUCTIONS_TARGET
_GSCINSTRUCTIONS_TARGET.containing_type = _GSCINSTRUCTIONS
DESCRIPTOR.message_types_by_name['Cr50Instructions'] = _CR50INSTRUCTIONS
DESCRIPTOR.message_types_by_name['GscInstructions'] = _GSCINSTRUCTIONS
DESCRIPTOR.enum_types_by_name['SignerType'] = _SIGNERTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Cr50Instructions = _reflection.GeneratedProtocolMessageType('Cr50Instructions', (_message.Message,), {
  'DESCRIPTOR' : _CR50INSTRUCTIONS,
  '__module__' : 'chromiumos.sign_image_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.Cr50Instructions)
  })
_sym_db.RegisterMessage(Cr50Instructions)

GscInstructions = _reflection.GeneratedProtocolMessageType('GscInstructions', (_message.Message,), {
  'DESCRIPTOR' : _GSCINSTRUCTIONS,
  '__module__' : 'chromiumos.sign_image_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.GscInstructions)
  })
_sym_db.RegisterMessage(GscInstructions)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
