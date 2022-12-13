# Copyright (c) 2012 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Configuration options for various cbuildbot tests."""

import copy
import logging

from chromite.lib import config_lib
from chromite.lib import constants


vmtest_boards = frozenset([
    # Full VMTest support on ChromeOS is currently limited to devices derived
    # from betty & co.
    'amd64-generic', # Has kernel 4.4, used with public Chromium.
    'amd64-generic-vm', # amd64-generic with optimization for VMs.
    'betty',         # amd64 Chrome OS VM board with 32 bit arm/x86 ARC++ ABI.
    'betty-kernelnext', # Like betty but on the next kernel version.
    'betty-pi-arc',  # Like betty but P version of ARC++.
    'betty-arc-r',  # Like betty but R version of ARC++.
    'novato',        # Like betty but with GMSCore but not the Play Store
    'novato-arc64',  # 64 bit x86_64 ARC++ ABI
    'reven-vmtest',  # Like betty, but based on reven.
])


class HWTestList(object):
  """Container for methods to generate HWTest lists."""

  def __init__(self, ge_build_config):
    """Helper class for creating hwtests.

    Args:
      ge_build_config: Dictionary containing the decoded GE configuration file.
    """
    self.is_release_branch = ge_build_config[
        config_lib.CONFIG_TEMPLATE_RELEASE_BRANCH]

  def DefaultList(self, **kwargs):
    """Returns a default list of HWTestConfigs for a build.

    Args:
      *kwargs: overrides for the configs
    """
    return [
        config_lib.HWTestConfig(constants.HWTEST_BVT_SUITE,
                                **self._bvtInlineHWTestArgs(kwargs)),
        config_lib.HWTestConfig(constants.HWTEST_ARC_COMMIT_SUITE,
                                **self._bvtInlineHWTestArgs(kwargs)),
        self.TastConfig(constants.HWTEST_TAST_CQ_SUITE,
                        **self._bvtInlineHWTestArgs(kwargs)),
        # Start informational Tast tests before the installer suite to let the
        # former run even if the latter fails: https://crbug.com/911921
        self.TastConfig(constants.HWTEST_TAST_INFORMATIONAL_SUITE,
                        **self._asyncHWTestArgs(kwargs)),
        config_lib.HWTestConfig(constants.HWTEST_INSTALLER_SUITE,
                                **self._asyncHWTestArgs(kwargs)),
        config_lib.HWTestConfig(constants.HWTEST_COMMIT_SUITE,
                                **self._asyncHWTestArgs(kwargs)),
        config_lib.HWTestConfig(constants.HWTEST_CANARY_SUITE,
                                **self._asyncHWTestArgs(kwargs)),
    ]

  def _asyncHWTestArgs(self, kwargs):
    """Get updated kwargs for asynchronous hardware tests."""
    kwargs = kwargs.copy()
    kwargs['priority'] = constants.HWTEST_POST_BUILD_PRIORITY
    kwargs['async'] = True
    kwargs['suite_min_duts'] = 1
    kwargs['timeout'] = config_lib.HWTestConfig.ASYNC_HW_TEST_TIMEOUT
    return kwargs

  def _blockingHWTestArgs(self, kwargs):
    """Get updated kwargs for blockiong hardware tests."""
    kwargs = kwargs.copy()
    kwargs['blocking'] = True
    kwargs['async'] = False
    kwargs['priority'] = constants.HWTEST_CQ_PRIORITY
    kwargs['quota_account'] = constants.HWTEST_QUOTA_ACCOUNT_BVT_SYNC
    return kwargs

  def _bvtInlineHWTestArgs(self, kwargs):
    """Get updated kwargs for bvt-inline hardware tests."""
    if self.is_release_branch:
      return self._asyncHWTestArgs(kwargs)
    kwargs = kwargs.copy()
    kwargs['timeout'] = config_lib.HWTestConfig.SHARED_HW_TEST_TIMEOUT
    return kwargs

  def DefaultListCanary(self, **kwargs):
    """Returns a default list of config_lib.HWTestConfig's for a canary build.

    Args:
      *kwargs: overrides for the configs
    """
    # Set minimum_duts default to 4, which means that lab will check the
    # number of available duts to meet the minimum requirement before creating
    # the suite job for canary builds.
    kwargs.setdefault('minimum_duts', 4)
    kwargs.setdefault('file_bugs', True)
    kwargs['blocking'] = False
    kwargs['async'] = True
    return self.DefaultList(**kwargs)

  def DefaultListNonCanary(self, **kwargs):
    """Return a default list of HWTestConfigs for a non-canary build.

    Optional arguments may be overridden in `kwargs`, except that
    the `blocking` setting cannot be provided.
    """
    # N.B.  The ordering here is coupled with the column order of
    # entries in _paladin_hwtest_assignments, below.  If you change the
    # ordering here you must also change the ordering there.
    return [
        config_lib.HWTestConfig(constants.HWTEST_BVT_SUITE,
                                **kwargs),
        config_lib.HWTestConfig(constants.HWTEST_COMMIT_SUITE,
                                **kwargs),
        config_lib.HWTestConfig(constants.HWTEST_ARC_COMMIT_SUITE,
                                **kwargs)]

  def DefaultListPFQ(self, **kwargs):
    """Return a default list of HWTestConfig's for a PFQ build.

    Optional arguments may be overridden in `kwargs`, except that
    the `blocking` setting cannot be provided.
    """
    default_dict = dict(file_bugs=True,
                        pool=constants.HWTEST_QUOTA_POOL,
                        quota_account=constants.HWTEST_QUOTA_ACCOUNT_PFQ,
                        timeout=config_lib.HWTestConfig.PFQ_HW_TEST_TIMEOUT,
                        priority=constants.HWTEST_PFQ_PRIORITY, minimum_duts=3)
    # Allows kwargs overrides to default_dict for pfq.
    default_dict.update(kwargs)

    return [
        config_lib.HWTestConfig(constants.HWTEST_ARC_COMMIT_SUITE,
                                **default_dict),
        self.TastConfig(constants.HWTEST_TAST_ANDROID_PFQ_SUITE,
                        **default_dict),
    ]

  def SharedPoolPFQ(self, **kwargs):
    """Return a list of HWTestConfigs for PFQ which uses a shared pool.

    The returned suites will run in quotascheduler by default, which is
    shared with other types of builders (canaries, cq). The first suite in the
    list is a blocking sanity suite that verifies the build will not break dut.
    """
    sanity_dict = dict(pool=constants.HWTEST_QUOTA_POOL,
                       file_bugs=True,
                       timeout=config_lib.HWTestConfig.PFQ_HW_TEST_TIMEOUT,
                       quota_account=constants.HWTEST_QUOTA_ACCOUNT_PFQ)
    sanity_dict.update(kwargs)
    sanity_dict.update(dict(minimum_duts=1, suite_min_duts=1,
                            blocking=True))
    default_dict = dict(suite_min_duts=3)
    default_dict.update(kwargs)
    suite_list = [config_lib.HWTestConfig(constants.HWTEST_SANITY_SUITE,
                                          **sanity_dict)]
    suite_list.extend(self.DefaultListPFQ(**default_dict))
    return suite_list

  def SharedPoolCanary(self, **kwargs):
    """Return a list of HWTestConfigs for Canary which uses a shared pool.

    The returned suites will run in pool:critical by default, which is
    shared with CQs.
    """
    default_dict = dict(suite_min_duts=6)
    default_dict.update(kwargs)
    suite_list = self.DefaultListCanary(**default_dict)
    return suite_list

  def AFDORecordTest(self, **kwargs):
    default_dict = dict(pool=constants.HWTEST_QUOTA_POOL,
                        quota_account=constants.HWTEST_QUOTA_ACCOUNT_TOOLCHAIN,
                        file_bugs=True,
                        timeout=constants.AFDO_GENERATE_TIMEOUT,
                        priority=constants.HWTEST_PFQ_PRIORITY)
    # Allows kwargs overrides to default_dict for cq.
    default_dict.update(kwargs)
    return config_lib.HWTestConfig(constants.HWTEST_AFDO_SUITE, **default_dict)

  def ToolchainTestFull(self, machine_pool, **kwargs):
    """Return full set of HWTESTConfigs to run toolchain correctness tests."""
    default_dict = dict(pool=machine_pool,
                        file_bugs=False,
                        priority=constants.HWTEST_DEFAULT_PRIORITY)
    # Python 3.7+ made async a reserved keyword.
    default_dict['async'] = False
    default_dict.update(kwargs)
    return [config_lib.HWTestConfig(constants.HWTEST_BVT_SUITE,
                                    **default_dict),
            config_lib.HWTestConfig(constants.HWTEST_COMMIT_SUITE,
                                    **default_dict),
            self.TastConfig(constants.HWTEST_TAST_CQ_SUITE,
                            **default_dict),
            config_lib.HWTestConfig('security',
                                    **default_dict),
            config_lib.HWTestConfig('kernel_daily_regression',
                                    **default_dict),
            config_lib.HWTestConfig('kernel_daily_benchmarks',
                                    **default_dict)]

  def ToolchainTestMedium(self, machine_pool, **kwargs):
    """Return list of HWTESTConfigs to run toolchain LLVM correctness tests.

    Since the kernel is not built with LLVM, it makes no sense for the
    toolchain to run kernel tests on LLVM builds.
    """
    default_dict = dict(pool=machine_pool,
                        file_bugs=False,
                        priority=constants.HWTEST_DEFAULT_PRIORITY)
    # Python 3.7+ made async a reserved keyword.
    default_dict['async'] = False
    default_dict.update(kwargs)
    return [config_lib.HWTestConfig(constants.HWTEST_BVT_SUITE,
                                    **default_dict),
            config_lib.HWTestConfig(constants.HWTEST_COMMIT_SUITE,
                                    **default_dict),
            self.TastConfig(constants.HWTEST_TAST_CQ_SUITE,
                            **default_dict),
            config_lib.HWTestConfig('security',
                                    **default_dict)]

  def TastConfig(self, suite_name, **kwargs):
    """Return an HWTestConfig that runs the provided Tast test suite.

    Args:
      suite_name: String suite name, e.g. constants.HWTEST_TAST_CQ_SUITE.
      kwargs: Dict containing additional keyword args to use when constructing
              the HWTestConfig.

    Returns:
      HWTestConfig object for running the suite.
    """
    kwargs = kwargs.copy()

    # Tast test suites run at most three jobs (for system, Chrome, and Android
    # tests) and have short timeouts, so request at most 1 DUT (while retaining
    # passed-in requests for 0 DUTs).
    if kwargs.get('minimum_duts', 0):
      kwargs['minimum_duts'] = 1
    if kwargs.get('suite_min_duts', 0):
      kwargs['suite_min_duts'] = 1

    return config_lib.HWTestConfig(suite_name, **kwargs)

TRADITIONAL_VM_TESTS_SUPPORTED = [
    config_lib.VMTestConfig(constants.VM_SUITE_TEST_TYPE,
                            test_suite='smoke',
                            use_ctest=False),
    config_lib.VMTestConfig(constants.SIMPLE_AU_TEST_TYPE),
    config_lib.VMTestConfig(constants.CROS_VM_TEST_TYPE)]

def InsertHwTestsOverrideDefaults(build):
  """Insert default hw_tests values for a given build.

  Also updates child builds.

  Args:
    build: BuildConfig instance to modify in place.
  """
  for child in build['child_configs']:
    InsertHwTestsOverrideDefaults(child)

  if build['hw_tests_override'] is not None:
    # Explicitly set, no need to insert defaults.
    return

  if build['hw_tests']:
    # Copy over base tests.
    build['hw_tests_override'] = [copy.copy(x) for x in build['hw_tests']]

    # Adjust for manual test environment.
    for hw_config in build['hw_tests_override']:
      # Explicitly set quota account to preserve pre-QuotaScheduler behaviour:
      # Skylab tasks created for tryjobs compete with the general
      # suite_scheduler triggered tasks.
      hw_config.pool = constants.HWTEST_QUOTA_POOL
      hw_config.quota_account = constants.HWTEST_QUOTA_ACCOUNT_SUITES

      hw_config.file_bugs = False
      hw_config.priority = constants.HWTEST_DEFAULT_PRIORITY


def EnsureVmTestsOnVmTestBoards(site_config, boards_dict, _gs_build_config):
  """Make sure VMTests are only enabled on boards that support them.

  Args:
    site_config: config_lib.SiteConfig containing builds to have their
                 waterfall values updated.
    boards_dict: A dict mapping board types to board name collections.
    ge_build_config: Dictionary containing the decoded GE configuration file.
  """
  for c in site_config.values():
    if set(c['boards']).intersection(set(boards_dict['no_vmtest_boards'])):
      c.apply(site_config.templates.no_vmtest_builder)
      if c.child_configs:
        for cc in c.child_configs:
          cc.apply(site_config.templates.no_vmtest_builder)


def ApplyCustomOverrides(site_config):
  """Method with to override specific flags for specific builders.

  Generally try really hard to avoid putting anything here that isn't
  a really special case for a single specific builder. This is performed
  after every other bit of processing, so it always has the final say.

  Args:
    site_config: config_lib.SiteConfig containing builds to have their
                 waterfall values updated.
  """
  overwritten_configs = {
      'guado_labstation-release': {
          'hw_tests': [],
          # 'hwqual':False,
          'image_test':False,
          # 'images':['test'],
          'signer_tests':False,
          'vm_tests':[],
      },

      'fizz-labstation-release': {
          'hw_tests': [],
          'image_test':False,
          'signer_tests':False,
          'vm_tests':[],
      },

      # There's no amd64-generic-release builder, so we use amd64-generic-full
      # to validate informational Tast tests on amd64-generic:
      # https://crbug.com/946858
      'amd64-generic-full': site_config.templates.tast_vm_canary_tests,
      'amd64-generic-vm-full': site_config.templates.tast_vm_canary_tests,
      'betty-kernelnext-release': site_config.templates.tast_vm_canary_tests,
      'betty-pi-arc-release': site_config.templates.tast_vm_canary_tests,
      'betty-release': site_config.templates.tast_vm_canary_tests,
      'novato-release': site_config.templates.tast_vm_canary_tests,
      'reven-vmtest-release': site_config.templates.tast_vm_canary_tests,
  }

  for config_name, overrides in overwritten_configs.items():
    # TODO: Turn this assert into a unittest.
    # config = site_config[config_name]
    # for k, v in overrides.items():
    #   assert config[k] != v, ('Unnecessary override: %s: %s' %
    #                           (config_name, k))
    if config_name in site_config:
      site_config[config_name].apply(**overrides)
    else:
      logging.warning('ignoring overrides for missing config %s', config_name)


def PostsubmitBuilders(site_config):
  """Create all postsubmit test configs.

  Args:
    site_config: config_lib.SiteConfig to be modified by adding templates
                 and configs.
  """
  for config in site_config.values():
    if config.name.endswith('postsubmit'):
      config.apply(
          site_config.templates.no_vmtest_builder,
          site_config.templates.no_hwtest_builder,
      )


def GeneralTemplates(site_config, ge_build_config):
  """Apply test config to general templates

  Args:
    site_config: config_lib.SiteConfig to be modified by adding templates
                 and configs.
    ge_build_config: Dictionary containing the decoded GE configuration file.
  """
  hw_test_list = HWTestList(ge_build_config)

  # TryjobMirrors uses hw_tests_override to ensure that tryjobs run all suites
  # rather than just the ones that are assigned to the board being used. Add
  # bvt-tast-cq here since it includes system, Chrome, and Android tests.
  site_config.AddTemplate(
      'default_hw_tests_override',
      hw_tests_override=hw_test_list.DefaultList(
          # Explicitly set quota account to preserve pre-QuotaScheduler
          # behaviour: Skylab tasks created for tryjobs compete with the general
          # suite_scheduler triggered tasks.
          pool=constants.HWTEST_QUOTA_POOL,
          quota_account=constants.HWTEST_QUOTA_ACCOUNT_SUITES,
          file_bugs=False,
      ),
  )

  # Notice all builders except for vmtest_boards should not run vmtest.
  site_config.AddTemplate(
      'no_vmtest_builder',
      vm_tests=[],
      vm_tests_override=None,
      tast_vm_tests=[],
  )

  site_config.AddTemplate(
      'no_hwtest_builder',
      hw_tests=[],
      hw_tests_override=[],
  )

  site_config.AddTemplate(
      'moblab',
      site_config.templates.no_vmtest_builder,
      image_test=False,
  )

  site_config.templates.full.apply(
      site_config.templates.default_hw_tests_override,
      image_test=True,
  )

  site_config.templates.fuzzer.apply(
      site_config.templates.default_hw_tests_override,
      site_config.templates.no_hwtest_builder,
      image_test=True,
  )

  # BEGIN asan
  site_config.templates.asan.apply(
      site_config.templates.default_hw_tests_override,
  )
  # END asan

  # BEGIN Factory
  site_config.templates.factory.apply(
      # site_config.templates.default_hw_tests_override,
      site_config.templates.no_vmtest_builder,
      site_config.templates.no_hwtest_builder,
  )
  # END Factory

  # BEGIN Loonix
  site_config.templates.loonix.apply(
      site_config.templates.no_vmtest_builder,
      site_config.templates.no_hwtest_builder,
  )
  # END Loonix

  # BEGIN WSHWOS
  site_config.templates.wshwos.apply(
      site_config.templates.no_vmtest_builder,
      site_config.templates.no_hwtest_builder,
  )
  # END WSHWOS

  # BEGIN Dustbuster
  site_config.templates.dustbuster.apply(
      site_config.templates.no_vmtest_builder,
      site_config.templates.no_hwtest_builder,
  )
  # END Dustbuster

  # BEGIN Release
  release_hw_tests = hw_test_list.SharedPoolCanary()

  site_config.templates.release.apply(
      site_config.templates.default_hw_tests_override,
      hw_tests=release_hw_tests,
  )

  site_config.templates.moblab_release.apply(
      site_config.templates.default_hw_tests_override,
      hw_tests=[
          config_lib.HWTestConfig(constants.HWTEST_MOBLAB_SUITE,
                                  timeout=120*60),
          config_lib.HWTestConfig(constants.HWTEST_BVT_SUITE,
                                  warn_only=True),
          hw_test_list.TastConfig(constants.HWTEST_TAST_CQ_SUITE,
                                  warn_only=True),
          config_lib.HWTestConfig(constants.HWTEST_INSTALLER_SUITE,
                                  warn_only=True)],
  )

  site_config.templates.payloads.apply(
      site_config.templates.no_vmtest_builder,
      site_config.templates.no_hwtest_builder,
  )
  # END Release

  site_config.templates.test_ap.apply(
      site_config.templates.no_vmtest_builder,
      site_config.templates.default_hw_tests_override,
  )

  # BEGIN Termina
  site_config.templates.termina.apply(
      site_config.templates.no_vmtest_builder,
      site_config.templates.no_hwtest_builder,
  )
  # END Termina

  # BEGIN Ubsan
  site_config.templates.ubsan.apply(
      site_config.templates.default_hw_tests_override,
  )
  # END Ubsan


def ApplyConfig(site_config, boards_dict, ge_build_config):
  """Apply test specific config to site_config

  Args:
    site_config: config_lib.SiteConfig to be modified by adding templates
                 and configs.
    boards_dict: A dict mapping board types to board name collections.
    ge_build_config: Dictionary containing the decoded GE configuration file.
  """

  # Insert default HwTests for tryjobs.
  for build in site_config.values():
    InsertHwTestsOverrideDefaults(build)

  PostsubmitBuilders(site_config)

  EnsureVmTestsOnVmTestBoards(site_config, boards_dict, ge_build_config)

  ApplyCustomOverrides(site_config)
