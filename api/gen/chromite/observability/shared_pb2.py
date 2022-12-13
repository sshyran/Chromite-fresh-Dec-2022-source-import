# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromite/observability/shared.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import message as _message
from chromite.third_party.google.protobuf import reflection as _reflection
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.third_party.google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from chromite.api.gen.chromiumos import common_pb2 as chromiumos_dot_common__pb2
from chromite.api.gen.chromiumos import builder_config_pb2 as chromiumos_dot_builder__config__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromite/observability/shared.proto',
  package='chromite.observability',
  syntax='proto3',
  serialized_options=b'Z@go.chromium.org/chromiumos/infra/proto/go/chromite/observability',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n#chromite/observability/shared.proto\x12\x16\x63hromite.observability\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x17\x63hromiumos/common.proto\x1a\x1f\x63hromiumos/builder_config.proto\"\x95\x02\n\x0f\x42uilderMetadata\x12\x16\n\x0e\x62uildbucket_id\x18\x01 \x01(\x04\x12\x33\n\x0fstart_timestamp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12-\n\x0c\x62uild_target\x18\x03 \x01(\x0b\x32\x17.chromiumos.BuildTarget\x12\x35\n\nbuild_type\x18\x04 \x01(\x0e\x32!.chromiumos.BuilderConfig.Id.Type\x12\x19\n\x11\x62uild_config_name\x18\x05 \x01(\t\x12\x1b\n\x13\x61nnealing_commit_id\x18\x06 \x01(\r\x12\x17\n\x0fmanifest_commit\x18\x07 \x01(\t\"h\n\x10\x42uildVersionData\x12\x11\n\tmilestone\x18\x01 \x01(\r\x12\x41\n\x10platform_version\x18\x02 \x01(\x0b\x32\'.chromite.observability.PlatformVersion\"Z\n\x0fPlatformVersion\x12\x16\n\x0eplatform_build\x18\x01 \x01(\r\x12\x17\n\x0fplatform_branch\x18\x02 \x01(\r\x12\x16\n\x0eplatform_patch\x18\x03 \x01(\rBBZ@go.chromium.org/chromiumos/infra/proto/go/chromite/observabilityb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,chromiumos_dot_common__pb2.DESCRIPTOR,chromiumos_dot_builder__config__pb2.DESCRIPTOR,])




_BUILDERMETADATA = _descriptor.Descriptor(
  name='BuilderMetadata',
  full_name='chromite.observability.BuilderMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='buildbucket_id', full_name='chromite.observability.BuilderMetadata.buildbucket_id', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='start_timestamp', full_name='chromite.observability.BuilderMetadata.start_timestamp', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='build_target', full_name='chromite.observability.BuilderMetadata.build_target', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='build_type', full_name='chromite.observability.BuilderMetadata.build_type', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='build_config_name', full_name='chromite.observability.BuilderMetadata.build_config_name', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='annealing_commit_id', full_name='chromite.observability.BuilderMetadata.annealing_commit_id', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='manifest_commit', full_name='chromite.observability.BuilderMetadata.manifest_commit', index=6,
      number=7, type=9, cpp_type=9, label=1,
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
  serialized_start=155,
  serialized_end=432,
)


_BUILDVERSIONDATA = _descriptor.Descriptor(
  name='BuildVersionData',
  full_name='chromite.observability.BuildVersionData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='milestone', full_name='chromite.observability.BuildVersionData.milestone', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='platform_version', full_name='chromite.observability.BuildVersionData.platform_version', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  serialized_start=434,
  serialized_end=538,
)


_PLATFORMVERSION = _descriptor.Descriptor(
  name='PlatformVersion',
  full_name='chromite.observability.PlatformVersion',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='platform_build', full_name='chromite.observability.PlatformVersion.platform_build', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='platform_branch', full_name='chromite.observability.PlatformVersion.platform_branch', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='platform_patch', full_name='chromite.observability.PlatformVersion.platform_patch', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=540,
  serialized_end=630,
)

_BUILDERMETADATA.fields_by_name['start_timestamp'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_BUILDERMETADATA.fields_by_name['build_target'].message_type = chromiumos_dot_common__pb2._BUILDTARGET
_BUILDERMETADATA.fields_by_name['build_type'].enum_type = chromiumos_dot_builder__config__pb2._BUILDERCONFIG_ID_TYPE
_BUILDVERSIONDATA.fields_by_name['platform_version'].message_type = _PLATFORMVERSION
DESCRIPTOR.message_types_by_name['BuilderMetadata'] = _BUILDERMETADATA
DESCRIPTOR.message_types_by_name['BuildVersionData'] = _BUILDVERSIONDATA
DESCRIPTOR.message_types_by_name['PlatformVersion'] = _PLATFORMVERSION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BuilderMetadata = _reflection.GeneratedProtocolMessageType('BuilderMetadata', (_message.Message,), {
  'DESCRIPTOR' : _BUILDERMETADATA,
  '__module__' : 'chromite.observability.shared_pb2'
  # @@protoc_insertion_point(class_scope:chromite.observability.BuilderMetadata)
  })
_sym_db.RegisterMessage(BuilderMetadata)

BuildVersionData = _reflection.GeneratedProtocolMessageType('BuildVersionData', (_message.Message,), {
  'DESCRIPTOR' : _BUILDVERSIONDATA,
  '__module__' : 'chromite.observability.shared_pb2'
  # @@protoc_insertion_point(class_scope:chromite.observability.BuildVersionData)
  })
_sym_db.RegisterMessage(BuildVersionData)

PlatformVersion = _reflection.GeneratedProtocolMessageType('PlatformVersion', (_message.Message,), {
  'DESCRIPTOR' : _PLATFORMVERSION,
  '__module__' : 'chromite.observability.shared_pb2'
  # @@protoc_insertion_point(class_scope:chromite.observability.PlatformVersion)
  })
_sym_db.RegisterMessage(PlatformVersion)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
