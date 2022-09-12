# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/chromiumdash.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import message as _message
from chromite.third_party.google.protobuf import reflection as _reflection
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.third_party.google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromiumos/chromiumdash.proto',
  package='chromiumos',
  syntax='proto3',
  serialized_options=b'\n!com.google.chrome.crosinfra.protoZ4go.chromium.org/chromiumos/infra/proto/go/chromiumos',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1d\x63hromiumos/chromiumdash.proto\x12\nchromiumos\x1a\x1fgoogle/protobuf/timestamp.proto\"\x9e\x08\n\tMilestone\x12\x32\n\x0e\x66inal_beta_cut\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nfinal_beta\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x32\n\x0e\x66\x65\x61ture_freeze\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x31\n\rearliest_beta\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x38\n\x14stable_refresh_first\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x0blatest_beta\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x31\n\x06owners\x18\x07 \x03(\x0b\x32!.chromiumos.Milestone.OwnersEntry\x12.\n\nstable_cut\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x39\n\x15stable_refresh_second\x18\t \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0e\n\x06mstone\x18\n \x01(\x05\x12\x34\n\x10late_stable_date\x18\x0b \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x0bstable_date\x18\x0c \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x05ldaps\x18\r \x03(\x0b\x32 .chromiumos.Milestone.LdapsEntry\x12\x35\n\x11\x65\x61rliest_beta_ios\x18\x0e \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x30\n\x0c\x62ranch_point\x18\x0f \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x38\n\x14stable_refresh_third\x18\x10 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12,\n\x08ltc_date\x18\x11 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12,\n\x08ltr_date\x18\x12 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x39\n\x15ltr_last_refresh_date\x18\x13 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x1a-\n\x0bOwnersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a,\n\nLdapsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"H\n\x1e\x46\x65tchMilestoneScheduleResponse\x12&\n\x07mstones\x18\x01 \x03(\x0b\x32\x15.chromiumos.MilestoneBY\n!com.google.chrome.crosinfra.protoZ4go.chromium.org/chromiumos/infra/proto/go/chromiumosb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])




_MILESTONE_OWNERSENTRY = _descriptor.Descriptor(
  name='OwnersEntry',
  full_name='chromiumos.Milestone.OwnersEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='chromiumos.Milestone.OwnersEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='chromiumos.Milestone.OwnersEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1042,
  serialized_end=1087,
)

_MILESTONE_LDAPSENTRY = _descriptor.Descriptor(
  name='LdapsEntry',
  full_name='chromiumos.Milestone.LdapsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='chromiumos.Milestone.LdapsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='chromiumos.Milestone.LdapsEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1089,
  serialized_end=1133,
)

_MILESTONE = _descriptor.Descriptor(
  name='Milestone',
  full_name='chromiumos.Milestone',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='final_beta_cut', full_name='chromiumos.Milestone.final_beta_cut', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='final_beta', full_name='chromiumos.Milestone.final_beta', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='feature_freeze', full_name='chromiumos.Milestone.feature_freeze', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='earliest_beta', full_name='chromiumos.Milestone.earliest_beta', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stable_refresh_first', full_name='chromiumos.Milestone.stable_refresh_first', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='latest_beta', full_name='chromiumos.Milestone.latest_beta', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='owners', full_name='chromiumos.Milestone.owners', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stable_cut', full_name='chromiumos.Milestone.stable_cut', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stable_refresh_second', full_name='chromiumos.Milestone.stable_refresh_second', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mstone', full_name='chromiumos.Milestone.mstone', index=9,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='late_stable_date', full_name='chromiumos.Milestone.late_stable_date', index=10,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stable_date', full_name='chromiumos.Milestone.stable_date', index=11,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ldaps', full_name='chromiumos.Milestone.ldaps', index=12,
      number=13, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='earliest_beta_ios', full_name='chromiumos.Milestone.earliest_beta_ios', index=13,
      number=14, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='branch_point', full_name='chromiumos.Milestone.branch_point', index=14,
      number=15, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stable_refresh_third', full_name='chromiumos.Milestone.stable_refresh_third', index=15,
      number=16, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ltc_date', full_name='chromiumos.Milestone.ltc_date', index=16,
      number=17, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ltr_date', full_name='chromiumos.Milestone.ltr_date', index=17,
      number=18, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ltr_last_refresh_date', full_name='chromiumos.Milestone.ltr_last_refresh_date', index=18,
      number=19, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_MILESTONE_OWNERSENTRY, _MILESTONE_LDAPSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=79,
  serialized_end=1133,
)


_FETCHMILESTONESCHEDULERESPONSE = _descriptor.Descriptor(
  name='FetchMilestoneScheduleResponse',
  full_name='chromiumos.FetchMilestoneScheduleResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='mstones', full_name='chromiumos.FetchMilestoneScheduleResponse.mstones', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=1135,
  serialized_end=1207,
)

_MILESTONE_OWNERSENTRY.containing_type = _MILESTONE
_MILESTONE_LDAPSENTRY.containing_type = _MILESTONE
_MILESTONE.fields_by_name['final_beta_cut'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_MILESTONE.fields_by_name['final_beta'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_MILESTONE.fields_by_name['feature_freeze'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_MILESTONE.fields_by_name['earliest_beta'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_MILESTONE.fields_by_name['stable_refresh_first'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_MILESTONE.fields_by_name['latest_beta'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_MILESTONE.fields_by_name['owners'].message_type = _MILESTONE_OWNERSENTRY
_MILESTONE.fields_by_name['stable_cut'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_MILESTONE.fields_by_name['stable_refresh_second'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_MILESTONE.fields_by_name['late_stable_date'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_MILESTONE.fields_by_name['stable_date'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_MILESTONE.fields_by_name['ldaps'].message_type = _MILESTONE_LDAPSENTRY
_MILESTONE.fields_by_name['earliest_beta_ios'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_MILESTONE.fields_by_name['branch_point'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_MILESTONE.fields_by_name['stable_refresh_third'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_MILESTONE.fields_by_name['ltc_date'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_MILESTONE.fields_by_name['ltr_date'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_MILESTONE.fields_by_name['ltr_last_refresh_date'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_FETCHMILESTONESCHEDULERESPONSE.fields_by_name['mstones'].message_type = _MILESTONE
DESCRIPTOR.message_types_by_name['Milestone'] = _MILESTONE
DESCRIPTOR.message_types_by_name['FetchMilestoneScheduleResponse'] = _FETCHMILESTONESCHEDULERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Milestone = _reflection.GeneratedProtocolMessageType('Milestone', (_message.Message,), {

  'OwnersEntry' : _reflection.GeneratedProtocolMessageType('OwnersEntry', (_message.Message,), {
    'DESCRIPTOR' : _MILESTONE_OWNERSENTRY,
    '__module__' : 'chromiumos.chromiumdash_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.Milestone.OwnersEntry)
    })
  ,

  'LdapsEntry' : _reflection.GeneratedProtocolMessageType('LdapsEntry', (_message.Message,), {
    'DESCRIPTOR' : _MILESTONE_LDAPSENTRY,
    '__module__' : 'chromiumos.chromiumdash_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.Milestone.LdapsEntry)
    })
  ,
  'DESCRIPTOR' : _MILESTONE,
  '__module__' : 'chromiumos.chromiumdash_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.Milestone)
  })
_sym_db.RegisterMessage(Milestone)
_sym_db.RegisterMessage(Milestone.OwnersEntry)
_sym_db.RegisterMessage(Milestone.LdapsEntry)

FetchMilestoneScheduleResponse = _reflection.GeneratedProtocolMessageType('FetchMilestoneScheduleResponse', (_message.Message,), {
  'DESCRIPTOR' : _FETCHMILESTONESCHEDULERESPONSE,
  '__module__' : 'chromiumos.chromiumdash_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.FetchMilestoneScheduleResponse)
  })
_sym_db.RegisterMessage(FetchMilestoneScheduleResponse)


DESCRIPTOR._options = None
_MILESTONE_OWNERSENTRY._options = None
_MILESTONE_LDAPSENTRY._options = None
# @@protoc_insertion_point(module_scope)
