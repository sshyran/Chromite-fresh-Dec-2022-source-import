# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/result_flow/test_runner.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen_sdk.test_platform.result_flow import common_pb2 as test__platform_dot_result__flow_dot_common__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+test_platform/result_flow/test_runner.proto\x12\x19test_platform.result_flow\x1a&test_platform/result_flow/common.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xe4\x01\n\x11TestRunnerRequest\x12\x36\n\x0btest_runner\x18\x01 \x01(\x0b\x32!.test_platform.result_flow.Source\x12\x33\n\x08test_run\x18\x02 \x01(\x0b\x32!.test_platform.result_flow.Target\x12\x34\n\ttest_case\x18\x03 \x01(\x0b\x32!.test_platform.result_flow.Target\x12,\n\x08\x64\x65\x61\x64line\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"E\n\x12TestRunnerResponse\x12/\n\x05state\x18\x01 \x01(\x0e\x32 .test_platform.result_flow.StateBEZCgo.chromium.org/chromiumos/infra/proto/go/test_platform/result_flowb\x06proto3')



_TESTRUNNERREQUEST = DESCRIPTOR.message_types_by_name['TestRunnerRequest']
_TESTRUNNERRESPONSE = DESCRIPTOR.message_types_by_name['TestRunnerResponse']
TestRunnerRequest = _reflection.GeneratedProtocolMessageType('TestRunnerRequest', (_message.Message,), {
  'DESCRIPTOR' : _TESTRUNNERREQUEST,
  '__module__' : 'test_platform.result_flow.test_runner_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.result_flow.TestRunnerRequest)
  })
_sym_db.RegisterMessage(TestRunnerRequest)

TestRunnerResponse = _reflection.GeneratedProtocolMessageType('TestRunnerResponse', (_message.Message,), {
  'DESCRIPTOR' : _TESTRUNNERRESPONSE,
  '__module__' : 'test_platform.result_flow.test_runner_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.result_flow.TestRunnerResponse)
  })
_sym_db.RegisterMessage(TestRunnerResponse)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'ZCgo.chromium.org/chromiumos/infra/proto/go/test_platform/result_flow'
  _TESTRUNNERREQUEST._serialized_start=148
  _TESTRUNNERREQUEST._serialized_end=376
  _TESTRUNNERRESPONSE._serialized_start=378
  _TESTRUNNERRESPONSE._serialized_end=447
# @@protoc_insertion_point(module_scope)
