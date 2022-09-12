# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/config/api/program.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen_sdk.chromiumos.config.api import component_pb2 as chromiumos_dot_config_dot_api_dot_component__pb2
from chromite.api.gen_sdk.chromiumos.config.api import design_pb2 as chromiumos_dot_config_dot_api_dot_design__pb2
from chromite.api.gen_sdk.chromiumos.config.api import design_id_pb2 as chromiumos_dot_config_dot_api_dot_design__id__pb2
from chromite.api.gen_sdk.chromiumos.config.api import device_brand_id_pb2 as chromiumos_dot_config_dot_api_dot_device__brand__id__pb2
from chromite.api.gen_sdk.chromiumos.config.api import program_id_pb2 as chromiumos_dot_config_dot_api_dot_program__id__pb2
from chromite.api.gen_sdk.chromiumos.config.api import topology_pb2 as chromiumos_dot_config_dot_api_dot_topology__pb2
from chromite.api.gen_sdk.chromiumos.config.public_replication import public_replication_pb2 as chromiumos_dot_config_dot_public__replication_dot_public__replication__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromiumos/config/api/program.proto',
  package='chromiumos.config.api',
  syntax='proto3',
  serialized_options=b'Z(go.chromium.org/chromiumos/config/go/api',
  serialized_pb=b'\n#chromiumos/config/api/program.proto\x12\x15\x63hromiumos.config.api\x1a%chromiumos/config/api/component.proto\x1a\"chromiumos/config/api/design.proto\x1a%chromiumos/config/api/design_id.proto\x1a+chromiumos/config/api/device_brand_id.proto\x1a&chromiumos/config/api/program_id.proto\x1a$chromiumos/config/api/topology.proto\x1a=chromiumos/config/public_replication/public_replication.proto\":\n\x1c\x46irmwareConfigurationSegment\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04mask\x18\x02 \x01(\r\"k\n\x15\x44\x65signConfigIdSegment\x12\x32\n\tdesign_id\x18\x01 \x01(\x0b\x32\x1f.chromiumos.config.api.DesignId\x12\x0e\n\x06min_id\x18\x02 \x01(\r\x12\x0e\n\x06max_id\x18\x03 \x01(\r\"\xa2\x01\n\x12\x44\x65viceSignerConfig\x12\x38\n\x08\x62rand_id\x18\x01 \x01(\x0b\x32$.chromiumos.config.api.DeviceBrandIdH\x00\x12\x34\n\tdesign_id\x18\x03 \x01(\x0b\x32\x1f.chromiumos.config.api.DesignIdH\x00\x12\x0e\n\x06key_id\x18\x02 \x01(\tB\x0c\n\nidentifier\"\xfb\r\n\x07Program\x12S\n\x12public_replication\x18\x08 \x01(\x0b\x32\x37.chromiumos.config.public_replication.PublicReplication\x12,\n\x02id\x18\x01 \x01(\x0b\x32 .chromiumos.config.api.ProgramId\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x1b\n\x13mosys_platform_name\x18\n \x01(\t\x12\x39\n\x08platform\x18\x0b \x01(\x0b\x32\'.chromiumos.config.api.Program.Platform\x12@\n\x0c\x61udio_config\x18\x0c \x01(\x0b\x32*.chromiumos.config.api.Program.AudioConfig\x12R\n\x19\x64\x65sign_config_constraints\x18\x03 \x03(\x0b\x32/.chromiumos.config.api.Design.Config.Constraint\x12G\n\x0f\x63omponent_quals\x18\x04 \x03(\x0b\x32..chromiumos.config.api.Component.Qualification\x12\\\n\x1f\x66irmware_configuration_segments\x18\x05 \x03(\x0b\x32\x33.chromiumos.config.api.FirmwareConfigurationSegment\x12J\n\rssfc_segments\x18\t \x03(\x0b\x32\x33.chromiumos.config.api.FirmwareConfigurationSegment\x12O\n\x19\x64\x65sign_config_id_segments\x18\x07 \x03(\x0b\x32,.chromiumos.config.api.DesignConfigIdSegment\x12H\n\x15\x64\x65vice_signer_configs\x18\x06 \x03(\x0b\x32).chromiumos.config.api.DeviceSignerConfig\x1a\xcd\x06\n\x08Platform\x12\x12\n\nsoc_family\x18\x01 \x01(\t\x12>\n\x08soc_arch\x18\x02 \x01(\x0e\x32,.chromiumos.config.api.Program.Platform.Arch\x12\x12\n\ngpu_family\x18\x03 \x01(\t\x12J\n\rgraphics_apis\x18\x04 \x03(\x0e\x32\x33.chromiumos.config.api.Program.Platform.GraphicsApi\x12S\n\x0cvideo_codecs\x18\x05 \x03(\x0e\x32=.chromiumos.config.api.Program.Platform.AcceleratedVideoCodec\x12J\n\x0c\x63\x61pabilities\x18\x06 \x01(\x0b\x32\x34.chromiumos.config.api.Program.Platform.Capabilities\x1aP\n\x0c\x43\x61pabilities\x12\x17\n\x0fsuspend_to_idle\x18\x01 \x01(\x08\x12\x13\n\x0b\x64\x61rk_resume\x18\x02 \x01(\x08\x12\x12\n\nwake_on_dp\x18\x03 \x01(\x08\"A\n\x04\x41rch\x12\x10\n\x0c\x41RCH_UNKNOWN\x10\x00\x12\x07\n\x03X86\x10\x01\x12\n\n\x06X86_64\x10\x02\x12\x07\n\x03\x41RM\x10\x03\x12\t\n\x05\x41RM64\x10\x04\"\xf6\x01\n\x15\x41\x63\x63\x65leratedVideoCodec\x12\x13\n\x0f\x43ODEC_UNDEFINED\x10\x00\x12\x0f\n\x0bH264_DECODE\x10\x01\x12\x0f\n\x0bH264_ENCODE\x10\x02\x12\x0e\n\nVP8_DECODE\x10\x03\x12\x0e\n\nVP8_ENCODE\x10\x04\x12\x0e\n\nVP9_DECODE\x10\x05\x12\x0e\n\nVP9_ENCODE\x10\x06\x12\x10\n\x0cVP9_2_DECODE\x10\x07\x12\x10\n\x0cVP9_2_ENCODE\x10\x08\x12\x0f\n\x0bH265_DECODE\x10\t\x12\x0f\n\x0bH265_ENCODE\x10\n\x12\x0f\n\x0bMJPG_DECODE\x10\x0b\x12\x0f\n\x0bMJPG_ENCODE\x10\x0c\"^\n\x0bGraphicsApi\x12\x1a\n\x16GRAPHICS_API_UNDEFINED\x10\x00\x12\x17\n\x13GRAPHICS_API_OPENGL\x10\x01\x12\x1a\n\x16GRAPHICS_API_OPENGL_ES\x10\x02\x1a\x92\x01\n\x0b\x41udioConfig\x12N\n\x0c\x63\x61rd_configs\x18\x01 \x03(\x0b\x32\x38.chromiumos.config.api.HardwareFeatures.Audio.CardConfig\x12\x17\n\x0fhas_module_file\x18\x02 \x01(\x08\x12\x1a\n\x12\x64\x65\x66\x61ult_ucm_suffix\x18\x03 \x01(\tB*Z(go.chromium.org/chromiumos/config/go/apib\x06proto3'
  ,
  dependencies=[chromiumos_dot_config_dot_api_dot_component__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_design__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_design__id__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_device__brand__id__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_program__id__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_topology__pb2.DESCRIPTOR,chromiumos_dot_config_dot_public__replication_dot_public__replication__pb2.DESCRIPTOR,])



_PROGRAM_PLATFORM_ARCH = _descriptor.EnumDescriptor(
  name='Arch',
  full_name='chromiumos.config.api.Program.Platform.Arch',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ARCH_UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='X86', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='X86_64', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ARM', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ARM64', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1925,
  serialized_end=1990,
)
_sym_db.RegisterEnumDescriptor(_PROGRAM_PLATFORM_ARCH)

_PROGRAM_PLATFORM_ACCELERATEDVIDEOCODEC = _descriptor.EnumDescriptor(
  name='AcceleratedVideoCodec',
  full_name='chromiumos.config.api.Program.Platform.AcceleratedVideoCodec',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CODEC_UNDEFINED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='H264_DECODE', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='H264_ENCODE', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VP8_DECODE', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VP8_ENCODE', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VP9_DECODE', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VP9_ENCODE', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VP9_2_DECODE', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VP9_2_ENCODE', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='H265_DECODE', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='H265_ENCODE', index=10, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MJPG_DECODE', index=11, number=11,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MJPG_ENCODE', index=12, number=12,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1993,
  serialized_end=2239,
)
_sym_db.RegisterEnumDescriptor(_PROGRAM_PLATFORM_ACCELERATEDVIDEOCODEC)

_PROGRAM_PLATFORM_GRAPHICSAPI = _descriptor.EnumDescriptor(
  name='GraphicsApi',
  full_name='chromiumos.config.api.Program.Platform.GraphicsApi',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='GRAPHICS_API_UNDEFINED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GRAPHICS_API_OPENGL', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GRAPHICS_API_OPENGL_ES', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=2241,
  serialized_end=2335,
)
_sym_db.RegisterEnumDescriptor(_PROGRAM_PLATFORM_GRAPHICSAPI)


_FIRMWARECONFIGURATIONSEGMENT = _descriptor.Descriptor(
  name='FirmwareConfigurationSegment',
  full_name='chromiumos.config.api.FirmwareConfigurationSegment',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='chromiumos.config.api.FirmwareConfigurationSegment.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mask', full_name='chromiumos.config.api.FirmwareConfigurationSegment.mask', index=1,
      number=2, type=13, cpp_type=3, label=1,
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
  serialized_start=362,
  serialized_end=420,
)


_DESIGNCONFIGIDSEGMENT = _descriptor.Descriptor(
  name='DesignConfigIdSegment',
  full_name='chromiumos.config.api.DesignConfigIdSegment',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='design_id', full_name='chromiumos.config.api.DesignConfigIdSegment.design_id', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='min_id', full_name='chromiumos.config.api.DesignConfigIdSegment.min_id', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='max_id', full_name='chromiumos.config.api.DesignConfigIdSegment.max_id', index=2,
      number=3, type=13, cpp_type=3, label=1,
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
  serialized_start=422,
  serialized_end=529,
)


_DEVICESIGNERCONFIG = _descriptor.Descriptor(
  name='DeviceSignerConfig',
  full_name='chromiumos.config.api.DeviceSignerConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='brand_id', full_name='chromiumos.config.api.DeviceSignerConfig.brand_id', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='design_id', full_name='chromiumos.config.api.DeviceSignerConfig.design_id', index=1,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='key_id', full_name='chromiumos.config.api.DeviceSignerConfig.key_id', index=2,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
    _descriptor.OneofDescriptor(
      name='identifier', full_name='chromiumos.config.api.DeviceSignerConfig.identifier',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=532,
  serialized_end=694,
)


_PROGRAM_PLATFORM_CAPABILITIES = _descriptor.Descriptor(
  name='Capabilities',
  full_name='chromiumos.config.api.Program.Platform.Capabilities',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='suspend_to_idle', full_name='chromiumos.config.api.Program.Platform.Capabilities.suspend_to_idle', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dark_resume', full_name='chromiumos.config.api.Program.Platform.Capabilities.dark_resume', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='wake_on_dp', full_name='chromiumos.config.api.Program.Platform.Capabilities.wake_on_dp', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=1843,
  serialized_end=1923,
)

_PROGRAM_PLATFORM = _descriptor.Descriptor(
  name='Platform',
  full_name='chromiumos.config.api.Program.Platform',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='soc_family', full_name='chromiumos.config.api.Program.Platform.soc_family', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='soc_arch', full_name='chromiumos.config.api.Program.Platform.soc_arch', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='gpu_family', full_name='chromiumos.config.api.Program.Platform.gpu_family', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='graphics_apis', full_name='chromiumos.config.api.Program.Platform.graphics_apis', index=3,
      number=4, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='video_codecs', full_name='chromiumos.config.api.Program.Platform.video_codecs', index=4,
      number=5, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='capabilities', full_name='chromiumos.config.api.Program.Platform.capabilities', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_PROGRAM_PLATFORM_CAPABILITIES, ],
  enum_types=[
    _PROGRAM_PLATFORM_ARCH,
    _PROGRAM_PLATFORM_ACCELERATEDVIDEOCODEC,
    _PROGRAM_PLATFORM_GRAPHICSAPI,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1490,
  serialized_end=2335,
)

_PROGRAM_AUDIOCONFIG = _descriptor.Descriptor(
  name='AudioConfig',
  full_name='chromiumos.config.api.Program.AudioConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='card_configs', full_name='chromiumos.config.api.Program.AudioConfig.card_configs', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='has_module_file', full_name='chromiumos.config.api.Program.AudioConfig.has_module_file', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='default_ucm_suffix', full_name='chromiumos.config.api.Program.AudioConfig.default_ucm_suffix', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=2338,
  serialized_end=2484,
)

_PROGRAM = _descriptor.Descriptor(
  name='Program',
  full_name='chromiumos.config.api.Program',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='public_replication', full_name='chromiumos.config.api.Program.public_replication', index=0,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='chromiumos.config.api.Program.id', index=1,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='chromiumos.config.api.Program.name', index=2,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mosys_platform_name', full_name='chromiumos.config.api.Program.mosys_platform_name', index=3,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='platform', full_name='chromiumos.config.api.Program.platform', index=4,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='audio_config', full_name='chromiumos.config.api.Program.audio_config', index=5,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='design_config_constraints', full_name='chromiumos.config.api.Program.design_config_constraints', index=6,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='component_quals', full_name='chromiumos.config.api.Program.component_quals', index=7,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='firmware_configuration_segments', full_name='chromiumos.config.api.Program.firmware_configuration_segments', index=8,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ssfc_segments', full_name='chromiumos.config.api.Program.ssfc_segments', index=9,
      number=9, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='design_config_id_segments', full_name='chromiumos.config.api.Program.design_config_id_segments', index=10,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='device_signer_configs', full_name='chromiumos.config.api.Program.device_signer_configs', index=11,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_PROGRAM_PLATFORM, _PROGRAM_AUDIOCONFIG, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=697,
  serialized_end=2484,
)

_DESIGNCONFIGIDSEGMENT.fields_by_name['design_id'].message_type = chromiumos_dot_config_dot_api_dot_design__id__pb2._DESIGNID
_DEVICESIGNERCONFIG.fields_by_name['brand_id'].message_type = chromiumos_dot_config_dot_api_dot_device__brand__id__pb2._DEVICEBRANDID
_DEVICESIGNERCONFIG.fields_by_name['design_id'].message_type = chromiumos_dot_config_dot_api_dot_design__id__pb2._DESIGNID
_DEVICESIGNERCONFIG.oneofs_by_name['identifier'].fields.append(
  _DEVICESIGNERCONFIG.fields_by_name['brand_id'])
_DEVICESIGNERCONFIG.fields_by_name['brand_id'].containing_oneof = _DEVICESIGNERCONFIG.oneofs_by_name['identifier']
_DEVICESIGNERCONFIG.oneofs_by_name['identifier'].fields.append(
  _DEVICESIGNERCONFIG.fields_by_name['design_id'])
_DEVICESIGNERCONFIG.fields_by_name['design_id'].containing_oneof = _DEVICESIGNERCONFIG.oneofs_by_name['identifier']
_PROGRAM_PLATFORM_CAPABILITIES.containing_type = _PROGRAM_PLATFORM
_PROGRAM_PLATFORM.fields_by_name['soc_arch'].enum_type = _PROGRAM_PLATFORM_ARCH
_PROGRAM_PLATFORM.fields_by_name['graphics_apis'].enum_type = _PROGRAM_PLATFORM_GRAPHICSAPI
_PROGRAM_PLATFORM.fields_by_name['video_codecs'].enum_type = _PROGRAM_PLATFORM_ACCELERATEDVIDEOCODEC
_PROGRAM_PLATFORM.fields_by_name['capabilities'].message_type = _PROGRAM_PLATFORM_CAPABILITIES
_PROGRAM_PLATFORM.containing_type = _PROGRAM
_PROGRAM_PLATFORM_ARCH.containing_type = _PROGRAM_PLATFORM
_PROGRAM_PLATFORM_ACCELERATEDVIDEOCODEC.containing_type = _PROGRAM_PLATFORM
_PROGRAM_PLATFORM_GRAPHICSAPI.containing_type = _PROGRAM_PLATFORM
_PROGRAM_AUDIOCONFIG.fields_by_name['card_configs'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._HARDWAREFEATURES_AUDIO_CARDCONFIG
_PROGRAM_AUDIOCONFIG.containing_type = _PROGRAM
_PROGRAM.fields_by_name['public_replication'].message_type = chromiumos_dot_config_dot_public__replication_dot_public__replication__pb2._PUBLICREPLICATION
_PROGRAM.fields_by_name['id'].message_type = chromiumos_dot_config_dot_api_dot_program__id__pb2._PROGRAMID
_PROGRAM.fields_by_name['platform'].message_type = _PROGRAM_PLATFORM
_PROGRAM.fields_by_name['audio_config'].message_type = _PROGRAM_AUDIOCONFIG
_PROGRAM.fields_by_name['design_config_constraints'].message_type = chromiumos_dot_config_dot_api_dot_design__pb2._DESIGN_CONFIG_CONSTRAINT
_PROGRAM.fields_by_name['component_quals'].message_type = chromiumos_dot_config_dot_api_dot_component__pb2._COMPONENT_QUALIFICATION
_PROGRAM.fields_by_name['firmware_configuration_segments'].message_type = _FIRMWARECONFIGURATIONSEGMENT
_PROGRAM.fields_by_name['ssfc_segments'].message_type = _FIRMWARECONFIGURATIONSEGMENT
_PROGRAM.fields_by_name['design_config_id_segments'].message_type = _DESIGNCONFIGIDSEGMENT
_PROGRAM.fields_by_name['device_signer_configs'].message_type = _DEVICESIGNERCONFIG
DESCRIPTOR.message_types_by_name['FirmwareConfigurationSegment'] = _FIRMWARECONFIGURATIONSEGMENT
DESCRIPTOR.message_types_by_name['DesignConfigIdSegment'] = _DESIGNCONFIGIDSEGMENT
DESCRIPTOR.message_types_by_name['DeviceSignerConfig'] = _DEVICESIGNERCONFIG
DESCRIPTOR.message_types_by_name['Program'] = _PROGRAM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FirmwareConfigurationSegment = _reflection.GeneratedProtocolMessageType('FirmwareConfigurationSegment', (_message.Message,), {
  'DESCRIPTOR' : _FIRMWARECONFIGURATIONSEGMENT,
  '__module__' : 'chromiumos.config.api.program_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.FirmwareConfigurationSegment)
  })
_sym_db.RegisterMessage(FirmwareConfigurationSegment)

DesignConfigIdSegment = _reflection.GeneratedProtocolMessageType('DesignConfigIdSegment', (_message.Message,), {
  'DESCRIPTOR' : _DESIGNCONFIGIDSEGMENT,
  '__module__' : 'chromiumos.config.api.program_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.DesignConfigIdSegment)
  })
_sym_db.RegisterMessage(DesignConfigIdSegment)

DeviceSignerConfig = _reflection.GeneratedProtocolMessageType('DeviceSignerConfig', (_message.Message,), {
  'DESCRIPTOR' : _DEVICESIGNERCONFIG,
  '__module__' : 'chromiumos.config.api.program_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.DeviceSignerConfig)
  })
_sym_db.RegisterMessage(DeviceSignerConfig)

Program = _reflection.GeneratedProtocolMessageType('Program', (_message.Message,), {

  'Platform' : _reflection.GeneratedProtocolMessageType('Platform', (_message.Message,), {

    'Capabilities' : _reflection.GeneratedProtocolMessageType('Capabilities', (_message.Message,), {
      'DESCRIPTOR' : _PROGRAM_PLATFORM_CAPABILITIES,
      '__module__' : 'chromiumos.config.api.program_pb2'
      # @@protoc_insertion_point(class_scope:chromiumos.config.api.Program.Platform.Capabilities)
      })
    ,
    'DESCRIPTOR' : _PROGRAM_PLATFORM,
    '__module__' : 'chromiumos.config.api.program_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.config.api.Program.Platform)
    })
  ,

  'AudioConfig' : _reflection.GeneratedProtocolMessageType('AudioConfig', (_message.Message,), {
    'DESCRIPTOR' : _PROGRAM_AUDIOCONFIG,
    '__module__' : 'chromiumos.config.api.program_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.config.api.Program.AudioConfig)
    })
  ,
  'DESCRIPTOR' : _PROGRAM,
  '__module__' : 'chromiumos.config.api.program_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.Program)
  })
_sym_db.RegisterMessage(Program)
_sym_db.RegisterMessage(Program.Platform)
_sym_db.RegisterMessage(Program.Platform.Capabilities)
_sym_db.RegisterMessage(Program.AudioConfig)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
