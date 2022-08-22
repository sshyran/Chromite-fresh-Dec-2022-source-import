# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/test/api/cros_publish_service.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import message as _message
from chromite.third_party.google.protobuf import reflection as _reflection
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.chromiumos.longrunning import operations_pb2 as chromiumos_dot_longrunning_dot_operations__pb2
from chromite.third_party.google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from chromite.api.gen.chromiumos import storage_path_pb2 as chromiumos_dot_storage__path__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromiumos/test/api/cros_publish_service.proto',
  package='chromiumos.test.api',
  syntax='proto3',
  serialized_options=b'Z-go.chromium.org/chromiumos/config/go/test/api',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n.chromiumos/test/api/cros_publish_service.proto\x12\x13\x63hromiumos.test.api\x1a\'chromiumos/longrunning/operations.proto\x1a\x19google/protobuf/any.proto\x1a\x1d\x63hromiumos/storage_path.proto\"\x81\x01\n\x0ePublishRequest\x12\x32\n\x11\x61rtifact_dir_path\x18\x01 \x01(\x0b\x32\x17.chromiumos.StoragePath\x12\x13\n\x0bretry_count\x18\x02 \x01(\x05\x12&\n\x08metadata\x18\x03 \x01(\x0b\x32\x14.google.protobuf.Any\"\xd5\x01\n\x0fPublishResponse\x12;\n\x06status\x18\x01 \x01(\x0e\x32+.chromiumos.test.api.PublishResponse.Status\x12\x0f\n\x07message\x18\x02 \x01(\t\x12&\n\x08metadata\x18\x03 \x01(\x0b\x32\x14.google.protobuf.Any\"L\n\x06Status\x12\x12\n\x0eSTATUS_SUCCESS\x10\x00\x12\x1a\n\x16STATUS_INVALID_REQUEST\x10\x01\x12\x12\n\x0eSTATUS_FAILURE\x10\x02\x32\x91\x01\n\x15GenericPublishService\x12x\n\x07Publish\x12#.chromiumos.test.api.PublishRequest\x1a!.chromiumos.longrunning.Operation\"%\xd2\x41\"\n\x0fPublishResponse\x12\x0fPublishMetadataB/Z-go.chromium.org/chromiumos/config/go/test/apib\x06proto3'
  ,
  dependencies=[chromiumos_dot_longrunning_dot_operations__pb2.DESCRIPTOR,google_dot_protobuf_dot_any__pb2.DESCRIPTOR,chromiumos_dot_storage__path__pb2.DESCRIPTOR,])



_PUBLISHRESPONSE_STATUS = _descriptor.EnumDescriptor(
  name='Status',
  full_name='chromiumos.test.api.PublishResponse.Status',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='STATUS_SUCCESS', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STATUS_INVALID_REQUEST', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STATUS_FAILURE', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=440,
  serialized_end=516,
)
_sym_db.RegisterEnumDescriptor(_PUBLISHRESPONSE_STATUS)


_PUBLISHREQUEST = _descriptor.Descriptor(
  name='PublishRequest',
  full_name='chromiumos.test.api.PublishRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='artifact_dir_path', full_name='chromiumos.test.api.PublishRequest.artifact_dir_path', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='retry_count', full_name='chromiumos.test.api.PublishRequest.retry_count', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='metadata', full_name='chromiumos.test.api.PublishRequest.metadata', index=2,
      number=3, type=11, cpp_type=10, label=1,
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
  serialized_start=171,
  serialized_end=300,
)


_PUBLISHRESPONSE = _descriptor.Descriptor(
  name='PublishResponse',
  full_name='chromiumos.test.api.PublishResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='chromiumos.test.api.PublishResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='chromiumos.test.api.PublishResponse.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='metadata', full_name='chromiumos.test.api.PublishResponse.metadata', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _PUBLISHRESPONSE_STATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=303,
  serialized_end=516,
)

_PUBLISHREQUEST.fields_by_name['artifact_dir_path'].message_type = chromiumos_dot_storage__path__pb2._STORAGEPATH
_PUBLISHREQUEST.fields_by_name['metadata'].message_type = google_dot_protobuf_dot_any__pb2._ANY
_PUBLISHRESPONSE.fields_by_name['status'].enum_type = _PUBLISHRESPONSE_STATUS
_PUBLISHRESPONSE.fields_by_name['metadata'].message_type = google_dot_protobuf_dot_any__pb2._ANY
_PUBLISHRESPONSE_STATUS.containing_type = _PUBLISHRESPONSE
DESCRIPTOR.message_types_by_name['PublishRequest'] = _PUBLISHREQUEST
DESCRIPTOR.message_types_by_name['PublishResponse'] = _PUBLISHRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PublishRequest = _reflection.GeneratedProtocolMessageType('PublishRequest', (_message.Message,), {
  'DESCRIPTOR' : _PUBLISHREQUEST,
  '__module__' : 'chromiumos.test.api.cros_publish_service_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.api.PublishRequest)
  })
_sym_db.RegisterMessage(PublishRequest)

PublishResponse = _reflection.GeneratedProtocolMessageType('PublishResponse', (_message.Message,), {
  'DESCRIPTOR' : _PUBLISHRESPONSE,
  '__module__' : 'chromiumos.test.api.cros_publish_service_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.api.PublishResponse)
  })
_sym_db.RegisterMessage(PublishResponse)


DESCRIPTOR._options = None

_GENERICPUBLISHSERVICE = _descriptor.ServiceDescriptor(
  name='GenericPublishService',
  full_name='chromiumos.test.api.GenericPublishService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=519,
  serialized_end=664,
  methods=[
  _descriptor.MethodDescriptor(
    name='Publish',
    full_name='chromiumos.test.api.GenericPublishService.Publish',
    index=0,
    containing_service=None,
    input_type=_PUBLISHREQUEST,
    output_type=chromiumos_dot_longrunning_dot_operations__pb2._OPERATION,
    serialized_options=b'\322A\"\n\017PublishResponse\022\017PublishMetadata',
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_GENERICPUBLISHSERVICE)

DESCRIPTOR.services_by_name['GenericPublishService'] = _GENERICPUBLISHSERVICE

# @@protoc_insertion_point(module_scope)
