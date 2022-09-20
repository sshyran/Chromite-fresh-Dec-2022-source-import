# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/analytics/result.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$test_platform/analytics/result.proto\x12\x17test_platform.analytics\x1a\x1fgoogle/protobuf/timestamp.proto\"\x8b\x03\n\x0bTestPlanRun\x12\x0b\n\x03uid\x18\x01 \x01(\t\x12\x10\n\x08\x62uild_id\x18\x02 \x01(\x03\x12\r\n\x05suite\x18\x03 \x01(\t\x12\x15\n\rexecution_url\x18\x04 \x01(\t\x12\x10\n\x08\x64ut_pool\x18\x05 \x01(\t\x12\x14\n\x0c\x62uild_target\x18\x06 \x01(\t\x12\x16\n\x0e\x63hromeos_build\x18\x07 \x01(\t\x12/\n\x06status\x18\x08 \x01(\x0b\x32\x1f.test_platform.analytics.Status\x12\x37\n\x08timeline\x18\t \x01(\x0b\x32!.test_platform.analytics.TimelineB\x02\x18\x01\x12/\n\x0b\x63reate_time\x18\n \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nstart_time\x18\x0b \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12,\n\x08\x65nd_time\x18\x0c \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\xa3\x04\n\x07TestRun\x12\x10\n\x08\x62uild_id\x18\x01 \x01(\x03\x12\x14\n\x0c\x64isplay_name\x18\x02 \x01(\t\x12\x15\n\rexecution_url\x18\x03 \x01(\t\x12\x12\n\nparent_uid\x18\x04 \x01(\t\x12\r\n\x05model\x18\x05 \x01(\t\x12\x37\n\x08timeline\x18\x06 \x01(\x0b\x32!.test_platform.analytics.TimelineB\x02\x18\x01\x12/\n\x06status\x18\x07 \x01(\x0b\x32\x1f.test_platform.analytics.Status\x12\x31\n\x07verdict\x18\x08 \x01(\x0b\x32 .test_platform.analytics.Verdict\x12\x14\n\x0c\x66ull_log_url\x18\t \x01(\t\x12\x37\n\x06prejob\x18\n \x01(\x0b\x32\'.test_platform.analytics.TestRun.Prejob\x12/\n\x0b\x63reate_time\x18\x0b \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nstart_time\x18\x0c \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12,\n\x08\x65nd_time\x18\r \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x1a;\n\x06Prejob\x12\x31\n\x07verdict\x18\x01 \x01(\x0b\x32 .test_platform.analytics.Verdict\"\xd0\x01\n\x0eTestCaseResult\x12\x0b\n\x03uid\x18\x01 \x01(\t\x12\x14\n\x0c\x64isplay_name\x18\x02 \x01(\t\x12\x17\n\x0fparent_build_id\x18\x03 \x01(\x03\x12\x31\n\x07verdict\x18\x04 \x01(\x0b\x32 .test_platform.analytics.Verdict\x12\x1e\n\x16human_readable_summary\x18\x05 \x01(\t\x12/\n\x0b\x63reate_time\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\xcb\x01\n\x08Timeline\x12/\n\x0b\x63reate_time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nstart_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12,\n\x08\x65nd_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x30\n\x0c\x61\x62\x61ndon_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\x17\n\x06Status\x12\r\n\x05value\x18\x01 \x01(\t\"\x18\n\x07Verdict\x12\r\n\x05value\x18\x01 \x01(\tBCZAgo.chromium.org/chromiumos/infra/proto/go/test_platform/analyticsb\x06proto3')



_TESTPLANRUN = DESCRIPTOR.message_types_by_name['TestPlanRun']
_TESTRUN = DESCRIPTOR.message_types_by_name['TestRun']
_TESTRUN_PREJOB = _TESTRUN.nested_types_by_name['Prejob']
_TESTCASERESULT = DESCRIPTOR.message_types_by_name['TestCaseResult']
_TIMELINE = DESCRIPTOR.message_types_by_name['Timeline']
_STATUS = DESCRIPTOR.message_types_by_name['Status']
_VERDICT = DESCRIPTOR.message_types_by_name['Verdict']
TestPlanRun = _reflection.GeneratedProtocolMessageType('TestPlanRun', (_message.Message,), {
  'DESCRIPTOR' : _TESTPLANRUN,
  '__module__' : 'test_platform.analytics.result_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.analytics.TestPlanRun)
  })
_sym_db.RegisterMessage(TestPlanRun)

TestRun = _reflection.GeneratedProtocolMessageType('TestRun', (_message.Message,), {

  'Prejob' : _reflection.GeneratedProtocolMessageType('Prejob', (_message.Message,), {
    'DESCRIPTOR' : _TESTRUN_PREJOB,
    '__module__' : 'test_platform.analytics.result_pb2'
    # @@protoc_insertion_point(class_scope:test_platform.analytics.TestRun.Prejob)
    })
  ,
  'DESCRIPTOR' : _TESTRUN,
  '__module__' : 'test_platform.analytics.result_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.analytics.TestRun)
  })
_sym_db.RegisterMessage(TestRun)
_sym_db.RegisterMessage(TestRun.Prejob)

TestCaseResult = _reflection.GeneratedProtocolMessageType('TestCaseResult', (_message.Message,), {
  'DESCRIPTOR' : _TESTCASERESULT,
  '__module__' : 'test_platform.analytics.result_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.analytics.TestCaseResult)
  })
_sym_db.RegisterMessage(TestCaseResult)

Timeline = _reflection.GeneratedProtocolMessageType('Timeline', (_message.Message,), {
  'DESCRIPTOR' : _TIMELINE,
  '__module__' : 'test_platform.analytics.result_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.analytics.Timeline)
  })
_sym_db.RegisterMessage(Timeline)

Status = _reflection.GeneratedProtocolMessageType('Status', (_message.Message,), {
  'DESCRIPTOR' : _STATUS,
  '__module__' : 'test_platform.analytics.result_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.analytics.Status)
  })
_sym_db.RegisterMessage(Status)

Verdict = _reflection.GeneratedProtocolMessageType('Verdict', (_message.Message,), {
  'DESCRIPTOR' : _VERDICT,
  '__module__' : 'test_platform.analytics.result_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.analytics.Verdict)
  })
_sym_db.RegisterMessage(Verdict)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'ZAgo.chromium.org/chromiumos/infra/proto/go/test_platform/analytics'
  _TESTPLANRUN.fields_by_name['timeline']._options = None
  _TESTPLANRUN.fields_by_name['timeline']._serialized_options = b'\030\001'
  _TESTRUN.fields_by_name['timeline']._options = None
  _TESTRUN.fields_by_name['timeline']._serialized_options = b'\030\001'
  _TESTPLANRUN._serialized_start=99
  _TESTPLANRUN._serialized_end=494
  _TESTRUN._serialized_start=497
  _TESTRUN._serialized_end=1044
  _TESTRUN_PREJOB._serialized_start=985
  _TESTRUN_PREJOB._serialized_end=1044
  _TESTCASERESULT._serialized_start=1047
  _TESTCASERESULT._serialized_end=1255
  _TIMELINE._serialized_start=1258
  _TIMELINE._serialized_end=1461
  _STATUS._serialized_start=1463
  _STATUS._serialized_end=1486
  _VERDICT._serialized_start=1488
  _VERDICT._serialized_end=1512
# @@protoc_insertion_point(module_scope)
