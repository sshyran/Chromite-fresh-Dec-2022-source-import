# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/config/api/mfg_config_id.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromiumos/config/api/mfg_config_id.proto',
  package='chromiumos.config.api',
  syntax='proto3',
  serialized_options=b'Z(go.chromium.org/chromiumos/config/go/api',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n)chromiumos/config/api/mfg_config_id.proto\x12\x15\x63hromiumos.config.api\"8\n\x0bMfgConfigId\x12\r\n\x05value\x18\x01 \x01(\t\x1a\x1a\n\nScanConfig\x12\x0c\n\x04hwid\x18\x01 \x01(\tB*Z(go.chromium.org/chromiumos/config/go/apib\x06proto3'
)




_MFGCONFIGID_SCANCONFIG = _descriptor.Descriptor(
  name='ScanConfig',
  full_name='chromiumos.config.api.MfgConfigId.ScanConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='hwid', full_name='chromiumos.config.api.MfgConfigId.ScanConfig.hwid', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=98,
  serialized_end=124,
)

_MFGCONFIGID = _descriptor.Descriptor(
  name='MfgConfigId',
  full_name='chromiumos.config.api.MfgConfigId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='chromiumos.config.api.MfgConfigId.value', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_MFGCONFIGID_SCANCONFIG, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=68,
  serialized_end=124,
)

_MFGCONFIGID_SCANCONFIG.containing_type = _MFGCONFIGID
DESCRIPTOR.message_types_by_name['MfgConfigId'] = _MFGCONFIGID
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MfgConfigId = _reflection.GeneratedProtocolMessageType('MfgConfigId', (_message.Message,), {

  'ScanConfig' : _reflection.GeneratedProtocolMessageType('ScanConfig', (_message.Message,), {
    'DESCRIPTOR' : _MFGCONFIGID_SCANCONFIG,
    '__module__' : 'chromiumos.config.api.mfg_config_id_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.config.api.MfgConfigId.ScanConfig)
    })
  ,
  'DESCRIPTOR' : _MFGCONFIGID,
  '__module__' : 'chromiumos.config.api.mfg_config_id_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.MfgConfigId)
  })
_sym_db.RegisterMessage(MfgConfigId)
_sym_db.RegisterMessage(MfgConfigId.ScanConfig)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
