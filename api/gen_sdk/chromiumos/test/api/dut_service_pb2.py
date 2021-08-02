# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/test/api/dut_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen_sdk.chromiumos.config.api import device_config_id_pb2 as chromiumos_dot_config_dot_api_dot_device__config__id__pb2
from chromite.api.gen_sdk.chromiumos.longrunning import operations_pb2 as chromiumos_dot_longrunning_dot_operations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromiumos/test/api/dut_service.proto',
  package='chromiumos.test.api',
  syntax='proto3',
  serialized_options=b'Z-go.chromium.org/chromiumos/config/go/test/api',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n%chromiumos/test/api/dut_service.proto\x12\x13\x63hromiumos.test.api\x1a,chromiumos/config/api/device_config_id.proto\x1a\'chromiumos/longrunning/operations.proto\"\xaa\x01\n\x12\x45xecCommandRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07\x63ommand\x18\x02 \x01(\t\x12\x0c\n\x04\x61rgs\x18\x03 \x03(\t\x12\r\n\x05stdin\x18\x04 \x01(\x0c\x12+\n\x06stdout\x18\x05 \x01(\x0e\x32\x1b.chromiumos.test.api.Output\x12+\n\x06stderr\x18\x06 \x01(\x0e\x32\x1b.chromiumos.test.api.Output\"\xd1\x01\n\x13\x45xecCommandResponse\x12\x44\n\texit_info\x18\x01 \x01(\x0b\x32\x31.chromiumos.test.api.ExecCommandResponse.ExitInfo\x12\x0e\n\x06stdout\x18\x02 \x01(\x0c\x12\x0e\n\x06stderr\x18\x03 \x01(\x0c\x1aT\n\x08\x45xitInfo\x12\x0e\n\x06status\x18\x01 \x01(\x05\x12\x10\n\x08signaled\x18\x02 \x01(\x08\x12\x0f\n\x07started\x18\x03 \x01(\x08\x12\x15\n\rerror_message\x18\x04 \x01(\t\"/\n\x13\x46\x65tchCrashesRequest\x12\x12\n\nfetch_core\x18\x02 \x01(\x08J\x04\x08\x01\x10\x02\"\xa1\x01\n\x14\x46\x65tchCrashesResponse\x12\x10\n\x08\x63rash_id\x18\x01 \x01(\x03\x12/\n\x05\x63rash\x18\x02 \x01(\x0b\x32\x1e.chromiumos.test.api.CrashInfoH\x00\x12.\n\x04\x62lob\x18\x03 \x01(\x0b\x32\x1e.chromiumos.test.api.CrashBlobH\x00\x12\x0e\n\x04\x63ore\x18\x04 \x01(\x0cH\x00\x42\x06\n\x04\x64\x61ta\"\xb3\x01\n\tCrashInfo\x12\x11\n\texec_name\x18\x01 \x01(\t\x12\x0c\n\x04prod\x18\x02 \x01(\t\x12\x0b\n\x03ver\x18\x03 \x01(\t\x12\x0b\n\x03sig\x18\x04 \x01(\t\x12$\n\x1cin_progress_integration_test\x18\x05 \x01(\t\x12\x11\n\tcollector\x18\x06 \x01(\t\x12\x32\n\x06\x66ields\x18\x07 \x03(\x0b\x32\".chromiumos.test.api.CrashMetadata\"*\n\rCrashMetadata\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0c\n\x04text\x18\x02 \x01(\t\"8\n\tCrashBlob\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0c\n\x04\x62lob\x18\x02 \x01(\x0c\x12\x10\n\x08\x66ilename\x18\x03 \x01(\t\"\x1e\n\x0eRestartRequest\x12\x0c\n\x04\x61rgs\x18\x01 \x03(\t\"!\n\x0fRestartResponse\x12\x0e\n\x06output\x18\x01 \x01(\t\"\x11\n\x0fRestartMetadata\"\x1d\n\x1b\x44\x65tectDeviceConfigIdRequest\"\xc1\x02\n\x1c\x44\x65tectDeviceConfigIdResponse\x12L\n\x07success\x18\x01 \x01(\x0b\x32\x39.chromiumos.test.api.DetectDeviceConfigIdResponse.SuccessH\x00\x12L\n\x07\x66\x61ilure\x18\x02 \x01(\x0b\x32\x39.chromiumos.test.api.DetectDeviceConfigIdResponse.FailureH\x00\x1aY\n\x07Success\x12N\n\x14\x64\x65tected_scan_config\x18\x01 \x01(\x0b\x32\x30.chromiumos.config.api.DeviceConfigId.ScanConfig\x1a \n\x07\x46\x61ilure\x12\x15\n\rerror_message\x18\x01 \x01(\tB\x08\n\x06result*,\n\x06Output\x12\x0f\n\x0bOUTPUT_PIPE\x10\x00\x12\x11\n\rOUTPUT_STDOUT\x10\x01\x32\xd0\x03\n\nDutService\x12\x62\n\x0b\x45xecCommand\x12\'.chromiumos.test.api.ExecCommandRequest\x1a(.chromiumos.test.api.ExecCommandResponse0\x01\x12\x65\n\x0c\x46\x65tchCrashes\x12(.chromiumos.test.api.FetchCrashesRequest\x1a).chromiumos.test.api.FetchCrashesResponse0\x01\x12x\n\x07Restart\x12#.chromiumos.test.api.RestartRequest\x1a!.chromiumos.longrunning.Operation\"%\xd2\x41\"\n\x0fRestartResponse\x12\x0fRestartMetadata\x12}\n\x14\x44\x65tectDeviceConfigId\x12\x30.chromiumos.test.api.DetectDeviceConfigIdRequest\x1a\x31.chromiumos.test.api.DetectDeviceConfigIdResponse0\x01\x42/Z-go.chromium.org/chromiumos/config/go/test/apib\x06proto3'
  ,
  dependencies=[chromiumos_dot_config_dot_api_dot_device__config__id__pb2.DESCRIPTOR,chromiumos_dot_longrunning_dot_operations__pb2.DESCRIPTOR,])

_OUTPUT = _descriptor.EnumDescriptor(
  name='Output',
  full_name='chromiumos.test.api.Output',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OUTPUT_PIPE', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='OUTPUT_STDOUT', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1472,
  serialized_end=1516,
)
_sym_db.RegisterEnumDescriptor(_OUTPUT)

Output = enum_type_wrapper.EnumTypeWrapper(_OUTPUT)
OUTPUT_PIPE = 0
OUTPUT_STDOUT = 1



_EXECCOMMANDREQUEST = _descriptor.Descriptor(
  name='ExecCommandRequest',
  full_name='chromiumos.test.api.ExecCommandRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='chromiumos.test.api.ExecCommandRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='command', full_name='chromiumos.test.api.ExecCommandRequest.command', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='args', full_name='chromiumos.test.api.ExecCommandRequest.args', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stdin', full_name='chromiumos.test.api.ExecCommandRequest.stdin', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stdout', full_name='chromiumos.test.api.ExecCommandRequest.stdout', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stderr', full_name='chromiumos.test.api.ExecCommandRequest.stderr', index=5,
      number=6, type=14, cpp_type=8, label=1,
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
  serialized_start=150,
  serialized_end=320,
)


_EXECCOMMANDRESPONSE_EXITINFO = _descriptor.Descriptor(
  name='ExitInfo',
  full_name='chromiumos.test.api.ExecCommandResponse.ExitInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='chromiumos.test.api.ExecCommandResponse.ExitInfo.status', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='signaled', full_name='chromiumos.test.api.ExecCommandResponse.ExitInfo.signaled', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='started', full_name='chromiumos.test.api.ExecCommandResponse.ExitInfo.started', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='error_message', full_name='chromiumos.test.api.ExecCommandResponse.ExitInfo.error_message', index=3,
      number=4, type=9, cpp_type=9, label=1,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=448,
  serialized_end=532,
)

_EXECCOMMANDRESPONSE = _descriptor.Descriptor(
  name='ExecCommandResponse',
  full_name='chromiumos.test.api.ExecCommandResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='exit_info', full_name='chromiumos.test.api.ExecCommandResponse.exit_info', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stdout', full_name='chromiumos.test.api.ExecCommandResponse.stdout', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stderr', full_name='chromiumos.test.api.ExecCommandResponse.stderr', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_EXECCOMMANDRESPONSE_EXITINFO, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=323,
  serialized_end=532,
)


_FETCHCRASHESREQUEST = _descriptor.Descriptor(
  name='FetchCrashesRequest',
  full_name='chromiumos.test.api.FetchCrashesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='fetch_core', full_name='chromiumos.test.api.FetchCrashesRequest.fetch_core', index=0,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=534,
  serialized_end=581,
)


_FETCHCRASHESRESPONSE = _descriptor.Descriptor(
  name='FetchCrashesResponse',
  full_name='chromiumos.test.api.FetchCrashesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='crash_id', full_name='chromiumos.test.api.FetchCrashesResponse.crash_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='crash', full_name='chromiumos.test.api.FetchCrashesResponse.crash', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='blob', full_name='chromiumos.test.api.FetchCrashesResponse.blob', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='core', full_name='chromiumos.test.api.FetchCrashesResponse.core', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
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
    _descriptor.OneofDescriptor(
      name='data', full_name='chromiumos.test.api.FetchCrashesResponse.data',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=584,
  serialized_end=745,
)


_CRASHINFO = _descriptor.Descriptor(
  name='CrashInfo',
  full_name='chromiumos.test.api.CrashInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='exec_name', full_name='chromiumos.test.api.CrashInfo.exec_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='prod', full_name='chromiumos.test.api.CrashInfo.prod', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ver', full_name='chromiumos.test.api.CrashInfo.ver', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sig', full_name='chromiumos.test.api.CrashInfo.sig', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='in_progress_integration_test', full_name='chromiumos.test.api.CrashInfo.in_progress_integration_test', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='collector', full_name='chromiumos.test.api.CrashInfo.collector', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fields', full_name='chromiumos.test.api.CrashInfo.fields', index=6,
      number=7, type=11, cpp_type=10, label=3,
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
  serialized_start=748,
  serialized_end=927,
)


_CRASHMETADATA = _descriptor.Descriptor(
  name='CrashMetadata',
  full_name='chromiumos.test.api.CrashMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='chromiumos.test.api.CrashMetadata.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='text', full_name='chromiumos.test.api.CrashMetadata.text', index=1,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=929,
  serialized_end=971,
)


_CRASHBLOB = _descriptor.Descriptor(
  name='CrashBlob',
  full_name='chromiumos.test.api.CrashBlob',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='chromiumos.test.api.CrashBlob.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='blob', full_name='chromiumos.test.api.CrashBlob.blob', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filename', full_name='chromiumos.test.api.CrashBlob.filename', index=2,
      number=3, type=9, cpp_type=9, label=1,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=973,
  serialized_end=1029,
)


_RESTARTREQUEST = _descriptor.Descriptor(
  name='RestartRequest',
  full_name='chromiumos.test.api.RestartRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='args', full_name='chromiumos.test.api.RestartRequest.args', index=0,
      number=1, type=9, cpp_type=9, label=3,
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
  serialized_start=1031,
  serialized_end=1061,
)


_RESTARTRESPONSE = _descriptor.Descriptor(
  name='RestartResponse',
  full_name='chromiumos.test.api.RestartResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='output', full_name='chromiumos.test.api.RestartResponse.output', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1063,
  serialized_end=1096,
)


_RESTARTMETADATA = _descriptor.Descriptor(
  name='RestartMetadata',
  full_name='chromiumos.test.api.RestartMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=1098,
  serialized_end=1115,
)


_DETECTDEVICECONFIGIDREQUEST = _descriptor.Descriptor(
  name='DetectDeviceConfigIdRequest',
  full_name='chromiumos.test.api.DetectDeviceConfigIdRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=1117,
  serialized_end=1146,
)


_DETECTDEVICECONFIGIDRESPONSE_SUCCESS = _descriptor.Descriptor(
  name='Success',
  full_name='chromiumos.test.api.DetectDeviceConfigIdResponse.Success',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='detected_scan_config', full_name='chromiumos.test.api.DetectDeviceConfigIdResponse.Success.detected_scan_config', index=0,
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
  serialized_start=1337,
  serialized_end=1426,
)

_DETECTDEVICECONFIGIDRESPONSE_FAILURE = _descriptor.Descriptor(
  name='Failure',
  full_name='chromiumos.test.api.DetectDeviceConfigIdResponse.Failure',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='error_message', full_name='chromiumos.test.api.DetectDeviceConfigIdResponse.Failure.error_message', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1428,
  serialized_end=1460,
)

_DETECTDEVICECONFIGIDRESPONSE = _descriptor.Descriptor(
  name='DetectDeviceConfigIdResponse',
  full_name='chromiumos.test.api.DetectDeviceConfigIdResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='chromiumos.test.api.DetectDeviceConfigIdResponse.success', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='failure', full_name='chromiumos.test.api.DetectDeviceConfigIdResponse.failure', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_DETECTDEVICECONFIGIDRESPONSE_SUCCESS, _DETECTDEVICECONFIGIDRESPONSE_FAILURE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='result', full_name='chromiumos.test.api.DetectDeviceConfigIdResponse.result',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=1149,
  serialized_end=1470,
)

_EXECCOMMANDREQUEST.fields_by_name['stdout'].enum_type = _OUTPUT
_EXECCOMMANDREQUEST.fields_by_name['stderr'].enum_type = _OUTPUT
_EXECCOMMANDRESPONSE_EXITINFO.containing_type = _EXECCOMMANDRESPONSE
_EXECCOMMANDRESPONSE.fields_by_name['exit_info'].message_type = _EXECCOMMANDRESPONSE_EXITINFO
_FETCHCRASHESRESPONSE.fields_by_name['crash'].message_type = _CRASHINFO
_FETCHCRASHESRESPONSE.fields_by_name['blob'].message_type = _CRASHBLOB
_FETCHCRASHESRESPONSE.oneofs_by_name['data'].fields.append(
  _FETCHCRASHESRESPONSE.fields_by_name['crash'])
_FETCHCRASHESRESPONSE.fields_by_name['crash'].containing_oneof = _FETCHCRASHESRESPONSE.oneofs_by_name['data']
_FETCHCRASHESRESPONSE.oneofs_by_name['data'].fields.append(
  _FETCHCRASHESRESPONSE.fields_by_name['blob'])
_FETCHCRASHESRESPONSE.fields_by_name['blob'].containing_oneof = _FETCHCRASHESRESPONSE.oneofs_by_name['data']
_FETCHCRASHESRESPONSE.oneofs_by_name['data'].fields.append(
  _FETCHCRASHESRESPONSE.fields_by_name['core'])
_FETCHCRASHESRESPONSE.fields_by_name['core'].containing_oneof = _FETCHCRASHESRESPONSE.oneofs_by_name['data']
_CRASHINFO.fields_by_name['fields'].message_type = _CRASHMETADATA
_DETECTDEVICECONFIGIDRESPONSE_SUCCESS.fields_by_name['detected_scan_config'].message_type = chromiumos_dot_config_dot_api_dot_device__config__id__pb2._DEVICECONFIGID_SCANCONFIG
_DETECTDEVICECONFIGIDRESPONSE_SUCCESS.containing_type = _DETECTDEVICECONFIGIDRESPONSE
_DETECTDEVICECONFIGIDRESPONSE_FAILURE.containing_type = _DETECTDEVICECONFIGIDRESPONSE
_DETECTDEVICECONFIGIDRESPONSE.fields_by_name['success'].message_type = _DETECTDEVICECONFIGIDRESPONSE_SUCCESS
_DETECTDEVICECONFIGIDRESPONSE.fields_by_name['failure'].message_type = _DETECTDEVICECONFIGIDRESPONSE_FAILURE
_DETECTDEVICECONFIGIDRESPONSE.oneofs_by_name['result'].fields.append(
  _DETECTDEVICECONFIGIDRESPONSE.fields_by_name['success'])
_DETECTDEVICECONFIGIDRESPONSE.fields_by_name['success'].containing_oneof = _DETECTDEVICECONFIGIDRESPONSE.oneofs_by_name['result']
_DETECTDEVICECONFIGIDRESPONSE.oneofs_by_name['result'].fields.append(
  _DETECTDEVICECONFIGIDRESPONSE.fields_by_name['failure'])
_DETECTDEVICECONFIGIDRESPONSE.fields_by_name['failure'].containing_oneof = _DETECTDEVICECONFIGIDRESPONSE.oneofs_by_name['result']
DESCRIPTOR.message_types_by_name['ExecCommandRequest'] = _EXECCOMMANDREQUEST
DESCRIPTOR.message_types_by_name['ExecCommandResponse'] = _EXECCOMMANDRESPONSE
DESCRIPTOR.message_types_by_name['FetchCrashesRequest'] = _FETCHCRASHESREQUEST
DESCRIPTOR.message_types_by_name['FetchCrashesResponse'] = _FETCHCRASHESRESPONSE
DESCRIPTOR.message_types_by_name['CrashInfo'] = _CRASHINFO
DESCRIPTOR.message_types_by_name['CrashMetadata'] = _CRASHMETADATA
DESCRIPTOR.message_types_by_name['CrashBlob'] = _CRASHBLOB
DESCRIPTOR.message_types_by_name['RestartRequest'] = _RESTARTREQUEST
DESCRIPTOR.message_types_by_name['RestartResponse'] = _RESTARTRESPONSE
DESCRIPTOR.message_types_by_name['RestartMetadata'] = _RESTARTMETADATA
DESCRIPTOR.message_types_by_name['DetectDeviceConfigIdRequest'] = _DETECTDEVICECONFIGIDREQUEST
DESCRIPTOR.message_types_by_name['DetectDeviceConfigIdResponse'] = _DETECTDEVICECONFIGIDRESPONSE
DESCRIPTOR.enum_types_by_name['Output'] = _OUTPUT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ExecCommandRequest = _reflection.GeneratedProtocolMessageType('ExecCommandRequest', (_message.Message,), {
  'DESCRIPTOR' : _EXECCOMMANDREQUEST,
  '__module__' : 'chromiumos.test.api.dut_service_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.api.ExecCommandRequest)
  })
_sym_db.RegisterMessage(ExecCommandRequest)

ExecCommandResponse = _reflection.GeneratedProtocolMessageType('ExecCommandResponse', (_message.Message,), {

  'ExitInfo' : _reflection.GeneratedProtocolMessageType('ExitInfo', (_message.Message,), {
    'DESCRIPTOR' : _EXECCOMMANDRESPONSE_EXITINFO,
    '__module__' : 'chromiumos.test.api.dut_service_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.test.api.ExecCommandResponse.ExitInfo)
    })
  ,
  'DESCRIPTOR' : _EXECCOMMANDRESPONSE,
  '__module__' : 'chromiumos.test.api.dut_service_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.api.ExecCommandResponse)
  })
_sym_db.RegisterMessage(ExecCommandResponse)
_sym_db.RegisterMessage(ExecCommandResponse.ExitInfo)

FetchCrashesRequest = _reflection.GeneratedProtocolMessageType('FetchCrashesRequest', (_message.Message,), {
  'DESCRIPTOR' : _FETCHCRASHESREQUEST,
  '__module__' : 'chromiumos.test.api.dut_service_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.api.FetchCrashesRequest)
  })
_sym_db.RegisterMessage(FetchCrashesRequest)

FetchCrashesResponse = _reflection.GeneratedProtocolMessageType('FetchCrashesResponse', (_message.Message,), {
  'DESCRIPTOR' : _FETCHCRASHESRESPONSE,
  '__module__' : 'chromiumos.test.api.dut_service_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.api.FetchCrashesResponse)
  })
_sym_db.RegisterMessage(FetchCrashesResponse)

CrashInfo = _reflection.GeneratedProtocolMessageType('CrashInfo', (_message.Message,), {
  'DESCRIPTOR' : _CRASHINFO,
  '__module__' : 'chromiumos.test.api.dut_service_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.api.CrashInfo)
  })
_sym_db.RegisterMessage(CrashInfo)

CrashMetadata = _reflection.GeneratedProtocolMessageType('CrashMetadata', (_message.Message,), {
  'DESCRIPTOR' : _CRASHMETADATA,
  '__module__' : 'chromiumos.test.api.dut_service_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.api.CrashMetadata)
  })
_sym_db.RegisterMessage(CrashMetadata)

CrashBlob = _reflection.GeneratedProtocolMessageType('CrashBlob', (_message.Message,), {
  'DESCRIPTOR' : _CRASHBLOB,
  '__module__' : 'chromiumos.test.api.dut_service_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.api.CrashBlob)
  })
_sym_db.RegisterMessage(CrashBlob)

RestartRequest = _reflection.GeneratedProtocolMessageType('RestartRequest', (_message.Message,), {
  'DESCRIPTOR' : _RESTARTREQUEST,
  '__module__' : 'chromiumos.test.api.dut_service_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.api.RestartRequest)
  })
_sym_db.RegisterMessage(RestartRequest)

RestartResponse = _reflection.GeneratedProtocolMessageType('RestartResponse', (_message.Message,), {
  'DESCRIPTOR' : _RESTARTRESPONSE,
  '__module__' : 'chromiumos.test.api.dut_service_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.api.RestartResponse)
  })
_sym_db.RegisterMessage(RestartResponse)

RestartMetadata = _reflection.GeneratedProtocolMessageType('RestartMetadata', (_message.Message,), {
  'DESCRIPTOR' : _RESTARTMETADATA,
  '__module__' : 'chromiumos.test.api.dut_service_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.api.RestartMetadata)
  })
_sym_db.RegisterMessage(RestartMetadata)

DetectDeviceConfigIdRequest = _reflection.GeneratedProtocolMessageType('DetectDeviceConfigIdRequest', (_message.Message,), {
  'DESCRIPTOR' : _DETECTDEVICECONFIGIDREQUEST,
  '__module__' : 'chromiumos.test.api.dut_service_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.api.DetectDeviceConfigIdRequest)
  })
_sym_db.RegisterMessage(DetectDeviceConfigIdRequest)

DetectDeviceConfigIdResponse = _reflection.GeneratedProtocolMessageType('DetectDeviceConfigIdResponse', (_message.Message,), {

  'Success' : _reflection.GeneratedProtocolMessageType('Success', (_message.Message,), {
    'DESCRIPTOR' : _DETECTDEVICECONFIGIDRESPONSE_SUCCESS,
    '__module__' : 'chromiumos.test.api.dut_service_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.test.api.DetectDeviceConfigIdResponse.Success)
    })
  ,

  'Failure' : _reflection.GeneratedProtocolMessageType('Failure', (_message.Message,), {
    'DESCRIPTOR' : _DETECTDEVICECONFIGIDRESPONSE_FAILURE,
    '__module__' : 'chromiumos.test.api.dut_service_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.test.api.DetectDeviceConfigIdResponse.Failure)
    })
  ,
  'DESCRIPTOR' : _DETECTDEVICECONFIGIDRESPONSE,
  '__module__' : 'chromiumos.test.api.dut_service_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.api.DetectDeviceConfigIdResponse)
  })
_sym_db.RegisterMessage(DetectDeviceConfigIdResponse)
_sym_db.RegisterMessage(DetectDeviceConfigIdResponse.Success)
_sym_db.RegisterMessage(DetectDeviceConfigIdResponse.Failure)


DESCRIPTOR._options = None

_DUTSERVICE = _descriptor.ServiceDescriptor(
  name='DutService',
  full_name='chromiumos.test.api.DutService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1519,
  serialized_end=1983,
  methods=[
  _descriptor.MethodDescriptor(
    name='ExecCommand',
    full_name='chromiumos.test.api.DutService.ExecCommand',
    index=0,
    containing_service=None,
    input_type=_EXECCOMMANDREQUEST,
    output_type=_EXECCOMMANDRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='FetchCrashes',
    full_name='chromiumos.test.api.DutService.FetchCrashes',
    index=1,
    containing_service=None,
    input_type=_FETCHCRASHESREQUEST,
    output_type=_FETCHCRASHESRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Restart',
    full_name='chromiumos.test.api.DutService.Restart',
    index=2,
    containing_service=None,
    input_type=_RESTARTREQUEST,
    output_type=chromiumos_dot_longrunning_dot_operations__pb2._OPERATION,
    serialized_options=b'\322A\"\n\017RestartResponse\022\017RestartMetadata',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='DetectDeviceConfigId',
    full_name='chromiumos.test.api.DutService.DetectDeviceConfigId',
    index=3,
    containing_service=None,
    input_type=_DETECTDEVICECONFIGIDREQUEST,
    output_type=_DETECTDEVICECONFIGIDRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_DUTSERVICE)

DESCRIPTOR.services_by_name['DutService'] = _DUTSERVICE

# @@protoc_insertion_point(module_scope)
