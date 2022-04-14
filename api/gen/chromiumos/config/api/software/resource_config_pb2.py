# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/config/api/software/resource_config.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import message as _message
from chromite.third_party.google.protobuf import reflection as _reflection
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromiumos/config/api/software/resource_config.proto',
  package='chromiumos.config.api.software',
  syntax='proto3',
  serialized_options=b'Z1go.chromium.org/chromiumos/config/go/api/software',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n4chromiumos/config/api/software/resource_config.proto\x12\x1e\x63hromiumos.config.api.software\"\x9f\x06\n\x0eResourceConfig\x12}\n\x19\x64\x65\x66\x61ult_power_preferences\x18\x01 \x01(\x0b\x32?.chromiumos.config.api.software.ResourceConfig.PowerPreferencesR\x19\x64\x65\x66\x61ult-power-preferences\x12}\n\x19web_rtc_power_preferences\x18\x02 \x01(\x0b\x32?.chromiumos.config.api.software.ResourceConfig.PowerPreferencesR\x19web-rtc-power-preferences\x12\x89\x01\n\"fullscreen_video_power_preferences\x18\x03 \x01(\x0b\x32?.chromiumos.config.api.software.ResourceConfig.PowerPreferencesR\x1c\x66ullscreen-power-preferences\x12{\n\x18gaming_power_preferences\x18\x04 \x01(\x0b\x32?.chromiumos.config.api.software.ResourceConfig.PowerPreferencesR\x18gaming-power-preferences\x1a:\n\x10OndemandGovernor\x12&\n\x0epowersave_bias\x18\x01 \x01(\rR\x0epowersave-bias\x1ak\n\x08Governor\x12S\n\x08ondemand\x18\x01 \x01(\x0b\x32?.chromiumos.config.api.software.ResourceConfig.OndemandGovernorH\x00\x42\n\n\x08governor\x1a]\n\x10PowerPreferences\x12I\n\x08governor\x18\x01 \x01(\x0b\x32\x37.chromiumos.config.api.software.ResourceConfig.GovernorB3Z1go.chromium.org/chromiumos/config/go/api/softwareb\x06proto3'
)




_RESOURCECONFIG_ONDEMANDGOVERNOR = _descriptor.Descriptor(
  name='OndemandGovernor',
  full_name='chromiumos.config.api.software.ResourceConfig.OndemandGovernor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='powersave_bias', full_name='chromiumos.config.api.software.ResourceConfig.OndemandGovernor.powersave_bias', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='powersave-bias', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=626,
  serialized_end=684,
)

_RESOURCECONFIG_GOVERNOR = _descriptor.Descriptor(
  name='Governor',
  full_name='chromiumos.config.api.software.ResourceConfig.Governor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ondemand', full_name='chromiumos.config.api.software.ResourceConfig.Governor.ondemand', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
    _descriptor.OneofDescriptor(
      name='governor', full_name='chromiumos.config.api.software.ResourceConfig.Governor.governor',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=686,
  serialized_end=793,
)

_RESOURCECONFIG_POWERPREFERENCES = _descriptor.Descriptor(
  name='PowerPreferences',
  full_name='chromiumos.config.api.software.ResourceConfig.PowerPreferences',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='governor', full_name='chromiumos.config.api.software.ResourceConfig.PowerPreferences.governor', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=795,
  serialized_end=888,
)

_RESOURCECONFIG = _descriptor.Descriptor(
  name='ResourceConfig',
  full_name='chromiumos.config.api.software.ResourceConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='default_power_preferences', full_name='chromiumos.config.api.software.ResourceConfig.default_power_preferences', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='default-power-preferences', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='web_rtc_power_preferences', full_name='chromiumos.config.api.software.ResourceConfig.web_rtc_power_preferences', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='web-rtc-power-preferences', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fullscreen_video_power_preferences', full_name='chromiumos.config.api.software.ResourceConfig.fullscreen_video_power_preferences', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='fullscreen-power-preferences', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='gaming_power_preferences', full_name='chromiumos.config.api.software.ResourceConfig.gaming_power_preferences', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='gaming-power-preferences', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_RESOURCECONFIG_ONDEMANDGOVERNOR, _RESOURCECONFIG_GOVERNOR, _RESOURCECONFIG_POWERPREFERENCES, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=89,
  serialized_end=888,
)

_RESOURCECONFIG_ONDEMANDGOVERNOR.containing_type = _RESOURCECONFIG
_RESOURCECONFIG_GOVERNOR.fields_by_name['ondemand'].message_type = _RESOURCECONFIG_ONDEMANDGOVERNOR
_RESOURCECONFIG_GOVERNOR.containing_type = _RESOURCECONFIG
_RESOURCECONFIG_GOVERNOR.oneofs_by_name['governor'].fields.append(
  _RESOURCECONFIG_GOVERNOR.fields_by_name['ondemand'])
_RESOURCECONFIG_GOVERNOR.fields_by_name['ondemand'].containing_oneof = _RESOURCECONFIG_GOVERNOR.oneofs_by_name['governor']
_RESOURCECONFIG_POWERPREFERENCES.fields_by_name['governor'].message_type = _RESOURCECONFIG_GOVERNOR
_RESOURCECONFIG_POWERPREFERENCES.containing_type = _RESOURCECONFIG
_RESOURCECONFIG.fields_by_name['default_power_preferences'].message_type = _RESOURCECONFIG_POWERPREFERENCES
_RESOURCECONFIG.fields_by_name['web_rtc_power_preferences'].message_type = _RESOURCECONFIG_POWERPREFERENCES
_RESOURCECONFIG.fields_by_name['fullscreen_video_power_preferences'].message_type = _RESOURCECONFIG_POWERPREFERENCES
_RESOURCECONFIG.fields_by_name['gaming_power_preferences'].message_type = _RESOURCECONFIG_POWERPREFERENCES
DESCRIPTOR.message_types_by_name['ResourceConfig'] = _RESOURCECONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ResourceConfig = _reflection.GeneratedProtocolMessageType('ResourceConfig', (_message.Message,), {

  'OndemandGovernor' : _reflection.GeneratedProtocolMessageType('OndemandGovernor', (_message.Message,), {
    'DESCRIPTOR' : _RESOURCECONFIG_ONDEMANDGOVERNOR,
    '__module__' : 'chromiumos.config.api.software.resource_config_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.config.api.software.ResourceConfig.OndemandGovernor)
    })
  ,

  'Governor' : _reflection.GeneratedProtocolMessageType('Governor', (_message.Message,), {
    'DESCRIPTOR' : _RESOURCECONFIG_GOVERNOR,
    '__module__' : 'chromiumos.config.api.software.resource_config_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.config.api.software.ResourceConfig.Governor)
    })
  ,

  'PowerPreferences' : _reflection.GeneratedProtocolMessageType('PowerPreferences', (_message.Message,), {
    'DESCRIPTOR' : _RESOURCECONFIG_POWERPREFERENCES,
    '__module__' : 'chromiumos.config.api.software.resource_config_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.config.api.software.ResourceConfig.PowerPreferences)
    })
  ,
  'DESCRIPTOR' : _RESOURCECONFIG,
  '__module__' : 'chromiumos.config.api.software.resource_config_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.software.ResourceConfig)
  })
_sym_db.RegisterMessage(ResourceConfig)
_sym_db.RegisterMessage(ResourceConfig.OndemandGovernor)
_sym_db.RegisterMessage(ResourceConfig.Governor)
_sym_db.RegisterMessage(ResourceConfig.PowerPreferences)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
