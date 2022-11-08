# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/test/api/android_provision_metadata.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import message as _message
from chromite.third_party.google.protobuf import reflection as _reflection
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromiumos/test/api/android_provision_metadata.proto',
  package='chromiumos.test.api',
  syntax='proto3',
  serialized_options=b'Z-go.chromium.org/chromiumos/config/go/test/api',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n4chromiumos/test/api/android_provision_metadata.proto\x12\x13\x63hromiumos.test.api\"\xe8\x05\n\nGMSCoreApk\x12\x42\n\x0c\x61rchitecture\x18\x01 \x01(\x0e\x32,.chromiumos.test.api.GMSCoreApk.Architecture\x12=\n\nbuild_type\x18\x02 \x01(\x0e\x32).chromiumos.test.api.GMSCoreApk.BuildType\x12\x43\n\rbuild_purpose\x18\x03 \x01(\x0e\x32,.chromiumos.test.api.GMSCoreApk.BuildPurpose\x12\x38\n\x07\x64\x65nsity\x18\x04 \x01(\x0e\x32\'.chromiumos.test.api.GMSCoreApk.Density\"W\n\x0c\x41rchitecture\x12\x1c\n\x18\x41RCHITECTURE_UNSPECIFIED\x10\x00\x12\t\n\x05\x41RMV7\x10\x01\x12\t\n\x05\x41RM64\x10\x02\x12\x07\n\x03X86\x10\x03\x12\n\n\x06X86_64\x10\x04\"\xc1\x01\n\tBuildType\x12\x1a\n\x16\x42UILD_TYPE_UNSPECIFIED\x10\x00\x12\x11\n\rPHONE_PRE_LMP\x10\x01\x12\r\n\tPHONE_LMP\x10\x02\x12\r\n\tPHONE_MNC\x10\x03\x12\x0c\n\x08PHONE_PI\x10\x04\x12\r\n\tPHONE_RVC\x10\x05\x12\x0c\n\x08PHONE_SC\x10\x06\x12\x0e\n\nPHONE_NEXT\x10\x07\x12\x0c\n\x08PHONE_GO\x10\x08\x12\x0e\n\nPHONE_GO_R\x10\t\x12\x0e\n\nPHONE_GO_S\x10\n\"`\n\x0c\x42uildPurpose\x12\x1d\n\x19\x42UILD_PURPOSE_UNSPECIFIED\x10\x00\x12\x07\n\x03RAW\x10\x01\x12\x0b\n\x07RELEASE\x10\x02\x12\t\n\x05\x44\x45\x42UG\x10\x03\x12\x10\n\x0c\x44\x45\x42UG_SHRUNK\x10\x04\"Y\n\x07\x44\x65nsity\x12\x17\n\x13\x44\x45NSITY_UNSPECIFIED\x10\x00\x12\x08\n\x04MDPI\x10\x01\x12\x08\n\x04HDPI\x10\x02\x12\t\n\x05XHDPI\x10\x03\x12\n\n\x06XXHDPI\x10\x04\x12\n\n\x06\x41LLDPI\x10\x05\"\xc6\x03\n\x0b\x43IPDPackage\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x03ref\x18\x02 \x01(\tH\x00\x12\r\n\x03tag\x18\x03 \x01(\tH\x00\x12\x15\n\x0binstance_id\x18\x04 \x01(\tH\x00\x12\x0e\n\x06server\x18\x05 \x01(\t\x12L\n\x0fpackage_details\x18\x06 \x01(\x0b\x32\x33.chromiumos.test.api.CIPDPackage.CIPDPackageDetails\x1a\x84\x02\n\x12\x43IPDPackageDetails\x12U\n\x0cpackage_type\x18\x01 \x01(\x0e\x32?.chromiumos.test.api.CIPDPackage.CIPDPackageDetails.PackageType\x12?\n\x14gms_core_apk_details\x18\x02 \x01(\x0b\x32\x1f.chromiumos.test.api.GMSCoreApkH\x00\"=\n\x0bPackageType\x12\x1c\n\x18PACKAGE_TYPE_UNSPECIFIED\x10\x00\x12\x10\n\x0cGMS_CORE_APK\x10\x01\x42\x17\n\x15\x61\x64\x64itional_info_oneofB\x0f\n\rversion_oneof\"\xb4\x01\n\x1e\x41ndroidDeviceProvisionMetadata\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x15\n\rserial_number\x18\x02 \x01(\t\x12\x1b\n\x13\x61ssociated_hostname\x18\x03 \x01(\t\x12\x17\n\x0f\x61\x64\x62_vendor_keys\x18\x04 \x03(\t\x12\x37\n\rcipd_packages\x18\x05 \x03(\x0b\x32 .chromiumos.test.api.CIPDPackageB/Z-go.chromium.org/chromiumos/config/go/test/apib\x06proto3'
)



_GMSCOREAPK_ARCHITECTURE = _descriptor.EnumDescriptor(
  name='Architecture',
  full_name='chromiumos.test.api.GMSCoreApk.Architecture',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ARCHITECTURE_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ARMV7', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ARM64', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='X86', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='X86_64', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=350,
  serialized_end=437,
)
_sym_db.RegisterEnumDescriptor(_GMSCOREAPK_ARCHITECTURE)

_GMSCOREAPK_BUILDTYPE = _descriptor.EnumDescriptor(
  name='BuildType',
  full_name='chromiumos.test.api.GMSCoreApk.BuildType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='BUILD_TYPE_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PHONE_PRE_LMP', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PHONE_LMP', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PHONE_MNC', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PHONE_PI', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PHONE_RVC', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PHONE_SC', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PHONE_NEXT', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PHONE_GO', index=8, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PHONE_GO_R', index=9, number=9,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PHONE_GO_S', index=10, number=10,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=440,
  serialized_end=633,
)
_sym_db.RegisterEnumDescriptor(_GMSCOREAPK_BUILDTYPE)

_GMSCOREAPK_BUILDPURPOSE = _descriptor.EnumDescriptor(
  name='BuildPurpose',
  full_name='chromiumos.test.api.GMSCoreApk.BuildPurpose',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='BUILD_PURPOSE_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RAW', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RELEASE', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DEBUG', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DEBUG_SHRUNK', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=635,
  serialized_end=731,
)
_sym_db.RegisterEnumDescriptor(_GMSCOREAPK_BUILDPURPOSE)

_GMSCOREAPK_DENSITY = _descriptor.EnumDescriptor(
  name='Density',
  full_name='chromiumos.test.api.GMSCoreApk.Density',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DENSITY_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MDPI', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='HDPI', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='XHDPI', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='XXHDPI', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ALLDPI', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=733,
  serialized_end=822,
)
_sym_db.RegisterEnumDescriptor(_GMSCOREAPK_DENSITY)

_CIPDPACKAGE_CIPDPACKAGEDETAILS_PACKAGETYPE = _descriptor.EnumDescriptor(
  name='PackageType',
  full_name='chromiumos.test.api.CIPDPackage.CIPDPackageDetails.PackageType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='PACKAGE_TYPE_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GMS_CORE_APK', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1176,
  serialized_end=1237,
)
_sym_db.RegisterEnumDescriptor(_CIPDPACKAGE_CIPDPACKAGEDETAILS_PACKAGETYPE)


_GMSCOREAPK = _descriptor.Descriptor(
  name='GMSCoreApk',
  full_name='chromiumos.test.api.GMSCoreApk',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='architecture', full_name='chromiumos.test.api.GMSCoreApk.architecture', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='build_type', full_name='chromiumos.test.api.GMSCoreApk.build_type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='build_purpose', full_name='chromiumos.test.api.GMSCoreApk.build_purpose', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='density', full_name='chromiumos.test.api.GMSCoreApk.density', index=3,
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
    _GMSCOREAPK_ARCHITECTURE,
    _GMSCOREAPK_BUILDTYPE,
    _GMSCOREAPK_BUILDPURPOSE,
    _GMSCOREAPK_DENSITY,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=78,
  serialized_end=822,
)


_CIPDPACKAGE_CIPDPACKAGEDETAILS = _descriptor.Descriptor(
  name='CIPDPackageDetails',
  full_name='chromiumos.test.api.CIPDPackage.CIPDPackageDetails',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='package_type', full_name='chromiumos.test.api.CIPDPackage.CIPDPackageDetails.package_type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='gms_core_apk_details', full_name='chromiumos.test.api.CIPDPackage.CIPDPackageDetails.gms_core_apk_details', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CIPDPACKAGE_CIPDPACKAGEDETAILS_PACKAGETYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='additional_info_oneof', full_name='chromiumos.test.api.CIPDPackage.CIPDPackageDetails.additional_info_oneof',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=1002,
  serialized_end=1262,
)

_CIPDPACKAGE = _descriptor.Descriptor(
  name='CIPDPackage',
  full_name='chromiumos.test.api.CIPDPackage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='chromiumos.test.api.CIPDPackage.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ref', full_name='chromiumos.test.api.CIPDPackage.ref', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tag', full_name='chromiumos.test.api.CIPDPackage.tag', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='instance_id', full_name='chromiumos.test.api.CIPDPackage.instance_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='server', full_name='chromiumos.test.api.CIPDPackage.server', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='package_details', full_name='chromiumos.test.api.CIPDPackage.package_details', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_CIPDPACKAGE_CIPDPACKAGEDETAILS, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='version_oneof', full_name='chromiumos.test.api.CIPDPackage.version_oneof',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=825,
  serialized_end=1279,
)


_ANDROIDDEVICEPROVISIONMETADATA = _descriptor.Descriptor(
  name='AndroidDeviceProvisionMetadata',
  full_name='chromiumos.test.api.AndroidDeviceProvisionMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='chromiumos.test.api.AndroidDeviceProvisionMetadata.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='serial_number', full_name='chromiumos.test.api.AndroidDeviceProvisionMetadata.serial_number', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='associated_hostname', full_name='chromiumos.test.api.AndroidDeviceProvisionMetadata.associated_hostname', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='adb_vendor_keys', full_name='chromiumos.test.api.AndroidDeviceProvisionMetadata.adb_vendor_keys', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cipd_packages', full_name='chromiumos.test.api.AndroidDeviceProvisionMetadata.cipd_packages', index=4,
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
  serialized_start=1282,
  serialized_end=1462,
)

_GMSCOREAPK.fields_by_name['architecture'].enum_type = _GMSCOREAPK_ARCHITECTURE
_GMSCOREAPK.fields_by_name['build_type'].enum_type = _GMSCOREAPK_BUILDTYPE
_GMSCOREAPK.fields_by_name['build_purpose'].enum_type = _GMSCOREAPK_BUILDPURPOSE
_GMSCOREAPK.fields_by_name['density'].enum_type = _GMSCOREAPK_DENSITY
_GMSCOREAPK_ARCHITECTURE.containing_type = _GMSCOREAPK
_GMSCOREAPK_BUILDTYPE.containing_type = _GMSCOREAPK
_GMSCOREAPK_BUILDPURPOSE.containing_type = _GMSCOREAPK
_GMSCOREAPK_DENSITY.containing_type = _GMSCOREAPK
_CIPDPACKAGE_CIPDPACKAGEDETAILS.fields_by_name['package_type'].enum_type = _CIPDPACKAGE_CIPDPACKAGEDETAILS_PACKAGETYPE
_CIPDPACKAGE_CIPDPACKAGEDETAILS.fields_by_name['gms_core_apk_details'].message_type = _GMSCOREAPK
_CIPDPACKAGE_CIPDPACKAGEDETAILS.containing_type = _CIPDPACKAGE
_CIPDPACKAGE_CIPDPACKAGEDETAILS_PACKAGETYPE.containing_type = _CIPDPACKAGE_CIPDPACKAGEDETAILS
_CIPDPACKAGE_CIPDPACKAGEDETAILS.oneofs_by_name['additional_info_oneof'].fields.append(
  _CIPDPACKAGE_CIPDPACKAGEDETAILS.fields_by_name['gms_core_apk_details'])
_CIPDPACKAGE_CIPDPACKAGEDETAILS.fields_by_name['gms_core_apk_details'].containing_oneof = _CIPDPACKAGE_CIPDPACKAGEDETAILS.oneofs_by_name['additional_info_oneof']
_CIPDPACKAGE.fields_by_name['package_details'].message_type = _CIPDPACKAGE_CIPDPACKAGEDETAILS
_CIPDPACKAGE.oneofs_by_name['version_oneof'].fields.append(
  _CIPDPACKAGE.fields_by_name['ref'])
_CIPDPACKAGE.fields_by_name['ref'].containing_oneof = _CIPDPACKAGE.oneofs_by_name['version_oneof']
_CIPDPACKAGE.oneofs_by_name['version_oneof'].fields.append(
  _CIPDPACKAGE.fields_by_name['tag'])
_CIPDPACKAGE.fields_by_name['tag'].containing_oneof = _CIPDPACKAGE.oneofs_by_name['version_oneof']
_CIPDPACKAGE.oneofs_by_name['version_oneof'].fields.append(
  _CIPDPACKAGE.fields_by_name['instance_id'])
_CIPDPACKAGE.fields_by_name['instance_id'].containing_oneof = _CIPDPACKAGE.oneofs_by_name['version_oneof']
_ANDROIDDEVICEPROVISIONMETADATA.fields_by_name['cipd_packages'].message_type = _CIPDPACKAGE
DESCRIPTOR.message_types_by_name['GMSCoreApk'] = _GMSCOREAPK
DESCRIPTOR.message_types_by_name['CIPDPackage'] = _CIPDPACKAGE
DESCRIPTOR.message_types_by_name['AndroidDeviceProvisionMetadata'] = _ANDROIDDEVICEPROVISIONMETADATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GMSCoreApk = _reflection.GeneratedProtocolMessageType('GMSCoreApk', (_message.Message,), {
  'DESCRIPTOR' : _GMSCOREAPK,
  '__module__' : 'chromiumos.test.api.android_provision_metadata_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.api.GMSCoreApk)
  })
_sym_db.RegisterMessage(GMSCoreApk)

CIPDPackage = _reflection.GeneratedProtocolMessageType('CIPDPackage', (_message.Message,), {

  'CIPDPackageDetails' : _reflection.GeneratedProtocolMessageType('CIPDPackageDetails', (_message.Message,), {
    'DESCRIPTOR' : _CIPDPACKAGE_CIPDPACKAGEDETAILS,
    '__module__' : 'chromiumos.test.api.android_provision_metadata_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.test.api.CIPDPackage.CIPDPackageDetails)
    })
  ,
  'DESCRIPTOR' : _CIPDPACKAGE,
  '__module__' : 'chromiumos.test.api.android_provision_metadata_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.api.CIPDPackage)
  })
_sym_db.RegisterMessage(CIPDPackage)
_sym_db.RegisterMessage(CIPDPackage.CIPDPackageDetails)

AndroidDeviceProvisionMetadata = _reflection.GeneratedProtocolMessageType('AndroidDeviceProvisionMetadata', (_message.Message,), {
  'DESCRIPTOR' : _ANDROIDDEVICEPROVISIONMETADATA,
  '__module__' : 'chromiumos.test.api.android_provision_metadata_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.api.AndroidDeviceProvisionMetadata)
  })
_sym_db.RegisterMessage(AndroidDeviceProvisionMetadata)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
