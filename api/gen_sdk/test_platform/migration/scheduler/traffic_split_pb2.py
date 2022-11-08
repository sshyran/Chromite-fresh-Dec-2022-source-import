# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/migration/scheduler/traffic_split.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen_sdk.chromiumos import common_pb2 as chromiumos_dot_common__pb2
from chromite.api.gen_sdk.test_platform import request_pb2 as test__platform_dot_request__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n5test_platform/migration/scheduler/traffic_split.proto\x12!test_platform.migration.scheduler\x1a\x17\x63hromiumos/common.proto\x1a\x1btest_platform/request.proto\"\x91\x01\n\x0cTrafficSplit\x12\x36\n\x05rules\x18\x01 \x03(\x0b\x32\'.test_platform.migration.scheduler.Rule\x12I\n\x0fsuite_overrides\x18\x02 \x03(\x0b\x32\x30.test_platform.migration.scheduler.SuiteOverride\"\xc4\x01\n\x04Rule\x12;\n\x07request\x18\x01 \x01(\x0b\x32*.test_platform.migration.scheduler.Request\x12;\n\x07\x62\x61\x63kend\x18\x02 \x01(\x0e\x32*.test_platform.migration.scheduler.Backend\x12\x42\n\x0brequest_mod\x18\x03 \x01(\x0b\x32-.test_platform.migration.scheduler.RequestMod\"\x85\x01\n\x07Request\x12<\n\nscheduling\x18\x01 \x01(\x0b\x32(.test_platform.Request.Params.Scheduling\x12\r\n\x05model\x18\x02 \x01(\t\x12-\n\x0c\x62uild_target\x18\x03 \x01(\x0b\x32\x17.chromiumos.BuildTarget\"J\n\nRequestMod\x12<\n\nscheduling\x18\x01 \x01(\x0b\x32(.test_platform.Request.Params.Scheduling\"s\n\rSuiteOverride\x12+\n\x05suite\x18\x01 \x01(\x0b\x32\x1c.test_platform.Request.Suite\x12\x35\n\x04rule\x18\x02 \x01(\x0b\x32\'.test_platform.migration.scheduler.Rule*L\n\x07\x42\x61\x63kend\x12\x17\n\x13\x42\x41\x43KEND_UNSPECIFIED\x10\x00\x12\x14\n\x10\x42\x41\x43KEND_AUTOTEST\x10\x01\x12\x12\n\x0e\x42\x41\x43KEND_SKYLAB\x10\x02\x42MZKgo.chromium.org/chromiumos/infra/proto/go/test_platform/migration/schedulerb\x06proto3')

_BACKEND = DESCRIPTOR.enum_types_by_name['Backend']
Backend = enum_type_wrapper.EnumTypeWrapper(_BACKEND)
BACKEND_UNSPECIFIED = 0
BACKEND_AUTOTEST = 1
BACKEND_SKYLAB = 2


_TRAFFICSPLIT = DESCRIPTOR.message_types_by_name['TrafficSplit']
_RULE = DESCRIPTOR.message_types_by_name['Rule']
_REQUEST = DESCRIPTOR.message_types_by_name['Request']
_REQUESTMOD = DESCRIPTOR.message_types_by_name['RequestMod']
_SUITEOVERRIDE = DESCRIPTOR.message_types_by_name['SuiteOverride']
TrafficSplit = _reflection.GeneratedProtocolMessageType('TrafficSplit', (_message.Message,), {
  'DESCRIPTOR' : _TRAFFICSPLIT,
  '__module__' : 'test_platform.migration.scheduler.traffic_split_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.migration.scheduler.TrafficSplit)
  })
_sym_db.RegisterMessage(TrafficSplit)

Rule = _reflection.GeneratedProtocolMessageType('Rule', (_message.Message,), {
  'DESCRIPTOR' : _RULE,
  '__module__' : 'test_platform.migration.scheduler.traffic_split_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.migration.scheduler.Rule)
  })
_sym_db.RegisterMessage(Rule)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), {
  'DESCRIPTOR' : _REQUEST,
  '__module__' : 'test_platform.migration.scheduler.traffic_split_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.migration.scheduler.Request)
  })
_sym_db.RegisterMessage(Request)

RequestMod = _reflection.GeneratedProtocolMessageType('RequestMod', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTMOD,
  '__module__' : 'test_platform.migration.scheduler.traffic_split_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.migration.scheduler.RequestMod)
  })
_sym_db.RegisterMessage(RequestMod)

SuiteOverride = _reflection.GeneratedProtocolMessageType('SuiteOverride', (_message.Message,), {
  'DESCRIPTOR' : _SUITEOVERRIDE,
  '__module__' : 'test_platform.migration.scheduler.traffic_split_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.migration.scheduler.SuiteOverride)
  })
_sym_db.RegisterMessage(SuiteOverride)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'ZKgo.chromium.org/chromiumos/infra/proto/go/test_platform/migration/scheduler'
  _BACKEND._serialized_start=822
  _BACKEND._serialized_end=898
  _TRAFFICSPLIT._serialized_start=147
  _TRAFFICSPLIT._serialized_end=292
  _RULE._serialized_start=295
  _RULE._serialized_end=491
  _REQUEST._serialized_start=494
  _REQUEST._serialized_end=627
  _REQUESTMOD._serialized_start=629
  _REQUESTMOD._serialized_end=703
  _SUITEOVERRIDE._serialized_start=705
  _SUITEOVERRIDE._serialized_end=820
# @@protoc_insertion_point(module_scope)
