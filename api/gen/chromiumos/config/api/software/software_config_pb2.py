# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/config/api/software/software_config.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import message as _message
from chromite.third_party.google.protobuf import reflection as _reflection
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.chromiumos.build.api import factory_pb2 as chromiumos_dot_build_dot_api_dot_factory__pb2
from chromite.api.gen.chromiumos.build.api import firmware_config_pb2 as chromiumos_dot_build_dot_api_dot_firmware__config__pb2
from chromite.api.gen.chromiumos.build.api import system_image_pb2 as chromiumos_dot_build_dot_api_dot_system__image__pb2
from chromite.api.gen.chromiumos.config.api import design_config_id_pb2 as chromiumos_dot_config_dot_api_dot_design__config__id__pb2
from chromite.api.gen.chromiumos.config.api.software import audio_config_pb2 as chromiumos_dot_config_dot_api_dot_software_dot_audio__config__pb2
from chromite.api.gen.chromiumos.config.api.software import bluetooth_config_pb2 as chromiumos_dot_config_dot_api_dot_software_dot_bluetooth__config__pb2
from chromite.api.gen.chromiumos.config.api.software import camera_config_pb2 as chromiumos_dot_config_dot_api_dot_software_dot_camera__config__pb2
from chromite.api.gen.chromiumos.config.api.software import health_config_pb2 as chromiumos_dot_config_dot_api_dot_software_dot_health__config__pb2
from chromite.api.gen.chromiumos.config.api.software import nnpalm_config_pb2 as chromiumos_dot_config_dot_api_dot_software_dot_nnpalm__config__pb2
from chromite.api.gen.chromiumos.config.api.software import power_config_pb2 as chromiumos_dot_config_dot_api_dot_software_dot_power__config__pb2
from chromite.api.gen.chromiumos.config.api.software import resource_config_pb2 as chromiumos_dot_config_dot_api_dot_software_dot_resource__config__pb2
from chromite.api.gen.chromiumos.config.api.software import ui_config_pb2 as chromiumos_dot_config_dot_api_dot_software_dot_ui__config__pb2
from chromite.api.gen.chromiumos.config.api.software import usb_config_pb2 as chromiumos_dot_config_dot_api_dot_software_dot_usb__config__pb2
from chromite.api.gen.chromiumos.config.api import wifi_config_pb2 as chromiumos_dot_config_dot_api_dot_wifi__config__pb2
from chromite.api.gen.chromiumos.config.public_replication import public_replication_pb2 as chromiumos_dot_config_dot_public__replication_dot_public__replication__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromiumos/config/api/software/software_config.proto',
  package='chromiumos.config.api.software',
  syntax='proto3',
  serialized_options=b'Z1go.chromium.org/chromiumos/config/go/api/software',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n4chromiumos/config/api/software/software_config.proto\x12\x1e\x63hromiumos.config.api.software\x1a\"chromiumos/build/api/factory.proto\x1a*chromiumos/build/api/firmware_config.proto\x1a\'chromiumos/build/api/system_image.proto\x1a,chromiumos/config/api/design_config_id.proto\x1a\x31\x63hromiumos/config/api/software/audio_config.proto\x1a\x35\x63hromiumos/config/api/software/bluetooth_config.proto\x1a\x32\x63hromiumos/config/api/software/camera_config.proto\x1a\x32\x63hromiumos/config/api/software/health_config.proto\x1a\x32\x63hromiumos/config/api/software/nnpalm_config.proto\x1a\x31\x63hromiumos/config/api/software/power_config.proto\x1a\x34\x63hromiumos/config/api/software/resource_config.proto\x1a.chromiumos/config/api/software/ui_config.proto\x1a/chromiumos/config/api/software/usb_config.proto\x1a\'chromiumos/config/api/wifi_config.proto\x1a=chromiumos/config/public_replication/public_replication.proto\"\x84\n\n\x0eSoftwareConfig\x12S\n\x12public_replication\x18\x0c \x01(\x0b\x32\x37.chromiumos.config.public_replication.PublicReplication\x12?\n\x10\x64\x65sign_config_id\x18\x07 \x01(\x0b\x32%.chromiumos.config.api.DesignConfigId\x12H\n\x0eid_scan_config\x18\x08 \x01(\x0b\x32\x30.chromiumos.config.api.DesignConfigId.ScanConfig\x12\x36\n\x08\x66irmware\x18\x03 \x01(\x0b\x32$.chromiumos.build.api.FirmwareConfig\x12H\n\x15\x66irmware_build_config\x18\t \x01(\x0b\x32).chromiumos.build.api.FirmwareBuildConfig\x12K\n\x16\x66irmware_build_targets\x18\x10 \x01(\x0b\x32+.chromiumos.build.api.Firmware.BuildTargets\x12J\n\x13system_build_target\x18\r \x01(\x0b\x32-.chromiumos.build.api.SystemImage.BuildTarget\x12G\n\x14\x66\x61\x63tory_build_target\x18\x0e \x01(\x0b\x32).chromiumos.build.api.Factory.BuildTarget\x12I\n\x10\x62luetooth_config\x18\x04 \x01(\x0b\x32/.chromiumos.config.api.software.BluetoothConfig\x12\x41\n\x0cpower_config\x18\x05 \x01(\x0b\x32+.chromiumos.config.api.software.PowerConfig\x12G\n\x0fresource_config\x18\x13 \x01(\x0b\x32..chromiumos.config.api.software.ResourceConfig\x12\x42\n\raudio_configs\x18\n \x03(\x0b\x32+.chromiumos.config.api.software.AudioConfig\x12\x36\n\x0bwifi_config\x18\x0b \x01(\x0b\x32!.chromiumos.config.api.WifiConfig\x12\x43\n\rhealth_config\x18\x12 \x01(\x0b\x32,.chromiumos.config.api.software.HealthConfig\x12\x43\n\rcamera_config\x18\x0f \x01(\x0b\x32,.chromiumos.config.api.software.CameraConfig\x12;\n\tui_config\x18\x11 \x01(\x0b\x32(.chromiumos.config.api.software.UiConfig\x12=\n\nusb_config\x18\x14 \x01(\x0b\x32).chromiumos.config.api.software.UsbConfig\x12\x43\n\rnnpalm_config\x18\x15 \x01(\x0b\x32,.chromiumos.config.api.software.NnpalmConfigJ\x04\x08\x01\x10\x02J\x04\x08\x02\x10\x03J\x04\x08\x06\x10\x07\x42\x33Z1go.chromium.org/chromiumos/config/go/api/softwareb\x06proto3'
  ,
  dependencies=[chromiumos_dot_build_dot_api_dot_factory__pb2.DESCRIPTOR,chromiumos_dot_build_dot_api_dot_firmware__config__pb2.DESCRIPTOR,chromiumos_dot_build_dot_api_dot_system__image__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_design__config__id__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_software_dot_audio__config__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_software_dot_bluetooth__config__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_software_dot_camera__config__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_software_dot_health__config__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_software_dot_nnpalm__config__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_software_dot_power__config__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_software_dot_resource__config__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_software_dot_ui__config__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_software_dot_usb__config__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_wifi__config__pb2.DESCRIPTOR,chromiumos_dot_config_dot_public__replication_dot_public__replication__pb2.DESCRIPTOR,])




_SOFTWARECONFIG = _descriptor.Descriptor(
  name='SoftwareConfig',
  full_name='chromiumos.config.api.software.SoftwareConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='public_replication', full_name='chromiumos.config.api.software.SoftwareConfig.public_replication', index=0,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='design_config_id', full_name='chromiumos.config.api.software.SoftwareConfig.design_config_id', index=1,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='id_scan_config', full_name='chromiumos.config.api.software.SoftwareConfig.id_scan_config', index=2,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='firmware', full_name='chromiumos.config.api.software.SoftwareConfig.firmware', index=3,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='firmware_build_config', full_name='chromiumos.config.api.software.SoftwareConfig.firmware_build_config', index=4,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='firmware_build_targets', full_name='chromiumos.config.api.software.SoftwareConfig.firmware_build_targets', index=5,
      number=16, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='system_build_target', full_name='chromiumos.config.api.software.SoftwareConfig.system_build_target', index=6,
      number=13, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='factory_build_target', full_name='chromiumos.config.api.software.SoftwareConfig.factory_build_target', index=7,
      number=14, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bluetooth_config', full_name='chromiumos.config.api.software.SoftwareConfig.bluetooth_config', index=8,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='power_config', full_name='chromiumos.config.api.software.SoftwareConfig.power_config', index=9,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='resource_config', full_name='chromiumos.config.api.software.SoftwareConfig.resource_config', index=10,
      number=19, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='audio_configs', full_name='chromiumos.config.api.software.SoftwareConfig.audio_configs', index=11,
      number=10, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='wifi_config', full_name='chromiumos.config.api.software.SoftwareConfig.wifi_config', index=12,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='health_config', full_name='chromiumos.config.api.software.SoftwareConfig.health_config', index=13,
      number=18, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='camera_config', full_name='chromiumos.config.api.software.SoftwareConfig.camera_config', index=14,
      number=15, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ui_config', full_name='chromiumos.config.api.software.SoftwareConfig.ui_config', index=15,
      number=17, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='usb_config', full_name='chromiumos.config.api.software.SoftwareConfig.usb_config', index=16,
      number=20, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nnpalm_config', full_name='chromiumos.config.api.software.SoftwareConfig.nnpalm_config', index=17,
      number=21, type=11, cpp_type=10, label=1,
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
  serialized_start=824,
  serialized_end=2108,
)

_SOFTWARECONFIG.fields_by_name['public_replication'].message_type = chromiumos_dot_config_dot_public__replication_dot_public__replication__pb2._PUBLICREPLICATION
_SOFTWARECONFIG.fields_by_name['design_config_id'].message_type = chromiumos_dot_config_dot_api_dot_design__config__id__pb2._DESIGNCONFIGID
_SOFTWARECONFIG.fields_by_name['id_scan_config'].message_type = chromiumos_dot_config_dot_api_dot_design__config__id__pb2._DESIGNCONFIGID_SCANCONFIG
_SOFTWARECONFIG.fields_by_name['firmware'].message_type = chromiumos_dot_build_dot_api_dot_firmware__config__pb2._FIRMWARECONFIG
_SOFTWARECONFIG.fields_by_name['firmware_build_config'].message_type = chromiumos_dot_build_dot_api_dot_firmware__config__pb2._FIRMWAREBUILDCONFIG
_SOFTWARECONFIG.fields_by_name['firmware_build_targets'].message_type = chromiumos_dot_build_dot_api_dot_firmware__config__pb2._FIRMWARE_BUILDTARGETS
_SOFTWARECONFIG.fields_by_name['system_build_target'].message_type = chromiumos_dot_build_dot_api_dot_system__image__pb2._SYSTEMIMAGE_BUILDTARGET
_SOFTWARECONFIG.fields_by_name['factory_build_target'].message_type = chromiumos_dot_build_dot_api_dot_factory__pb2._FACTORY_BUILDTARGET
_SOFTWARECONFIG.fields_by_name['bluetooth_config'].message_type = chromiumos_dot_config_dot_api_dot_software_dot_bluetooth__config__pb2._BLUETOOTHCONFIG
_SOFTWARECONFIG.fields_by_name['power_config'].message_type = chromiumos_dot_config_dot_api_dot_software_dot_power__config__pb2._POWERCONFIG
_SOFTWARECONFIG.fields_by_name['resource_config'].message_type = chromiumos_dot_config_dot_api_dot_software_dot_resource__config__pb2._RESOURCECONFIG
_SOFTWARECONFIG.fields_by_name['audio_configs'].message_type = chromiumos_dot_config_dot_api_dot_software_dot_audio__config__pb2._AUDIOCONFIG
_SOFTWARECONFIG.fields_by_name['wifi_config'].message_type = chromiumos_dot_config_dot_api_dot_wifi__config__pb2._WIFICONFIG
_SOFTWARECONFIG.fields_by_name['health_config'].message_type = chromiumos_dot_config_dot_api_dot_software_dot_health__config__pb2._HEALTHCONFIG
_SOFTWARECONFIG.fields_by_name['camera_config'].message_type = chromiumos_dot_config_dot_api_dot_software_dot_camera__config__pb2._CAMERACONFIG
_SOFTWARECONFIG.fields_by_name['ui_config'].message_type = chromiumos_dot_config_dot_api_dot_software_dot_ui__config__pb2._UICONFIG
_SOFTWARECONFIG.fields_by_name['usb_config'].message_type = chromiumos_dot_config_dot_api_dot_software_dot_usb__config__pb2._USBCONFIG
_SOFTWARECONFIG.fields_by_name['nnpalm_config'].message_type = chromiumos_dot_config_dot_api_dot_software_dot_nnpalm__config__pb2._NNPALMCONFIG
DESCRIPTOR.message_types_by_name['SoftwareConfig'] = _SOFTWARECONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SoftwareConfig = _reflection.GeneratedProtocolMessageType('SoftwareConfig', (_message.Message,), {
  'DESCRIPTOR' : _SOFTWARECONFIG,
  '__module__' : 'chromiumos.config.api.software.software_config_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.software.SoftwareConfig)
  })
_sym_db.RegisterMessage(SoftwareConfig)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
