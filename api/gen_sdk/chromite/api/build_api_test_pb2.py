# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromite/api/build_api_test.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen_sdk.chromite.api import build_api_pb2 as chromite_dot_api_dot_build__api__pb2
from chromite.api.gen_sdk.chromiumos import common_pb2 as chromiumos_dot_common__pb2
from chromite.api.gen_sdk.chromiumos import metrics_pb2 as chromiumos_dot_metrics__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromite/api/build_api_test.proto',
  package='chromite.api',
  syntax='proto3',
  serialized_options=b'Z6go.chromium.org/chromiumos/infra/proto/go/chromite/api',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n!chromite/api/build_api_test.proto\x12\x0c\x63hromite.api\x1a\x1c\x63hromite/api/build_api.proto\x1a\x17\x63hromiumos/common.proto\x1a\x18\x63hromiumos/metrics.proto\",\n\nNestedPath\x12\x1e\n\x04path\x18\x01 \x01(\x0b\x32\x10.chromiumos.Path\"f\n\x11MultiFieldMessage\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0c\n\x04\x66lag\x18\x03 \x01(\x08\x12)\n\ttest_enum\x18\x04 \x01(\x0e\x32\x16.chromite.api.TestEnum\"\xc9\x04\n\x12TestRequestMessage\x12\n\n\x02id\x18\x01 \x01(\t\x12\"\n\x06\x63hroot\x18\x02 \x01(\x0b\x32\x12.chromiumos.Chroot\x12\x1e\n\x04path\x18\x03 \x01(\x0b\x32\x10.chromiumos.Path\x12&\n\x0c\x61nother_path\x18\x04 \x01(\x0b\x32\x10.chromiumos.Path\x12-\n\x0bnested_path\x18\x05 \x01(\x0b\x32\x18.chromite.api.NestedPath\x12+\n\x0bresult_path\x18\x06 \x01(\x0b\x32\x16.chromiumos.ResultPath\x12-\n\x0c\x62uild_target\x18\x07 \x01(\x0b\x32\x17.chromiumos.BuildTarget\x12.\n\rbuild_targets\x18\x08 \x03(\x0b\x32\x17.chromiumos.BuildTarget\x12)\n\nsynced_dir\x18\t \x01(\x0b\x32\x15.chromiumos.SyncedDir\x12*\n\x0bsynced_dirs\x18\n \x03(\x0b\x32\x15.chromiumos.SyncedDir\x12\x31\n\x08messages\x18\x0b \x03(\x0b\x32\x1f.chromite.api.MultiFieldMessage\x12)\n\ttest_enum\x18\x0c \x01(\x0e\x32\x16.chromite.api.TestEnum\x12*\n\ntest_enums\x18\r \x03(\x0e\x32\x16.chromite.api.TestEnum\x12\x0e\n\x06number\x18\x0e \x01(\x05\x12\x0f\n\x07numbers\x18\x0f \x03(\x05\"\xc8\x01\n\x11TestResultMessage\x12\x0e\n\x06result\x18\x01 \x01(\t\x12\"\n\x08\x61rtifact\x18\x02 \x01(\x0b\x32\x10.chromiumos.Path\x12\x31\n\x0fnested_artifact\x18\x03 \x01(\x0b\x32\x18.chromite.api.NestedPath\x12#\n\tartifacts\x18\x04 \x03(\x0b\x32\x10.chromiumos.Path\x12\'\n\x06\x65vents\x18\x05 \x03(\x0b\x32\x17.chromiumos.MetricEvent*^\n\x08TestEnum\x12\x19\n\x15TEST_ENUM_UNSPECIFIED\x10\x00\x12\x11\n\rTEST_ENUM_FOO\x10\x01\x12\x11\n\rTEST_ENUM_BAR\x10\x02\x12\x11\n\rTEST_ENUM_BAZ\x10\x03\x32\xc0\x02\n\x0eTestApiService\x12V\n\x11InputOutputMethod\x12 .chromite.api.TestRequestMessage\x1a\x1f.chromite.api.TestResultMessage\x12\x65\n\rRenamedMethod\x12 .chromite.api.TestRequestMessage\x1a\x1f.chromite.api.TestResultMessage\"\x11\xc2\xed\x1a\r\n\x0b\x43orrectName\x12Y\n\x0cHiddenMethod\x12 .chromite.api.TestRequestMessage\x1a\x1f.chromite.api.TestResultMessage\"\x06\xc2\xed\x1a\x02\x18\x02\x1a\x14\xc2\xed\x1a\x10\n\x0e\x62uild_api_test2\xf9\x01\n\x16InsideChrootApiService\x12^\n\x19InsideServiceInsideMethod\x12 .chromite.api.TestRequestMessage\x1a\x1f.chromite.api.TestResultMessage\x12g\n\x1aInsideServiceOutsideMethod\x12 .chromite.api.TestRequestMessage\x1a\x1f.chromite.api.TestResultMessage\"\x06\xc2\xed\x1a\x02\x10\x02\x1a\x16\xc2\xed\x1a\x12\n\x0e\x62uild_api_test\x10\x01\x32\xfc\x01\n\x17OutsideChrootApiService\x12`\n\x1bOutsideServiceOutsideMethod\x12 .chromite.api.TestRequestMessage\x1a\x1f.chromite.api.TestResultMessage\x12g\n\x1aOutsideServiceInsideMethod\x12 .chromite.api.TestRequestMessage\x1a\x1f.chromite.api.TestResultMessage\"\x06\xc2\xed\x1a\x02\x10\x01\x1a\x16\xc2\xed\x1a\x12\n\x0e\x62uild_api_test\x10\x02\x32|\n\rHiddenService\x12Q\n\x0cHiddenMethod\x12 .chromite.api.TestRequestMessage\x1a\x1f.chromite.api.TestResultMessage\x1a\x18\xc2\xed\x1a\x14\n\x0e\x62uild_api_test\x10\x02\x18\x02\x42\x38Z6go.chromium.org/chromiumos/infra/proto/go/chromite/apib\x06proto3'
  ,
  dependencies=[chromite_dot_api_dot_build__api__pb2.DESCRIPTOR,chromiumos_dot_common__pb2.DESCRIPTOR,chromiumos_dot_metrics__pb2.DESCRIPTOR,])

_TESTENUM = _descriptor.EnumDescriptor(
  name='TestEnum',
  full_name='chromite.api.TestEnum',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='TEST_ENUM_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TEST_ENUM_FOO', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TEST_ENUM_BAR', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TEST_ENUM_BAZ', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1073,
  serialized_end=1167,
)
_sym_db.RegisterEnumDescriptor(_TESTENUM)

TestEnum = enum_type_wrapper.EnumTypeWrapper(_TESTENUM)
TEST_ENUM_UNSPECIFIED = 0
TEST_ENUM_FOO = 1
TEST_ENUM_BAR = 2
TEST_ENUM_BAZ = 3



_NESTEDPATH = _descriptor.Descriptor(
  name='NestedPath',
  full_name='chromite.api.NestedPath',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='chromite.api.NestedPath.path', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=132,
  serialized_end=176,
)


_MULTIFIELDMESSAGE = _descriptor.Descriptor(
  name='MultiFieldMessage',
  full_name='chromite.api.MultiFieldMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='chromite.api.MultiFieldMessage.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='chromite.api.MultiFieldMessage.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='flag', full_name='chromite.api.MultiFieldMessage.flag', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='test_enum', full_name='chromite.api.MultiFieldMessage.test_enum', index=3,
      number=4, type=14, cpp_type=8, label=1,
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
  serialized_start=178,
  serialized_end=280,
)


_TESTREQUESTMESSAGE = _descriptor.Descriptor(
  name='TestRequestMessage',
  full_name='chromite.api.TestRequestMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='chromite.api.TestRequestMessage.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='chroot', full_name='chromite.api.TestRequestMessage.chroot', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='path', full_name='chromite.api.TestRequestMessage.path', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='another_path', full_name='chromite.api.TestRequestMessage.another_path', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nested_path', full_name='chromite.api.TestRequestMessage.nested_path', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='result_path', full_name='chromite.api.TestRequestMessage.result_path', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='build_target', full_name='chromite.api.TestRequestMessage.build_target', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='build_targets', full_name='chromite.api.TestRequestMessage.build_targets', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='synced_dir', full_name='chromite.api.TestRequestMessage.synced_dir', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='synced_dirs', full_name='chromite.api.TestRequestMessage.synced_dirs', index=9,
      number=10, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='messages', full_name='chromite.api.TestRequestMessage.messages', index=10,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='test_enum', full_name='chromite.api.TestRequestMessage.test_enum', index=11,
      number=12, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='test_enums', full_name='chromite.api.TestRequestMessage.test_enums', index=12,
      number=13, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='number', full_name='chromite.api.TestRequestMessage.number', index=13,
      number=14, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='numbers', full_name='chromite.api.TestRequestMessage.numbers', index=14,
      number=15, type=5, cpp_type=1, label=3,
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
  serialized_start=283,
  serialized_end=868,
)


_TESTRESULTMESSAGE = _descriptor.Descriptor(
  name='TestResultMessage',
  full_name='chromite.api.TestResultMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='chromite.api.TestResultMessage.result', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='artifact', full_name='chromite.api.TestResultMessage.artifact', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nested_artifact', full_name='chromite.api.TestResultMessage.nested_artifact', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='artifacts', full_name='chromite.api.TestResultMessage.artifacts', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='events', full_name='chromite.api.TestResultMessage.events', index=4,
      number=5, type=11, cpp_type=10, label=3,
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
  serialized_start=871,
  serialized_end=1071,
)

_NESTEDPATH.fields_by_name['path'].message_type = chromiumos_dot_common__pb2._PATH
_MULTIFIELDMESSAGE.fields_by_name['test_enum'].enum_type = _TESTENUM
_TESTREQUESTMESSAGE.fields_by_name['chroot'].message_type = chromiumos_dot_common__pb2._CHROOT
_TESTREQUESTMESSAGE.fields_by_name['path'].message_type = chromiumos_dot_common__pb2._PATH
_TESTREQUESTMESSAGE.fields_by_name['another_path'].message_type = chromiumos_dot_common__pb2._PATH
_TESTREQUESTMESSAGE.fields_by_name['nested_path'].message_type = _NESTEDPATH
_TESTREQUESTMESSAGE.fields_by_name['result_path'].message_type = chromiumos_dot_common__pb2._RESULTPATH
_TESTREQUESTMESSAGE.fields_by_name['build_target'].message_type = chromiumos_dot_common__pb2._BUILDTARGET
_TESTREQUESTMESSAGE.fields_by_name['build_targets'].message_type = chromiumos_dot_common__pb2._BUILDTARGET
_TESTREQUESTMESSAGE.fields_by_name['synced_dir'].message_type = chromiumos_dot_common__pb2._SYNCEDDIR
_TESTREQUESTMESSAGE.fields_by_name['synced_dirs'].message_type = chromiumos_dot_common__pb2._SYNCEDDIR
_TESTREQUESTMESSAGE.fields_by_name['messages'].message_type = _MULTIFIELDMESSAGE
_TESTREQUESTMESSAGE.fields_by_name['test_enum'].enum_type = _TESTENUM
_TESTREQUESTMESSAGE.fields_by_name['test_enums'].enum_type = _TESTENUM
_TESTRESULTMESSAGE.fields_by_name['artifact'].message_type = chromiumos_dot_common__pb2._PATH
_TESTRESULTMESSAGE.fields_by_name['nested_artifact'].message_type = _NESTEDPATH
_TESTRESULTMESSAGE.fields_by_name['artifacts'].message_type = chromiumos_dot_common__pb2._PATH
_TESTRESULTMESSAGE.fields_by_name['events'].message_type = chromiumos_dot_metrics__pb2._METRICEVENT
DESCRIPTOR.message_types_by_name['NestedPath'] = _NESTEDPATH
DESCRIPTOR.message_types_by_name['MultiFieldMessage'] = _MULTIFIELDMESSAGE
DESCRIPTOR.message_types_by_name['TestRequestMessage'] = _TESTREQUESTMESSAGE
DESCRIPTOR.message_types_by_name['TestResultMessage'] = _TESTRESULTMESSAGE
DESCRIPTOR.enum_types_by_name['TestEnum'] = _TESTENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

NestedPath = _reflection.GeneratedProtocolMessageType('NestedPath', (_message.Message,), {
  'DESCRIPTOR' : _NESTEDPATH,
  '__module__' : 'chromite.api.build_api_test_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.NestedPath)
  })
_sym_db.RegisterMessage(NestedPath)

MultiFieldMessage = _reflection.GeneratedProtocolMessageType('MultiFieldMessage', (_message.Message,), {
  'DESCRIPTOR' : _MULTIFIELDMESSAGE,
  '__module__' : 'chromite.api.build_api_test_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.MultiFieldMessage)
  })
_sym_db.RegisterMessage(MultiFieldMessage)

TestRequestMessage = _reflection.GeneratedProtocolMessageType('TestRequestMessage', (_message.Message,), {
  'DESCRIPTOR' : _TESTREQUESTMESSAGE,
  '__module__' : 'chromite.api.build_api_test_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.TestRequestMessage)
  })
_sym_db.RegisterMessage(TestRequestMessage)

TestResultMessage = _reflection.GeneratedProtocolMessageType('TestResultMessage', (_message.Message,), {
  'DESCRIPTOR' : _TESTRESULTMESSAGE,
  '__module__' : 'chromite.api.build_api_test_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.TestResultMessage)
  })
_sym_db.RegisterMessage(TestResultMessage)


DESCRIPTOR._options = None

_TESTAPISERVICE = _descriptor.ServiceDescriptor(
  name='TestApiService',
  full_name='chromite.api.TestApiService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=b'\302\355\032\020\n\016build_api_test',
  create_key=_descriptor._internal_create_key,
  serialized_start=1170,
  serialized_end=1490,
  methods=[
  _descriptor.MethodDescriptor(
    name='InputOutputMethod',
    full_name='chromite.api.TestApiService.InputOutputMethod',
    index=0,
    containing_service=None,
    input_type=_TESTREQUESTMESSAGE,
    output_type=_TESTRESULTMESSAGE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='RenamedMethod',
    full_name='chromite.api.TestApiService.RenamedMethod',
    index=1,
    containing_service=None,
    input_type=_TESTREQUESTMESSAGE,
    output_type=_TESTRESULTMESSAGE,
    serialized_options=b'\302\355\032\r\n\013CorrectName',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='HiddenMethod',
    full_name='chromite.api.TestApiService.HiddenMethod',
    index=2,
    containing_service=None,
    input_type=_TESTREQUESTMESSAGE,
    output_type=_TESTRESULTMESSAGE,
    serialized_options=b'\302\355\032\002\030\002',
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_TESTAPISERVICE)

DESCRIPTOR.services_by_name['TestApiService'] = _TESTAPISERVICE


_INSIDECHROOTAPISERVICE = _descriptor.ServiceDescriptor(
  name='InsideChrootApiService',
  full_name='chromite.api.InsideChrootApiService',
  file=DESCRIPTOR,
  index=1,
  serialized_options=b'\302\355\032\022\n\016build_api_test\020\001',
  create_key=_descriptor._internal_create_key,
  serialized_start=1493,
  serialized_end=1742,
  methods=[
  _descriptor.MethodDescriptor(
    name='InsideServiceInsideMethod',
    full_name='chromite.api.InsideChrootApiService.InsideServiceInsideMethod',
    index=0,
    containing_service=None,
    input_type=_TESTREQUESTMESSAGE,
    output_type=_TESTRESULTMESSAGE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='InsideServiceOutsideMethod',
    full_name='chromite.api.InsideChrootApiService.InsideServiceOutsideMethod',
    index=1,
    containing_service=None,
    input_type=_TESTREQUESTMESSAGE,
    output_type=_TESTRESULTMESSAGE,
    serialized_options=b'\302\355\032\002\020\002',
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_INSIDECHROOTAPISERVICE)

DESCRIPTOR.services_by_name['InsideChrootApiService'] = _INSIDECHROOTAPISERVICE


_OUTSIDECHROOTAPISERVICE = _descriptor.ServiceDescriptor(
  name='OutsideChrootApiService',
  full_name='chromite.api.OutsideChrootApiService',
  file=DESCRIPTOR,
  index=2,
  serialized_options=b'\302\355\032\022\n\016build_api_test\020\002',
  create_key=_descriptor._internal_create_key,
  serialized_start=1745,
  serialized_end=1997,
  methods=[
  _descriptor.MethodDescriptor(
    name='OutsideServiceOutsideMethod',
    full_name='chromite.api.OutsideChrootApiService.OutsideServiceOutsideMethod',
    index=0,
    containing_service=None,
    input_type=_TESTREQUESTMESSAGE,
    output_type=_TESTRESULTMESSAGE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='OutsideServiceInsideMethod',
    full_name='chromite.api.OutsideChrootApiService.OutsideServiceInsideMethod',
    index=1,
    containing_service=None,
    input_type=_TESTREQUESTMESSAGE,
    output_type=_TESTRESULTMESSAGE,
    serialized_options=b'\302\355\032\002\020\001',
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_OUTSIDECHROOTAPISERVICE)

DESCRIPTOR.services_by_name['OutsideChrootApiService'] = _OUTSIDECHROOTAPISERVICE


_HIDDENSERVICE = _descriptor.ServiceDescriptor(
  name='HiddenService',
  full_name='chromite.api.HiddenService',
  file=DESCRIPTOR,
  index=3,
  serialized_options=b'\302\355\032\024\n\016build_api_test\020\002\030\002',
  create_key=_descriptor._internal_create_key,
  serialized_start=1999,
  serialized_end=2123,
  methods=[
  _descriptor.MethodDescriptor(
    name='HiddenMethod',
    full_name='chromite.api.HiddenService.HiddenMethod',
    index=0,
    containing_service=None,
    input_type=_TESTREQUESTMESSAGE,
    output_type=_TESTRESULTMESSAGE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_HIDDENSERVICE)

DESCRIPTOR.services_by_name['HiddenService'] = _HIDDENSERVICE

# @@protoc_insertion_point(module_scope)
