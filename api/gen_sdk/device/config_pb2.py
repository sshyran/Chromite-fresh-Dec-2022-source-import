# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: device/config.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chromite.api.gen_sdk.device import config_id_pb2 as device_dot_config__id__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='device/config.proto',
  package='device',
  syntax='proto3',
  serialized_options=b'Z0go.chromium.org/chromiumos/infra/proto/go/device',
  serialized_pb=b'\n\x13\x64\x65vice/config.proto\x12\x06\x64\x65vice\x1a\x16\x64\x65vice/config_id.proto\"\xde\x18\n\x06\x43onfig\x12\x1c\n\x02id\x18\x01 \x01(\x0b\x32\x10.device.ConfigId\x12.\n\x0b\x66orm_factor\x18\x03 \x01(\x0e\x32\x19.device.Config.FormFactor\x12\x12\n\ngpu_family\x18\x04 \x01(\t\x12)\n\x08graphics\x18\x05 \x01(\x0e\x32\x17.device.Config.Graphics\x12\x39\n\x11hardware_features\x18\x06 \x03(\x0e\x32\x1e.device.Config.HardwareFeature\x12)\n\x05power\x18\x08 \x01(\x0e\x32\x1a.device.Config.PowerSupply\x12\'\n\x07storage\x18\t \x01(\x0e\x32\x16.device.Config.Storage\x12\x45\n\x1bvideo_acceleration_supports\x18\n \x03(\x0e\x32 .device.Config.VideoAcceleration\x12\x1f\n\x03soc\x18\x0b \x01(\x0e\x32\x12.device.Config.SOC\x12\x0b\n\x03tam\x18\x0c \x03(\t\x12\n\n\x02\x65\x65\x18\r \x03(\t\x12\x1f\n\x03odm\x18\x0e \x01(\x0e\x32\x12.device.Config.ODM\x12\x17\n\x0fodm_email_group\x18\x0f \x01(\t\x12\x1f\n\x03oem\x18\x10 \x01(\x0e\x32\x12.device.Config.OEM\x12\x17\n\x0foem_email_group\x18\x11 \x01(\t\x12\x17\n\x0fsoc_email_group\x18\x12 \x01(\t\x12\x1e\n\x16\x66irmware_configuration\x18\x13 \x01(\r\x12(\n\x03\x63pu\x18\x14 \x01(\x0e\x32\x1b.device.Config.Architecture\x12\x1d\n\x02\x65\x63\x18\x15 \x01(\x0e\x32\x11.device.Config.EC\"\xec\x01\n\nFormFactor\x12\x1b\n\x17\x46ORM_FACTOR_UNSPECIFIED\x10\x00\x12\x19\n\x15\x46ORM_FACTOR_CLAMSHELL\x10\x01\x12\x1b\n\x17\x46ORM_FACTOR_CONVERTIBLE\x10\x02\x12\x1a\n\x16\x46ORM_FACTOR_DETACHABLE\x10\x03\x12\x1a\n\x16\x46ORM_FACTOR_CHROMEBASE\x10\x04\x12\x19\n\x15\x46ORM_FACTOR_CHROMEBOX\x10\x05\x12\x19\n\x15\x46ORM_FACTOR_CHROMEBIT\x10\x06\x12\x1b\n\x17\x46ORM_FACTOR_CHROMESLATE\x10\x07\"G\n\x08Graphics\x12\x18\n\x14GRAPHICS_UNSPECIFIED\x10\x00\x12\x0f\n\x0bGRAPHICS_GL\x10\x01\x12\x10\n\x0cGRAPHICS_GLE\x10\x02\"\xa3\x03\n\x0fHardwareFeature\x12 \n\x1cHARDWARE_FEATURE_UNSPECIFIED\x10\x00\x12\x1e\n\x1aHARDWARE_FEATURE_BLUETOOTH\x10\x01\x12\x1d\n\x19HARDWARE_FEATURE_FLASHROM\x10\x02\x12\x1f\n\x1bHARDWARE_FEATURE_HOTWORDING\x10\x03\x12%\n!HARDWARE_FEATURE_INTERNAL_DISPLAY\x10\x04\x12 \n\x1cHARDWARE_FEATURE_LUCID_SLEEP\x10\x05\x12\x1b\n\x17HARDWARE_FEATURE_WEBCAM\x10\x06\x12\x1b\n\x17HARDWARE_FEATURE_STYLUS\x10\x07\x12\x1d\n\x19HARDWARE_FEATURE_TOUCHPAD\x10\x08\x12 \n\x1cHARDWARE_FEATURE_TOUCHSCREEN\x10\t\x12(\n$HARDWARE_FEATURE_DETACHABLE_KEYBOARD\x10\n\x12 \n\x1cHARDWARE_FEATURE_FINGERPRINT\x10\x0b\"_\n\x0bPowerSupply\x12\x1c\n\x18POWER_SUPPLY_UNSPECIFIED\x10\x00\x12\x18\n\x14POWER_SUPPLY_BATTERY\x10\x01\x12\x18\n\x14POWER_SUPPLY_AC_ONLY\x10\x02\"x\n\x07Storage\x12\x17\n\x13STORAGE_UNSPECIFIED\x10\x00\x12\x0f\n\x0bSTORAGE_SSD\x10\x01\x12\x0f\n\x0bSTORAGE_HDD\x10\x02\x12\x0f\n\x0bSTORAGE_MMC\x10\x03\x12\x10\n\x0cSTORAGE_NVME\x10\x04\x12\x0f\n\x0bSTORAGE_UFS\x10\x05\"\x9c\x03\n\x11VideoAcceleration\x12\x15\n\x11VIDEO_UNSPECIFIED\x10\x00\x12\x1b\n\x17VIDEO_ACCELERATION_H264\x10\x01\x12\x1f\n\x1bVIDEO_ACCELERATION_ENC_H264\x10\x02\x12\x1a\n\x16VIDEO_ACCELERATION_VP8\x10\x03\x12\x1e\n\x1aVIDEO_ACCELERATION_ENC_VP8\x10\x04\x12\x1a\n\x16VIDEO_ACCELERATION_VP9\x10\x05\x12\x1e\n\x1aVIDEO_ACCELERATION_ENC_VP9\x10\x06\x12\x1c\n\x18VIDEO_ACCELERATION_VP9_2\x10\x07\x12 \n\x1cVIDEO_ACCELERATION_ENC_VP9_2\x10\x08\x12\x1b\n\x17VIDEO_ACCELERATION_H265\x10\t\x12\x1f\n\x1bVIDEO_ACCELERATION_ENC_H265\x10\n\x12\x1b\n\x17VIDEO_ACCELERATION_MJPG\x10\x0b\x12\x1f\n\x1bVIDEO_ACCELERATION_ENC_MJPG\x10\x0c\"\xdd\x05\n\x03SOC\x12\x13\n\x0fSOC_UNSPECIFIED\x10\x00\x12\x13\n\x0fSOC_AMBERLAKE_Y\x10\x01\x12\x13\n\x0fSOC_APOLLO_LAKE\x10\x02\x12\x11\n\rSOC_BAY_TRAIL\x10\x03\x12\x10\n\x0cSOC_BRASWELL\x10\x04\x12\x11\n\rSOC_BROADWELL\x10\x05\x12\x15\n\x11SOC_CANNON_LAKE_Y\x10\x06\x12\x14\n\x10SOC_COMET_LAKE_U\x10\x07\x12\x13\n\x0fSOC_EXYNOS_5250\x10\x08\x12\x13\n\x0fSOC_EXYNOS_5420\x10\t\x12\x13\n\x0fSOC_GEMINI_LAKE\x10\n\x12\x0f\n\x0bSOC_HASWELL\x10\x0b\x12\x12\n\x0eSOC_ICE_LAKE_Y\x10\x0c\x12\x12\n\x0eSOC_IVY_BRIDGE\x10\r\x12\x12\n\x0eSOC_KABYLAKE_U\x10\x0e\x12\x14\n\x10SOC_KABYLAKE_U_R\x10\x0f\x12\x12\n\x0eSOC_KABYLAKE_Y\x10\x10\x12\x0e\n\nSOC_MT8173\x10\x11\x12\x0e\n\nSOC_MT8176\x10\x12\x12\x0e\n\nSOC_MT8183\x10\x13\x12\x0f\n\x0bSOC_PICASSO\x10\x14\x12\x12\n\x0eSOC_PINE_TRAIL\x10\x15\x12\x0e\n\nSOC_RK3288\x10\x16\x12\x0e\n\nSOC_RK3399\x10\x17\x12\x14\n\x10SOC_SANDY_BRIDGE\x10\x18\x12\x0e\n\nSOC_SDM845\x10\x19\x12\x11\n\rSOC_SKYLAKE_U\x10\x1a\x12\x11\n\rSOC_SKYLAKE_Y\x10\x1b\x12\x14\n\x10SOC_STONEY_RIDGE\x10\x1c\x12\x10\n\x0cSOC_TEGRA_K1\x10\x1d\x12\x16\n\x12SOC_WHISKEY_LAKE_U\x10\x1e\x12\x0e\n\nSOC_SC7180\x10\x1f\x12\x13\n\x0fSOC_JASPER_LAKE\x10 \x12\x12\n\x0eSOC_TIGER_LAKE\x10!\x12\x0e\n\nSOC_MT8192\x10\"\x12\x12\n\x0eSOC_ALDER_LAKE\x10#\x12\x0e\n\nSOC_SC7280\x10$\x12\x0e\n\nSOC_MT8195\x10%\"n\n\x03ODM\x12\x13\n\x0fODM_UNSPECIFIED\x10\x00\x12\x0e\n\nODM_QUANTA\x10\x01\x12\x0f\n\x0bODM_BITLAND\x10\x02\x12\x0f\n\x0bODM_SAMSUNG\x10\x03\x12\x10\n\x0cODM_PEGATRON\x10\x04\x12\x0e\n\nODM_COMPAL\x10\x05\"~\n\x03OEM\x12\x13\n\x0fOEM_UNSPECIFIED\x10\x00\x12\x0c\n\x08OEM_ACER\x10\x01\x12\x0c\n\x08OEM_DELL\x10\x02\x12\x0f\n\x0bOEM_SAMSUNG\x10\x03\x12\n\n\x06OEM_HP\x10\x04\x12\x0e\n\nOEM_LENOVO\x10\x05\x12\x0c\n\x08OEM_ASUS\x10\x06\x12\x0b\n\x07OEM_NEC\x10\x07\"S\n\x0c\x41rchitecture\x12\x1a\n\x16\x41RCHITECTURE_UNDEFINED\x10\x00\x12\x07\n\x03X86\x10\x01\x12\n\n\x06X86_64\x10\x02\x12\x07\n\x03\x41RM\x10\x03\x12\t\n\x05\x41RM64\x10\x04\"5\n\x02\x45\x43\x12\x12\n\x0e\x45\x43_UNSPECIFIED\x10\x00\x12\r\n\tEC_CHROME\x10\x01\x12\x0c\n\x08\x45\x43_WILCO\x10\x02J\x04\x08\x02\x10\x03R\x07\x63\x61rrier\"-\n\nAllConfigs\x12\x1f\n\x07\x63onfigs\x18\x01 \x03(\x0b\x32\x0e.device.ConfigB2Z0go.chromium.org/chromiumos/infra/proto/go/deviceb\x06proto3'
  ,
  dependencies=[device_dot_config__id__pb2.DESCRIPTOR,])



_CONFIG_FORMFACTOR = _descriptor.EnumDescriptor(
  name='FormFactor',
  full_name='device.Config.FormFactor',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='FORM_FACTOR_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FORM_FACTOR_CLAMSHELL', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FORM_FACTOR_CONVERTIBLE', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FORM_FACTOR_DETACHABLE', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FORM_FACTOR_CHROMEBASE', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FORM_FACTOR_CHROMEBOX', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FORM_FACTOR_CHROMEBIT', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FORM_FACTOR_CHROMESLATE', index=7, number=7,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=726,
  serialized_end=962,
)
_sym_db.RegisterEnumDescriptor(_CONFIG_FORMFACTOR)

_CONFIG_GRAPHICS = _descriptor.EnumDescriptor(
  name='Graphics',
  full_name='device.Config.Graphics',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='GRAPHICS_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GRAPHICS_GL', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GRAPHICS_GLE', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=964,
  serialized_end=1035,
)
_sym_db.RegisterEnumDescriptor(_CONFIG_GRAPHICS)

_CONFIG_HARDWAREFEATURE = _descriptor.EnumDescriptor(
  name='HardwareFeature',
  full_name='device.Config.HardwareFeature',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='HARDWARE_FEATURE_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HARDWARE_FEATURE_BLUETOOTH', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HARDWARE_FEATURE_FLASHROM', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HARDWARE_FEATURE_HOTWORDING', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HARDWARE_FEATURE_INTERNAL_DISPLAY', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HARDWARE_FEATURE_LUCID_SLEEP', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HARDWARE_FEATURE_WEBCAM', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HARDWARE_FEATURE_STYLUS', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HARDWARE_FEATURE_TOUCHPAD', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HARDWARE_FEATURE_TOUCHSCREEN', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HARDWARE_FEATURE_DETACHABLE_KEYBOARD', index=10, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HARDWARE_FEATURE_FINGERPRINT', index=11, number=11,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1038,
  serialized_end=1457,
)
_sym_db.RegisterEnumDescriptor(_CONFIG_HARDWAREFEATURE)

_CONFIG_POWERSUPPLY = _descriptor.EnumDescriptor(
  name='PowerSupply',
  full_name='device.Config.PowerSupply',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='POWER_SUPPLY_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='POWER_SUPPLY_BATTERY', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='POWER_SUPPLY_AC_ONLY', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1459,
  serialized_end=1554,
)
_sym_db.RegisterEnumDescriptor(_CONFIG_POWERSUPPLY)

_CONFIG_STORAGE = _descriptor.EnumDescriptor(
  name='Storage',
  full_name='device.Config.Storage',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='STORAGE_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STORAGE_SSD', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STORAGE_HDD', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STORAGE_MMC', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STORAGE_NVME', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STORAGE_UFS', index=5, number=5,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1556,
  serialized_end=1676,
)
_sym_db.RegisterEnumDescriptor(_CONFIG_STORAGE)

_CONFIG_VIDEOACCELERATION = _descriptor.EnumDescriptor(
  name='VideoAcceleration',
  full_name='device.Config.VideoAcceleration',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='VIDEO_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO_ACCELERATION_H264', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO_ACCELERATION_ENC_H264', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO_ACCELERATION_VP8', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO_ACCELERATION_ENC_VP8', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO_ACCELERATION_VP9', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO_ACCELERATION_ENC_VP9', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO_ACCELERATION_VP9_2', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO_ACCELERATION_ENC_VP9_2', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO_ACCELERATION_H265', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO_ACCELERATION_ENC_H265', index=10, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO_ACCELERATION_MJPG', index=11, number=11,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO_ACCELERATION_ENC_MJPG', index=12, number=12,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1679,
  serialized_end=2091,
)
_sym_db.RegisterEnumDescriptor(_CONFIG_VIDEOACCELERATION)

_CONFIG_SOC = _descriptor.EnumDescriptor(
  name='SOC',
  full_name='device.Config.SOC',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SOC_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_AMBERLAKE_Y', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_APOLLO_LAKE', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_BAY_TRAIL', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_BRASWELL', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_BROADWELL', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_CANNON_LAKE_Y', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_COMET_LAKE_U', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_EXYNOS_5250', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_EXYNOS_5420', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_GEMINI_LAKE', index=10, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_HASWELL', index=11, number=11,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_ICE_LAKE_Y', index=12, number=12,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_IVY_BRIDGE', index=13, number=13,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_KABYLAKE_U', index=14, number=14,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_KABYLAKE_U_R', index=15, number=15,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_KABYLAKE_Y', index=16, number=16,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_MT8173', index=17, number=17,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_MT8176', index=18, number=18,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_MT8183', index=19, number=19,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_PICASSO', index=20, number=20,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_PINE_TRAIL', index=21, number=21,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_RK3288', index=22, number=22,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_RK3399', index=23, number=23,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_SANDY_BRIDGE', index=24, number=24,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_SDM845', index=25, number=25,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_SKYLAKE_U', index=26, number=26,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_SKYLAKE_Y', index=27, number=27,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_STONEY_RIDGE', index=28, number=28,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_TEGRA_K1', index=29, number=29,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_WHISKEY_LAKE_U', index=30, number=30,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_SC7180', index=31, number=31,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_JASPER_LAKE', index=32, number=32,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_TIGER_LAKE', index=33, number=33,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_MT8192', index=34, number=34,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_ALDER_LAKE', index=35, number=35,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_SC7280', index=36, number=36,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_MT8195', index=37, number=37,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=2094,
  serialized_end=2827,
)
_sym_db.RegisterEnumDescriptor(_CONFIG_SOC)

_CONFIG_ODM = _descriptor.EnumDescriptor(
  name='ODM',
  full_name='device.Config.ODM',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ODM_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ODM_QUANTA', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ODM_BITLAND', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ODM_SAMSUNG', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ODM_PEGATRON', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ODM_COMPAL', index=5, number=5,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=2829,
  serialized_end=2939,
)
_sym_db.RegisterEnumDescriptor(_CONFIG_ODM)

_CONFIG_OEM = _descriptor.EnumDescriptor(
  name='OEM',
  full_name='device.Config.OEM',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OEM_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OEM_ACER', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OEM_DELL', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OEM_SAMSUNG', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OEM_HP', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OEM_LENOVO', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OEM_ASUS', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OEM_NEC', index=7, number=7,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=2941,
  serialized_end=3067,
)
_sym_db.RegisterEnumDescriptor(_CONFIG_OEM)

_CONFIG_ARCHITECTURE = _descriptor.EnumDescriptor(
  name='Architecture',
  full_name='device.Config.Architecture',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ARCHITECTURE_UNDEFINED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='X86', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='X86_64', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ARM', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ARM64', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=3069,
  serialized_end=3152,
)
_sym_db.RegisterEnumDescriptor(_CONFIG_ARCHITECTURE)

_CONFIG_EC = _descriptor.EnumDescriptor(
  name='EC',
  full_name='device.Config.EC',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='EC_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EC_CHROME', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EC_WILCO', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=3154,
  serialized_end=3207,
)
_sym_db.RegisterEnumDescriptor(_CONFIG_EC)


_CONFIG = _descriptor.Descriptor(
  name='Config',
  full_name='device.Config',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='device.Config.id', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='form_factor', full_name='device.Config.form_factor', index=1,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='gpu_family', full_name='device.Config.gpu_family', index=2,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='graphics', full_name='device.Config.graphics', index=3,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hardware_features', full_name='device.Config.hardware_features', index=4,
      number=6, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='power', full_name='device.Config.power', index=5,
      number=8, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='storage', full_name='device.Config.storage', index=6,
      number=9, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='video_acceleration_supports', full_name='device.Config.video_acceleration_supports', index=7,
      number=10, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='soc', full_name='device.Config.soc', index=8,
      number=11, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tam', full_name='device.Config.tam', index=9,
      number=12, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ee', full_name='device.Config.ee', index=10,
      number=13, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='odm', full_name='device.Config.odm', index=11,
      number=14, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='odm_email_group', full_name='device.Config.odm_email_group', index=12,
      number=15, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='oem', full_name='device.Config.oem', index=13,
      number=16, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='oem_email_group', full_name='device.Config.oem_email_group', index=14,
      number=17, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='soc_email_group', full_name='device.Config.soc_email_group', index=15,
      number=18, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='firmware_configuration', full_name='device.Config.firmware_configuration', index=16,
      number=19, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cpu', full_name='device.Config.cpu', index=17,
      number=20, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ec', full_name='device.Config.ec', index=18,
      number=21, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CONFIG_FORMFACTOR,
    _CONFIG_GRAPHICS,
    _CONFIG_HARDWAREFEATURE,
    _CONFIG_POWERSUPPLY,
    _CONFIG_STORAGE,
    _CONFIG_VIDEOACCELERATION,
    _CONFIG_SOC,
    _CONFIG_ODM,
    _CONFIG_OEM,
    _CONFIG_ARCHITECTURE,
    _CONFIG_EC,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=56,
  serialized_end=3222,
)


_ALLCONFIGS = _descriptor.Descriptor(
  name='AllConfigs',
  full_name='device.AllConfigs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='configs', full_name='device.AllConfigs.configs', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=3224,
  serialized_end=3269,
)

_CONFIG.fields_by_name['id'].message_type = device_dot_config__id__pb2._CONFIGID
_CONFIG.fields_by_name['form_factor'].enum_type = _CONFIG_FORMFACTOR
_CONFIG.fields_by_name['graphics'].enum_type = _CONFIG_GRAPHICS
_CONFIG.fields_by_name['hardware_features'].enum_type = _CONFIG_HARDWAREFEATURE
_CONFIG.fields_by_name['power'].enum_type = _CONFIG_POWERSUPPLY
_CONFIG.fields_by_name['storage'].enum_type = _CONFIG_STORAGE
_CONFIG.fields_by_name['video_acceleration_supports'].enum_type = _CONFIG_VIDEOACCELERATION
_CONFIG.fields_by_name['soc'].enum_type = _CONFIG_SOC
_CONFIG.fields_by_name['odm'].enum_type = _CONFIG_ODM
_CONFIG.fields_by_name['oem'].enum_type = _CONFIG_OEM
_CONFIG.fields_by_name['cpu'].enum_type = _CONFIG_ARCHITECTURE
_CONFIG.fields_by_name['ec'].enum_type = _CONFIG_EC
_CONFIG_FORMFACTOR.containing_type = _CONFIG
_CONFIG_GRAPHICS.containing_type = _CONFIG
_CONFIG_HARDWAREFEATURE.containing_type = _CONFIG
_CONFIG_POWERSUPPLY.containing_type = _CONFIG
_CONFIG_STORAGE.containing_type = _CONFIG
_CONFIG_VIDEOACCELERATION.containing_type = _CONFIG
_CONFIG_SOC.containing_type = _CONFIG
_CONFIG_ODM.containing_type = _CONFIG
_CONFIG_OEM.containing_type = _CONFIG
_CONFIG_ARCHITECTURE.containing_type = _CONFIG
_CONFIG_EC.containing_type = _CONFIG
_ALLCONFIGS.fields_by_name['configs'].message_type = _CONFIG
DESCRIPTOR.message_types_by_name['Config'] = _CONFIG
DESCRIPTOR.message_types_by_name['AllConfigs'] = _ALLCONFIGS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Config = _reflection.GeneratedProtocolMessageType('Config', (_message.Message,), {
  'DESCRIPTOR' : _CONFIG,
  '__module__' : 'device.config_pb2'
  # @@protoc_insertion_point(class_scope:device.Config)
  })
_sym_db.RegisterMessage(Config)

AllConfigs = _reflection.GeneratedProtocolMessageType('AllConfigs', (_message.Message,), {
  'DESCRIPTOR' : _ALLCONFIGS,
  '__module__' : 'device.config_pb2'
  # @@protoc_insertion_point(class_scope:device.AllConfigs)
  })
_sym_db.RegisterMessage(AllConfigs)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
