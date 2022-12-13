// Copyright 2022 The ChromiumOS Authors.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

import * as metrics from '../../metrics/metrics';
import {CommandContext} from './common';

export async function refreshLeases(context: CommandContext): Promise<void> {
  metrics.send({
    category: 'interactive',
    group: 'device',
    action: 'refresh leases',
  });

  context.deviceRepository.leased.refresh();
}
