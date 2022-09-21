# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/test/api/test_case.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromiumos/test/api/test_case.proto',
  package='chromiumos.test.api',
  syntax='proto3',
  serialized_options=b'Z-go.chromium.org/chromiumos/config/go/test/api',
  serialized_pb=b'\n#chromiumos/test/api/test_case.proto\x12\x13\x63hromiumos.test.api\"\xff\x01\n\x08TestCase\x12,\n\x02id\x18\x01 \x01(\x0b\x32 .chromiumos.test.api.TestCase.Id\x12\x0c\n\x04name\x18\x02 \x01(\t\x12/\n\x04tags\x18\x03 \x03(\x0b\x32!.chromiumos.test.api.TestCase.Tag\x12>\n\x0c\x64\x65pendencies\x18\x04 \x03(\x0b\x32(.chromiumos.test.api.TestCase.Dependency\x1a\x13\n\x02Id\x12\r\n\x05value\x18\x01 \x01(\t\x1a\x14\n\x03Tag\x12\r\n\x05value\x18\x01 \x01(\t\x1a\x1b\n\nDependency\x12\r\n\x05value\x18\x01 \x01(\t\"I\n\x0eTestCaseIdList\x12\x37\n\rtest_case_ids\x18\x01 \x03(\x0b\x32 .chromiumos.test.api.TestCase.Id\"A\n\x0cTestCaseList\x12\x31\n\ntest_cases\x18\x01 \x03(\x0b\x32\x1d.chromiumos.test.api.TestCaseB/Z-go.chromium.org/chromiumos/config/go/test/apib\x06proto3'
)




_TESTCASE_ID = _descriptor.Descriptor(
  name='Id',
  full_name='chromiumos.test.api.TestCase.Id',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='chromiumos.test.api.TestCase.Id.value', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=246,
  serialized_end=265,
)

_TESTCASE_TAG = _descriptor.Descriptor(
  name='Tag',
  full_name='chromiumos.test.api.TestCase.Tag',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='chromiumos.test.api.TestCase.Tag.value', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=267,
  serialized_end=287,
)

_TESTCASE_DEPENDENCY = _descriptor.Descriptor(
  name='Dependency',
  full_name='chromiumos.test.api.TestCase.Dependency',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='chromiumos.test.api.TestCase.Dependency.value', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=289,
  serialized_end=316,
)

_TESTCASE = _descriptor.Descriptor(
  name='TestCase',
  full_name='chromiumos.test.api.TestCase',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='chromiumos.test.api.TestCase.id', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='chromiumos.test.api.TestCase.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tags', full_name='chromiumos.test.api.TestCase.tags', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dependencies', full_name='chromiumos.test.api.TestCase.dependencies', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_TESTCASE_ID, _TESTCASE_TAG, _TESTCASE_DEPENDENCY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=61,
  serialized_end=316,
)


_TESTCASEIDLIST = _descriptor.Descriptor(
  name='TestCaseIdList',
  full_name='chromiumos.test.api.TestCaseIdList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='test_case_ids', full_name='chromiumos.test.api.TestCaseIdList.test_case_ids', index=0,
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
  serialized_start=318,
  serialized_end=391,
)


_TESTCASELIST = _descriptor.Descriptor(
  name='TestCaseList',
  full_name='chromiumos.test.api.TestCaseList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='test_cases', full_name='chromiumos.test.api.TestCaseList.test_cases', index=0,
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
  serialized_start=393,
  serialized_end=458,
)

_TESTCASE_ID.containing_type = _TESTCASE
_TESTCASE_TAG.containing_type = _TESTCASE
_TESTCASE_DEPENDENCY.containing_type = _TESTCASE
_TESTCASE.fields_by_name['id'].message_type = _TESTCASE_ID
_TESTCASE.fields_by_name['tags'].message_type = _TESTCASE_TAG
_TESTCASE.fields_by_name['dependencies'].message_type = _TESTCASE_DEPENDENCY
_TESTCASEIDLIST.fields_by_name['test_case_ids'].message_type = _TESTCASE_ID
_TESTCASELIST.fields_by_name['test_cases'].message_type = _TESTCASE
DESCRIPTOR.message_types_by_name['TestCase'] = _TESTCASE
DESCRIPTOR.message_types_by_name['TestCaseIdList'] = _TESTCASEIDLIST
DESCRIPTOR.message_types_by_name['TestCaseList'] = _TESTCASELIST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TestCase = _reflection.GeneratedProtocolMessageType('TestCase', (_message.Message,), {

  'Id' : _reflection.GeneratedProtocolMessageType('Id', (_message.Message,), {
    'DESCRIPTOR' : _TESTCASE_ID,
    '__module__' : 'chromiumos.test.api.test_case_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.test.api.TestCase.Id)
    })
  ,

  'Tag' : _reflection.GeneratedProtocolMessageType('Tag', (_message.Message,), {
    'DESCRIPTOR' : _TESTCASE_TAG,
    '__module__' : 'chromiumos.test.api.test_case_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.test.api.TestCase.Tag)
    })
  ,

  'Dependency' : _reflection.GeneratedProtocolMessageType('Dependency', (_message.Message,), {
    'DESCRIPTOR' : _TESTCASE_DEPENDENCY,
    '__module__' : 'chromiumos.test.api.test_case_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.test.api.TestCase.Dependency)
    })
  ,
  'DESCRIPTOR' : _TESTCASE,
  '__module__' : 'chromiumos.test.api.test_case_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.api.TestCase)
  })
_sym_db.RegisterMessage(TestCase)
_sym_db.RegisterMessage(TestCase.Id)
_sym_db.RegisterMessage(TestCase.Tag)
_sym_db.RegisterMessage(TestCase.Dependency)

TestCaseIdList = _reflection.GeneratedProtocolMessageType('TestCaseIdList', (_message.Message,), {
  'DESCRIPTOR' : _TESTCASEIDLIST,
  '__module__' : 'chromiumos.test.api.test_case_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.api.TestCaseIdList)
  })
_sym_db.RegisterMessage(TestCaseIdList)

TestCaseList = _reflection.GeneratedProtocolMessageType('TestCaseList', (_message.Message,), {
  'DESCRIPTOR' : _TESTCASELIST,
  '__module__' : 'chromiumos.test.api.test_case_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.api.TestCaseList)
  })
_sym_db.RegisterMessage(TestCaseList)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
