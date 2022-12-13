# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/generate_build_plan.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import message as _message
from chromite.third_party.google.protobuf import reflection as _reflection
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.chromiumos import builder_config_pb2 as chromiumos_dot_builder__config__pb2
from chromite.api.gen.chromiumos import common_pb2 as chromiumos_dot_common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromiumos/generate_build_plan.proto',
  package='chromiumos',
  syntax='proto3',
  serialized_options=b'\n!com.google.chrome.crosinfra.protoZ4go.chromium.org/chromiumos/infra/proto/go/chromiumos',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n$chromiumos/generate_build_plan.proto\x12\nchromiumos\x1a\x1f\x63hromiumos/builder_config.proto\x1a\x17\x63hromiumos/common.proto\"\xa4\x02\n\x18GenerateBuildPlanRequest\x12\x41\n\x0e\x61\x66\x66\x65\x63ted_paths\x18\x05 \x03(\x0b\x32).chromiumos.GenerateBuildPlanRequest.Path\x12.\n\x0egerrit_changes\x18\x01 \x03(\x0b\x32\x16.chromiumos.ProtoBytes\x12.\n\x0egitiles_commit\x18\x04 \x01(\x0b\x32\x16.chromiumos.ProtoBytes\x12\x1b\n\x0fmanifest_commit\x18\x02 \x01(\tB\x02\x18\x01\x12\x32\n\x0f\x62uilder_configs\x18\x03 \x03(\x0b\x32\x19.chromiumos.BuilderConfig\x1a\x14\n\x04Path\x12\x0c\n\x04path\x18\x01 \x01(\t\"\xd8\x01\n\x19GenerateBuildPlanResponse\x12\x33\n\rbuilds_to_run\x18\x01 \x03(\x0b\x32\x1c.chromiumos.BuilderConfig.Id\x12G\n!skip_for_global_build_irrelevance\x18\x02 \x03(\x0b\x32\x1c.chromiumos.BuilderConfig.Id\x12=\n\x17skip_for_run_when_rules\x18\x03 \x03(\x0b\x32\x1c.chromiumos.BuilderConfig.IdBY\n!com.google.chrome.crosinfra.protoZ4go.chromium.org/chromiumos/infra/proto/go/chromiumosb\x06proto3'
  ,
  dependencies=[chromiumos_dot_builder__config__pb2.DESCRIPTOR,chromiumos_dot_common__pb2.DESCRIPTOR,])




_GENERATEBUILDPLANREQUEST_PATH = _descriptor.Descriptor(
  name='Path',
  full_name='chromiumos.GenerateBuildPlanRequest.Path',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='chromiumos.GenerateBuildPlanRequest.Path.path', index=0,
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
  serialized_start=383,
  serialized_end=403,
)

_GENERATEBUILDPLANREQUEST = _descriptor.Descriptor(
  name='GenerateBuildPlanRequest',
  full_name='chromiumos.GenerateBuildPlanRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='affected_paths', full_name='chromiumos.GenerateBuildPlanRequest.affected_paths', index=0,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='gerrit_changes', full_name='chromiumos.GenerateBuildPlanRequest.gerrit_changes', index=1,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='gitiles_commit', full_name='chromiumos.GenerateBuildPlanRequest.gitiles_commit', index=2,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='manifest_commit', full_name='chromiumos.GenerateBuildPlanRequest.manifest_commit', index=3,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='builder_configs', full_name='chromiumos.GenerateBuildPlanRequest.builder_configs', index=4,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_GENERATEBUILDPLANREQUEST_PATH, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=111,
  serialized_end=403,
)


_GENERATEBUILDPLANRESPONSE = _descriptor.Descriptor(
  name='GenerateBuildPlanResponse',
  full_name='chromiumos.GenerateBuildPlanResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='builds_to_run', full_name='chromiumos.GenerateBuildPlanResponse.builds_to_run', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='skip_for_global_build_irrelevance', full_name='chromiumos.GenerateBuildPlanResponse.skip_for_global_build_irrelevance', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='skip_for_run_when_rules', full_name='chromiumos.GenerateBuildPlanResponse.skip_for_run_when_rules', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=406,
  serialized_end=622,
)

_GENERATEBUILDPLANREQUEST_PATH.containing_type = _GENERATEBUILDPLANREQUEST
_GENERATEBUILDPLANREQUEST.fields_by_name['affected_paths'].message_type = _GENERATEBUILDPLANREQUEST_PATH
_GENERATEBUILDPLANREQUEST.fields_by_name['gerrit_changes'].message_type = chromiumos_dot_common__pb2._PROTOBYTES
_GENERATEBUILDPLANREQUEST.fields_by_name['gitiles_commit'].message_type = chromiumos_dot_common__pb2._PROTOBYTES
_GENERATEBUILDPLANREQUEST.fields_by_name['builder_configs'].message_type = chromiumos_dot_builder__config__pb2._BUILDERCONFIG
_GENERATEBUILDPLANRESPONSE.fields_by_name['builds_to_run'].message_type = chromiumos_dot_builder__config__pb2._BUILDERCONFIG_ID
_GENERATEBUILDPLANRESPONSE.fields_by_name['skip_for_global_build_irrelevance'].message_type = chromiumos_dot_builder__config__pb2._BUILDERCONFIG_ID
_GENERATEBUILDPLANRESPONSE.fields_by_name['skip_for_run_when_rules'].message_type = chromiumos_dot_builder__config__pb2._BUILDERCONFIG_ID
DESCRIPTOR.message_types_by_name['GenerateBuildPlanRequest'] = _GENERATEBUILDPLANREQUEST
DESCRIPTOR.message_types_by_name['GenerateBuildPlanResponse'] = _GENERATEBUILDPLANRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GenerateBuildPlanRequest = _reflection.GeneratedProtocolMessageType('GenerateBuildPlanRequest', (_message.Message,), {

  'Path' : _reflection.GeneratedProtocolMessageType('Path', (_message.Message,), {
    'DESCRIPTOR' : _GENERATEBUILDPLANREQUEST_PATH,
    '__module__' : 'chromiumos.generate_build_plan_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.GenerateBuildPlanRequest.Path)
    })
  ,
  'DESCRIPTOR' : _GENERATEBUILDPLANREQUEST,
  '__module__' : 'chromiumos.generate_build_plan_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.GenerateBuildPlanRequest)
  })
_sym_db.RegisterMessage(GenerateBuildPlanRequest)
_sym_db.RegisterMessage(GenerateBuildPlanRequest.Path)

GenerateBuildPlanResponse = _reflection.GeneratedProtocolMessageType('GenerateBuildPlanResponse', (_message.Message,), {
  'DESCRIPTOR' : _GENERATEBUILDPLANRESPONSE,
  '__module__' : 'chromiumos.generate_build_plan_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.GenerateBuildPlanResponse)
  })
_sym_db.RegisterMessage(GenerateBuildPlanResponse)


DESCRIPTOR._options = None
_GENERATEBUILDPLANREQUEST.fields_by_name['manifest_commit']._options = None
# @@protoc_insertion_point(module_scope)
