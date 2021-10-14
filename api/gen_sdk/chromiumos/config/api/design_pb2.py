# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/config/api/design.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen_sdk.chromiumos.config.api import design_config_id_pb2 as chromiumos_dot_config_dot_api_dot_design__config__id__pb2
from chromite.api.gen_sdk.chromiumos.config.api import design_id_pb2 as chromiumos_dot_config_dot_api_dot_design__id__pb2
from chromite.api.gen_sdk.chromiumos.config.api import hardware_topology_pb2 as chromiumos_dot_config_dot_api_dot_hardware__topology__pb2
from chromite.api.gen_sdk.chromiumos.config.api import partner_id_pb2 as chromiumos_dot_config_dot_api_dot_partner__id__pb2
from chromite.api.gen_sdk.chromiumos.config.api import program_id_pb2 as chromiumos_dot_config_dot_api_dot_program__id__pb2
from chromite.api.gen_sdk.chromiumos.config.api import topology_pb2 as chromiumos_dot_config_dot_api_dot_topology__pb2
from chromite.api.gen_sdk.chromiumos.config.public_replication import public_replication_pb2 as chromiumos_dot_config_dot_public__replication_dot_public__replication__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromiumos/config/api/design.proto',
  package='chromiumos.config.api',
  syntax='proto3',
  serialized_options=b'Z(go.chromium.org/chromiumos/config/go/api',
  serialized_pb=b'\n\"chromiumos/config/api/design.proto\x12\x15\x63hromiumos.config.api\x1a,chromiumos/config/api/design_config_id.proto\x1a%chromiumos/config/api/design_id.proto\x1a-chromiumos/config/api/hardware_topology.proto\x1a&chromiumos/config/api/partner_id.proto\x1a&chromiumos/config/api/program_id.proto\x1a$chromiumos/config/api/topology.proto\x1a=chromiumos/config/public_replication/public_replication.proto\"\xb6\x08\n\x06\x44\x65sign\x12S\n\x12public_replication\x18\x07 \x01(\x0b\x32\x37.chromiumos.config.public_replication.PublicReplication\x12+\n\x02id\x18\x01 \x01(\x0b\x32\x1f.chromiumos.config.api.DesignId\x12\x34\n\nprogram_id\x18\x02 \x01(\x0b\x32 .chromiumos.config.api.ProgramId\x12\x30\n\x06odm_id\x18\x03 \x01(\x0b\x32 .chromiumos.config.api.PartnerId\x12\x0c\n\x04name\x18\x04 \x01(\t\x12G\n\x0e\x62oard_id_phase\x18\x05 \x03(\x0b\x32/.chromiumos.config.api.Design.BoardIdPhaseEntry\x12\x35\n\x07\x63onfigs\x18\x06 \x03(\x0b\x32$.chromiumos.config.api.Design.Config\x12@\n\nssfc_value\x18\x08 \x03(\x0b\x32,.chromiumos.config.api.Design.SsfcValueEntry\x1a\x33\n\x11\x42oardIdPhaseEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x30\n\x0eSsfcValueEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\xfa\x03\n\x06\x43onfig\x12S\n\x12public_replication\x18\x05 \x01(\x0b\x32\x37.chromiumos.config.public_replication.PublicReplication\x12\x31\n\x02id\x18\x01 \x01(\x0b\x32%.chromiumos.config.api.DesignConfigId\x12\x42\n\x11hardware_topology\x18\x02 \x01(\x0b\x32\'.chromiumos.config.api.HardwareTopology\x12\x42\n\x11hardware_features\x18\x03 \x01(\x0b\x32\'.chromiumos.config.api.HardwareFeatures\x1a\xd3\x01\n\nConstraint\x12\x44\n\x05level\x18\x01 \x01(\x0e\x32\x35.chromiumos.config.api.Design.Config.Constraint.Level\x12\x39\n\x08\x66\x65\x61tures\x18\x02 \x01(\x0b\x32\'.chromiumos.config.api.HardwareFeatures\"D\n\x05Level\x12\x10\n\x0cTYPE_UNKNOWN\x10\x00\x12\x0c\n\x08REQUIRED\x10\x01\x12\r\n\tPREFERRED\x10\x02\x12\x0c\n\x08OPTIONAL\x10\x03J\x04\x08\x04\x10\x05J\x04\x08\x07\x10\x08J\x04\x08\t\x10\nR\x08platformB*Z(go.chromium.org/chromiumos/config/go/apib\x06proto3'
  ,
  dependencies=[chromiumos_dot_config_dot_api_dot_design__config__id__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_design__id__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_hardware__topology__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_partner__id__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_program__id__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_topology__pb2.DESCRIPTOR,chromiumos_dot_config_dot_public__replication_dot_public__replication__pb2.DESCRIPTOR,])



_DESIGN_CONFIG_CONSTRAINT_LEVEL = _descriptor.EnumDescriptor(
  name='Level',
  full_name='chromiumos.config.api.Design.Config.Constraint.Level',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='TYPE_UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REQUIRED', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PREFERRED', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OPTIONAL', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1357,
  serialized_end=1425,
)
_sym_db.RegisterEnumDescriptor(_DESIGN_CONFIG_CONSTRAINT_LEVEL)


_DESIGN_BOARDIDPHASEENTRY = _descriptor.Descriptor(
  name='BoardIdPhaseEntry',
  full_name='chromiumos.config.api.Design.BoardIdPhaseEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='chromiumos.config.api.Design.BoardIdPhaseEntry.key', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='chromiumos.config.api.Design.BoardIdPhaseEntry.value', index=1,
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
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=827,
  serialized_end=878,
)

_DESIGN_SSFCVALUEENTRY = _descriptor.Descriptor(
  name='SsfcValueEntry',
  full_name='chromiumos.config.api.Design.SsfcValueEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='chromiumos.config.api.Design.SsfcValueEntry.key', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='chromiumos.config.api.Design.SsfcValueEntry.value', index=1,
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
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=880,
  serialized_end=928,
)

_DESIGN_CONFIG_CONSTRAINT = _descriptor.Descriptor(
  name='Constraint',
  full_name='chromiumos.config.api.Design.Config.Constraint',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='level', full_name='chromiumos.config.api.Design.Config.Constraint.level', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='features', full_name='chromiumos.config.api.Design.Config.Constraint.features', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _DESIGN_CONFIG_CONSTRAINT_LEVEL,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1214,
  serialized_end=1425,
)

_DESIGN_CONFIG = _descriptor.Descriptor(
  name='Config',
  full_name='chromiumos.config.api.Design.Config',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='public_replication', full_name='chromiumos.config.api.Design.Config.public_replication', index=0,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='chromiumos.config.api.Design.Config.id', index=1,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hardware_topology', full_name='chromiumos.config.api.Design.Config.hardware_topology', index=2,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hardware_features', full_name='chromiumos.config.api.Design.Config.hardware_features', index=3,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_DESIGN_CONFIG_CONSTRAINT, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=931,
  serialized_end=1437,
)

_DESIGN = _descriptor.Descriptor(
  name='Design',
  full_name='chromiumos.config.api.Design',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='public_replication', full_name='chromiumos.config.api.Design.public_replication', index=0,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='chromiumos.config.api.Design.id', index=1,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='program_id', full_name='chromiumos.config.api.Design.program_id', index=2,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='odm_id', full_name='chromiumos.config.api.Design.odm_id', index=3,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='chromiumos.config.api.Design.name', index=4,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='board_id_phase', full_name='chromiumos.config.api.Design.board_id_phase', index=5,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='configs', full_name='chromiumos.config.api.Design.configs', index=6,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ssfc_value', full_name='chromiumos.config.api.Design.ssfc_value', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_DESIGN_BOARDIDPHASEENTRY, _DESIGN_SSFCVALUEENTRY, _DESIGN_CONFIG, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=375,
  serialized_end=1453,
)

_DESIGN_BOARDIDPHASEENTRY.containing_type = _DESIGN
_DESIGN_SSFCVALUEENTRY.containing_type = _DESIGN
_DESIGN_CONFIG_CONSTRAINT.fields_by_name['level'].enum_type = _DESIGN_CONFIG_CONSTRAINT_LEVEL
_DESIGN_CONFIG_CONSTRAINT.fields_by_name['features'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._HARDWAREFEATURES
_DESIGN_CONFIG_CONSTRAINT.containing_type = _DESIGN_CONFIG
_DESIGN_CONFIG_CONSTRAINT_LEVEL.containing_type = _DESIGN_CONFIG_CONSTRAINT
_DESIGN_CONFIG.fields_by_name['public_replication'].message_type = chromiumos_dot_config_dot_public__replication_dot_public__replication__pb2._PUBLICREPLICATION
_DESIGN_CONFIG.fields_by_name['id'].message_type = chromiumos_dot_config_dot_api_dot_design__config__id__pb2._DESIGNCONFIGID
_DESIGN_CONFIG.fields_by_name['hardware_topology'].message_type = chromiumos_dot_config_dot_api_dot_hardware__topology__pb2._HARDWARETOPOLOGY
_DESIGN_CONFIG.fields_by_name['hardware_features'].message_type = chromiumos_dot_config_dot_api_dot_topology__pb2._HARDWAREFEATURES
_DESIGN_CONFIG.containing_type = _DESIGN
_DESIGN.fields_by_name['public_replication'].message_type = chromiumos_dot_config_dot_public__replication_dot_public__replication__pb2._PUBLICREPLICATION
_DESIGN.fields_by_name['id'].message_type = chromiumos_dot_config_dot_api_dot_design__id__pb2._DESIGNID
_DESIGN.fields_by_name['program_id'].message_type = chromiumos_dot_config_dot_api_dot_program__id__pb2._PROGRAMID
_DESIGN.fields_by_name['odm_id'].message_type = chromiumos_dot_config_dot_api_dot_partner__id__pb2._PARTNERID
_DESIGN.fields_by_name['board_id_phase'].message_type = _DESIGN_BOARDIDPHASEENTRY
_DESIGN.fields_by_name['configs'].message_type = _DESIGN_CONFIG
_DESIGN.fields_by_name['ssfc_value'].message_type = _DESIGN_SSFCVALUEENTRY
DESCRIPTOR.message_types_by_name['Design'] = _DESIGN
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Design = _reflection.GeneratedProtocolMessageType('Design', (_message.Message,), {

  'BoardIdPhaseEntry' : _reflection.GeneratedProtocolMessageType('BoardIdPhaseEntry', (_message.Message,), {
    'DESCRIPTOR' : _DESIGN_BOARDIDPHASEENTRY,
    '__module__' : 'chromiumos.config.api.design_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.config.api.Design.BoardIdPhaseEntry)
    })
  ,

  'SsfcValueEntry' : _reflection.GeneratedProtocolMessageType('SsfcValueEntry', (_message.Message,), {
    'DESCRIPTOR' : _DESIGN_SSFCVALUEENTRY,
    '__module__' : 'chromiumos.config.api.design_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.config.api.Design.SsfcValueEntry)
    })
  ,

  'Config' : _reflection.GeneratedProtocolMessageType('Config', (_message.Message,), {

    'Constraint' : _reflection.GeneratedProtocolMessageType('Constraint', (_message.Message,), {
      'DESCRIPTOR' : _DESIGN_CONFIG_CONSTRAINT,
      '__module__' : 'chromiumos.config.api.design_pb2'
      # @@protoc_insertion_point(class_scope:chromiumos.config.api.Design.Config.Constraint)
      })
    ,
    'DESCRIPTOR' : _DESIGN_CONFIG,
    '__module__' : 'chromiumos.config.api.design_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.config.api.Design.Config)
    })
  ,
  'DESCRIPTOR' : _DESIGN,
  '__module__' : 'chromiumos.config.api.design_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.Design)
  })
_sym_db.RegisterMessage(Design)
_sym_db.RegisterMessage(Design.BoardIdPhaseEntry)
_sym_db.RegisterMessage(Design.SsfcValueEntry)
_sym_db.RegisterMessage(Design.Config)
_sym_db.RegisterMessage(Design.Config.Constraint)


DESCRIPTOR._options = None
_DESIGN_BOARDIDPHASEENTRY._options = None
_DESIGN_SSFCVALUEENTRY._options = None
# @@protoc_insertion_point(module_scope)
