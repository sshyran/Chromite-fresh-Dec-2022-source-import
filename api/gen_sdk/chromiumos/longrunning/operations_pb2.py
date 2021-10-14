# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/longrunning/operations.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromiumos/longrunning/operations.proto',
  package='chromiumos.longrunning',
  syntax='proto3',
  serialized_options=b'Z0go.chromium.org/chromiumos/config/go/longrunning',
  serialized_pb=b'\n\'chromiumos/longrunning/operations.proto\x12\x16\x63hromiumos.longrunning\x1a\x19google/protobuf/any.proto\x1a google/protobuf/descriptor.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1bgoogle/protobuf/empty.proto\"\xb4\x01\n\tOperation\x12\x0c\n\x04name\x18\x01 \x01(\t\x12&\n\x08metadata\x18\x02 \x01(\x0b\x32\x14.google.protobuf.Any\x12\x0c\n\x04\x64one\x18\x03 \x01(\x08\x12/\n\x05\x65rror\x18\x04 \x01(\x0b\x32\x1e.chromiumos.longrunning.StatusH\x00\x12(\n\x08response\x18\x05 \x01(\x0b\x32\x14.google.protobuf.AnyH\x00\x42\x08\n\x06result\"#\n\x13GetOperationRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"\\\n\x15ListOperationsRequest\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x0e\n\x06\x66ilter\x18\x01 \x01(\t\x12\x11\n\tpage_size\x18\x02 \x01(\x05\x12\x12\n\npage_token\x18\x03 \x01(\t\"h\n\x16ListOperationsResponse\x12\x35\n\noperations\x18\x01 \x03(\x0b\x32!.chromiumos.longrunning.Operation\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"&\n\x16\x43\x61ncelOperationRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"&\n\x16\x44\x65leteOperationRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"P\n\x14WaitOperationRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12*\n\x07timeout\x18\x02 \x01(\x0b\x32\x19.google.protobuf.Duration\"=\n\rOperationInfo\x12\x15\n\rresponse_type\x18\x01 \x01(\t\x12\x15\n\rmetadata_type\x18\x02 \x01(\t\"N\n\x06Status\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t\x12%\n\x07\x64\x65tails\x18\x03 \x03(\x0b\x32\x14.google.protobuf.Any2\xff\x03\n\nOperations\x12q\n\x0eListOperations\x12-.chromiumos.longrunning.ListOperationsRequest\x1a..chromiumos.longrunning.ListOperationsResponse\"\x00\x12`\n\x0cGetOperation\x12+.chromiumos.longrunning.GetOperationRequest\x1a!.chromiumos.longrunning.Operation\"\x00\x12[\n\x0f\x44\x65leteOperation\x12..chromiumos.longrunning.DeleteOperationRequest\x1a\x16.google.protobuf.Empty\"\x00\x12[\n\x0f\x43\x61ncelOperation\x12..chromiumos.longrunning.CancelOperationRequest\x1a\x16.google.protobuf.Empty\"\x00\x12\x62\n\rWaitOperation\x12,.chromiumos.longrunning.WaitOperationRequest\x1a!.chromiumos.longrunning.Operation\"\x00:^\n\x0eoperation_info\x12\x1e.google.protobuf.MethodOptions\x18\x9a\x08 \x01(\x0b\x32%.chromiumos.longrunning.OperationInfoB2Z0go.chromium.org/chromiumos/config/go/longrunningb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_any__pb2.DESCRIPTOR,google_dot_protobuf_dot_descriptor__pb2.DESCRIPTOR,google_dot_protobuf_dot_duration__pb2.DESCRIPTOR,google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,])


OPERATION_INFO_FIELD_NUMBER = 1050
operation_info = _descriptor.FieldDescriptor(
  name='operation_info', full_name='chromiumos.longrunning.operation_info', index=0,
  number=1050, type=11, cpp_type=10, label=1,
  has_default_value=False, default_value=None,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  serialized_options=None, file=DESCRIPTOR)


_OPERATION = _descriptor.Descriptor(
  name='Operation',
  full_name='chromiumos.longrunning.Operation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='chromiumos.longrunning.Operation.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='metadata', full_name='chromiumos.longrunning.Operation.metadata', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='done', full_name='chromiumos.longrunning.Operation.done', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='error', full_name='chromiumos.longrunning.Operation.error', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='response', full_name='chromiumos.longrunning.Operation.response', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
    _descriptor.OneofDescriptor(
      name='result', full_name='chromiumos.longrunning.Operation.result',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=190,
  serialized_end=370,
)


_GETOPERATIONREQUEST = _descriptor.Descriptor(
  name='GetOperationRequest',
  full_name='chromiumos.longrunning.GetOperationRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='chromiumos.longrunning.GetOperationRequest.name', index=0,
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
  serialized_start=372,
  serialized_end=407,
)


_LISTOPERATIONSREQUEST = _descriptor.Descriptor(
  name='ListOperationsRequest',
  full_name='chromiumos.longrunning.ListOperationsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='chromiumos.longrunning.ListOperationsRequest.name', index=0,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='filter', full_name='chromiumos.longrunning.ListOperationsRequest.filter', index=1,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='page_size', full_name='chromiumos.longrunning.ListOperationsRequest.page_size', index=2,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='page_token', full_name='chromiumos.longrunning.ListOperationsRequest.page_token', index=3,
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
  serialized_start=409,
  serialized_end=501,
)


_LISTOPERATIONSRESPONSE = _descriptor.Descriptor(
  name='ListOperationsResponse',
  full_name='chromiumos.longrunning.ListOperationsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='operations', full_name='chromiumos.longrunning.ListOperationsResponse.operations', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='next_page_token', full_name='chromiumos.longrunning.ListOperationsResponse.next_page_token', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=503,
  serialized_end=607,
)


_CANCELOPERATIONREQUEST = _descriptor.Descriptor(
  name='CancelOperationRequest',
  full_name='chromiumos.longrunning.CancelOperationRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='chromiumos.longrunning.CancelOperationRequest.name', index=0,
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
  serialized_start=609,
  serialized_end=647,
)


_DELETEOPERATIONREQUEST = _descriptor.Descriptor(
  name='DeleteOperationRequest',
  full_name='chromiumos.longrunning.DeleteOperationRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='chromiumos.longrunning.DeleteOperationRequest.name', index=0,
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
  serialized_start=649,
  serialized_end=687,
)


_WAITOPERATIONREQUEST = _descriptor.Descriptor(
  name='WaitOperationRequest',
  full_name='chromiumos.longrunning.WaitOperationRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='chromiumos.longrunning.WaitOperationRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timeout', full_name='chromiumos.longrunning.WaitOperationRequest.timeout', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=689,
  serialized_end=769,
)


_OPERATIONINFO = _descriptor.Descriptor(
  name='OperationInfo',
  full_name='chromiumos.longrunning.OperationInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='response_type', full_name='chromiumos.longrunning.OperationInfo.response_type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='metadata_type', full_name='chromiumos.longrunning.OperationInfo.metadata_type', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=771,
  serialized_end=832,
)


_STATUS = _descriptor.Descriptor(
  name='Status',
  full_name='chromiumos.longrunning.Status',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='chromiumos.longrunning.Status.code', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='message', full_name='chromiumos.longrunning.Status.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='details', full_name='chromiumos.longrunning.Status.details', index=2,
      number=3, type=11, cpp_type=10, label=3,
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
  serialized_start=834,
  serialized_end=912,
)

_OPERATION.fields_by_name['metadata'].message_type = google_dot_protobuf_dot_any__pb2._ANY
_OPERATION.fields_by_name['error'].message_type = _STATUS
_OPERATION.fields_by_name['response'].message_type = google_dot_protobuf_dot_any__pb2._ANY
_OPERATION.oneofs_by_name['result'].fields.append(
  _OPERATION.fields_by_name['error'])
_OPERATION.fields_by_name['error'].containing_oneof = _OPERATION.oneofs_by_name['result']
_OPERATION.oneofs_by_name['result'].fields.append(
  _OPERATION.fields_by_name['response'])
_OPERATION.fields_by_name['response'].containing_oneof = _OPERATION.oneofs_by_name['result']
_LISTOPERATIONSRESPONSE.fields_by_name['operations'].message_type = _OPERATION
_WAITOPERATIONREQUEST.fields_by_name['timeout'].message_type = google_dot_protobuf_dot_duration__pb2._DURATION
_STATUS.fields_by_name['details'].message_type = google_dot_protobuf_dot_any__pb2._ANY
DESCRIPTOR.message_types_by_name['Operation'] = _OPERATION
DESCRIPTOR.message_types_by_name['GetOperationRequest'] = _GETOPERATIONREQUEST
DESCRIPTOR.message_types_by_name['ListOperationsRequest'] = _LISTOPERATIONSREQUEST
DESCRIPTOR.message_types_by_name['ListOperationsResponse'] = _LISTOPERATIONSRESPONSE
DESCRIPTOR.message_types_by_name['CancelOperationRequest'] = _CANCELOPERATIONREQUEST
DESCRIPTOR.message_types_by_name['DeleteOperationRequest'] = _DELETEOPERATIONREQUEST
DESCRIPTOR.message_types_by_name['WaitOperationRequest'] = _WAITOPERATIONREQUEST
DESCRIPTOR.message_types_by_name['OperationInfo'] = _OPERATIONINFO
DESCRIPTOR.message_types_by_name['Status'] = _STATUS
DESCRIPTOR.extensions_by_name['operation_info'] = operation_info
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Operation = _reflection.GeneratedProtocolMessageType('Operation', (_message.Message,), {
  'DESCRIPTOR' : _OPERATION,
  '__module__' : 'chromiumos.longrunning.operations_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.longrunning.Operation)
  })
_sym_db.RegisterMessage(Operation)

GetOperationRequest = _reflection.GeneratedProtocolMessageType('GetOperationRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETOPERATIONREQUEST,
  '__module__' : 'chromiumos.longrunning.operations_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.longrunning.GetOperationRequest)
  })
_sym_db.RegisterMessage(GetOperationRequest)

ListOperationsRequest = _reflection.GeneratedProtocolMessageType('ListOperationsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTOPERATIONSREQUEST,
  '__module__' : 'chromiumos.longrunning.operations_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.longrunning.ListOperationsRequest)
  })
_sym_db.RegisterMessage(ListOperationsRequest)

ListOperationsResponse = _reflection.GeneratedProtocolMessageType('ListOperationsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTOPERATIONSRESPONSE,
  '__module__' : 'chromiumos.longrunning.operations_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.longrunning.ListOperationsResponse)
  })
_sym_db.RegisterMessage(ListOperationsResponse)

CancelOperationRequest = _reflection.GeneratedProtocolMessageType('CancelOperationRequest', (_message.Message,), {
  'DESCRIPTOR' : _CANCELOPERATIONREQUEST,
  '__module__' : 'chromiumos.longrunning.operations_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.longrunning.CancelOperationRequest)
  })
_sym_db.RegisterMessage(CancelOperationRequest)

DeleteOperationRequest = _reflection.GeneratedProtocolMessageType('DeleteOperationRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEOPERATIONREQUEST,
  '__module__' : 'chromiumos.longrunning.operations_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.longrunning.DeleteOperationRequest)
  })
_sym_db.RegisterMessage(DeleteOperationRequest)

WaitOperationRequest = _reflection.GeneratedProtocolMessageType('WaitOperationRequest', (_message.Message,), {
  'DESCRIPTOR' : _WAITOPERATIONREQUEST,
  '__module__' : 'chromiumos.longrunning.operations_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.longrunning.WaitOperationRequest)
  })
_sym_db.RegisterMessage(WaitOperationRequest)

OperationInfo = _reflection.GeneratedProtocolMessageType('OperationInfo', (_message.Message,), {
  'DESCRIPTOR' : _OPERATIONINFO,
  '__module__' : 'chromiumos.longrunning.operations_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.longrunning.OperationInfo)
  })
_sym_db.RegisterMessage(OperationInfo)

Status = _reflection.GeneratedProtocolMessageType('Status', (_message.Message,), {
  'DESCRIPTOR' : _STATUS,
  '__module__' : 'chromiumos.longrunning.operations_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.longrunning.Status)
  })
_sym_db.RegisterMessage(Status)

operation_info.message_type = _OPERATIONINFO
google_dot_protobuf_dot_descriptor__pb2.MethodOptions.RegisterExtension(operation_info)

DESCRIPTOR._options = None

_OPERATIONS = _descriptor.ServiceDescriptor(
  name='Operations',
  full_name='chromiumos.longrunning.Operations',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=915,
  serialized_end=1426,
  methods=[
  _descriptor.MethodDescriptor(
    name='ListOperations',
    full_name='chromiumos.longrunning.Operations.ListOperations',
    index=0,
    containing_service=None,
    input_type=_LISTOPERATIONSREQUEST,
    output_type=_LISTOPERATIONSRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetOperation',
    full_name='chromiumos.longrunning.Operations.GetOperation',
    index=1,
    containing_service=None,
    input_type=_GETOPERATIONREQUEST,
    output_type=_OPERATION,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='DeleteOperation',
    full_name='chromiumos.longrunning.Operations.DeleteOperation',
    index=2,
    containing_service=None,
    input_type=_DELETEOPERATIONREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='CancelOperation',
    full_name='chromiumos.longrunning.Operations.CancelOperation',
    index=3,
    containing_service=None,
    input_type=_CANCELOPERATIONREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='WaitOperation',
    full_name='chromiumos.longrunning.Operations.WaitOperation',
    index=4,
    containing_service=None,
    input_type=_WAITOPERATIONREQUEST,
    output_type=_OPERATION,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_OPERATIONS)

DESCRIPTOR.services_by_name['Operations'] = _OPERATIONS

# @@protoc_insertion_point(module_scope)
