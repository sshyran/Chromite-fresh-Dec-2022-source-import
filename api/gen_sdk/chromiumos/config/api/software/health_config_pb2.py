# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/config/api/software/health_config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n2chromiumos/config/api/software/health_config.proto\x12\x1e\x63hromiumos.config.api.software\"\xd1\x03\n\x0cHealthConfig\x12\x45\n\x07\x62\x61ttery\x18\x01 \x01(\x0b\x32\x34.chromiumos.config.api.software.HealthConfig.Battery\x12J\n\ncached_vpd\x18\x02 \x01(\x0b\x32\x36.chromiumos.config.api.software.HealthConfig.CachedVpd\x12G\n\x08routines\x18\x03 \x01(\x0b\x32\x35.chromiumos.config.api.software.HealthConfig.Routines\x1a)\n\x07\x42\x61ttery\x12\x1e\n\x16has_smart_battery_info\x18\x01 \x01(\x08\x1a#\n\tCachedVpd\x12\x16\n\x0ehas_sku_number\x18\x01 \x01(\x08\x1a\x35\n\rBatteryHealth\x12$\n\x1cpercent_battery_wear_allowed\x18\x01 \x01(\r\x1a^\n\x08Routines\x12R\n\x0e\x62\x61ttery_health\x18\x01 \x01(\x0b\x32:.chromiumos.config.api.software.HealthConfig.BatteryHealthB3Z1go.chromium.org/chromiumos/config/go/api/softwareb\x06proto3')



_HEALTHCONFIG = DESCRIPTOR.message_types_by_name['HealthConfig']
_HEALTHCONFIG_BATTERY = _HEALTHCONFIG.nested_types_by_name['Battery']
_HEALTHCONFIG_CACHEDVPD = _HEALTHCONFIG.nested_types_by_name['CachedVpd']
_HEALTHCONFIG_BATTERYHEALTH = _HEALTHCONFIG.nested_types_by_name['BatteryHealth']
_HEALTHCONFIG_ROUTINES = _HEALTHCONFIG.nested_types_by_name['Routines']
HealthConfig = _reflection.GeneratedProtocolMessageType('HealthConfig', (_message.Message,), {

  'Battery' : _reflection.GeneratedProtocolMessageType('Battery', (_message.Message,), {
    'DESCRIPTOR' : _HEALTHCONFIG_BATTERY,
    '__module__' : 'chromiumos.config.api.software.health_config_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.config.api.software.HealthConfig.Battery)
    })
  ,

  'CachedVpd' : _reflection.GeneratedProtocolMessageType('CachedVpd', (_message.Message,), {
    'DESCRIPTOR' : _HEALTHCONFIG_CACHEDVPD,
    '__module__' : 'chromiumos.config.api.software.health_config_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.config.api.software.HealthConfig.CachedVpd)
    })
  ,

  'BatteryHealth' : _reflection.GeneratedProtocolMessageType('BatteryHealth', (_message.Message,), {
    'DESCRIPTOR' : _HEALTHCONFIG_BATTERYHEALTH,
    '__module__' : 'chromiumos.config.api.software.health_config_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.config.api.software.HealthConfig.BatteryHealth)
    })
  ,

  'Routines' : _reflection.GeneratedProtocolMessageType('Routines', (_message.Message,), {
    'DESCRIPTOR' : _HEALTHCONFIG_ROUTINES,
    '__module__' : 'chromiumos.config.api.software.health_config_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.config.api.software.HealthConfig.Routines)
    })
  ,
  'DESCRIPTOR' : _HEALTHCONFIG,
  '__module__' : 'chromiumos.config.api.software.health_config_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.software.HealthConfig)
  })
_sym_db.RegisterMessage(HealthConfig)
_sym_db.RegisterMessage(HealthConfig.Battery)
_sym_db.RegisterMessage(HealthConfig.CachedVpd)
_sym_db.RegisterMessage(HealthConfig.BatteryHealth)
_sym_db.RegisterMessage(HealthConfig.Routines)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z1go.chromium.org/chromiumos/config/go/api/software'
  _HEALTHCONFIG._serialized_start=87
  _HEALTHCONFIG._serialized_end=552
  _HEALTHCONFIG_BATTERY._serialized_start=323
  _HEALTHCONFIG_BATTERY._serialized_end=364
  _HEALTHCONFIG_CACHEDVPD._serialized_start=366
  _HEALTHCONFIG_CACHEDVPD._serialized_end=401
  _HEALTHCONFIG_BATTERYHEALTH._serialized_start=403
  _HEALTHCONFIG_BATTERYHEALTH._serialized_end=456
  _HEALTHCONFIG_ROUTINES._serialized_start=458
  _HEALTHCONFIG_ROUTINES._serialized_end=552
# @@protoc_insertion_point(module_scope)
