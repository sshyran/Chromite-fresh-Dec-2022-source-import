# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/config/api/test/tls/wiring.proto
"""Generated protocol buffer code."""
from chromite.third_party.google.protobuf import descriptor as _descriptor
from chromite.third_party.google.protobuf import message as _message
from chromite.third_party.google.protobuf import reflection as _reflection
from chromite.third_party.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen.chromiumos.longrunning import operations_pb2 as chromiumos_dot_longrunning_dot_operations__pb2
from chromite.api.gen.chromiumos.config.api.test.xmlrpc import xmlrpc_pb2 as chromiumos_dot_config_dot_api_dot_test_dot_xmlrpc_dot_xmlrpc__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='chromiumos/config/api/test/tls/wiring.proto',
  package='chromiumos.config.api.test.tls',
  syntax='proto3',
  serialized_options=b'Z1go.chromium.org/chromiumos/config/go/api/test/tls',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n+chromiumos/config/api/test/tls/wiring.proto\x12\x1e\x63hromiumos.config.api.test.tls\x1a\'chromiumos/longrunning/operations.proto\x1a.chromiumos/config/api/test/xmlrpc/xmlrpc.proto\"\x1d\n\rGetDutRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"N\n\x03\x44ut\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x39\n\x08licenses\x18\x02 \x03(\x0b\x32\'.chromiumos.config.api.test.tls.License\"\x9d\x01\n\x07License\x12\x0c\n\x04name\x18\x01 \x01(\t\x12:\n\x04type\x18\x02 \x01(\x0e\x32,.chromiumos.config.api.test.tls.License.Type\"H\n\x04Type\x12\x14\n\x10TYPE_UNSPECIFIED\x10\x00\x12\x12\n\x0eWINDOWS_10_PRO\x10\x01\x12\x16\n\x12MS_OFFICE_STANDARD\x10\x02\"0\n\x12OpenDutPortRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\"4\n\x13OpenDutPortResponse\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\"\xaf\x01\n\x18SetDutPowerSupplyRequest\x12\x0b\n\x03\x64ut\x18\x01 \x01(\t\x12M\n\x05state\x18\x02 \x01(\x0e\x32>.chromiumos.config.api.test.tls.SetDutPowerSupplyRequest.State\"7\n\x05State\x12\x11\n\rSTATE_UNKNOWN\x10\x00\x12\x0c\n\x08STATE_ON\x10\x01\x12\r\n\tSTATE_OFF\x10\x02\"\x80\x02\n\x19SetDutPowerSupplyResponse\x12P\n\x06status\x18\x01 \x01(\x0e\x32@.chromiumos.config.api.test.tls.SetDutPowerSupplyResponse.Status\x12\x0e\n\x06reason\x18\x02 \x01(\t\"\x80\x01\n\x06Status\x12\x12\n\x0eSTATUS_UNKNOWN\x10\x00\x12\r\n\tSTATUS_OK\x10\x01\x12\x12\n\x0eSTATUS_BAD_DUT\x10\x02\x12\x16\n\x12STATUS_BAD_REQUEST\x10\x03\x12\x11\n\rSTATUS_NO_RPM\x10\x04\x12\x14\n\x10STATUS_RPM_ERROR\x10\x05\"3\n\x12\x43\x61\x63heForDutRequest\x12\x0b\n\x03url\x18\x01 \x01(\t\x12\x10\n\x08\x64ut_name\x18\x02 \x01(\t\"\"\n\x13\x43\x61\x63heForDutResponse\x12\x0b\n\x03url\x18\x01 \x01(\t\"\x15\n\x13\x43\x61\x63heForDutMetadata\"g\n\x10\x43\x61llServoRequest\x12\x0b\n\x03\x64ut\x18\x01 \x01(\t\x12\x0e\n\x06method\x18\x02 \x01(\t\x12\x36\n\x04\x61rgs\x18\x03 \x03(\x0b\x32(.chromiumos.config.api.test.xmlrpc.Value\"[\n\x11\x43\x61llServoResponse\x12\x37\n\x05value\x18\x01 \x01(\x0b\x32(.chromiumos.config.api.test.xmlrpc.Value\x12\r\n\x05\x66\x61ult\x18\x02 \x01(\x08\"\\\n\x16\x45xposePortToDutRequest\x12\x10\n\x08\x64ut_name\x18\x01 \x01(\t\x12\x12\n\nlocal_port\x18\x02 \x01(\x05\x12\x1c\n\x14require_remote_proxy\x18\x03 \x01(\x08\"H\n\x17\x45xposePortToDutResponse\x12\x17\n\x0f\x65xposed_address\x18\x01 \x01(\t\x12\x14\n\x0c\x65xposed_port\x18\x02 \x01(\x05\x32\xf6\x05\n\x06Wiring\x12\\\n\x06GetDut\x12-.chromiumos.config.api.test.tls.GetDutRequest\x1a#.chromiumos.config.api.test.tls.Dut\x12v\n\x0bOpenDutPort\x12\x32.chromiumos.config.api.test.tls.OpenDutPortRequest\x1a\x33.chromiumos.config.api.test.tls.OpenDutPortResponse\x12\x88\x01\n\x11SetDutPowerSupply\x12\x38.chromiumos.config.api.test.tls.SetDutPowerSupplyRequest\x1a\x39.chromiumos.config.api.test.tls.SetDutPowerSupplyResponse\x12\x93\x01\n\x0b\x43\x61\x63heForDut\x12\x32.chromiumos.config.api.test.tls.CacheForDutRequest\x1a!.chromiumos.longrunning.Operation\"-\xd2\x41*\n\x13\x43\x61\x63heForDutResponse\x12\x13\x43\x61\x63heForDutMetadata\x12p\n\tCallServo\x12\x30.chromiumos.config.api.test.tls.CallServoRequest\x1a\x31.chromiumos.config.api.test.tls.CallServoResponse\x12\x82\x01\n\x0f\x45xposePortToDut\x12\x36.chromiumos.config.api.test.tls.ExposePortToDutRequest\x1a\x37.chromiumos.config.api.test.tls.ExposePortToDutResponseB3Z1go.chromium.org/chromiumos/config/go/api/test/tlsb\x06proto3'
  ,
  dependencies=[chromiumos_dot_longrunning_dot_operations__pb2.DESCRIPTOR,chromiumos_dot_config_dot_api_dot_test_dot_xmlrpc_dot_xmlrpc__pb2.DESCRIPTOR,])



_LICENSE_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='chromiumos.config.api.test.tls.License.Type',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='TYPE_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WINDOWS_10_PRO', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MS_OFFICE_STANDARD', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=365,
  serialized_end=437,
)
_sym_db.RegisterEnumDescriptor(_LICENSE_TYPE)

_SETDUTPOWERSUPPLYREQUEST_STATE = _descriptor.EnumDescriptor(
  name='State',
  full_name='chromiumos.config.api.test.tls.SetDutPowerSupplyRequest.State',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='STATE_UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STATE_ON', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STATE_OFF', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=664,
  serialized_end=719,
)
_sym_db.RegisterEnumDescriptor(_SETDUTPOWERSUPPLYREQUEST_STATE)

_SETDUTPOWERSUPPLYRESPONSE_STATUS = _descriptor.EnumDescriptor(
  name='Status',
  full_name='chromiumos.config.api.test.tls.SetDutPowerSupplyResponse.Status',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='STATUS_UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STATUS_OK', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STATUS_BAD_DUT', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STATUS_BAD_REQUEST', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STATUS_NO_RPM', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STATUS_RPM_ERROR', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=850,
  serialized_end=978,
)
_sym_db.RegisterEnumDescriptor(_SETDUTPOWERSUPPLYRESPONSE_STATUS)


_GETDUTREQUEST = _descriptor.Descriptor(
  name='GetDutRequest',
  full_name='chromiumos.config.api.test.tls.GetDutRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='chromiumos.config.api.test.tls.GetDutRequest.name', index=0,
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
  serialized_start=168,
  serialized_end=197,
)


_DUT = _descriptor.Descriptor(
  name='Dut',
  full_name='chromiumos.config.api.test.tls.Dut',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='chromiumos.config.api.test.tls.Dut.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='licenses', full_name='chromiumos.config.api.test.tls.Dut.licenses', index=1,
      number=2, type=11, cpp_type=10, label=3,
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
  serialized_start=199,
  serialized_end=277,
)


_LICENSE = _descriptor.Descriptor(
  name='License',
  full_name='chromiumos.config.api.test.tls.License',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='chromiumos.config.api.test.tls.License.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='chromiumos.config.api.test.tls.License.type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _LICENSE_TYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=280,
  serialized_end=437,
)


_OPENDUTPORTREQUEST = _descriptor.Descriptor(
  name='OpenDutPortRequest',
  full_name='chromiumos.config.api.test.tls.OpenDutPortRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='chromiumos.config.api.test.tls.OpenDutPortRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='port', full_name='chromiumos.config.api.test.tls.OpenDutPortRequest.port', index=1,
      number=2, type=5, cpp_type=1, label=1,
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
  serialized_start=439,
  serialized_end=487,
)


_OPENDUTPORTRESPONSE = _descriptor.Descriptor(
  name='OpenDutPortResponse',
  full_name='chromiumos.config.api.test.tls.OpenDutPortResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='address', full_name='chromiumos.config.api.test.tls.OpenDutPortResponse.address', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='port', full_name='chromiumos.config.api.test.tls.OpenDutPortResponse.port', index=1,
      number=2, type=5, cpp_type=1, label=1,
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
  serialized_start=489,
  serialized_end=541,
)


_SETDUTPOWERSUPPLYREQUEST = _descriptor.Descriptor(
  name='SetDutPowerSupplyRequest',
  full_name='chromiumos.config.api.test.tls.SetDutPowerSupplyRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='dut', full_name='chromiumos.config.api.test.tls.SetDutPowerSupplyRequest.dut', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='state', full_name='chromiumos.config.api.test.tls.SetDutPowerSupplyRequest.state', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SETDUTPOWERSUPPLYREQUEST_STATE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=544,
  serialized_end=719,
)


_SETDUTPOWERSUPPLYRESPONSE = _descriptor.Descriptor(
  name='SetDutPowerSupplyResponse',
  full_name='chromiumos.config.api.test.tls.SetDutPowerSupplyResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='chromiumos.config.api.test.tls.SetDutPowerSupplyResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='reason', full_name='chromiumos.config.api.test.tls.SetDutPowerSupplyResponse.reason', index=1,
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
    _SETDUTPOWERSUPPLYRESPONSE_STATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=722,
  serialized_end=978,
)


_CACHEFORDUTREQUEST = _descriptor.Descriptor(
  name='CacheForDutRequest',
  full_name='chromiumos.config.api.test.tls.CacheForDutRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='url', full_name='chromiumos.config.api.test.tls.CacheForDutRequest.url', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dut_name', full_name='chromiumos.config.api.test.tls.CacheForDutRequest.dut_name', index=1,
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
  serialized_start=980,
  serialized_end=1031,
)


_CACHEFORDUTRESPONSE = _descriptor.Descriptor(
  name='CacheForDutResponse',
  full_name='chromiumos.config.api.test.tls.CacheForDutResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='url', full_name='chromiumos.config.api.test.tls.CacheForDutResponse.url', index=0,
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
  serialized_start=1033,
  serialized_end=1067,
)


_CACHEFORDUTMETADATA = _descriptor.Descriptor(
  name='CacheForDutMetadata',
  full_name='chromiumos.config.api.test.tls.CacheForDutMetadata',
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
  serialized_start=1069,
  serialized_end=1090,
)


_CALLSERVOREQUEST = _descriptor.Descriptor(
  name='CallServoRequest',
  full_name='chromiumos.config.api.test.tls.CallServoRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='dut', full_name='chromiumos.config.api.test.tls.CallServoRequest.dut', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='method', full_name='chromiumos.config.api.test.tls.CallServoRequest.method', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='args', full_name='chromiumos.config.api.test.tls.CallServoRequest.args', index=2,
      number=3, type=11, cpp_type=10, label=3,
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
  serialized_start=1092,
  serialized_end=1195,
)


_CALLSERVORESPONSE = _descriptor.Descriptor(
  name='CallServoResponse',
  full_name='chromiumos.config.api.test.tls.CallServoResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='chromiumos.config.api.test.tls.CallServoResponse.value', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fault', full_name='chromiumos.config.api.test.tls.CallServoResponse.fault', index=1,
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
  serialized_start=1197,
  serialized_end=1288,
)


_EXPOSEPORTTODUTREQUEST = _descriptor.Descriptor(
  name='ExposePortToDutRequest',
  full_name='chromiumos.config.api.test.tls.ExposePortToDutRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='dut_name', full_name='chromiumos.config.api.test.tls.ExposePortToDutRequest.dut_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='local_port', full_name='chromiumos.config.api.test.tls.ExposePortToDutRequest.local_port', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='require_remote_proxy', full_name='chromiumos.config.api.test.tls.ExposePortToDutRequest.require_remote_proxy', index=2,
      number=3, type=8, cpp_type=7, label=1,
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
  serialized_start=1290,
  serialized_end=1382,
)


_EXPOSEPORTTODUTRESPONSE = _descriptor.Descriptor(
  name='ExposePortToDutResponse',
  full_name='chromiumos.config.api.test.tls.ExposePortToDutResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='exposed_address', full_name='chromiumos.config.api.test.tls.ExposePortToDutResponse.exposed_address', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='exposed_port', full_name='chromiumos.config.api.test.tls.ExposePortToDutResponse.exposed_port', index=1,
      number=2, type=5, cpp_type=1, label=1,
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
  serialized_start=1384,
  serialized_end=1456,
)

_DUT.fields_by_name['licenses'].message_type = _LICENSE
_LICENSE.fields_by_name['type'].enum_type = _LICENSE_TYPE
_LICENSE_TYPE.containing_type = _LICENSE
_SETDUTPOWERSUPPLYREQUEST.fields_by_name['state'].enum_type = _SETDUTPOWERSUPPLYREQUEST_STATE
_SETDUTPOWERSUPPLYREQUEST_STATE.containing_type = _SETDUTPOWERSUPPLYREQUEST
_SETDUTPOWERSUPPLYRESPONSE.fields_by_name['status'].enum_type = _SETDUTPOWERSUPPLYRESPONSE_STATUS
_SETDUTPOWERSUPPLYRESPONSE_STATUS.containing_type = _SETDUTPOWERSUPPLYRESPONSE
_CALLSERVOREQUEST.fields_by_name['args'].message_type = chromiumos_dot_config_dot_api_dot_test_dot_xmlrpc_dot_xmlrpc__pb2._VALUE
_CALLSERVORESPONSE.fields_by_name['value'].message_type = chromiumos_dot_config_dot_api_dot_test_dot_xmlrpc_dot_xmlrpc__pb2._VALUE
DESCRIPTOR.message_types_by_name['GetDutRequest'] = _GETDUTREQUEST
DESCRIPTOR.message_types_by_name['Dut'] = _DUT
DESCRIPTOR.message_types_by_name['License'] = _LICENSE
DESCRIPTOR.message_types_by_name['OpenDutPortRequest'] = _OPENDUTPORTREQUEST
DESCRIPTOR.message_types_by_name['OpenDutPortResponse'] = _OPENDUTPORTRESPONSE
DESCRIPTOR.message_types_by_name['SetDutPowerSupplyRequest'] = _SETDUTPOWERSUPPLYREQUEST
DESCRIPTOR.message_types_by_name['SetDutPowerSupplyResponse'] = _SETDUTPOWERSUPPLYRESPONSE
DESCRIPTOR.message_types_by_name['CacheForDutRequest'] = _CACHEFORDUTREQUEST
DESCRIPTOR.message_types_by_name['CacheForDutResponse'] = _CACHEFORDUTRESPONSE
DESCRIPTOR.message_types_by_name['CacheForDutMetadata'] = _CACHEFORDUTMETADATA
DESCRIPTOR.message_types_by_name['CallServoRequest'] = _CALLSERVOREQUEST
DESCRIPTOR.message_types_by_name['CallServoResponse'] = _CALLSERVORESPONSE
DESCRIPTOR.message_types_by_name['ExposePortToDutRequest'] = _EXPOSEPORTTODUTREQUEST
DESCRIPTOR.message_types_by_name['ExposePortToDutResponse'] = _EXPOSEPORTTODUTRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetDutRequest = _reflection.GeneratedProtocolMessageType('GetDutRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETDUTREQUEST,
  '__module__' : 'chromiumos.config.api.test.tls.wiring_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.test.tls.GetDutRequest)
  })
_sym_db.RegisterMessage(GetDutRequest)

Dut = _reflection.GeneratedProtocolMessageType('Dut', (_message.Message,), {
  'DESCRIPTOR' : _DUT,
  '__module__' : 'chromiumos.config.api.test.tls.wiring_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.test.tls.Dut)
  })
_sym_db.RegisterMessage(Dut)

License = _reflection.GeneratedProtocolMessageType('License', (_message.Message,), {
  'DESCRIPTOR' : _LICENSE,
  '__module__' : 'chromiumos.config.api.test.tls.wiring_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.test.tls.License)
  })
_sym_db.RegisterMessage(License)

OpenDutPortRequest = _reflection.GeneratedProtocolMessageType('OpenDutPortRequest', (_message.Message,), {
  'DESCRIPTOR' : _OPENDUTPORTREQUEST,
  '__module__' : 'chromiumos.config.api.test.tls.wiring_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.test.tls.OpenDutPortRequest)
  })
_sym_db.RegisterMessage(OpenDutPortRequest)

OpenDutPortResponse = _reflection.GeneratedProtocolMessageType('OpenDutPortResponse', (_message.Message,), {
  'DESCRIPTOR' : _OPENDUTPORTRESPONSE,
  '__module__' : 'chromiumos.config.api.test.tls.wiring_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.test.tls.OpenDutPortResponse)
  })
_sym_db.RegisterMessage(OpenDutPortResponse)

SetDutPowerSupplyRequest = _reflection.GeneratedProtocolMessageType('SetDutPowerSupplyRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETDUTPOWERSUPPLYREQUEST,
  '__module__' : 'chromiumos.config.api.test.tls.wiring_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.test.tls.SetDutPowerSupplyRequest)
  })
_sym_db.RegisterMessage(SetDutPowerSupplyRequest)

SetDutPowerSupplyResponse = _reflection.GeneratedProtocolMessageType('SetDutPowerSupplyResponse', (_message.Message,), {
  'DESCRIPTOR' : _SETDUTPOWERSUPPLYRESPONSE,
  '__module__' : 'chromiumos.config.api.test.tls.wiring_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.test.tls.SetDutPowerSupplyResponse)
  })
_sym_db.RegisterMessage(SetDutPowerSupplyResponse)

CacheForDutRequest = _reflection.GeneratedProtocolMessageType('CacheForDutRequest', (_message.Message,), {
  'DESCRIPTOR' : _CACHEFORDUTREQUEST,
  '__module__' : 'chromiumos.config.api.test.tls.wiring_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.test.tls.CacheForDutRequest)
  })
_sym_db.RegisterMessage(CacheForDutRequest)

CacheForDutResponse = _reflection.GeneratedProtocolMessageType('CacheForDutResponse', (_message.Message,), {
  'DESCRIPTOR' : _CACHEFORDUTRESPONSE,
  '__module__' : 'chromiumos.config.api.test.tls.wiring_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.test.tls.CacheForDutResponse)
  })
_sym_db.RegisterMessage(CacheForDutResponse)

CacheForDutMetadata = _reflection.GeneratedProtocolMessageType('CacheForDutMetadata', (_message.Message,), {
  'DESCRIPTOR' : _CACHEFORDUTMETADATA,
  '__module__' : 'chromiumos.config.api.test.tls.wiring_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.test.tls.CacheForDutMetadata)
  })
_sym_db.RegisterMessage(CacheForDutMetadata)

CallServoRequest = _reflection.GeneratedProtocolMessageType('CallServoRequest', (_message.Message,), {
  'DESCRIPTOR' : _CALLSERVOREQUEST,
  '__module__' : 'chromiumos.config.api.test.tls.wiring_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.test.tls.CallServoRequest)
  })
_sym_db.RegisterMessage(CallServoRequest)

CallServoResponse = _reflection.GeneratedProtocolMessageType('CallServoResponse', (_message.Message,), {
  'DESCRIPTOR' : _CALLSERVORESPONSE,
  '__module__' : 'chromiumos.config.api.test.tls.wiring_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.test.tls.CallServoResponse)
  })
_sym_db.RegisterMessage(CallServoResponse)

ExposePortToDutRequest = _reflection.GeneratedProtocolMessageType('ExposePortToDutRequest', (_message.Message,), {
  'DESCRIPTOR' : _EXPOSEPORTTODUTREQUEST,
  '__module__' : 'chromiumos.config.api.test.tls.wiring_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.test.tls.ExposePortToDutRequest)
  })
_sym_db.RegisterMessage(ExposePortToDutRequest)

ExposePortToDutResponse = _reflection.GeneratedProtocolMessageType('ExposePortToDutResponse', (_message.Message,), {
  'DESCRIPTOR' : _EXPOSEPORTTODUTRESPONSE,
  '__module__' : 'chromiumos.config.api.test.tls.wiring_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.config.api.test.tls.ExposePortToDutResponse)
  })
_sym_db.RegisterMessage(ExposePortToDutResponse)


DESCRIPTOR._options = None

_WIRING = _descriptor.ServiceDescriptor(
  name='Wiring',
  full_name='chromiumos.config.api.test.tls.Wiring',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1459,
  serialized_end=2217,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetDut',
    full_name='chromiumos.config.api.test.tls.Wiring.GetDut',
    index=0,
    containing_service=None,
    input_type=_GETDUTREQUEST,
    output_type=_DUT,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='OpenDutPort',
    full_name='chromiumos.config.api.test.tls.Wiring.OpenDutPort',
    index=1,
    containing_service=None,
    input_type=_OPENDUTPORTREQUEST,
    output_type=_OPENDUTPORTRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='SetDutPowerSupply',
    full_name='chromiumos.config.api.test.tls.Wiring.SetDutPowerSupply',
    index=2,
    containing_service=None,
    input_type=_SETDUTPOWERSUPPLYREQUEST,
    output_type=_SETDUTPOWERSUPPLYRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='CacheForDut',
    full_name='chromiumos.config.api.test.tls.Wiring.CacheForDut',
    index=3,
    containing_service=None,
    input_type=_CACHEFORDUTREQUEST,
    output_type=chromiumos_dot_longrunning_dot_operations__pb2._OPERATION,
    serialized_options=b'\322A*\n\023CacheForDutResponse\022\023CacheForDutMetadata',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='CallServo',
    full_name='chromiumos.config.api.test.tls.Wiring.CallServo',
    index=4,
    containing_service=None,
    input_type=_CALLSERVOREQUEST,
    output_type=_CALLSERVORESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ExposePortToDut',
    full_name='chromiumos.config.api.test.tls.Wiring.ExposePortToDut',
    index=5,
    containing_service=None,
    input_type=_EXPOSEPORTTODUTREQUEST,
    output_type=_EXPOSEPORTTODUTRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_WIRING)

DESCRIPTOR.services_by_name['Wiring'] = _WIRING

# @@protoc_insertion_point(module_scope)