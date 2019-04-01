# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/builder_config.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromiumos/builder_config.proto',
  package='chromiumos',
  syntax='proto3',
  serialized_options=_b('Z4go.chromium.org/chromiumos/infra/proto/go/chromiumos'),
  serialized_pb=_b('\n\x1f\x63hromiumos/builder_config.proto\x12\nchromiumos\x1a\x1egoogle/protobuf/wrappers.proto\"\xe5\x04\n\rBuilderConfig\x12(\n\x02id\x18\x01 \x01(\x0b\x32\x1c.chromiumos.BuilderConfig.Id\x12\x32\n\x07general\x18\x02 \x01(\x0b\x32!.chromiumos.BuilderConfig.General\x12<\n\x0corchestrator\x18\x03 \x01(\x0b\x32&.chromiumos.BuilderConfig.Orchestrator\x12\x36\n\tartifacts\x18\x04 \x01(\x0b\x32#.chromiumos.BuilderConfig.Artifacts\x1a\x89\x01\n\x02Id\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06\x62ranch\x18\x02 \x01(\t\x12/\n\x04type\x18\x03 \x01(\x0e\x32!.chromiumos.BuilderConfig.Id.Type\"4\n\x04Type\x12\x14\n\x10TYPE_UNSPECIFIED\x10\x00\x12\x06\n\x02\x43Q\x10\x01\x12\x0e\n\nPOSTSUBMIT\x10\x02\x1a\x37\n\x07General\x12,\n\x08\x63ritical\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x1a \n\x0cOrchestrator\x12\x10\n\x08\x63hildren\x18\x01 \x03(\t\x1a\x98\x01\n\tArtifacts\x12@\n\tprebuilts\x18\x01 \x01(\x0e\x32-.chromiumos.BuilderConfig.Artifacts.Prebuilts\"I\n\tPrebuilts\x12\x19\n\x15PREBUILTS_UNSPECIFIED\x10\x00\x12\n\n\x06PUBLIC\x10\x01\x12\x0b\n\x07PRIVATE\x10\x02\x12\x08\n\x04NONE\x10\x03\"D\n\x0e\x42uilderConfigs\x12\x32\n\x0f\x62uilder_configs\x18\x01 \x03(\x0b\x32\x19.chromiumos.BuilderConfigB6Z4go.chromium.org/chromiumos/infra/proto/go/chromiumosb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,])



_BUILDERCONFIG_ID_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='chromiumos.BuilderConfig.Id.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='TYPE_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CQ', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='POSTSUBMIT', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=395,
  serialized_end=447,
)
_sym_db.RegisterEnumDescriptor(_BUILDERCONFIG_ID_TYPE)

_BUILDERCONFIG_ARTIFACTS_PREBUILTS = _descriptor.EnumDescriptor(
  name='Prebuilts',
  full_name='chromiumos.BuilderConfig.Artifacts.Prebuilts',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='PREBUILTS_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PUBLIC', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PRIVATE', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NONE', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=620,
  serialized_end=693,
)
_sym_db.RegisterEnumDescriptor(_BUILDERCONFIG_ARTIFACTS_PREBUILTS)


_BUILDERCONFIG_ID = _descriptor.Descriptor(
  name='Id',
  full_name='chromiumos.BuilderConfig.Id',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='chromiumos.BuilderConfig.Id.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='branch', full_name='chromiumos.BuilderConfig.Id.branch', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='chromiumos.BuilderConfig.Id.type', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _BUILDERCONFIG_ID_TYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=310,
  serialized_end=447,
)

_BUILDERCONFIG_GENERAL = _descriptor.Descriptor(
  name='General',
  full_name='chromiumos.BuilderConfig.General',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='critical', full_name='chromiumos.BuilderConfig.General.critical', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=449,
  serialized_end=504,
)

_BUILDERCONFIG_ORCHESTRATOR = _descriptor.Descriptor(
  name='Orchestrator',
  full_name='chromiumos.BuilderConfig.Orchestrator',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='children', full_name='chromiumos.BuilderConfig.Orchestrator.children', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=506,
  serialized_end=538,
)

_BUILDERCONFIG_ARTIFACTS = _descriptor.Descriptor(
  name='Artifacts',
  full_name='chromiumos.BuilderConfig.Artifacts',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='prebuilts', full_name='chromiumos.BuilderConfig.Artifacts.prebuilts', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _BUILDERCONFIG_ARTIFACTS_PREBUILTS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=541,
  serialized_end=693,
)

_BUILDERCONFIG = _descriptor.Descriptor(
  name='BuilderConfig',
  full_name='chromiumos.BuilderConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='chromiumos.BuilderConfig.id', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='general', full_name='chromiumos.BuilderConfig.general', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='orchestrator', full_name='chromiumos.BuilderConfig.orchestrator', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='artifacts', full_name='chromiumos.BuilderConfig.artifacts', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_BUILDERCONFIG_ID, _BUILDERCONFIG_GENERAL, _BUILDERCONFIG_ORCHESTRATOR, _BUILDERCONFIG_ARTIFACTS, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=80,
  serialized_end=693,
)


_BUILDERCONFIGS = _descriptor.Descriptor(
  name='BuilderConfigs',
  full_name='chromiumos.BuilderConfigs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='builder_configs', full_name='chromiumos.BuilderConfigs.builder_configs', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=695,
  serialized_end=763,
)

_BUILDERCONFIG_ID.fields_by_name['type'].enum_type = _BUILDERCONFIG_ID_TYPE
_BUILDERCONFIG_ID.containing_type = _BUILDERCONFIG
_BUILDERCONFIG_ID_TYPE.containing_type = _BUILDERCONFIG_ID
_BUILDERCONFIG_GENERAL.fields_by_name['critical'].message_type = google_dot_protobuf_dot_wrappers__pb2._BOOLVALUE
_BUILDERCONFIG_GENERAL.containing_type = _BUILDERCONFIG
_BUILDERCONFIG_ORCHESTRATOR.containing_type = _BUILDERCONFIG
_BUILDERCONFIG_ARTIFACTS.fields_by_name['prebuilts'].enum_type = _BUILDERCONFIG_ARTIFACTS_PREBUILTS
_BUILDERCONFIG_ARTIFACTS.containing_type = _BUILDERCONFIG
_BUILDERCONFIG_ARTIFACTS_PREBUILTS.containing_type = _BUILDERCONFIG_ARTIFACTS
_BUILDERCONFIG.fields_by_name['id'].message_type = _BUILDERCONFIG_ID
_BUILDERCONFIG.fields_by_name['general'].message_type = _BUILDERCONFIG_GENERAL
_BUILDERCONFIG.fields_by_name['orchestrator'].message_type = _BUILDERCONFIG_ORCHESTRATOR
_BUILDERCONFIG.fields_by_name['artifacts'].message_type = _BUILDERCONFIG_ARTIFACTS
_BUILDERCONFIGS.fields_by_name['builder_configs'].message_type = _BUILDERCONFIG
DESCRIPTOR.message_types_by_name['BuilderConfig'] = _BUILDERCONFIG
DESCRIPTOR.message_types_by_name['BuilderConfigs'] = _BUILDERCONFIGS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BuilderConfig = _reflection.GeneratedProtocolMessageType('BuilderConfig', (_message.Message,), dict(

  Id = _reflection.GeneratedProtocolMessageType('Id', (_message.Message,), dict(
    DESCRIPTOR = _BUILDERCONFIG_ID,
    __module__ = 'chromiumos.builder_config_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.BuilderConfig.Id)
    ))
  ,

  General = _reflection.GeneratedProtocolMessageType('General', (_message.Message,), dict(
    DESCRIPTOR = _BUILDERCONFIG_GENERAL,
    __module__ = 'chromiumos.builder_config_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.BuilderConfig.General)
    ))
  ,

  Orchestrator = _reflection.GeneratedProtocolMessageType('Orchestrator', (_message.Message,), dict(
    DESCRIPTOR = _BUILDERCONFIG_ORCHESTRATOR,
    __module__ = 'chromiumos.builder_config_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.BuilderConfig.Orchestrator)
    ))
  ,

  Artifacts = _reflection.GeneratedProtocolMessageType('Artifacts', (_message.Message,), dict(
    DESCRIPTOR = _BUILDERCONFIG_ARTIFACTS,
    __module__ = 'chromiumos.builder_config_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.BuilderConfig.Artifacts)
    ))
  ,
  DESCRIPTOR = _BUILDERCONFIG,
  __module__ = 'chromiumos.builder_config_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.BuilderConfig)
  ))
_sym_db.RegisterMessage(BuilderConfig)
_sym_db.RegisterMessage(BuilderConfig.Id)
_sym_db.RegisterMessage(BuilderConfig.General)
_sym_db.RegisterMessage(BuilderConfig.Orchestrator)
_sym_db.RegisterMessage(BuilderConfig.Artifacts)

BuilderConfigs = _reflection.GeneratedProtocolMessageType('BuilderConfigs', (_message.Message,), dict(
  DESCRIPTOR = _BUILDERCONFIGS,
  __module__ = 'chromiumos.builder_config_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.BuilderConfigs)
  ))
_sym_db.RegisterMessage(BuilderConfigs)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
