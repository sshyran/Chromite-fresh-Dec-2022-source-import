# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: test_platform/skylab_tool/result.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='test_platform/skylab_tool/result.proto',
  package='test_platform.skylab_tool',
  syntax='proto3',
  serialized_options=_b('ZCgo.chromium.org/chromiumos/infra/proto/go/test_platform/skylab_tool'),
  serialized_pb=_b('\n&test_platform/skylab_tool/result.proto\x12\x19test_platform.skylab_tool\"\x90\x04\n\x0eWaitTaskResult\x12K\n\x06result\x18\x01 \x01(\x0b\x32..test_platform.skylab_tool.WaitTaskResult.TaskR\x0btask-result\x12\x0e\n\x06stdout\x18\x02 \x01(\t\x12T\n\rchild_results\x18\x03 \x03(\x0b\x32..test_platform.skylab_tool.WaitTaskResult.TaskR\rchild-results\x12J\n\x0clog_data_url\x18\x04 \x01(\x0b\x32\x34.test_platform.skylab_tool.WaitTaskResult.LogDataURL\x1a\xdb\x01\n\x04Task\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05state\x18\x02 \x01(\t\x12\x0f\n\x07\x66\x61ilure\x18\x03 \x01(\x08\x12\x0f\n\x07success\x18\x04 \x01(\x08\x12 \n\x0btask_run_id\x18\x05 \x01(\tR\x0btask-run-id\x12(\n\x0ftask_request_id\x18\x06 \x01(\tR\x0ftask-request-id\x12\"\n\x0ctask_run_url\x18\x07 \x01(\tR\x0ctask-run-url\x12$\n\rtask_logs_url\x18\x08 \x01(\tR\rtask-logs-url\x1a!\n\nLogDataURL\x12\x13\n\x0bisolate_url\x18\x01 \x01(\t\"a\n\x0fWaitTasksResult\x12:\n\x07results\x18\x01 \x03(\x0b\x32).test_platform.skylab_tool.WaitTaskResult\x12\x12\n\nincomplete\x18\x02 \x01(\x08\x42\x45ZCgo.chromium.org/chromiumos/infra/proto/go/test_platform/skylab_toolb\x06proto3')
)




_WAITTASKRESULT_TASK = _descriptor.Descriptor(
  name='Task',
  full_name='test_platform.skylab_tool.WaitTaskResult.Task',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='test_platform.skylab_tool.WaitTaskResult.Task.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='state', full_name='test_platform.skylab_tool.WaitTaskResult.Task.state', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='failure', full_name='test_platform.skylab_tool.WaitTaskResult.Task.failure', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='success', full_name='test_platform.skylab_tool.WaitTaskResult.Task.success', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='task_run_id', full_name='test_platform.skylab_tool.WaitTaskResult.Task.task_run_id', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='task-run-id', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='task_request_id', full_name='test_platform.skylab_tool.WaitTaskResult.Task.task_request_id', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='task-request-id', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='task_run_url', full_name='test_platform.skylab_tool.WaitTaskResult.Task.task_run_url', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='task-run-url', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='task_logs_url', full_name='test_platform.skylab_tool.WaitTaskResult.Task.task_logs_url', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='task-logs-url', file=DESCRIPTOR),
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
  serialized_start=344,
  serialized_end=563,
)

_WAITTASKRESULT_LOGDATAURL = _descriptor.Descriptor(
  name='LogDataURL',
  full_name='test_platform.skylab_tool.WaitTaskResult.LogDataURL',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='isolate_url', full_name='test_platform.skylab_tool.WaitTaskResult.LogDataURL.isolate_url', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=565,
  serialized_end=598,
)

_WAITTASKRESULT = _descriptor.Descriptor(
  name='WaitTaskResult',
  full_name='test_platform.skylab_tool.WaitTaskResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='test_platform.skylab_tool.WaitTaskResult.result', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='task-result', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stdout', full_name='test_platform.skylab_tool.WaitTaskResult.stdout', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='child_results', full_name='test_platform.skylab_tool.WaitTaskResult.child_results', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='child-results', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='log_data_url', full_name='test_platform.skylab_tool.WaitTaskResult.log_data_url', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_WAITTASKRESULT_TASK, _WAITTASKRESULT_LOGDATAURL, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=70,
  serialized_end=598,
)


_WAITTASKSRESULT = _descriptor.Descriptor(
  name='WaitTasksResult',
  full_name='test_platform.skylab_tool.WaitTasksResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='results', full_name='test_platform.skylab_tool.WaitTasksResult.results', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='incomplete', full_name='test_platform.skylab_tool.WaitTasksResult.incomplete', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=600,
  serialized_end=697,
)

_WAITTASKRESULT_TASK.containing_type = _WAITTASKRESULT
_WAITTASKRESULT_LOGDATAURL.containing_type = _WAITTASKRESULT
_WAITTASKRESULT.fields_by_name['result'].message_type = _WAITTASKRESULT_TASK
_WAITTASKRESULT.fields_by_name['child_results'].message_type = _WAITTASKRESULT_TASK
_WAITTASKRESULT.fields_by_name['log_data_url'].message_type = _WAITTASKRESULT_LOGDATAURL
_WAITTASKSRESULT.fields_by_name['results'].message_type = _WAITTASKRESULT
DESCRIPTOR.message_types_by_name['WaitTaskResult'] = _WAITTASKRESULT
DESCRIPTOR.message_types_by_name['WaitTasksResult'] = _WAITTASKSRESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

WaitTaskResult = _reflection.GeneratedProtocolMessageType('WaitTaskResult', (_message.Message,), dict(

  Task = _reflection.GeneratedProtocolMessageType('Task', (_message.Message,), dict(
    DESCRIPTOR = _WAITTASKRESULT_TASK,
    __module__ = 'test_platform.skylab_tool.result_pb2'
    # @@protoc_insertion_point(class_scope:test_platform.skylab_tool.WaitTaskResult.Task)
    ))
  ,

  LogDataURL = _reflection.GeneratedProtocolMessageType('LogDataURL', (_message.Message,), dict(
    DESCRIPTOR = _WAITTASKRESULT_LOGDATAURL,
    __module__ = 'test_platform.skylab_tool.result_pb2'
    # @@protoc_insertion_point(class_scope:test_platform.skylab_tool.WaitTaskResult.LogDataURL)
    ))
  ,
  DESCRIPTOR = _WAITTASKRESULT,
  __module__ = 'test_platform.skylab_tool.result_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.skylab_tool.WaitTaskResult)
  ))
_sym_db.RegisterMessage(WaitTaskResult)
_sym_db.RegisterMessage(WaitTaskResult.Task)
_sym_db.RegisterMessage(WaitTaskResult.LogDataURL)

WaitTasksResult = _reflection.GeneratedProtocolMessageType('WaitTasksResult', (_message.Message,), dict(
  DESCRIPTOR = _WAITTASKSRESULT,
  __module__ = 'test_platform.skylab_tool.result_pb2'
  # @@protoc_insertion_point(class_scope:test_platform.skylab_tool.WaitTasksResult)
  ))
_sym_db.RegisterMessage(WaitTasksResult)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
