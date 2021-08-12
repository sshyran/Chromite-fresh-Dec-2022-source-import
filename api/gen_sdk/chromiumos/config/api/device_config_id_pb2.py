# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/config/api/device_config_id.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen_sdk.chromiumos.config.api import design_config_id_pb2 as chromiumos_dot_config_dot_api_dot_design__config__id__pb2
from chromite.api.gen_sdk.chromiumos.config.api import device_brand_id_pb2 as chromiumos_dot_config_dot_api_dot_device__brand__id__pb2
from chromite.api.gen_sdk.chromiumos.config.api import mfg_config_id_pb2 as chromiumos_dot_config_dot_api_dot_mfg__config__id__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromiumos/config/api/device_config_id.proto',
  package='chromiumos.config.api',
  syntax='proto3',
  serialized_options=b'Z(go.chromium.org/chromiumos/config/go/api',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n,chromiumos/config/api/device_config_id.proto\x12\x15\x63hromiumos.config.api\x1a,chromiumos/config/api/design_config_id.proto\x1a+chromiumos/config/api/device_brand_id.proto\x1a)chromiumos/config/api/mfg_config_id.proto\"\xbc\x03\n\x0e\x44\x65viceConfigId\x12?\n\x10\x64\x65sign_config_id\x18\x01 \x01(\x0b\x32%.chromiumos.config.api.DesignConfigId\x12=\n\x0f\x64\x65vice_brand_id\x18\x02 \x01(\x0b\x32$.chromiumos.config.api.DeviceBrandId\x12\x39\n\rmfg_config_id\x18\x03 \x01(\x0b\x32\".chromiumos.config.api.MfgConfigId\x1a\xee\x01\n\nScanConfig\x12L\n\x12\x64\x65sign_scan_config\x18\x01 \x01(\x0b\x32\x30.chromiumos.config.api.DesignConfigId.ScanConfig\x12J\n\x11\x62rand_scan_config\x18\x02 \x01(\x0b\x32/.chromiumos.config.api.DeviceBrandId.ScanConfig\x12\x46\n\x0fmfg_scan_config\x18\x03 \x01(\x0b\x32-.chromiumos.config.api.MfgConfigId.ScanConfigB*Z(go.chromium.org/chromiumos/config/go/apib\x06proto3'
  ,
  dependencies=[chromiumos_dot_config_dot_api_dot_design__config__id__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_device__brand__id__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_mfg__config__id__pb2.DESCRIPTOR,])




_DEVICECONFIGID_SCANCONFIG = _descriptor.Descriptor(
  name='ScanConfig',
  full_name='chromiumos.config.api.DeviceConfigId.ScanConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='design_scan_config', full_name='chromiumos.config.api.DeviceConfigId.ScanConfig.design_scan_config', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='brand_scan_config', full_name='chromiumos.config.api.DeviceConfigId.ScanConfig.brand_scan_config', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mfg_scan_config', full_name='chromiumos.config.api.DeviceConfigId.ScanConfig.mfg_scan_config', index=2,
      number=3, type=11, cpp_type=10, label=1,
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
  serialized_start=412,
  serialized_end=650,
)

_DEVICECONFIGID = _descriptor.Descriptor(
  name='DeviceConfigId',
  full_name='chromiumos.config.api.DeviceConfigId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='design_config_id', full_name='chromiumos.config.api.DeviceConfigId.design_config_id', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='device_brand_id', full_name='chromiumos.config.api.DeviceConfigId.device_brand_id', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mfg_config_id', full_name='chromiumos.config.api.DeviceConfigId.mfg_config_id', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_DEVICECONFIGID_SCANCONFIG, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=206,
  serialized_end=650,
)

_DEVICECONFIGID_SCANCONFIG.fields_by_name['design_scan_config'].message_type = chromiumos_dot_config_dot_api_dot_design__config__id__pb2._DESIGNCONFIGID_SCANCONFIG
_DEVICECONFIGID_SCANCONFIG.fields_by_name['brand_scan_config'].message_type = chromiumos_dot_config_dot_api_dot_device__brand__id__pb2._DEVICEBRANDID_SCANCONFIG
_DEVICECONFIGID_SCANCONFIG.fields_by_name['mfg_scan_config'].message_type = chromiumos_dot_config_dot_api_dot_mfg__config__id__pb2._MFGCONFIGID_SCANCONFIG
_DEVICECONFIGID_SCANCONFIG.containing_type = _DEVICECONFIGID
_DEVICECONFIGID.fields_by_name['design_config_id'].message_type = chromiumos_dot_config_dot_api_dot_design__config__id__pb2._DESIGNCONFIGID
_DEVICECONFIGID.fields_by_name['device_brand_id'].message_type = chromiumos_dot_config_dot_api_dot_device__brand__id__pb2._DEVICEBRANDID
_DEVICECONFIGID.fields_by_name['mfg_config_id'].message_type = chromiumos_dot_config_dot_api_dot_mfg__config__id__pb2._MFGCONFIGID
DESCRIPTOR.message_types_by_name['DeviceConfigId'] = _DEVICECONFIGID
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DeviceConfigId = _reflection.GeneratedProtocolMessageType('DeviceConfigId', (_message.Message,), {

  'ScanConfig' : _reflection.GeneratedProtocolMessageType('ScanConfig', (_message.Message,), {
    'DESCRIPTOR' : _DEVICECONFIGID_SCANCONFIG,
    '__module__' : 'chromiumos.config.api.device_config_id_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.config.api.DeviceConfigId.ScanConfig)
    })
  ,
  'DESCRIPTOR' : _DEVICECONFIGID,
  '__module__' : 'chromiumos.config.api.device_config_id_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.DeviceConfigId)
  })
_sym_db.RegisterMessage(DeviceConfigId)
_sym_db.RegisterMessage(DeviceConfigId.ScanConfig)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)