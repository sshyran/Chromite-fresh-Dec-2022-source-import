# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromite/api/build_api_config.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#chromite/api/build_api_config.proto\x12\x0c\x63hromite.api\"M\n\x0e\x42uildApiConfig\x12\x10\n\x08log_path\x18\x01 \x01(\t\x12)\n\tcall_type\x18\x02 \x01(\x0e\x32\x16.chromite.api.CallType*\xa6\x01\n\x08\x43\x61llType\x12\x12\n\x0e\x43\x41LL_TYPE_NONE\x10\x00\x12\x15\n\x11\x43\x41LL_TYPE_EXECUTE\x10\x01\x12\x1b\n\x17\x43\x41LL_TYPE_VALIDATE_ONLY\x10\x02\x12\x1a\n\x16\x43\x41LL_TYPE_MOCK_SUCCESS\x10\x03\x12\x1a\n\x16\x43\x41LL_TYPE_MOCK_FAILURE\x10\x04\x12\x1a\n\x16\x43\x41LL_TYPE_MOCK_INVALID\x10\x05\x42\x38Z6go.chromium.org/chromiumos/infra/proto/go/chromite/apib\x06proto3')

_CALLTYPE = DESCRIPTOR.enum_types_by_name['CallType']
CallType = enum_type_wrapper.EnumTypeWrapper(_CALLTYPE)
CALL_TYPE_NONE = 0
CALL_TYPE_EXECUTE = 1
CALL_TYPE_VALIDATE_ONLY = 2
CALL_TYPE_MOCK_SUCCESS = 3
CALL_TYPE_MOCK_FAILURE = 4
CALL_TYPE_MOCK_INVALID = 5


_BUILDAPICONFIG = DESCRIPTOR.message_types_by_name['BuildApiConfig']
BuildApiConfig = _reflection.GeneratedProtocolMessageType('BuildApiConfig', (_message.Message,), {
  'DESCRIPTOR' : _BUILDAPICONFIG,
  '__module__' : 'chromite.api.build_api_config_pb2'
  # @@protoc_insertion_point(class_scope:chromite.api.BuildApiConfig)
  })
_sym_db.RegisterMessage(BuildApiConfig)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z6go.chromium.org/chromiumos/infra/proto/go/chromite/api'
  _CALLTYPE._serialized_start=133
  _CALLTYPE._serialized_end=299
  _BUILDAPICONFIG._serialized_start=53
  _BUILDAPICONFIG._serialized_end=130
# @@protoc_insertion_point(module_scope)
