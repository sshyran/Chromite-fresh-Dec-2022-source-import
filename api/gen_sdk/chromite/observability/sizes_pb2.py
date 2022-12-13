# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromite/observability/sizes.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen_sdk.chromiumos import common_pb2 as chromiumos_dot_common__pb2
from chromite.api.gen_sdk.chromite.observability import shared_pb2 as chromite_dot_observability_dot_shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"chromite/observability/sizes.proto\x12\x16\x63hromite.observability\x1a\x17\x63hromiumos/common.proto\x1a#chromite/observability/shared.proto\"\xdc\x01\n\x1aImageSizeObservabilityData\x12\x41\n\x10\x62uilder_metadata\x18\x01 \x01(\x0b\x32\'.chromite.observability.BuilderMetadata\x12\x44\n\x12\x62uild_version_data\x18\x02 \x01(\x0b\x32(.chromite.observability.BuildVersionData\x12\x35\n\nimage_data\x18\x03 \x03(\x0b\x32!.chromite.observability.ImageData\"\x80\x01\n\tImageData\x12)\n\nimage_type\x18\x01 \x01(\x0e\x32\x15.chromiumos.ImageType\x12H\n\x14image_partition_data\x18\x02 \x03(\x0b\x32*.chromite.observability.ImagePartitionData\"\x7f\n\x12ImagePartitionData\x12\x16\n\x0epartition_name\x18\x01 \x01(\t\x12\x16\n\x0epartition_size\x18\x02 \x01(\x04\x12\x39\n\x08packages\x18\x03 \x03(\x0b\x32\'.chromite.observability.PackageSizeData\"^\n\x0fPackageSizeData\x12=\n\nidentifier\x18\x01 \x01(\x0b\x32).chromite.observability.PackageIdentifier\x12\x0c\n\x04size\x18\x02 \x01(\x04\"\x8f\x01\n\x11PackageIdentifier\x12\x39\n\x0cpackage_name\x18\x01 \x01(\x0b\x32#.chromite.observability.PackageName\x12?\n\x0fpackage_version\x18\x02 \x01(\x0b\x32&.chromite.observability.PackageVersion\"C\n\x0bPackageName\x12\x0c\n\x04\x61tom\x18\x01 \x01(\t\x12\x10\n\x08\x63\x61tegory\x18\x02 \x01(\t\x12\x14\n\x0cpackage_name\x18\x03 \x01(\t\"w\n\x0ePackageVersion\x12\r\n\x05major\x18\x01 \x01(\r\x12\r\n\x05minor\x18\x02 \x01(\r\x12\r\n\x05patch\x18\x03 \x01(\r\x12\x10\n\x08\x65xtended\x18\x04 \x01(\r\x12\x10\n\x08revision\x18\x05 \x01(\r\x12\x14\n\x0c\x66ull_version\x18\x06 \x01(\tBBZ@go.chromium.org/chromiumos/infra/proto/go/chromite/observabilityb\x06proto3')



_IMAGESIZEOBSERVABILITYDATA = DESCRIPTOR.message_types_by_name['ImageSizeObservabilityData']
_IMAGEDATA = DESCRIPTOR.message_types_by_name['ImageData']
_IMAGEPARTITIONDATA = DESCRIPTOR.message_types_by_name['ImagePartitionData']
_PACKAGESIZEDATA = DESCRIPTOR.message_types_by_name['PackageSizeData']
_PACKAGEIDENTIFIER = DESCRIPTOR.message_types_by_name['PackageIdentifier']
_PACKAGENAME = DESCRIPTOR.message_types_by_name['PackageName']
_PACKAGEVERSION = DESCRIPTOR.message_types_by_name['PackageVersion']
ImageSizeObservabilityData = _reflection.GeneratedProtocolMessageType('ImageSizeObservabilityData', (_message.Message,), {
  'DESCRIPTOR' : _IMAGESIZEOBSERVABILITYDATA,
  '__module__' : 'chromite.observability.sizes_pb2'
  # @@protoc_insertion_point(class_scope:chromite.observability.ImageSizeObservabilityData)
  })
_sym_db.RegisterMessage(ImageSizeObservabilityData)

ImageData = _reflection.GeneratedProtocolMessageType('ImageData', (_message.Message,), {
  'DESCRIPTOR' : _IMAGEDATA,
  '__module__' : 'chromite.observability.sizes_pb2'
  # @@protoc_insertion_point(class_scope:chromite.observability.ImageData)
  })
_sym_db.RegisterMessage(ImageData)

ImagePartitionData = _reflection.GeneratedProtocolMessageType('ImagePartitionData', (_message.Message,), {
  'DESCRIPTOR' : _IMAGEPARTITIONDATA,
  '__module__' : 'chromite.observability.sizes_pb2'
  # @@protoc_insertion_point(class_scope:chromite.observability.ImagePartitionData)
  })
_sym_db.RegisterMessage(ImagePartitionData)

PackageSizeData = _reflection.GeneratedProtocolMessageType('PackageSizeData', (_message.Message,), {
  'DESCRIPTOR' : _PACKAGESIZEDATA,
  '__module__' : 'chromite.observability.sizes_pb2'
  # @@protoc_insertion_point(class_scope:chromite.observability.PackageSizeData)
  })
_sym_db.RegisterMessage(PackageSizeData)

PackageIdentifier = _reflection.GeneratedProtocolMessageType('PackageIdentifier', (_message.Message,), {
  'DESCRIPTOR' : _PACKAGEIDENTIFIER,
  '__module__' : 'chromite.observability.sizes_pb2'
  # @@protoc_insertion_point(class_scope:chromite.observability.PackageIdentifier)
  })
_sym_db.RegisterMessage(PackageIdentifier)

PackageName = _reflection.GeneratedProtocolMessageType('PackageName', (_message.Message,), {
  'DESCRIPTOR' : _PACKAGENAME,
  '__module__' : 'chromite.observability.sizes_pb2'
  # @@protoc_insertion_point(class_scope:chromite.observability.PackageName)
  })
_sym_db.RegisterMessage(PackageName)

PackageVersion = _reflection.GeneratedProtocolMessageType('PackageVersion', (_message.Message,), {
  'DESCRIPTOR' : _PACKAGEVERSION,
  '__module__' : 'chromite.observability.sizes_pb2'
  # @@protoc_insertion_point(class_scope:chromite.observability.PackageVersion)
  })
_sym_db.RegisterMessage(PackageVersion)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z@go.chromium.org/chromiumos/infra/proto/go/chromite/observability'
  _IMAGESIZEOBSERVABILITYDATA._serialized_start=125
  _IMAGESIZEOBSERVABILITYDATA._serialized_end=345
  _IMAGEDATA._serialized_start=348
  _IMAGEDATA._serialized_end=476
  _IMAGEPARTITIONDATA._serialized_start=478
  _IMAGEPARTITIONDATA._serialized_end=605
  _PACKAGESIZEDATA._serialized_start=607
  _PACKAGESIZEDATA._serialized_end=701
  _PACKAGEIDENTIFIER._serialized_start=704
  _PACKAGEIDENTIFIER._serialized_end=847
  _PACKAGENAME._serialized_start=849
  _PACKAGENAME._serialized_end=916
  _PACKAGEVERSION._serialized_start=918
  _PACKAGEVERSION._serialized_end=1037
# @@protoc_insertion_point(module_scope)
