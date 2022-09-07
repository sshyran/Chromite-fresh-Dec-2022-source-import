# Copyright 2022 The ChromiumOS Authors.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Python formatter."""

from pathlib import Path

from chromite.lib import constants
from chromite.lib import cros_build_lib


def Data(data: str) -> str:
  """Format python |data|.

  Args:
   data: The file content to lint.

  Returns:
    Formatted data.
  """
  # We run through isort first to enforce module sorting order, then run that
  # result through black. We can't run isort independently (or after black)
  # because it has some known edge cases where it formats in black-incompatible
  # ways. See b/235526476 for details.
  result = cros_build_lib.run(
      [
          Path(constants.CHROMITE_SCRIPTS_DIR) / 'isort',
          '-',
          '-d',
      ],
      capture_output=True,
      input=data,
      encoding='utf-8',
  )

  config_path = Path(constants.CHROMITE_DIR) / 'pyproject.toml'
  result = cros_build_lib.run(
      [
          Path(constants.CHROMITE_SCRIPTS_DIR) / 'black',
          f'--config={config_path}',
          '-',
      ],
      input=result.stdout,
      capture_output=True,
      encoding="utf-8",
  )

  return result.stdout
