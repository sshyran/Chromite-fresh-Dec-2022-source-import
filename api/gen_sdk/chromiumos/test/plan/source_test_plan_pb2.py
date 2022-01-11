# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/test/plan/source_test_plan.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromiumos/test/plan/source_test_plan.proto',
  package='chromiumos.test.plan',
  syntax='proto3',
  serialized_options=b'Z.go.chromium.org/chromiumos/config/go/test/plan',
  serialized_pb=b'\n+chromiumos/test/plan/source_test_plan.proto\x12\x14\x63hromiumos.test.plan\"\xf2\x01\n\x0eSourceTestPlan\x12\x14\n\x0cpath_regexps\x18\x02 \x03(\t\x12\x1c\n\x14path_regexp_excludes\x18\x03 \x03(\t\x12[\n\x18test_plan_starlark_files\x18\x0f \x03(\x0b\x32\x39.chromiumos.test.plan.SourceTestPlan.TestPlanStarlarkFile\x1a\x43\n\x14TestPlanStarlarkFile\x12\x0c\n\x04host\x18\x01 \x01(\t\x12\x0f\n\x07project\x18\x02 \x01(\t\x12\x0c\n\x04path\x18\x03 \x01(\tJ\x04\x08\x01\x10\x02J\x04\x08\x04\x10\x0f\x42\x30Z.go.chromium.org/chromiumos/config/go/test/planb\x06proto3'
)




_SOURCETESTPLAN_TESTPLANSTARLARKFILE = _descriptor.Descriptor(
  name='TestPlanStarlarkFile',
  full_name='chromiumos.test.plan.SourceTestPlan.TestPlanStarlarkFile',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='host', full_name='chromiumos.test.plan.SourceTestPlan.TestPlanStarlarkFile.host', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='project', full_name='chromiumos.test.plan.SourceTestPlan.TestPlanStarlarkFile.project', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='path', full_name='chromiumos.test.plan.SourceTestPlan.TestPlanStarlarkFile.path', index=2,
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
  serialized_start=233,
  serialized_end=300,
)

_SOURCETESTPLAN = _descriptor.Descriptor(
  name='SourceTestPlan',
  full_name='chromiumos.test.plan.SourceTestPlan',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='path_regexps', full_name='chromiumos.test.plan.SourceTestPlan.path_regexps', index=0,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='path_regexp_excludes', full_name='chromiumos.test.plan.SourceTestPlan.path_regexp_excludes', index=1,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='test_plan_starlark_files', full_name='chromiumos.test.plan.SourceTestPlan.test_plan_starlark_files', index=2,
      number=15, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_SOURCETESTPLAN_TESTPLANSTARLARKFILE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=70,
  serialized_end=312,
)

_SOURCETESTPLAN_TESTPLANSTARLARKFILE.containing_type = _SOURCETESTPLAN
_SOURCETESTPLAN.fields_by_name['test_plan_starlark_files'].message_type = _SOURCETESTPLAN_TESTPLANSTARLARKFILE
DESCRIPTOR.message_types_by_name['SourceTestPlan'] = _SOURCETESTPLAN
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SourceTestPlan = _reflection.GeneratedProtocolMessageType('SourceTestPlan', (_message.Message,), {

  'TestPlanStarlarkFile' : _reflection.GeneratedProtocolMessageType('TestPlanStarlarkFile', (_message.Message,), {
    'DESCRIPTOR' : _SOURCETESTPLAN_TESTPLANSTARLARKFILE,
    '__module__' : 'chromiumos.test.plan.source_test_plan_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.test.plan.SourceTestPlan.TestPlanStarlarkFile)
    })
  ,
  'DESCRIPTOR' : _SOURCETESTPLAN,
  '__module__' : 'chromiumos.test.plan.source_test_plan_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.plan.SourceTestPlan)
  })
_sym_db.RegisterMessage(SourceTestPlan)
_sym_db.RegisterMessage(SourceTestPlan.TestPlanStarlarkFile)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
