# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chromiumos/test/lab/api/dut.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen_sdk.chromiumos.config.api import device_config_id_pb2 as chromiumos_dot_config_dot_api_dot_device__config__id__pb2
from chromite.api.gen_sdk.chromiumos.test.lab.api import ip_endpoint_pb2 as chromiumos_dot_test_dot_lab_dot_api_dot_ip__endpoint__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!chromiumos/test/lab/api/dut.proto\x12\x17\x63hromiumos.test.lab.api\x1a,chromiumos/config/api/device_config_id.proto\x1a)chromiumos/test/lab/api/ip_endpoint.proto\"\x94\n\n\x03\x44ut\x12+\n\x02id\x18\x01 \x01(\x0b\x32\x1f.chromiumos.test.lab.api.Dut.Id\x12\x39\n\x08\x63hromeos\x18\x02 \x01(\x0b\x32%.chromiumos.test.lab.api.Dut.ChromeOSH\x00\x12\x37\n\x07\x61ndroid\x18\x03 \x01(\x0b\x32$.chromiumos.test.lab.api.Dut.AndroidH\x00\x12:\n\x0c\x63\x61\x63he_server\x18\x04 \x01(\x0b\x32$.chromiumos.test.lab.api.CacheServer\x1a\x13\n\x02Id\x12\r\n\x05value\x18\x01 \x01(\t\x1a\xe5\x06\n\x08\x43hromeOS\x12?\n\x10\x64\x65vice_config_id\x18\x03 \x01(\x0b\x32%.chromiumos.config.api.DeviceConfigId\x12\x30\n\x03ssh\x18\x02 \x01(\x0b\x32#.chromiumos.test.lab.api.IpEndpoint\x12\x0c\n\x04name\x18\x0f \x01(\t\x12\x34\n\tdut_model\x18\x0e \x01(\x0b\x32!.chromiumos.test.lab.api.DutModel\x12-\n\x05servo\x18\x04 \x01(\x0b\x32\x1e.chromiumos.test.lab.api.Servo\x12\x35\n\tchameleon\x18\x05 \x01(\x0b\x32\".chromiumos.test.lab.api.Chameleon\x12)\n\x03rpm\x18\x06 \x01(\x0b\x32\x1c.chromiumos.test.lab.api.RPM\x12\x41\n\x10\x65xternal_cameras\x18\x07 \x03(\x0b\x32\'.chromiumos.test.lab.api.ExternalCamera\x12-\n\x05\x61udio\x18\x08 \x01(\x0b\x32\x1e.chromiumos.test.lab.api.Audio\x12+\n\x04wifi\x18\t \x01(\x0b\x32\x1d.chromiumos.test.lab.api.Wifi\x12-\n\x05touch\x18\n \x01(\x0b\x32\x1e.chromiumos.test.lab.api.Touch\x12\x35\n\tcamerabox\x18\x0b \x01(\x0b\x32\".chromiumos.test.lab.api.Camerabox\x12.\n\x06\x63\x61\x62les\x18\x0c \x03(\x0b\x32\x1e.chromiumos.test.lab.api.Cable\x12\x33\n\x08\x63\x65llular\x18\r \x01(\x0b\x32!.chromiumos.test.lab.api.Cellular\x12\x16\n\x0ehwid_component\x18\x10 \x03(\t\x12?\n\x0f\x62luetooth_peers\x18\x11 \x03(\x0b\x32&.chromiumos.test.lab.api.BluetoothPeer\x12\x0b\n\x03sku\x18\x12 \x01(\t\x12\x0c\n\x04hwid\x18\x13 \x01(\t\x12-\n\x05phase\x18\x14 \x01(\x0e\x32\x1e.chromiumos.test.lab.api.PhaseJ\x04\x08\x01\x10\x02\x1a\xa6\x01\n\x07\x41ndroid\x12@\n\x13\x61ssociated_hostname\x18\x01 \x01(\x0b\x32#.chromiumos.test.lab.api.IpEndpoint\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x15\n\rserial_number\x18\x03 \x01(\t\x12\x34\n\tdut_model\x18\x04 \x01(\x0b\x32!.chromiumos.test.lab.api.DutModelB\n\n\x08\x64ut_type\"4\n\x08\x44utModel\x12\x14\n\x0c\x62uild_target\x18\x01 \x01(\t\x12\x12\n\nmodel_name\x18\x02 \x01(\t\"\x8f\x01\n\x0b\x44utTopology\x12\x33\n\x02id\x18\x03 \x01(\x0b\x32\'.chromiumos.test.lab.api.DutTopology.Id\x12*\n\x04\x64uts\x18\x04 \x03(\x0b\x32\x1c.chromiumos.test.lab.api.Dut\x1a\x13\n\x02Id\x12\r\n\x05value\x18\x01 \x01(\tJ\x04\x08\x01\x10\x02J\x04\x08\x02\x10\x03\")\n\x05\x41udio\x12\x11\n\taudio_box\x18\x01 \x01(\x08\x12\r\n\x05\x61trus\x18\x02 \x01(\x08\"\x95\x01\n\x05\x43\x61\x62le\x12\x31\n\x04type\x18\x01 \x01(\x0e\x32#.chromiumos.test.lab.api.Cable.Type\"Y\n\x04Type\x12\x14\n\x10TYPE_UNSPECIFIED\x10\x00\x12\r\n\tAUDIOJACK\x10\x01\x12\x0c\n\x08USBAUDIO\x10\x02\x12\x0f\n\x0bUSBPRINTING\x10\x03\x12\r\n\tHDMIAUDIO\x10\x04\"C\n\x0b\x43\x61\x63heServer\x12\x34\n\x07\x61\x64\x64ress\x18\x01 \x01(\x0b\x32#.chromiumos.test.lab.api.IpEndpoint\"}\n\tCamerabox\x12\x39\n\x06\x66\x61\x63ing\x18\x01 \x01(\x0e\x32).chromiumos.test.lab.api.Camerabox.Facing\"5\n\x06\x46\x61\x63ing\x12\x16\n\x12\x46\x41\x43ING_UNSPECIFIED\x10\x00\x12\x08\n\x04\x42\x41\x43K\x10\x01\x12\t\n\x05\x46RONT\x10\x02\"\x92\x01\n\x08\x43\x65llular\x12=\n\toperators\x18\x01 \x03(\x0e\x32*.chromiumos.test.lab.api.Cellular.Operator\"G\n\x08Operator\x12\x18\n\x14OPERATOR_UNSPECIFIED\x10\x00\x12\x07\n\x03\x41TT\x10\x01\x12\x0b\n\x07VERIZON\x10\x02\x12\x0b\n\x07TMOBILE\x10\x03\"\xf2\x01\n\tChameleon\x12\x42\n\x0bperipherals\x18\x01 \x03(\x0e\x32-.chromiumos.test.lab.api.Chameleon.Peripheral\x12\x13\n\x0b\x61udio_board\x18\x02 \x01(\x08\"\x8b\x01\n\nPeripheral\x12\x1a\n\x16PREIPHERAL_UNSPECIFIED\x10\x00\x12\n\n\x06\x42T_HID\x10\x01\x12\x06\n\x02\x44P\x10\x02\x12\x0b\n\x07\x44P_HDMI\x10\x03\x12\x07\n\x03VGA\x10\x04\x12\x08\n\x04HDMI\x10\x05\x12\x0e\n\nBT_BLE_HID\x10\x06\x12\x10\n\x0c\x42T_A2DP_SINK\x10\x07\x12\x0b\n\x07\x42T_PEER\x10\x08\"\x83\x01\n\x0e\x45xternalCamera\x12:\n\x04type\x18\x01 \x01(\x0e\x32,.chromiumos.test.lab.api.ExternalCamera.Type\"5\n\x04Type\x12\x14\n\x10TYPE_UNSPECIFIED\x10\x00\x12\n\n\x06HUDDLY\x10\x01\x12\x0b\n\x07PTZPRO2\x10\x02\"\x16\n\x03RPM\x12\x0f\n\x07present\x18\x01 \x01(\x08\"e\n\x05Servo\x12\x0f\n\x07present\x18\x01 \x01(\x08\x12;\n\x0eservod_address\x18\x02 \x01(\x0b\x32#.chromiumos.test.lab.api.IpEndpoint\x12\x0e\n\x06serial\x18\x03 \x01(\t\"\x15\n\x05Touch\x12\x0c\n\x04mimo\x18\x01 \x01(\x08\"\xe6\x01\n\x04Wifi\x12>\n\x0b\x65nvironment\x18\x01 \x01(\x0e\x32).chromiumos.test.lab.api.Wifi.Environment\x12\x35\n\x07\x61ntenna\x18\x02 \x01(\x0b\x32$.chromiumos.test.lab.api.WifiAntenna\"g\n\x0b\x45nvironment\x12\x1b\n\x17\x45NVIRONMENT_UNSPECIFIED\x10\x00\x12\x0c\n\x08STANDARD\x10\x01\x12\r\n\tWIFI_CELL\x10\x02\x12\t\n\x05\x43HAOS\x10\x03\x12\x13\n\x0fROUTER_802_11AX\x10\x04\"\x95\x01\n\x0bWifiAntenna\x12\x43\n\nconnection\x18\x01 \x01(\x0e\x32/.chromiumos.test.lab.api.WifiAntenna.Connection\"A\n\nConnection\x12\x1a\n\x16\x43ONNECTION_UNSPECIFIED\x10\x00\x12\x0e\n\nCONDUCTIVE\x10\x01\x12\x07\n\x03OTA\x10\x02\"Z\n\rBluetoothPeer\x12\x10\n\x08hostname\x18\x01 \x01(\t\x12\x37\n\x05state\x18\x02 \x01(\x0e\x32(.chromiumos.test.lab.api.PeripheralState*L\n\x0fPeripheralState\x12 \n\x1cPERIPHERAL_STATE_UNSPECIFIED\x10\x00\x12\x0b\n\x07WORKING\x10\x01\x12\n\n\x06\x42ROKEN\x10\x02*\xfb\x03\n\x05Phase\x12\x15\n\x11PHASE_UNSPECIFIED\x10\x00\x12\x07\n\x03\x44VT\x10\x01\x12\t\n\x05\x44VT_2\x10\x02\x12\x11\n\rDVT_2_MPS_LTE\x10\x03\x12\x0f\n\x0b\x44VT_BIPSHIP\x10\x04\x12\x0e\n\nDVT_BOOKEM\x10\x05\x12\x0f\n\x0b\x44VT_ELECTRO\x10\x06\x12\r\n\tDVT_LOCKE\x10\x07\x12\x0e\n\nDVT_OSCINO\x10\x08\x12\x0e\n\nDVT_REKS14\x10\t\x12\x14\n\x10\x44VT_REKS14_TOUCH\x10\n\x12\r\n\tDVT_TOUCH\x10\x0b\x12\x07\n\x03\x45VT\x10\x0c\x12\x11\n\rEVT_FLEEX_LTE\x10\r\x12\n\n\x06\x45VT_HQ\x10\x0e\x12\x0b\n\x07\x45VT_LTE\x10\x0f\x12\r\n\tEVT_MAPLE\x10\x10\x12\r\n\tEVT_PUJJO\x10\x11\x12\t\n\x05PROTO\x10\x12\x12\n\n\x06PROTO1\x10\x13\x12\x07\n\x03PVT\x10\x14\x12\x0e\n\nPVT_TERRA3\x10\x15\x12\n\n\x06PVT_US\x10\x16\x12\t\n\x05PVT_2\x10\x17\x12\x0e\n\nPVT_BOOKEM\x10\x18\x12\x0f\n\x0bPVT_ELECTRO\x10\x19\x12\x0e\n\nPVT_GIK360\x10\x1a\x12\x0c\n\x08PVT_LILI\x10\x1b\x12\x0b\n\x07PVT_LTE\x10\x1c\x12\x0f\n\x0bPVT_NEW_CPU\x10\x1d\x12\x0c\n\x08PVT_SAND\x10\x1e\x12\x11\n\rPVT_TUNE_BITS\x10\x1f\x12\x0e\n\nPVT_TELESU\x10 \x12\x06\n\x02SR\x10!B3Z1go.chromium.org/chromiumos/config/go/test/lab/apib\x06proto3')

_PERIPHERALSTATE = DESCRIPTOR.enum_types_by_name['PeripheralState']
PeripheralState = enum_type_wrapper.EnumTypeWrapper(_PERIPHERALSTATE)
_PHASE = DESCRIPTOR.enum_types_by_name['Phase']
Phase = enum_type_wrapper.EnumTypeWrapper(_PHASE)
PERIPHERAL_STATE_UNSPECIFIED = 0
WORKING = 1
BROKEN = 2
PHASE_UNSPECIFIED = 0
DVT = 1
DVT_2 = 2
DVT_2_MPS_LTE = 3
DVT_BIPSHIP = 4
DVT_BOOKEM = 5
DVT_ELECTRO = 6
DVT_LOCKE = 7
DVT_OSCINO = 8
DVT_REKS14 = 9
DVT_REKS14_TOUCH = 10
DVT_TOUCH = 11
EVT = 12
EVT_FLEEX_LTE = 13
EVT_HQ = 14
EVT_LTE = 15
EVT_MAPLE = 16
EVT_PUJJO = 17
PROTO = 18
PROTO1 = 19
PVT = 20
PVT_TERRA3 = 21
PVT_US = 22
PVT_2 = 23
PVT_BOOKEM = 24
PVT_ELECTRO = 25
PVT_GIK360 = 26
PVT_LILI = 27
PVT_LTE = 28
PVT_NEW_CPU = 29
PVT_SAND = 30
PVT_TUNE_BITS = 31
PVT_TELESU = 32
SR = 33


_DUT = DESCRIPTOR.message_types_by_name['Dut']
_DUT_ID = _DUT.nested_types_by_name['Id']
_DUT_CHROMEOS = _DUT.nested_types_by_name['ChromeOS']
_DUT_ANDROID = _DUT.nested_types_by_name['Android']
_DUTMODEL = DESCRIPTOR.message_types_by_name['DutModel']
_DUTTOPOLOGY = DESCRIPTOR.message_types_by_name['DutTopology']
_DUTTOPOLOGY_ID = _DUTTOPOLOGY.nested_types_by_name['Id']
_AUDIO = DESCRIPTOR.message_types_by_name['Audio']
_CABLE = DESCRIPTOR.message_types_by_name['Cable']
_CACHESERVER = DESCRIPTOR.message_types_by_name['CacheServer']
_CAMERABOX = DESCRIPTOR.message_types_by_name['Camerabox']
_CELLULAR = DESCRIPTOR.message_types_by_name['Cellular']
_CHAMELEON = DESCRIPTOR.message_types_by_name['Chameleon']
_EXTERNALCAMERA = DESCRIPTOR.message_types_by_name['ExternalCamera']
_RPM = DESCRIPTOR.message_types_by_name['RPM']
_SERVO = DESCRIPTOR.message_types_by_name['Servo']
_TOUCH = DESCRIPTOR.message_types_by_name['Touch']
_WIFI = DESCRIPTOR.message_types_by_name['Wifi']
_WIFIANTENNA = DESCRIPTOR.message_types_by_name['WifiAntenna']
_BLUETOOTHPEER = DESCRIPTOR.message_types_by_name['BluetoothPeer']
_CABLE_TYPE = _CABLE.enum_types_by_name['Type']
_CAMERABOX_FACING = _CAMERABOX.enum_types_by_name['Facing']
_CELLULAR_OPERATOR = _CELLULAR.enum_types_by_name['Operator']
_CHAMELEON_PERIPHERAL = _CHAMELEON.enum_types_by_name['Peripheral']
_EXTERNALCAMERA_TYPE = _EXTERNALCAMERA.enum_types_by_name['Type']
_WIFI_ENVIRONMENT = _WIFI.enum_types_by_name['Environment']
_WIFIANTENNA_CONNECTION = _WIFIANTENNA.enum_types_by_name['Connection']
Dut = _reflection.GeneratedProtocolMessageType('Dut', (_message.Message,), {

  'Id' : _reflection.GeneratedProtocolMessageType('Id', (_message.Message,), {
    'DESCRIPTOR' : _DUT_ID,
    '__module__' : 'chromiumos.test.lab.api.dut_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.test.lab.api.Dut.Id)
    })
  ,

  'ChromeOS' : _reflection.GeneratedProtocolMessageType('ChromeOS', (_message.Message,), {
    'DESCRIPTOR' : _DUT_CHROMEOS,
    '__module__' : 'chromiumos.test.lab.api.dut_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.test.lab.api.Dut.ChromeOS)
    })
  ,

  'Android' : _reflection.GeneratedProtocolMessageType('Android', (_message.Message,), {
    'DESCRIPTOR' : _DUT_ANDROID,
    '__module__' : 'chromiumos.test.lab.api.dut_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.test.lab.api.Dut.Android)
    })
  ,
  'DESCRIPTOR' : _DUT,
  '__module__' : 'chromiumos.test.lab.api.dut_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.lab.api.Dut)
  })
_sym_db.RegisterMessage(Dut)
_sym_db.RegisterMessage(Dut.Id)
_sym_db.RegisterMessage(Dut.ChromeOS)
_sym_db.RegisterMessage(Dut.Android)

DutModel = _reflection.GeneratedProtocolMessageType('DutModel', (_message.Message,), {
  'DESCRIPTOR' : _DUTMODEL,
  '__module__' : 'chromiumos.test.lab.api.dut_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.lab.api.DutModel)
  })
_sym_db.RegisterMessage(DutModel)

DutTopology = _reflection.GeneratedProtocolMessageType('DutTopology', (_message.Message,), {

  'Id' : _reflection.GeneratedProtocolMessageType('Id', (_message.Message,), {
    'DESCRIPTOR' : _DUTTOPOLOGY_ID,
    '__module__' : 'chromiumos.test.lab.api.dut_pb2'
    # @@protoc_insertion_point(class_scope:chromiumos.test.lab.api.DutTopology.Id)
    })
  ,
  'DESCRIPTOR' : _DUTTOPOLOGY,
  '__module__' : 'chromiumos.test.lab.api.dut_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.lab.api.DutTopology)
  })
_sym_db.RegisterMessage(DutTopology)
_sym_db.RegisterMessage(DutTopology.Id)

Audio = _reflection.GeneratedProtocolMessageType('Audio', (_message.Message,), {
  'DESCRIPTOR' : _AUDIO,
  '__module__' : 'chromiumos.test.lab.api.dut_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.lab.api.Audio)
  })
_sym_db.RegisterMessage(Audio)

Cable = _reflection.GeneratedProtocolMessageType('Cable', (_message.Message,), {
  'DESCRIPTOR' : _CABLE,
  '__module__' : 'chromiumos.test.lab.api.dut_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.lab.api.Cable)
  })
_sym_db.RegisterMessage(Cable)

CacheServer = _reflection.GeneratedProtocolMessageType('CacheServer', (_message.Message,), {
  'DESCRIPTOR' : _CACHESERVER,
  '__module__' : 'chromiumos.test.lab.api.dut_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.lab.api.CacheServer)
  })
_sym_db.RegisterMessage(CacheServer)

Camerabox = _reflection.GeneratedProtocolMessageType('Camerabox', (_message.Message,), {
  'DESCRIPTOR' : _CAMERABOX,
  '__module__' : 'chromiumos.test.lab.api.dut_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.lab.api.Camerabox)
  })
_sym_db.RegisterMessage(Camerabox)

Cellular = _reflection.GeneratedProtocolMessageType('Cellular', (_message.Message,), {
  'DESCRIPTOR' : _CELLULAR,
  '__module__' : 'chromiumos.test.lab.api.dut_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.lab.api.Cellular)
  })
_sym_db.RegisterMessage(Cellular)

Chameleon = _reflection.GeneratedProtocolMessageType('Chameleon', (_message.Message,), {
  'DESCRIPTOR' : _CHAMELEON,
  '__module__' : 'chromiumos.test.lab.api.dut_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.lab.api.Chameleon)
  })
_sym_db.RegisterMessage(Chameleon)

ExternalCamera = _reflection.GeneratedProtocolMessageType('ExternalCamera', (_message.Message,), {
  'DESCRIPTOR' : _EXTERNALCAMERA,
  '__module__' : 'chromiumos.test.lab.api.dut_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.lab.api.ExternalCamera)
  })
_sym_db.RegisterMessage(ExternalCamera)

RPM = _reflection.GeneratedProtocolMessageType('RPM', (_message.Message,), {
  'DESCRIPTOR' : _RPM,
  '__module__' : 'chromiumos.test.lab.api.dut_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.lab.api.RPM)
  })
_sym_db.RegisterMessage(RPM)

Servo = _reflection.GeneratedProtocolMessageType('Servo', (_message.Message,), {
  'DESCRIPTOR' : _SERVO,
  '__module__' : 'chromiumos.test.lab.api.dut_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.lab.api.Servo)
  })
_sym_db.RegisterMessage(Servo)

Touch = _reflection.GeneratedProtocolMessageType('Touch', (_message.Message,), {
  'DESCRIPTOR' : _TOUCH,
  '__module__' : 'chromiumos.test.lab.api.dut_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.lab.api.Touch)
  })
_sym_db.RegisterMessage(Touch)

Wifi = _reflection.GeneratedProtocolMessageType('Wifi', (_message.Message,), {
  'DESCRIPTOR' : _WIFI,
  '__module__' : 'chromiumos.test.lab.api.dut_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.lab.api.Wifi)
  })
_sym_db.RegisterMessage(Wifi)

WifiAntenna = _reflection.GeneratedProtocolMessageType('WifiAntenna', (_message.Message,), {
  'DESCRIPTOR' : _WIFIANTENNA,
  '__module__' : 'chromiumos.test.lab.api.dut_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.lab.api.WifiAntenna)
  })
_sym_db.RegisterMessage(WifiAntenna)

BluetoothPeer = _reflection.GeneratedProtocolMessageType('BluetoothPeer', (_message.Message,), {
  'DESCRIPTOR' : _BLUETOOTHPEER,
  '__module__' : 'chromiumos.test.lab.api.dut_pb2'
  # @@protoc_insertion_point(class_scope:chromiumos.test.lab.api.BluetoothPeer)
  })
_sym_db.RegisterMessage(BluetoothPeer)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z1go.chromium.org/chromiumos/config/go/test/lab/api'
  _PERIPHERALSTATE._serialized_start=3200
  _PERIPHERALSTATE._serialized_end=3276
  _PHASE._serialized_start=3279
  _PHASE._serialized_end=3786
  _DUT._serialized_start=152
  _DUT._serialized_end=1452
  _DUT_ID._serialized_start=380
  _DUT_ID._serialized_end=399
  _DUT_CHROMEOS._serialized_start=402
  _DUT_CHROMEOS._serialized_end=1271
  _DUT_ANDROID._serialized_start=1274
  _DUT_ANDROID._serialized_end=1440
  _DUTMODEL._serialized_start=1454
  _DUTMODEL._serialized_end=1506
  _DUTTOPOLOGY._serialized_start=1509
  _DUTTOPOLOGY._serialized_end=1652
  _DUTTOPOLOGY_ID._serialized_start=380
  _DUTTOPOLOGY_ID._serialized_end=399
  _AUDIO._serialized_start=1654
  _AUDIO._serialized_end=1695
  _CABLE._serialized_start=1698
  _CABLE._serialized_end=1847
  _CABLE_TYPE._serialized_start=1758
  _CABLE_TYPE._serialized_end=1847
  _CACHESERVER._serialized_start=1849
  _CACHESERVER._serialized_end=1916
  _CAMERABOX._serialized_start=1918
  _CAMERABOX._serialized_end=2043
  _CAMERABOX_FACING._serialized_start=1990
  _CAMERABOX_FACING._serialized_end=2043
  _CELLULAR._serialized_start=2046
  _CELLULAR._serialized_end=2192
  _CELLULAR_OPERATOR._serialized_start=2121
  _CELLULAR_OPERATOR._serialized_end=2192
  _CHAMELEON._serialized_start=2195
  _CHAMELEON._serialized_end=2437
  _CHAMELEON_PERIPHERAL._serialized_start=2298
  _CHAMELEON_PERIPHERAL._serialized_end=2437
  _EXTERNALCAMERA._serialized_start=2440
  _EXTERNALCAMERA._serialized_end=2571
  _EXTERNALCAMERA_TYPE._serialized_start=2518
  _EXTERNALCAMERA_TYPE._serialized_end=2571
  _RPM._serialized_start=2573
  _RPM._serialized_end=2595
  _SERVO._serialized_start=2597
  _SERVO._serialized_end=2698
  _TOUCH._serialized_start=2700
  _TOUCH._serialized_end=2721
  _WIFI._serialized_start=2724
  _WIFI._serialized_end=2954
  _WIFI_ENVIRONMENT._serialized_start=2851
  _WIFI_ENVIRONMENT._serialized_end=2954
  _WIFIANTENNA._serialized_start=2957
  _WIFIANTENNA._serialized_end=3106
  _WIFIANTENNA_CONNECTION._serialized_start=3041
  _WIFIANTENNA_CONNECTION._serialized_end=3106
  _BLUETOOTHPEER._serialized_start=3108
  _BLUETOOTHPEER._serialized_end=3198
# @@protoc_insertion_point(module_scope)
