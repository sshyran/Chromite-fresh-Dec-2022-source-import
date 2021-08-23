# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/test/api/test_suite.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import message as _message
from chromite.third_party.google.protobuf import reflection as _reflection
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.chromiumos.test.api import test_case_pb2 as chromiumos_dot_test_dot_api_dot_test__case__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromiumos/test/api/test_suite.proto',
  package='chromiumos.test.api',
  syntax='proto3',
  serialized_options=b'Z-go.chromium.org/chromiumos/config/go/test/api',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n$chromiumos/test/api/test_suite.proto\x12\x13\x63hromiumos.test.api\x1a#chromiumos/test/api/test_case.proto\"\xe4\x01\n\tTestSuite\x12\x0c\n\x04name\x18\x01 \x01(\t\x12:\n\rtest_case_ids\x18\x02 \x01(\x0b\x32#.chromiumos.test.api.TestCaseIdList\x12R\n\x16test_case_tag_criteria\x18\x03 \x01(\x0b\x32\x32.chromiumos.test.api.TestSuite.TestCaseTagCriteria\x1a\x39\n\x13TestCaseTagCriteria\x12\x0c\n\x04tags\x18\x01 \x03(\t\x12\x14\n\x0ctag_excludes\x18\x02 \x03(\tB/Z-go.chromium.org/chromiumos/config/go/test/apib\x06proto3'
  ,
  dependencies=[chromiumos_dot_test_dot_api_dot_test__case__pb2.DESCRIPTOR,])




_TESTSUITE_TESTCASETAGCRITERIA = _descriptor.Descriptor(
  name='TestCaseTagCriteria',
  full_name='chromiumos.test.api.TestSuite.TestCaseTagCriteria',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='tags', full_name='chromiumos.test.api.TestSuite.TestCaseTagCriteria.tags', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tag_excludes', full_name='chromiumos.test.api.TestSuite.TestCaseTagCriteria.tag_excludes', index=1,
      number=2, type=9, cpp_type=9, label=3,
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
  serialized_start=270,
  serialized_end=327,
)

_TESTSUITE = _descriptor.Descriptor(
  name='TestSuite',
  full_name='chromiumos.test.api.TestSuite',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='chromiumos.test.api.TestSuite.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='test_case_ids', full_name='chromiumos.test.api.TestSuite.test_case_ids', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='test_case_tag_criteria', full_name='chromiumos.test.api.TestSuite.test_case_tag_criteria', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_TESTSUITE_TESTCASETAGCRITERIA, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=99,
  serialized_end=327,
)

_TESTSUITE_TESTCASETAGCRITERIA.containing_type = _TESTSUITE
_TESTSUITE.fields_by_name['test_case_ids'].message_type = chromiumos_dot_test_dot_api_dot_test__case__pb2._TESTCASEIDLIST
_TESTSUITE.fields_by_name['test_case_tag_criteria'].message_type = _TESTSUITE_TESTCASETAGCRITERIA
DESCRIPTOR.message_types_by_name['TestSuite'] = _TESTSUITE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TestSuite = _reflection.GeneratedProtocolMessageType('TestSuite', (_message.Message,), {

  'TestCaseTagCriteria' : _reflection.GeneratedProtocolMessageType('TestCaseTagCriteria', (_message.Message,), {
    'DESCRIPTOR' : _TESTSUITE_TESTCASETAGCRITERIA,
    '__module__' : 'chromiumos.test.api.test_suite_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.test.api.TestSuite.TestCaseTagCriteria)
    })
  ,
  'DESCRIPTOR' : _TESTSUITE,
  '__module__' : 'chromiumos.test.api.test_suite_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.api.TestSuite)
  })
_sym_db.RegisterMessage(TestSuite)
_sym_db.RegisterMessage(TestSuite.TestCaseTagCriteria)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
