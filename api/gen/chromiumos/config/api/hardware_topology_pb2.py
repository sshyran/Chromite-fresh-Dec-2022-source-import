# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/config/api/hardware_topology.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import message as _message
from chromite.third_party.google.protobuf import reflection as _reflection
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.chromiumos.config.api import topology_pb2 as chromiumos_dot_config_dot_api_dot_topology__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromiumos/config/api/hardware_topology.proto',
  package='chromiumos.config.api',
  syntax='proto3',
  serialized_options=b'Z(go.chromium.org/chromiumos/config/go/api',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n-chromiumos/config/api/hardware_topology.proto\x12\x15\x63hromiumos.config.api\x1a$chromiumos/config/api/topology.proto\"\x92\x0c\n\x10HardwareTopology\x12/\n\x06screen\x18\x01 \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12\x34\n\x0b\x66orm_factor\x18\x02 \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12.\n\x05\x61udio\x18\x03 \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12/\n\x06stylus\x18\x04 \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12\x31\n\x08keyboard\x18\x05 \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12\x30\n\x07thermal\x18\x06 \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12/\n\x06\x63\x61mera\x18\x07 \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12M\n$accelerometer_gyroscope_magnetometer\x18\x08 \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12\x34\n\x0b\x66ingerprint\x18\t \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12\x39\n\x10proximity_sensor\x18\n \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12\x37\n\x0e\x64\x61ughter_board\x18\x0b \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12=\n\x14non_volatile_storage\x18\x0c \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12,\n\x03ram\x18\r \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12-\n\x04wifi\x18\x0e \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12\x37\n\x0e\x63\x65llular_board\x18\x0f \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12\x32\n\tsd_reader\x18\x10 \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12\x38\n\x0fmotherboard_usb\x18\x11 \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12\x32\n\tbluetooth\x18\x12 \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12\x33\n\nbarreljack\x18\x13 \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12\x35\n\x0cpower_button\x18\x14 \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12\x36\n\rvolume_button\x18\x15 \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12+\n\x02\x65\x63\x18\x16 \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12.\n\x05touch\x18\x17 \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12,\n\x03tpm\x18\x18 \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12?\n\x16microphone_mute_switch\x18\x19 \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12-\n\x04hdmi\x18\x1a \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12,\n\x03hps\x18\x1b \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12\x35\n\x0c\x64p_converter\x18\x1c \x01(\x0b\x32\x1f.chromiumos.config.api.Topology\x12,\n\x03poe\x18\x1d \x01(\x0b\x32\x1f.chromiumos.config.api.TopologyB*Z(go.chromium.org/chromiumos/config/go/apib\x06proto3'
  ,
  dependencies=[chromiumos_dot_config_dot_api_dot_topology__pb2.DESCRIPTOR,])




_HARDWARETOPOLOGY = _descriptor.Descriptor(
  name='HardwareTopology',
  full_name='chromiumos.config.api.HardwareTopology',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='screen', full_name='chromiumos.config.api.HardwareTopology.screen', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='form_factor', full_name='chromiumos.config.api.HardwareTopology.form_factor', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='audio', full_name='chromiumos.config.api.HardwareTopology.audio', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stylus', full_name='chromiumos.config.api.HardwareTopology.stylus', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='keyboard', full_name='chromiumos.config.api.HardwareTopology.keyboard', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='thermal', full_name='chromiumos.config.api.HardwareTopology.thermal', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='camera', full_name='chromiumos.config.api.HardwareTopology.camera', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='accelerometer_gyroscope_magnetometer', full_name='chromiumos.config.api.HardwareTopology.accelerometer_gyroscope_magnetometer', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fingerprint', full_name='chromiumos.config.api.HardwareTopology.fingerprint', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='proximity_sensor', full_name='chromiumos.config.api.HardwareTopology.proximity_sensor', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='daughter_board', full_name='chromiumos.config.api.HardwareTopology.daughter_board', index=10,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='non_volatile_storage', full_name='chromiumos.config.api.HardwareTopology.non_volatile_storage', index=11,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ram', full_name='chromiumos.config.api.HardwareTopology.ram', index=12,
      number=13, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='wifi', full_name='chromiumos.config.api.HardwareTopology.wifi', index=13,
      number=14, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cellular_board', full_name='chromiumos.config.api.HardwareTopology.cellular_board', index=14,
      number=15, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sd_reader', full_name='chromiumos.config.api.HardwareTopology.sd_reader', index=15,
      number=16, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='motherboard_usb', full_name='chromiumos.config.api.HardwareTopology.motherboard_usb', index=16,
      number=17, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bluetooth', full_name='chromiumos.config.api.HardwareTopology.bluetooth', index=17,
      number=18, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='barreljack', full_name='chromiumos.config.api.HardwareTopology.barreljack', index=18,
      number=19, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='power_button', full_name='chromiumos.config.api.HardwareTopology.power_button', index=19,
      number=20, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='volume_button', full_name='chromiumos.config.api.HardwareTopology.volume_button', index=20,
      number=21, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ec', full_name='chromiumos.config.api.HardwareTopology.ec', index=21,
      number=22, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='touch', full_name='chromiumos.config.api.HardwareTopology.touch', index=22,
      number=23, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tpm', full_name='chromiumos.config.api.HardwareTopology.tpm', index=23,
      number=24, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='microphone_mute_switch', full_name='chromiumos.config.api.HardwareTopology.microphone_mute_switch', index=24,
      number=25, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='hdmi', full_name='chromiumos.config.api.HardwareTopology.hdmi', index=25,
      number=26, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='hps', full_name='chromiumos.config.api.HardwareTopology.hps', index=26,
      number=27, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dp_converter', full_name='chromiumos.config.api.HardwareTopology.dp_converter', index=27,
      number=28, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='poe', full_name='chromiumos.config.api.HardwareTopology.poe', index=28,
      number=29, type=11, cpp_type=10, label=1,
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
  serialized_start=111,
  serialized_end=1665,
)

_HARDWARETOPOLOGY.fields_by_name['screen'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['form_factor'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['audio'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['stylus'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['keyboard'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['thermal'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['camera'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['accelerometer_gyroscope_magnetometer'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['fingerprint'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['proximity_sensor'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['daughter_board'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['non_volatile_storage'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['ram'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['wifi'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['cellular_board'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['sd_reader'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['motherboard_usb'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['bluetooth'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['barreljack'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['power_button'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['volume_button'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['ec'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['touch'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['tpm'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['microphone_mute_switch'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['hdmi'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['hps'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['dp_converter'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
_HARDWARETOPOLOGY.fields_by_name['poe'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._TOPOLOGY
DESCRIPTOR.message_types_by_name['HardwareTopology'] = _HARDWARETOPOLOGY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

HardwareTopology = _reflection.GeneratedProtocolMessageType('HardwareTopology', (_message.Message,), {
  'DESCRIPTOR' : _HARDWARETOPOLOGY,
  '__module__' : 'chromiumos.config.api.hardware_topology_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.HardwareTopology)
  })
_sym_db.RegisterMessage(HardwareTopology)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
