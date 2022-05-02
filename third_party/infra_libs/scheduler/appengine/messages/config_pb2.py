# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: go.chromium.org/luci/scheduler/appengine/messages/config.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import message as _message
from chromite.third_party.google.protobuf import reflection as _reflection
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.third_party.infra_libs.common.proto import options_pb2 as go_dot_chromium_dot_org_dot_luci_dot_common_dot_proto_dot_options__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='go.chromium.org/luci/scheduler/appengine/messages/config.proto',
  package='scheduler.config',
  syntax='proto3',
  serialized_options=b'Z1go.chromium.org/luci/scheduler/appengine/messages\242\376#E\nChttps://luci-config.appspot.com/schemas/projects:luci-scheduler.cfg',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n>go.chromium.org/luci/scheduler/appengine/messages/config.proto\x12\x10scheduler.config\x1a/go.chromium.org/luci/common/proto/options.proto\"\xa7\x01\n\rProjectConfig\x12\"\n\x03job\x18\x01 \x03(\x0b\x32\x15.scheduler.config.Job\x12*\n\x07trigger\x18\x02 \x03(\x0b\x32\x19.scheduler.config.Trigger\x12.\n\x08\x61\x63l_sets\x18\x03 \x03(\x0b\x32\x18.scheduler.config.AclSetB\x02\x18\x01J\x04\x08\x04\x10\x05R\x10security_options\"q\n\x03\x41\x63l\x12(\n\x04role\x18\x01 \x01(\x0e\x32\x1a.scheduler.config.Acl.Role\x12\x12\n\ngranted_to\x18\x02 \x01(\t\",\n\x04Role\x12\n\n\x06READER\x10\x00\x12\r\n\tTRIGGERER\x10\x02\x12\t\n\x05OWNER\x10\x01\";\n\x06\x41\x63lSet\x12\x0c\n\x04name\x18\x01 \x01(\t\x12#\n\x04\x61\x63ls\x18\x02 \x03(\x0b\x32\x15.scheduler.config.Acl\"\xdd\x01\n\x10TriggeringPolicy\x12\x35\n\x04kind\x18\x01 \x01(\x0e\x32\'.scheduler.config.TriggeringPolicy.Kind\x12\"\n\x1amax_concurrent_invocations\x18\x02 \x01(\x03\x12\x16\n\x0emax_batch_size\x18\x03 \x01(\x03\x12\x10\n\x08log_base\x18\x04 \x01(\x02\"D\n\x04Kind\x12\r\n\tUNDEFINED\x10\x00\x12\x13\n\x0fGREEDY_BATCHING\x10\x01\x12\x18\n\x14LOGARITHMIC_BATCHING\x10\x02\"\xe3\x02\n\x03Job\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05realm\x18\x08 \x01(\t\x12\x10\n\x08schedule\x18\x02 \x01(\t\x12\x10\n\x08\x64isabled\x18\x03 \x01(\x08\x12\'\n\x04\x61\x63ls\x18\x05 \x03(\x0b\x32\x15.scheduler.config.AclB\x02\x18\x01\x12\x14\n\x08\x61\x63l_sets\x18\x06 \x03(\tB\x02\x18\x01\x12=\n\x11triggering_policy\x18\x07 \x01(\x0b\x32\".scheduler.config.TriggeringPolicy\x12(\n\x04noop\x18\x64 \x01(\x0b\x32\x1a.scheduler.config.NoopTask\x12\x31\n\turl_fetch\x18\x65 \x01(\x0b\x32\x1e.scheduler.config.UrlFetchTask\x12\x36\n\x0b\x62uildbucket\x18g \x01(\x0b\x32!.scheduler.config.BuildbucketTaskJ\x04\x08\x04\x10\x05J\x04\x08\x66\x10g\"\xb3\x02\n\x07Trigger\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05realm\x18\x07 \x01(\t\x12\x10\n\x08schedule\x18\x02 \x01(\t\x12\x10\n\x08\x64isabled\x18\x03 \x01(\x08\x12\'\n\x04\x61\x63ls\x18\x04 \x03(\x0b\x32\x15.scheduler.config.AclB\x02\x18\x01\x12\x14\n\x08\x61\x63l_sets\x18\x05 \x03(\tB\x02\x18\x01\x12=\n\x11triggering_policy\x18\x06 \x01(\x0b\x32\".scheduler.config.TriggeringPolicy\x12\x11\n\x08triggers\x18\xc8\x01 \x03(\t\x12(\n\x04noop\x18\x64 \x01(\x0b\x32\x1a.scheduler.config.NoopTask\x12.\n\x07gitiles\x18\x65 \x01(\x0b\x32\x1d.scheduler.config.GitilesTask\"4\n\x08NoopTask\x12\x10\n\x08sleep_ms\x18\x01 \x01(\x03\x12\x16\n\x0etriggers_count\x18\x02 \x01(\x03\"]\n\x0bGitilesTask\x12\x0c\n\x04repo\x18\x01 \x01(\t\x12\x0c\n\x04refs\x18\x02 \x03(\t\x12\x14\n\x0cpath_regexps\x18\x03 \x03(\t\x12\x1c\n\x14path_regexps_exclude\x18\x04 \x03(\t\"@\n\x0cUrlFetchTask\x12\x0e\n\x06method\x18\x01 \x01(\t\x12\x0b\n\x03url\x18\x02 \x01(\t\x12\x13\n\x0btimeout_sec\x18\x03 \x01(\x05\"d\n\x0f\x42uildbucketTask\x12\x0e\n\x06server\x18\x01 \x01(\t\x12\x0e\n\x06\x62ucket\x18\x02 \x01(\t\x12\x0f\n\x07\x62uilder\x18\x03 \x01(\t\x12\x12\n\nproperties\x18\x04 \x03(\t\x12\x0c\n\x04tags\x18\x05 \x03(\t\"\xdb\x01\n\x0eTaskDefWrapper\x12(\n\x04noop\x18\x01 \x01(\x0b\x32\x1a.scheduler.config.NoopTask\x12\x31\n\turl_fetch\x18\x02 \x01(\x0b\x32\x1e.scheduler.config.UrlFetchTask\x12\x36\n\x0b\x62uildbucket\x18\x04 \x01(\x0b\x32!.scheduler.config.BuildbucketTask\x12.\n\x07gitiles\x18\x05 \x01(\x0b\x32\x1d.scheduler.config.GitilesTaskJ\x04\x08\x03\x10\x04\x42|Z1go.chromium.org/luci/scheduler/appengine/messages\xa2\xfe#E\nChttps://luci-config.appspot.com/schemas/projects:luci-scheduler.cfgb\x06proto3'
  ,
  dependencies=[go_dot_chromium_dot_org_dot_luci_dot_common_dot_proto_dot_options__pb2.DESCRIPTOR,])



_ACL_ROLE = _descriptor.EnumDescriptor(
  name='Role',
  full_name='scheduler.config.Acl.Role',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='READER', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TRIGGERER', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='OWNER', index=2, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=372,
  serialized_end=416,
)
_sym_db.RegisterEnumDescriptor(_ACL_ROLE)

_TRIGGERINGPOLICY_KIND = _descriptor.EnumDescriptor(
  name='Kind',
  full_name='scheduler.config.TriggeringPolicy.Kind',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNDEFINED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GREEDY_BATCHING', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='LOGARITHMIC_BATCHING', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=633,
  serialized_end=701,
)
_sym_db.RegisterEnumDescriptor(_TRIGGERINGPOLICY_KIND)


_PROJECTCONFIG = _descriptor.Descriptor(
  name='ProjectConfig',
  full_name='scheduler.config.ProjectConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='job', full_name='scheduler.config.ProjectConfig.job', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='trigger', full_name='scheduler.config.ProjectConfig.trigger', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='acl_sets', full_name='scheduler.config.ProjectConfig.acl_sets', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=134,
  serialized_end=301,
)


_ACL = _descriptor.Descriptor(
  name='Acl',
  full_name='scheduler.config.Acl',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='role', full_name='scheduler.config.Acl.role', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='granted_to', full_name='scheduler.config.Acl.granted_to', index=1,
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
    _ACL_ROLE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=303,
  serialized_end=416,
)


_ACLSET = _descriptor.Descriptor(
  name='AclSet',
  full_name='scheduler.config.AclSet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='scheduler.config.AclSet.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='acls', full_name='scheduler.config.AclSet.acls', index=1,
      number=2, type=11, cpp_type=10, label=3,
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
  serialized_start=418,
  serialized_end=477,
)


_TRIGGERINGPOLICY = _descriptor.Descriptor(
  name='TriggeringPolicy',
  full_name='scheduler.config.TriggeringPolicy',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='kind', full_name='scheduler.config.TriggeringPolicy.kind', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_concurrent_invocations', full_name='scheduler.config.TriggeringPolicy.max_concurrent_invocations', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_batch_size', full_name='scheduler.config.TriggeringPolicy.max_batch_size', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='log_base', full_name='scheduler.config.TriggeringPolicy.log_base', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _TRIGGERINGPOLICY_KIND,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=480,
  serialized_end=701,
)


_JOB = _descriptor.Descriptor(
  name='Job',
  full_name='scheduler.config.Job',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='scheduler.config.Job.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='realm', full_name='scheduler.config.Job.realm', index=1,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='schedule', full_name='scheduler.config.Job.schedule', index=2,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='disabled', full_name='scheduler.config.Job.disabled', index=3,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='acls', full_name='scheduler.config.Job.acls', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='acl_sets', full_name='scheduler.config.Job.acl_sets', index=5,
      number=6, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='triggering_policy', full_name='scheduler.config.Job.triggering_policy', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='noop', full_name='scheduler.config.Job.noop', index=7,
      number=100, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='url_fetch', full_name='scheduler.config.Job.url_fetch', index=8,
      number=101, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='buildbucket', full_name='scheduler.config.Job.buildbucket', index=9,
      number=103, type=11, cpp_type=10, label=1,
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
  serialized_start=704,
  serialized_end=1059,
)


_TRIGGER = _descriptor.Descriptor(
  name='Trigger',
  full_name='scheduler.config.Trigger',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='scheduler.config.Trigger.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='realm', full_name='scheduler.config.Trigger.realm', index=1,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='schedule', full_name='scheduler.config.Trigger.schedule', index=2,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='disabled', full_name='scheduler.config.Trigger.disabled', index=3,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='acls', full_name='scheduler.config.Trigger.acls', index=4,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='acl_sets', full_name='scheduler.config.Trigger.acl_sets', index=5,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='triggering_policy', full_name='scheduler.config.Trigger.triggering_policy', index=6,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='triggers', full_name='scheduler.config.Trigger.triggers', index=7,
      number=200, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='noop', full_name='scheduler.config.Trigger.noop', index=8,
      number=100, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='gitiles', full_name='scheduler.config.Trigger.gitiles', index=9,
      number=101, type=11, cpp_type=10, label=1,
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
  serialized_start=1062,
  serialized_end=1369,
)


_NOOPTASK = _descriptor.Descriptor(
  name='NoopTask',
  full_name='scheduler.config.NoopTask',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='sleep_ms', full_name='scheduler.config.NoopTask.sleep_ms', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='triggers_count', full_name='scheduler.config.NoopTask.triggers_count', index=1,
      number=2, type=3, cpp_type=2, label=1,
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
  serialized_start=1371,
  serialized_end=1423,
)


_GITILESTASK = _descriptor.Descriptor(
  name='GitilesTask',
  full_name='scheduler.config.GitilesTask',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='repo', full_name='scheduler.config.GitilesTask.repo', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='refs', full_name='scheduler.config.GitilesTask.refs', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='path_regexps', full_name='scheduler.config.GitilesTask.path_regexps', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='path_regexps_exclude', full_name='scheduler.config.GitilesTask.path_regexps_exclude', index=3,
      number=4, type=9, cpp_type=9, label=3,
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
  serialized_start=1425,
  serialized_end=1518,
)


_URLFETCHTASK = _descriptor.Descriptor(
  name='UrlFetchTask',
  full_name='scheduler.config.UrlFetchTask',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='method', full_name='scheduler.config.UrlFetchTask.method', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='url', full_name='scheduler.config.UrlFetchTask.url', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timeout_sec', full_name='scheduler.config.UrlFetchTask.timeout_sec', index=2,
      number=3, type=5, cpp_type=1, label=1,
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
  serialized_start=1520,
  serialized_end=1584,
)


_BUILDBUCKETTASK = _descriptor.Descriptor(
  name='BuildbucketTask',
  full_name='scheduler.config.BuildbucketTask',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='server', full_name='scheduler.config.BuildbucketTask.server', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bucket', full_name='scheduler.config.BuildbucketTask.bucket', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='builder', full_name='scheduler.config.BuildbucketTask.builder', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='properties', full_name='scheduler.config.BuildbucketTask.properties', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tags', full_name='scheduler.config.BuildbucketTask.tags', index=4,
      number=5, type=9, cpp_type=9, label=3,
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
  serialized_start=1586,
  serialized_end=1686,
)


_TASKDEFWRAPPER = _descriptor.Descriptor(
  name='TaskDefWrapper',
  full_name='scheduler.config.TaskDefWrapper',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='noop', full_name='scheduler.config.TaskDefWrapper.noop', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='url_fetch', full_name='scheduler.config.TaskDefWrapper.url_fetch', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='buildbucket', full_name='scheduler.config.TaskDefWrapper.buildbucket', index=2,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='gitiles', full_name='scheduler.config.TaskDefWrapper.gitiles', index=3,
      number=5, type=11, cpp_type=10, label=1,
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
  serialized_start=1689,
  serialized_end=1908,
)

_PROJECTCONFIG.fields_by_name['job'].message_type = _JOB
_PROJECTCONFIG.fields_by_name['trigger'].message_type = _TRIGGER
_PROJECTCONFIG.fields_by_name['acl_sets'].message_type = _ACLSET
_ACL.fields_by_name['role'].enum_type = _ACL_ROLE
_ACL_ROLE.containing_type = _ACL
_ACLSET.fields_by_name['acls'].message_type = _ACL
_TRIGGERINGPOLICY.fields_by_name['kind'].enum_type = _TRIGGERINGPOLICY_KIND
_TRIGGERINGPOLICY_KIND.containing_type = _TRIGGERINGPOLICY
_JOB.fields_by_name['acls'].message_type = _ACL
_JOB.fields_by_name['triggering_policy'].message_type = _TRIGGERINGPOLICY
_JOB.fields_by_name['noop'].message_type = _NOOPTASK
_JOB.fields_by_name['url_fetch'].message_type = _URLFETCHTASK
_JOB.fields_by_name['buildbucket'].message_type = _BUILDBUCKETTASK
_TRIGGER.fields_by_name['acls'].message_type = _ACL
_TRIGGER.fields_by_name['triggering_policy'].message_type = _TRIGGERINGPOLICY
_TRIGGER.fields_by_name['noop'].message_type = _NOOPTASK
_TRIGGER.fields_by_name['gitiles'].message_type = _GITILESTASK
_TASKDEFWRAPPER.fields_by_name['noop'].message_type = _NOOPTASK
_TASKDEFWRAPPER.fields_by_name['url_fetch'].message_type = _URLFETCHTASK
_TASKDEFWRAPPER.fields_by_name['buildbucket'].message_type = _BUILDBUCKETTASK
_TASKDEFWRAPPER.fields_by_name['gitiles'].message_type = _GITILESTASK
DESCRIPTOR.message_types_by_name['ProjectConfig'] = _PROJECTCONFIG
DESCRIPTOR.message_types_by_name['Acl'] = _ACL
DESCRIPTOR.message_types_by_name['AclSet'] = _ACLSET
DESCRIPTOR.message_types_by_name['TriggeringPolicy'] = _TRIGGERINGPOLICY
DESCRIPTOR.message_types_by_name['Job'] = _JOB
DESCRIPTOR.message_types_by_name['Trigger'] = _TRIGGER
DESCRIPTOR.message_types_by_name['NoopTask'] = _NOOPTASK
DESCRIPTOR.message_types_by_name['GitilesTask'] = _GITILESTASK
DESCRIPTOR.message_types_by_name['UrlFetchTask'] = _URLFETCHTASK
DESCRIPTOR.message_types_by_name['BuildbucketTask'] = _BUILDBUCKETTASK
DESCRIPTOR.message_types_by_name['TaskDefWrapper'] = _TASKDEFWRAPPER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ProjectConfig = _reflection.GeneratedProtocolMessageType('ProjectConfig', (_message.Message,), {
  'DESCRIPTOR' : _PROJECTCONFIG,
  '__module__' : 'go.chromium.org.luci.scheduler.appengine.messages.config_pb2'
  # @@protoc_insertion_point(class_scope:scheduler.config.ProjectConfig)
  })
_sym_db.RegisterMessage(ProjectConfig)

Acl = _reflection.GeneratedProtocolMessageType('Acl', (_message.Message,), {
  'DESCRIPTOR' : _ACL,
  '__module__' : 'go.chromium.org.luci.scheduler.appengine.messages.config_pb2'
  # @@protoc_insertion_point(class_scope:scheduler.config.Acl)
  })
_sym_db.RegisterMessage(Acl)

AclSet = _reflection.GeneratedProtocolMessageType('AclSet', (_message.Message,), {
  'DESCRIPTOR' : _ACLSET,
  '__module__' : 'go.chromium.org.luci.scheduler.appengine.messages.config_pb2'
  # @@protoc_insertion_point(class_scope:scheduler.config.AclSet)
  })
_sym_db.RegisterMessage(AclSet)

TriggeringPolicy = _reflection.GeneratedProtocolMessageType('TriggeringPolicy', (_message.Message,), {
  'DESCRIPTOR' : _TRIGGERINGPOLICY,
  '__module__' : 'go.chromium.org.luci.scheduler.appengine.messages.config_pb2'
  # @@protoc_insertion_point(class_scope:scheduler.config.TriggeringPolicy)
  })
_sym_db.RegisterMessage(TriggeringPolicy)

Job = _reflection.GeneratedProtocolMessageType('Job', (_message.Message,), {
  'DESCRIPTOR' : _JOB,
  '__module__' : 'go.chromium.org.luci.scheduler.appengine.messages.config_pb2'
  # @@protoc_insertion_point(class_scope:scheduler.config.Job)
  })
_sym_db.RegisterMessage(Job)

Trigger = _reflection.GeneratedProtocolMessageType('Trigger', (_message.Message,), {
  'DESCRIPTOR' : _TRIGGER,
  '__module__' : 'go.chromium.org.luci.scheduler.appengine.messages.config_pb2'
  # @@protoc_insertion_point(class_scope:scheduler.config.Trigger)
  })
_sym_db.RegisterMessage(Trigger)

NoopTask = _reflection.GeneratedProtocolMessageType('NoopTask', (_message.Message,), {
  'DESCRIPTOR' : _NOOPTASK,
  '__module__' : 'go.chromium.org.luci.scheduler.appengine.messages.config_pb2'
  # @@protoc_insertion_point(class_scope:scheduler.config.NoopTask)
  })
_sym_db.RegisterMessage(NoopTask)

GitilesTask = _reflection.GeneratedProtocolMessageType('GitilesTask', (_message.Message,), {
  'DESCRIPTOR' : _GITILESTASK,
  '__module__' : 'go.chromium.org.luci.scheduler.appengine.messages.config_pb2'
  # @@protoc_insertion_point(class_scope:scheduler.config.GitilesTask)
  })
_sym_db.RegisterMessage(GitilesTask)

UrlFetchTask = _reflection.GeneratedProtocolMessageType('UrlFetchTask', (_message.Message,), {
  'DESCRIPTOR' : _URLFETCHTASK,
  '__module__' : 'go.chromium.org.luci.scheduler.appengine.messages.config_pb2'
  # @@protoc_insertion_point(class_scope:scheduler.config.UrlFetchTask)
  })
_sym_db.RegisterMessage(UrlFetchTask)

BuildbucketTask = _reflection.GeneratedProtocolMessageType('BuildbucketTask', (_message.Message,), {
  'DESCRIPTOR' : _BUILDBUCKETTASK,
  '__module__' : 'go.chromium.org.luci.scheduler.appengine.messages.config_pb2'
  # @@protoc_insertion_point(class_scope:scheduler.config.BuildbucketTask)
  })
_sym_db.RegisterMessage(BuildbucketTask)

TaskDefWrapper = _reflection.GeneratedProtocolMessageType('TaskDefWrapper', (_message.Message,), {
  'DESCRIPTOR' : _TASKDEFWRAPPER,
  '__module__' : 'go.chromium.org.luci.scheduler.appengine.messages.config_pb2'
  # @@protoc_insertion_point(class_scope:scheduler.config.TaskDefWrapper)
  })
_sym_db.RegisterMessage(TaskDefWrapper)


DESCRIPTOR._options = None
_PROJECTCONFIG.fields_by_name['acl_sets']._options = None
_JOB.fields_by_name['acls']._options = None
_JOB.fields_by_name['acl_sets']._options = None
_TRIGGER.fields_by_name['acls']._options = None
_TRIGGER.fields_by_name['acl_sets']._options = None
# @@protoc_insertion_point(module_scope)
