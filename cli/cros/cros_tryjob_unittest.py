# Copyright 2017 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Tests the `cros chroot` command."""

from unittest import mock

from chromite.cli import command_unittest
from chromite.cli.cros import cros_tryjob
from chromite.lib import config_lib
from chromite.lib import cros_build_lib
from chromite.lib import cros_test_lib
from chromite.utils import outcap


class MockTryjobCommand(command_unittest.MockCommand):
  """Mock out the `cros tryjob` command."""
  TARGET = 'chromite.cli.cros.cros_tryjob.TryjobCommand'
  TARGET_CLASS = cros_tryjob.TryjobCommand
  COMMAND = 'tryjob'


class TryjobTest(cros_test_lib.MockTestCase):
  """Base class for Tryjob command tests."""

  def setUp(self):
    self.cmd_mock = None

  def SetupCommandMock(self, cmd_args):
    """Sets up the `cros tryjob` command mock."""
    self.cmd_mock = MockTryjobCommand(cmd_args)
    self.StartPatcher(self.cmd_mock)

    return self.cmd_mock.inst.options


class TryjobTestPrintKnownConfigs(TryjobTest):
  """Test the PrintKnownConfigs function."""

  def setUp(self):
    self.site_config = config_lib.GetConfig()

  def testConfigsToPrintAllIncluded(self):
    """Test we can generate results for --list."""
    tryjob_configs = cros_tryjob.ConfigsToPrint(
        self.site_config, production=False, build_config_fragments=[])

    release_configs = cros_tryjob.ConfigsToPrint(
        self.site_config, production=True, build_config_fragments=[])

    self.assertEqual(len(self.site_config),
                     len(tryjob_configs) + len(release_configs))

  def testConfigsToPrintFiltered(self):
    """Test ConfigsToPrint filters correctly."""
    tryjob_configs = cros_tryjob.ConfigsToPrint(
        self.site_config, production=False, build_config_fragments=[])

    board_tryjob_configs = cros_tryjob.ConfigsToPrint(
        self.site_config, production=False, build_config_fragments=['hatch'])

    board_release_tryjob_configs = cros_tryjob.ConfigsToPrint(
        self.site_config, production=False,
        build_config_fragments=['hatch', 'release'])

    # Prove expecting things are there.
    self.assertIn(self.site_config['hatch-release-tryjob'],
                  tryjob_configs)
    self.assertIn(self.site_config['hatch-release-tryjob'],
                  board_tryjob_configs)
    self.assertIn(self.site_config['hatch-release-tryjob'],
                  board_release_tryjob_configs)

    # Unexpecting things aren't.
    self.assertNotIn(self.site_config['hatch-release'],
                     tryjob_configs)
    self.assertNotIn(self.site_config['glados-release'],
                     board_tryjob_configs)
    self.assertNotIn(self.site_config['hatch-full'],
                     board_release_tryjob_configs)

    # And that we really filtered something out in every case.
    self.assertLess(len(board_release_tryjob_configs),
                    len(board_tryjob_configs))

    self.assertLess(len(board_tryjob_configs), len(tryjob_configs))

  def testListTryjobs(self):
    """Test we can generate results for --list."""
    with outcap.OutputCapturer() as output:
      cros_tryjob.PrintKnownConfigs(
          self.site_config, production=False, build_config_fragments=[])

    # We have at least 100 lines of output, and no error out.
    self.assertGreater(len(output.GetStdoutLines()), 100)
    self.assertEqual('', output.GetStderr())

  def testListProduction(self):
    """Test we can generate results for --production --list."""
    with outcap.OutputCapturer() as output:
      cros_tryjob.PrintKnownConfigs(
          self.site_config, production=True, build_config_fragments=[])

    # We have at least 100 lines of output, and no error out.
    self.assertGreater(len(output.GetStdoutLines()), 100)
    self.assertEqual('', output.GetStderr())

  def testListTryjobsEmpty(self):
    """Test we can generate ~empty results for failed --list search."""
    with outcap.OutputCapturer() as output:
      cros_tryjob.PrintKnownConfigs(
          self.site_config, production=False,
          build_config_fragments=['this-is-not-a-builder-name'])

    # We have fewer than 6 lines of output, and no error out.
    self.assertLess(len(output.GetStdoutLines()), 6)
    self.assertEqual('', output.GetStderr())


class TryjobTestParsing(TryjobTest):
  """Test cros try command line parsing."""

  def setUp(self):
    self.expected = {
        'where': cros_tryjob.REMOTE,
        'buildroot': None,
        'branch': 'main',
        'production': False,
        'yes': False,
        'list': False,
        'gerrit_patches': [],
        'local_patches': [],
        'passthrough': None,
        'passthrough_raw': None,
        'build_configs': ['eve-full-tryjob'],
    }

  def testMinimalParsing(self):
    """Tests flow for an interactive session."""
    self.SetupCommandMock(['eve-full-tryjob'])
    options = self.cmd_mock.inst.options

    # pylint: disable=dict-items-not-iterating
    self.assertGreaterEqual(vars(options).items(), self.expected.items())

  def testComplexParsingRemote(self):
    """Tests flow for an interactive session."""
    self.SetupCommandMock([
        '--remote',
        '--yes',
        '--latest-toolchain', '--nochromesdk',
        '--hwtest', '--notests', '--novmtests', '--noimagetests',
        '--buildroot', '/buildroot',
        '--timeout', '5', '--sanity-check-build',
        '--gerrit-patches', '123', '-g', '*123', '-g', '123..456',
        '--local-patches', 'chromiumos/chromite:tryjob', '-p', 'other:other',
        '--chrome_version', 'chrome_git_hash',
        '--debug-cidb',
        '--pass-through=--cbuild-arg', '--pass-through', 'bar',
        '--list',
        'eve-full-tryjob', 'eve-release',
    ])
    options = self.cmd_mock.inst.options

    self.expected.update({
        'where': cros_tryjob.REMOTE,
        'buildroot': '/buildroot',
        'branch': 'main',
        'yes': True,
        'list': True,
        'gerrit_patches': ['123', '*123', '123..456'],
        'local_patches': ['chromiumos/chromite:tryjob', 'other:other'],
        'passthrough': [
            '--latest-toolchain', '--nochromesdk',
            '--hwtest', '--notests', '--novmtests', '--noimagetests',
            '--timeout', '5', '--sanity-check-build',
            '--chrome_version', 'chrome_git_hash',
            '--debug-cidb',
        ],
        'passthrough_raw': ['--cbuild-arg', 'bar'],
        'build_configs': ['eve-full-tryjob', 'eve-release'],
    })

    # pylint: disable=dict-items-not-iterating
    self.assertGreaterEqual(vars(options).items(), self.expected.items())

  def testComplexParsingLocal(self):
    """Tests flow for an interactive session."""
    self.SetupCommandMock([
        '--yes',
        '--latest-toolchain', '--nochromesdk',
        '--hwtest', '--notests', '--novmtests', '--noimagetests',
        '--local',
        '--buildroot', '/buildroot',
        '--git-cache-dir', '/git-cache',
        '--timeout', '5', '--sanity-check-build',
        '--gerrit-patches', '123', '-g', '*123', '-g', '123..456',
        '--local-patches', 'chromiumos/chromite:tryjob', '-p', 'other:other',
        '--chrome_version', 'chrome_git_hash',
        '--debug-cidb',
        '--pass-through=--cbuild-arg', '--pass-through', 'bar',
        '--list',
        'eve-full', 'eve-release',
    ])
    options = self.cmd_mock.inst.options

    self.expected.update({
        'where': cros_tryjob.LOCAL,
        'buildroot': '/buildroot',
        'git_cache_dir': '/git-cache',
        'branch': 'main',
        'yes': True,
        'list': True,
        'gerrit_patches': ['123', '*123', '123..456'],
        'local_patches': ['chromiumos/chromite:tryjob', 'other:other'],
        'passthrough': [
            '--latest-toolchain', '--nochromesdk',
            '--hwtest', '--notests', '--novmtests', '--noimagetests',
            '--timeout', '5', '--sanity-check-build',
            '--chrome_version', 'chrome_git_hash',
            '--debug-cidb',
        ],
        'passthrough_raw': ['--cbuild-arg', 'bar'],
        'build_configs': ['eve-full', 'eve-release'],
    })

    # pylint: disable=dict-items-not-iterating
    self.assertGreaterEqual(vars(options).items(), self.expected.items())

  def testComplexParsingCbuildbot(self):
    """Tests flow for an interactive session."""
    self.SetupCommandMock([
        '--yes',
        '--latest-toolchain', '--nochromesdk',
        '--hwtest', '--notests', '--novmtests', '--noimagetests',
        '--cbuildbot',
        '--buildroot', '/buildroot',
        '--git-cache-dir', '/git-cache',
        '--timeout', '5', '--sanity-check-build',
        '--gerrit-patches', '123', '-g', '*123', '-g', '123..456',
        '--local-patches', 'chromiumos/chromite:tryjob', '-p', 'other:other',
        '--chrome_version', 'chrome_git_hash',
        '--pass-through=--cbuild-arg', '--pass-through', 'bar',
        '--list',
        'eve-full-tryjob', 'eve-release',
    ])
    options = self.cmd_mock.inst.options

    self.expected.update({
        'where': cros_tryjob.CBUILDBOT,
        'buildroot': '/buildroot',
        'git_cache_dir': '/git-cache',
        'branch': 'main',
        'yes': True,
        'list': True,
        'gerrit_patches': ['123', '*123', '123..456'],
        'local_patches': ['chromiumos/chromite:tryjob', 'other:other'],
        'passthrough': [
            '--latest-toolchain', '--nochromesdk',
            '--hwtest', '--notests', '--novmtests', '--noimagetests',
            '--timeout', '5', '--sanity-check-build',
            '--chrome_version', 'chrome_git_hash',
        ],
        'passthrough_raw': ['--cbuild-arg', 'bar'],
        'build_configs': ['eve-full-tryjob', 'eve-release'],
    })

    # pylint: disable=dict-items-not-iterating
    self.assertGreaterEqual(vars(options).items(), self.expected.items())

  def testPayloadsParsing(self):
    """Tests flow for an interactive session."""
    self.SetupCommandMock([
        '--version', '9795.0.0', '--channel', 'canary', 'eve-payloads'
    ])
    options = self.cmd_mock.inst.options

    self.expected.update({
        'passthrough': ['--version', '9795.0.0', '--channel', 'canary'],
        'build_configs': ['eve-payloads'],
    })

    # pylint: disable=dict-items-not-iterating
    self.assertGreaterEqual(vars(options).items(), self.expected.items())


class TryjobTestProcessOptions(TryjobTest):
  """Test cros_tryjob.TryjobCommand.ProcessOptions."""

  def testRemote(self):
    """Test default remote buildroot."""
    self.SetupCommandMock(['config'])
    options = self.cmd_mock.inst.options

    cros_tryjob.TryjobCommand.ProcessOptions(None, options)

    self.assertIsNone(options.buildroot)
    self.assertIsNone(options.git_cache_dir)

  def testLocalDefault(self):
    """Test default local buildroot."""
    self.SetupCommandMock(['--local', 'config'])
    options = self.cmd_mock.inst.options

    cros_tryjob.TryjobCommand.ProcessOptions(None, options)

    self.assertTrue(options.buildroot.endswith('/tryjob'))
    self.assertTrue(options.git_cache_dir.endswith('/tryjob/.git_cache'))

  def testLocalExplicit(self):
    """Test explicit local buildroot."""
    self.SetupCommandMock(['--local',
                           '--buildroot', '/buildroot',
                           '--git-cache-dir', '/git-cache',
                           'config'])
    options = self.cmd_mock.inst.options

    cros_tryjob.TryjobCommand.ProcessOptions(None, options)

    self.assertEqual(options.buildroot, '/buildroot')
    self.assertEqual(options.git_cache_dir, '/git-cache')

  def testCbuildbotDefault(self):
    """Test default cbuildbot buildroot."""
    self.SetupCommandMock(['--cbuildbot', 'config'])
    options = self.cmd_mock.inst.options

    cros_tryjob.TryjobCommand.ProcessOptions(None, options)

    self.assertTrue(options.buildroot.endswith('/cbuild'))
    self.assertTrue(options.git_cache_dir.endswith('/cbuild/.git_cache'))

  def testCbuildbotExplicit(self):
    """Test explicit cbuildbot buildroot."""
    self.SetupCommandMock(['--cbuildbot',
                           '--buildroot', '/buildroot',
                           '--git-cache-dir', '/git-cache',
                           'config'])
    options = self.cmd_mock.inst.options

    cros_tryjob.TryjobCommand.ProcessOptions(None, options)

    self.assertEqual(options.buildroot, '/buildroot')
    self.assertEqual(options.git_cache_dir, '/git-cache')


class PromptException(Exception):
  """Raise this in tests, instead of using an interactive prompt."""

class TryjobTestVerifyOptions(TryjobTest):
  """Test cros_tryjob.VerifyOptions."""

  def setUp(self):
    self.site_config = config_lib.GetConfig()

    # Raise an exception instead of blocking the test on a prompt.
    self.PatchObject(cros_build_lib, 'BooleanPrompt',
                     side_effect=PromptException)

  def testEmpty(self):
    """Test option verification with no options."""
    self.SetupCommandMock([])

    with self.assertRaises(cros_build_lib.DieSystemExit) as cm:
      cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)
    self.assertEqual(cm.exception.code, 1)

  def testMinimal(self):
    """Test option verification with simplest normal options."""
    self.SetupCommandMock([
        '-g', '123',
        'amd64-generic-full-tryjob',
    ])
    cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

    self.assertIsNone(self.cmd_mock.inst.options.buildroot)

  def testMinimalLocal(self):
    """Test option verification with simplest normal options."""
    self.SetupCommandMock([
        '-g', '123',
        '--local',
        'amd64-generic-full-tryjob',
    ])
    cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

  def testMinimalCbuildbot(self):
    """Test option verification with simplest normal options."""
    self.SetupCommandMock([
        '--cbuildbot',
        'amd64-generic-full',
    ])
    cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

  def testComplexLocalTryjob(self):
    """Test option verification with complex mix of options."""
    self.SetupCommandMock([
        '--yes',
        '--latest-toolchain', '--nochromesdk',
        '--hwtest', '--notests', '--novmtests', '--noimagetests',
        '--local', '--buildroot', '/buildroot',
        '--timeout', '5', '--sanity-check-build',
        '--gerrit-patches', '123', '-g', '*123', '-g', '123..456',
        '--chrome_version', 'chrome_git_hash',
        '--committer-email', 'foo@bar',
        '--version', '1.2.3', '--channel', 'chan',
        '--pass-through=--cbuild-arg', '--pass-through=bar',
        'eve-full-tryjob', 'eve-release-tryjob',
    ])
    cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

  def testComplexCbuildbot(self):
    """Test option verification with complex mix of options."""
    self.SetupCommandMock([
        '--yes',
        '--latest-toolchain', '--nochromesdk',
        '--hwtest', '--notests', '--novmtests', '--noimagetests',
        '--hwtest_dut_dimensions',
        'label-board:foo label-model:bar label-pool:baz',
        '--cbuildbot', '--buildroot', '/buildroot',
        '--timeout', '5', '--sanity-check-build',
        '--gerrit-patches', '123', '-g', '*123', '-g', '123..456',
        '--committer-email', 'foo@bar',
        '--version', '1.2.3', '--channel', 'chan',
        '--pass-through=--cbuild-arg', '--pass-through=bar',
        'eve-full', 'eve-release',
    ])
    cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

  def testComplexRemoteTryjob(self):
    """Test option verification with complex mix of options."""
    self.SetupCommandMock([
        '--swarming',
        '--yes',
        '--latest-toolchain', '--nochromesdk',
        '--hwtest', '--notests', '--novmtests', '--noimagetests',
        '--timeout', '5', '--sanity-check-build',
        '--gerrit-patches', '123', '-g', '*123', '-g', '123..456',
        '--chrome_version', 'chrome_git_hash',
        '--committer-email', 'foo@bar',
        '--version', '1.2.3', '--channel', 'chan',
        '--pass-through=--cbuild-arg', '--pass-through=bar',
        'eve-full-tryjob', 'eve-release-tryjob',
    ])
    cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

  def testList(self):
    """Test option verification with config list behavior."""
    self.SetupCommandMock([
        '--list',
    ])

    with self.assertRaises(cros_build_lib.DieSystemExit) as cm:
      with outcap.OutputCapturer(quiet_fail=True):  # Hide list output.
        cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)
    self.assertEqual(cm.exception.code, 0)

  def testListProduction(self):
    """Test option verification with config list behavior."""
    self.SetupCommandMock([
        '--list', '--production',
    ])

    with self.assertRaises(cros_build_lib.DieSystemExit) as cm:
      with outcap.OutputCapturer(quiet_fail=True):  # Hide list output.
        cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)
    self.assertEqual(cm.exception.code, 0)

  def testProduction(self):
    """Test option verification with production/no patches."""
    self.SetupCommandMock([
        '--production',
        'eve-full-tryjob', 'eve-release'
    ])

    cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

  def testUnknownConfig(self):
    """Test option verification with production configs on branches."""

    # We have no way of knowing if the config is production or not on a branch,
    # so don't prompt at all
    self.SetupCommandMock([
        'bogus-config'
    ])

    with self.assertRaises(PromptException):
      cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

  def testBranchUnknownConfig(self):
    """Test option verification with production configs on branches."""

    # We have no way of knowing if the config is production or not on a branch,
    # so don't prompt at all
    self.SetupCommandMock([
        '--branch', 'old_branch',
        '--gerrit-patches', '123', '-g', '*123', '-g', '123..456',
        'bogus-config'
    ])

    cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

  def testBranchProductionUnknownConfig(self):
    """Test option verification with production configs on branches."""

    # We have no way of knowing if the config is production or not on a branch,
    # so don't prompt at all
    self.SetupCommandMock([
        '--branch', 'old_branch',
        '--production',
        'bogus-config'
    ])

    cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

  def testBranchProductionConfigTryjob(self):
    """Test option verification with production configs on branches."""

    # We have no way of knowing if the config is production or not on a branch,
    # so don't prompt at all
    self.SetupCommandMock([
        '--branch', 'old_branch',
        '--gerrit-patches', '123', '-g', '*123', '-g', '123..456',
        'eve-release'
    ])

    cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

  def testProductionPatches(self):
    """Test option verification with production/patches."""
    self.SetupCommandMock([
        '--production',
        '--gerrit-patches', '123', '-g', '*123', '-g', '123..456',
        'eve-full-tryjob', 'eve-release'
    ])

    with self.assertRaises(cros_build_lib.DieSystemExit) as cm:
      cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)
    self.assertEqual(cm.exception.code, 1)

  def testRemoteTryjobProductionConfig(self):
    """Test option verification remote tryjob w/production config."""
    self.SetupCommandMock([
        'eve-full-tryjob', 'eve-release'
    ])

    with self.assertRaises(cros_build_lib.DieSystemExit) as cm:
      cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)
    self.assertEqual(cm.exception.code, 1)

  def testLocalTryjobProductionConfig(self):
    """Test option verification local tryjob w/production config."""
    self.SetupCommandMock([
        '--local', 'eve-release'
    ])

    with self.assertRaises(cros_build_lib.DieSystemExit) as cm:
      cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)
    self.assertEqual(cm.exception.code, 1)

  def testInvalidHWTestDUTDimensions(self):
    """Test option verification with invalid hw_test_dut_dimensions."""
    self.SetupCommandMock([
        '--hwtest_dut_dimensions',
        'label-board:foo-board label-model:foo-model label-pol:foo-typo'])

    with self.assertRaises(cros_build_lib.DieSystemExit):
      cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

  def testRemoteTryjobBranchProductionConfig(self):
    """Test a tryjob on a branch for a production config w/confirm."""
    self.SetupCommandMock([
        '--yes', '--branch', 'foo', 'eve-release'
    ])

    cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

  def testRemoteProductionBranchProductionConfig(self):
    """Test a production job on a branch for a production config wo/confirm."""
    self.SetupCommandMock([
        '--production', '--branch', 'foo', 'eve-release'
    ])

    cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

  def testUnknownBuildYes(self):
    """Test option using yes to force accepting an unknown config."""
    self.SetupCommandMock([
        '--yes',
        '-g', '123',
        'unknown-config'
    ])
    cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

  def testNoPatchesYes(self):
    """Test option using yes to force an unknown config, no patches."""
    self.SetupCommandMock([
        '--yes',
        'unknown-config'
    ])
    cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)


class TryjobTestCbuildbotArgs(TryjobTest):
  """Test cros_tryjob.CbuildbotArgs."""

  def helperOptionsToCbuildbotArgs(self, args_in):
    """Convert cros tryjob arguments -> cbuildbot arguments.

    Does not do all intermediate steps, only for testing CbuildbotArgs.
    """
    self.SetupCommandMock(args_in)
    options = self.cmd_mock.inst.options
    cros_tryjob.TryjobCommand.ProcessOptions(None, options)
    args_out = cros_tryjob.CbuildbotArgs(options)
    return args_out

  def testCbuildbotArgsMinimal(self):
    args_in = ['foo-build']

    args_out = self.helperOptionsToCbuildbotArgs(args_in)

    self.assertEqual(args_out, [
        '--remote-trybot', '-b', 'main',
    ])

  def testCbuildbotArgsSimpleRemote(self):
    args_in = ['-g', '123', 'foo-build']

    args_out = self.helperOptionsToCbuildbotArgs(args_in)

    self.assertEqual(args_out, [
        '--remote-trybot', '-b', 'main', '-g', '123',
    ])

  def testCbuildbotArgsSimpleInfraTesting(self):
    args_in = ['--infra-testing', '-g', '123', 'foo-build']

    args_out = self.helperOptionsToCbuildbotArgs(args_in)

    self.assertEqual(args_out, [
        '--remote-trybot', '-b', 'main', '-g', '123',
    ])

  def testCbuildbotArgsSimpleLocal(self):
    args_in = [
        '--local', '-g', '123', 'foo-build',
    ]

    args_out = self.helperOptionsToCbuildbotArgs(args_in)

    # Default buildroot changes.
    self.assertEqual(args_out, [
        '--buildroot', mock.ANY,
        '--git-cache-dir', mock.ANY,
        '--no-buildbot-tags', '--debug',
        '-b', 'main',
        '-g', '123',
    ])

  def testCbuildbotArgsComplexRemote(self):
    args_in = [
        '--yes',
        '--latest-toolchain', '--nochromesdk',
        '--hwtest', '--notests', '--novmtests', '--noimagetests',
        '--timeout', '5', '--sanity-check-build',
        '--gerrit-patches', '123', '-g', '*123', '-g', '123..456',
        '--chrome_version', 'chrome_git_hash',
        '--committer-email', 'foo@bar',
        '--branch', 'source_branch',
        '--version', '1.2.3', '--channel', 'chan',
        '--pass-through=--cbuild-arg', '--pass-through=bar',
        'eve-release',
    ]

    args_out = self.helperOptionsToCbuildbotArgs(args_in)

    self.assertEqual(args_out, [
        '--remote-trybot', '-b', 'source_branch',
        '-g', '123', '-g', '*123', '-g', '123..456',
        '--latest-toolchain', '--nochromesdk',
        '--hwtest', '--notests', '--novmtests', '--noimagetests',
        '--timeout', '5', '--sanity-check-build',
        '--chrome_version', 'chrome_git_hash',
        '--version', '1.2.3', '--channel', 'chan',
        '--cbuild-arg', 'bar'
    ])

  def testCbuildbotArgsComplexLocal(self):
    args_in = [
        '--local', '--yes',
        '--latest-toolchain', '--nochromesdk',
        '--hwtest', '--notests', '--novmtests', '--noimagetests',
        '--buildroot', '/buildroot',
        '--timeout', '5', '--sanity-check-build',
        '--gerrit-patches', '123', '-g', '*123', '-g', '123..456',
        '--chrome_version', 'chrome_git_hash',
        '--committer-email', 'foo@bar',
        '--branch', 'source_branch',
        '--version', '1.2.3', '--channel', 'chan',
        '--pass-through=--cbuild-arg', '--pass-through=bar',
        'eve-release',
    ]

    args_out = self.helperOptionsToCbuildbotArgs(args_in)

    self.assertEqual(args_out, [
        '--buildroot', '/buildroot',
        '--git-cache-dir', '/buildroot/.git_cache',
        '--no-buildbot-tags', '--debug',
        '-b', 'source_branch',
        '-g', '123', '-g', '*123', '-g', '123..456',
        '--latest-toolchain', '--nochromesdk',
        '--hwtest', '--notests', '--novmtests', '--noimagetests',
        '--timeout', '5', '--sanity-check-build',
        '--chrome_version', 'chrome_git_hash',
        '--version', '1.2.3', '--channel', 'chan',
        '--cbuild-arg', 'bar'
    ])

  def testCbuildbotArgsComplexCbuildbot(self):
    args_in = [
        '--cbuildbot', '--yes',
        '--latest-toolchain', '--nochromesdk',
        '--hwtest', '--notests', '--novmtests', '--noimagetests',
        '--hwtest_dut_dimensions', 'foo:bar baz:lol',
        '--buildroot', '/buildroot',
        '--timeout', '5', '--sanity-check-build',
        '--gerrit-patches', '123', '-g', '*123', '-g', '123..456',
        '--committer-email', 'foo@bar',
        '--branch', 'source_branch',
        '--version', '1.2.3', '--channel', 'chan',
        '--pass-through=--cbuild-arg', '--pass-through=bar',
        'eve-full', 'eve-release',
    ]

    args_out = self.helperOptionsToCbuildbotArgs(args_in)

    self.assertEqual(args_out, [
        '--buildroot', '/buildroot/repository',
        '--workspace', '/buildroot/workspace',
        '--git-cache-dir', '/buildroot/.git_cache',
        '--debug', '--nobootstrap', '--noreexec',
        '--no-buildbot-tags',
        '-b', 'source_branch',
        '-g', '123', '-g', '*123', '-g', '123..456',
        '--hwtest_dut_dimensions', 'foo:bar baz:lol',
        '--latest-toolchain', '--nochromesdk',
        '--hwtest', '--notests', '--novmtests', '--noimagetests',
        '--timeout', '5', '--sanity-check-build',
        '--version', '1.2.3', '--channel', 'chan',
        '--cbuild-arg', 'bar'
    ])

  def testCbuildbotArgsProductionRemote(self):
    args_in = [
        '--production', 'foo-build',
    ]

    args_out = self.helperOptionsToCbuildbotArgs(args_in)

    self.assertEqual(args_out, [
        '--buildbot', '-b', 'main',
    ])

  def testCbuildbotArgsProductionLocal(self):
    args_in = [
        '--local', '--production', 'foo-build',
    ]

    args_out = self.helperOptionsToCbuildbotArgs(args_in)

    # Default buildroot changes.
    self.assertEqual(args_out, [
        '--buildroot', mock.ANY,
        '--git-cache-dir', mock.ANY,
        '--no-buildbot-tags', '--buildbot',
        '-b', 'main',
    ])

class TryjobTestDisplayLabel(TryjobTest):
  """Test the helper function DisplayLabel."""

  def FindLabel(self, args):
    site_config = config_lib.GetConfig()
    options = self.SetupCommandMock(args)
    config_name = options.build_configs[-1]
    return cros_tryjob.DisplayLabel(site_config, options, config_name)

  def testMainTryjob(self):
    label = self.FindLabel(['eve-full-tryjob'])
    self.assertEqual(label, 'tryjob')

  def testMainUnknown(self):
    label = self.FindLabel(['bogus-config'])
    self.assertEqual(label, 'tryjob')

  def testMainKnownProduction(self):
    label = self.FindLabel(['--production', 'eve-full'])
    self.assertEqual(label, 'production_tryjob')

  def testMainUnknownProduction(self):
    label = self.FindLabel(['--production', 'bogus-config'])
    self.assertEqual(label, 'production_tryjob')
