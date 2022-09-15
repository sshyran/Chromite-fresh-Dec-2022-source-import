# Copyright 2017 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Update the CHROMEOS_LKGM file in a chromium repository.

This script will upload an LKGM CL and potentially submit it to the CQ.
"""

import logging

from chromite.lib import chromeos_version
from chromite.lib import commandline
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import gerrit
from chromite.lib import gob_util


class LKGMNotValid(Exception):
    """Raised if the LKGM version is unset or not newer than the current value."""


class LKGMFileNotFound(Exception):
    """Raised if the LKGM file is not found."""


class ChromeLKGMCommitter(object):
    """Committer object responsible for obtaining a new LKGM and committing it."""

    # The list of trybots we require LKGM updates to run and pass on before
    # landing. Since they're internal trybots, the CQ won't automatically trigger
    # them, so we have to explicitly tell it to.
    _PRESUBMIT_BOTS = [
        "chromeos-betty-pi-arc-chrome",
        "chromeos-eve-chrome",
        "chromeos-kevin-chrome",
        "chromeos-octopus-chrome",
        "chromeos-reven-chrome",
        "lacros-amd64-generic-chrome",
    ]
    # Files needed in a local checkout to successfully update the LKGM. The OWNERS
    # file allows the --tbr-owners mechanism to select an appropriate OWNER to
    # TBR. TRANSLATION_OWNERS is necesssary to parse CHROMEOS_OWNERS file since
    # it has the reference.
    _NEEDED_FILES = [
        constants.PATH_TO_CHROME_CHROMEOS_OWNERS,
        constants.PATH_TO_CHROME_LKGM,
        "tools/translation/TRANSLATION_OWNERS",
    ]
    # First line of the commit message for all LKGM CLs.
    _COMMIT_MSG_HEADER = "Automated Commit: LKGM %(lkgm)s for chromeos."

    def __init__(self, lkgm, branch, dryrun=False, buildbucket_id=None):
        self._dryrun = dryrun
        self._branch = branch
        self._buildbucket_id = buildbucket_id
        self._gerrit_helper = gerrit.GetCrosExternal()

        # We need to use the account used by the builder to upload git CLs when
        # generating CLs.
        self._user_email = None
        if cros_build_lib.HostIsCIBuilder(golo_only=True):
            self._user_email = "chromeos-commit-bot@chromium.org"
        elif cros_build_lib.HostIsCIBuilder(gce_only=True):
            self._user_email = "3su6n15k.default@developer.gserviceaccount.com"

        # Strip any chrome branch from the lkgm version.
        self._lkgm = chromeos_version.VersionInfo(lkgm).VersionString()
        self._commit_msg_header = self._COMMIT_MSG_HEADER % {"lkgm": self._lkgm}
        self._current_lkgm = None

        if not self._lkgm:
            raise LKGMNotValid("LKGM not provided.")
        logging.info("lkgm=%s", lkgm)

    def Run(self):
        self.AbandonObsoleteLKGMRolls()
        self.UpdateLKGM()

    @property
    def lkgm_file(self):
        return self._committer.FullPath(constants.PATH_TO_CHROME_LKGM)

    def AbandonObsoleteLKGMRolls(self):
        """Abandon all obsolete LKGM roll CLs.

        This method finds the LKGM roll CLs that were trying changing to an
        older version than the current LKGM version, and abandons them.
        """
        query_params = {
            "project": constants.CHROMIUM_SRC_PROJECT,
            "branch": self._branch,
            "file": constants.PATH_TO_CHROME_LKGM,
            "status": "open",
            # Use 'owner' rather than 'uploader' or 'author' since those last two
            # can be overwritten when the gardener resolves a merge-conflict and
            # uploads a new patchset.
            "owner": self._user_email,
        }
        open_changes = self._gerrit_helper.Query(**query_params)
        if not open_changes:
            logging.info("No old LKGM rolls detected.")
            return

        logging.info(
            "Retrieved the current LKGM version: %s",
            self.GetCurrentLKGM().VersionString(),
        )

        build_link = ""
        if self._buildbucket_id:
            build_link = (
                "\nUpdated by"
                f" https://ci.chromium.org/b/{self._buildbucket_id}\n"
            )

        for change in open_changes:
            logging.info(
                "Found a open LKGM roll CL: %s (crrev.com/c/%s).",
                change.subject,
                change.gerrit_number,
            )
            version_string = change.GetFileContents(
                constants.PATH_TO_CHROME_LKGM
            )
            if version_string is None:
                logging.info("=> No LKGM change found in this CL.")
                continue

            version = chromeos_version.VersionInfo(version_string)
            if version <= self.GetCurrentLKGM():
                # The target version that the CL is changing to is older than
                # the current. The roll CL is useless so that it'd be abandoned.
                logging.info(
                    "=> This CL is an older LKGM roll than current: Abandoning"
                )
                if not self._dryrun:
                    abandon_message = (
                        "The newer LKGM"
                        f" ({self.GetCurrentLKGM().VersionString()}) roll than"
                        f" this CL has been landed.{build_link}"
                    )
                    self._gerrit_helper.AbandonChange(
                        change,
                        msg=abandon_message,
                    )
            else:
                # Do nothing with the roll CLs that tries changing to newer
                # version.
                # TODO(yoshiki): rebase the roll CL.
                logging.info(
                    "=> This CL is a newer LKGM roll than current: Do nothing."
                )

    def GetCurrentLKGM(self):
        """Returns the current LKGM version on the branch.

        On the first call, this method retrieves the LKGM version from Gltlies
        server and returns it. On subsequent calls, this method returns the
        cached LKGM version.

        Raises:
          LKGMNotValid: if the retrieved LKGM version from the repository is
          invalid.
        """
        if self._current_lkgm is not None:
            return self._current_lkgm

        current_lkgm = gob_util.GetFileContents(
            constants.CHROMIUM_GOB_URL,
            constants.PATH_TO_CHROME_LKGM,
            ref=self._branch,
        )
        if current_lkgm is None:
            raise LKGMNotValid(
                "The retrieved LKGM version from the repository is invalid:"
                f" {self._current_lkgm}."
            )

        self._current_lkgm = chromeos_version.VersionInfo(current_lkgm.strip())
        return self._current_lkgm

    def UpdateLKGM(self):
        """Updates the LKGM file with the new version."""
        if chromeos_version.VersionInfo(self._lkgm) <= self.GetCurrentLKGM():
            raise LKGMNotValid(
                f"LKGM version ({self._lkgm}) is not newer than current version"
                f" ({self.GetCurrentLKGM().VersionString()})."
            )

        logging.info(
            "Updating LKGM version: %s (was %s),",
            self._lkgm,
            self.GetCurrentLKGM().VersionString(),
        )
        change = self._gerrit_helper.CreateChange(
            "chromium/src", self._branch, self.ComposeCommitMsg(), False
        )
        self._gerrit_helper.ChangeEdit(
            change.gerrit_number, "chromeos/CHROMEOS_LKGM", self._lkgm
        )

        if self._dryrun:
            logging.info(
                "Would have applied CQ+2 to crrev.com/c/%s",
                change.gerrit_number,
            )
            self._gerrit_helper.AbandonChange(
                change,
                msg="Dry run",
            )
            return

        labels = {
            "Bot-Commit": 1,
            "Commit-Queue": 2,
        }
        logging.info(
            "Applying %s to crrev.com/c/%s", labels, change.gerrit_number
        )
        self._gerrit_helper.SetReview(
            change.gerrit_number, labels=labels, notify="NONE"
        )
        self._gerrit_helper.SetHashtags(
            change.gerrit_number, ["chrome-lkgm"], []
        )

    def ComposeCommitMsg(self):
        """Constructs and returns the commit message for the LKGM update."""
        dry_run_message = (
            "This CL was created during a dry run and is not "
            "intended to be committed.\n"
        )
        commit_msg_template = (
            "%(header)s\n%(build_link)s\n%(message)s\n%(cq_includes)s"
        )
        cq_includes = ""
        for bot in self._PRESUBMIT_BOTS:
            cq_includes += "CQ_INCLUDE_TRYBOTS=luci.chrome.try:%s\n" % bot
        build_link = ""
        if self._buildbucket_id:
            build_link = "\nUploaded by https://ci.chromium.org/b/%s\n" % (
                self._buildbucket_id
            )
        return commit_msg_template % dict(
            header=self._commit_msg_header,
            cq_includes=cq_includes,
            build_link=build_link,
            message=dry_run_message if self._dryrun else "",
        )


def GetOpts(argv):
    """Returns a dictionary of parsed options.

    Args:
      argv: raw command line.

    Returns:
      Dictionary of parsed options.
    """
    parser = commandline.ArgumentParser(description=__doc__, add_help=False)
    parser.add_argument(
        "--dryrun",
        action="store_true",
        default=False,
        help="Don't commit changes or send out emails.",
    )
    parser.add_argument(
        "--lkgm", required=True, help="LKGM version to update to."
    )
    parser.add_argument(
        "--buildbucket-id",
        help="Buildbucket ID of the build that ran this script. "
        "Will be linked in the commit message if specified.",
    )
    parser.add_argument(
        "--branch",
        default="main",
        help="Branch to upload change to, e.g. "
        "refs/branch-heads/5112. Defaults to main.",
    )
    return parser.parse_args(argv)


def main(argv):
    opts = GetOpts(argv)
    committer = ChromeLKGMCommitter(
        opts.lkgm, opts.branch, opts.dryrun, opts.buildbucket_id
    )
    committer.Run()
    return 0
