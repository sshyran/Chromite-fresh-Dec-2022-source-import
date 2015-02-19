# Copyright 2015 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from __future__ import print_function

from chromite.cbuildbot import constants
from chromite.lib import factory
from chromite.lib.graphite_lib import es_utils
from chromite.lib.graphite_lib import stats
from chromite.lib.graphite_lib import stats_es_mock


CONNECTION_TYPE_MOCK = 'none'
CONNECTION_TYPE_PROD = 'prod'
CONNECTION_TYPE_READONLY = 'readonly'


class ESMetadataFactoryClass(factory.ObjectFactory):
  """Factory class for setting up an Elastic Search connection."""

  _ELASTIC_SEARCH_TYPES = {
      CONNECTION_TYPE_PROD: factory.CachedFunctionCall(
          lambda: es_utils.ESMetadata(
              use_http=constants.ELASTIC_SEARCH_USE_HTTP,
              host=constants.ELASTIC_SEARCH_HOST,
              port=constants.ELASTIC_SEARCH_PORT,
              index=constants.ELASTIC_SEARCH_INDEX,
              udp_port=constants.ELASTIC_SEARCH_UDP_PORT)),
      CONNECTION_TYPE_READONLY: factory.CachedFunctionCall(
          lambda: es_utils.ESMetadataRO(
              use_http=constants.ELASTIC_SEARCH_USE_HTTP,
              host=constants.ELASTIC_SEARCH_HOST,
              port=constants.ELASTIC_SEARCH_PORT,
              index=constants.ELASTIC_SEARCH_INDEX,
              udp_port=constants.ELASTIC_SEARCH_UDP_PORT))
      }

  def __init__(self):
    super(ESMetadataFactoryClass, self).__init__(
        'elastic search connection', self._ELASTIC_SEARCH_TYPES,
        lambda from_setup, to_setup: from_setup == to_setup)

  def SetupProd(self):
    """Set up this factory to connect to the production Elastic Search."""
    self.Setup(CONNECTION_TYPE_PROD)

  def SetupReadOnly(self):
    """Set up this factory to allow querying the production Elastic Search."""
    self.Setup(CONNECTION_TYPE_READONLY)


ESMetadataFactory = ESMetadataFactoryClass()


class StatsFactoryClass(factory.ObjectFactory):
  """Factory class for setting up a Statsd connection."""

  _STATSD_TYPES = {
      CONNECTION_TYPE_PROD: factory.CachedFunctionCall(
          lambda: stats.Statsd(
              es=ESMetadataFactory.GetInstance(),
              host=constants.STATSD_HOST,
              port=constants.STATSD_PORT,
              prefix=constants.STATSD_PREFIX)),
      CONNECTION_TYPE_MOCK: factory.CachedFunctionCall(
          lambda: stats_es_mock.Stats())
      }

  def __init__(self):
    super(StatsFactoryClass, self).__init__(
        'statsd connection', self._STATSD_TYPES,
        lambda from_setup, to_setup: from_setup == to_setup)

  def SetupProd(self):
    """Set up this factory to connect to the production Statsd."""
    self.Setup(CONNECTION_TYPE_PROD)

  def SetupMock(self):
    """Set up this factory to return a mock statsd object."""
    self.Setup(CONNECTION_TYPE_MOCK)


StatsFactory = StatsFactoryClass()
