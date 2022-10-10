# Copyright 2015 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Module to download and run the CIPD client.

CIPD is the Chrome Infra Package Deployer, a simple method of resolving a
package/version into a GStorage link and installing them.
"""

import hashlib
import json
import logging
import os
from pathlib import Path
import pprint
import tempfile
from typing import Union
import urllib.parse

from chromite.third_party import httplib2

from chromite.lib import cache
from chromite.lib import cros_build_lib
from chromite.lib import osutils
from chromite.lib import path_util
from chromite.utils import memoize


# pylint: disable=line-too-long
# CIPD client to download.
#
# This is version "git_revision:78137bc2d58ebea680b6d513a3d7f6a8d25aa643".
#
# To switch to another version:
#   1. Find it in CIPD Web UI, e.g.
#      https://chrome-infra-packages.appspot.com/p/infra/tools/cipd/linux-amd64/+/latest
#   2. Look up SHA256 there.
# pylint: enable=line-too-long
CIPD_CLIENT_PACKAGE = "infra/tools/cipd/linux-amd64"
CIPD_CLIENT_SHA256 = (
    "b431c29c9fa132d4f7d6e86f053af02d490b51d742b4f01ea55618a5365d357d"
)

CHROME_INFRA_PACKAGES_API_BASE = (
    "https://chrome-infra-packages.appspot.com/prpc/cipd.Repository/"
)


class Error(Exception):
    """Raised on fatal errors."""


def _ChromeInfraRequest(method, request):
    """Makes a request to the Chrome Infra Packages API with httplib2.

    Args:
        method: Name of RPC method to call.
        request: RPC request body.

    Returns:
        Deserialized RPC response body.
    """
    resp, body = httplib2.Http().request(
        uri=CHROME_INFRA_PACKAGES_API_BASE + method,
        method="POST",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "chromite",
        },
        body=json.dumps(request),
    )
    if resp.status != 200:
        raise Error(
            "Got HTTP %d from CIPD %r: %s" % (resp.status, method, body)
        )
    try:
        return json.loads(body.lstrip(b")]}'\n"))
    except ValueError:
        raise Error("Bad response from CIPD server:\n%s" % (body,))


def _DownloadCIPD(instance_sha256):
    """Finds the CIPD download link and requests the binary.

    Args:
        instance_sha256: The version of CIPD client to download.

    Returns:
        The CIPD binary as a string.
    """
    # Grab the signed URL to fetch the client binary from.
    resp = _ChromeInfraRequest(
        "DescribeClient",
        {
            "package": CIPD_CLIENT_PACKAGE,
            "instance": {
                "hashAlgo": "SHA256",
                "hexDigest": instance_sha256,
            },
        },
    )
    if "clientBinary" not in resp:
        logging.error(
            "Error requesting the link to download CIPD from. Got:\n%s",
            pprint.pformat(resp),
        )
        raise Error("Failed to bootstrap CIPD client")

    # Download the actual binary.
    http = httplib2.Http(cache=None)
    response, binary = http.request(uri=resp["clientBinary"]["signedUrl"])
    if response.status != 200:
        raise Error("Got a %d response from Google Storage." % response.status)

    # Check SHA256 matches what server expects.
    digest = hashlib.sha256(binary).hexdigest()
    for alias in resp["clientRefAliases"]:
        if alias["hashAlgo"] == "SHA256":
            if digest != alias["hexDigest"]:
                raise Error(
                    "Unexpected CIPD client SHA256: got %s, want %s"
                    % (digest, alias["hexDigest"])
                )
            break
    else:
        raise Error("CIPD server didn't provide expected SHA256")

    return binary


class CipdCache(cache.RemoteCache):
    """Supports caching of the CIPD download."""

    def _Fetch(self, url, local_path):
        instance_sha256 = urllib.parse.urlparse(url).netloc
        binary = _DownloadCIPD(instance_sha256)
        logging.info(
            "Fetched CIPD package %s:%s", CIPD_CLIENT_PACKAGE, instance_sha256
        )
        osutils.WriteFile(local_path, binary, mode="wb")
        os.chmod(local_path, 0o755)


def GetCIPDFromCache():
    """Checks the cache, downloading CIPD if it is missing.

    Returns:
        Path to the CIPD binary.
    """
    cache_dir = os.path.join(path_util.GetCacheDir(), "cipd")
    bin_cache = CipdCache(cache_dir)
    key = (CIPD_CLIENT_SHA256,)
    ref = bin_cache.Lookup(key)
    ref.SetDefault("cipd://" + CIPD_CLIENT_SHA256)
    return ref.path


def GetInstanceID(cipd_path, package, version, service_account_json=None):
    """Get the latest instance ID for ref latest.

    Args:
        cipd_path: Path to a cipd executable. GetCIPDFromCache can give this.
        package: A string package name.
        version: A string version of package.
        service_account_json: The path of the service account credentials.

    Returns:
        A string instance ID.
    """
    service_account_flag = []
    if service_account_json:
        service_account_flag = ["-service-account-json", service_account_json]

    result = cros_build_lib.run(
        [cipd_path, "resolve", package, "-version", version]
        + service_account_flag,
        capture_output=True,
        encoding="utf-8",
    )
    # An example output of resolve is like:
    #   Packages:\n package:instance_id
    return result.stdout.splitlines()[-1].split(":")[-1]


@memoize.Memoize
def InstallPackage(
    cipd_path,
    package,
    version,
    destination: Union[os.PathLike, str] = None,
    service_account_json=None,
):
    """Installs a package at a given destination using cipd.

    Args:
        cipd_path: Path to a cipd executable. GetCIPDFromCache can give this.
        package: A package name.
        version: The CIPD version of the package to install (can be instance ID
            or a ref).
        destination: The folder to install the package under.
        service_account_json: The path of the service account credentials.

    Returns:
      The path of the package.
    """
    if not destination:
        # GetCacheDir does a non-trivial amount of work,
        # too much for a constant. If needed elsewhere, a
        # memoized function would be a good alternative.
        destination = (
            Path(path_util.GetCacheDir()).absolute() / "cipd" / "packages"
        )

    destination = Path(destination) / package

    service_account_flag = []
    if service_account_json:
        service_account_flag = ["-service-account-json", service_account_json]

    with tempfile.NamedTemporaryFile() as f:
        f.write(("%s %s" % (package, version)).encode("utf-8"))
        f.flush()

        cros_build_lib.dbg_run(
            [cipd_path, "ensure", "-root", destination, "-list", f.name]
            + service_account_flag,
            capture_output=True,
        )

    return destination


def CreatePackage(cipd_path, package, in_dir, tags, refs, cred_path=None):
    """Create (build and register) a package using cipd.

    Args:
        cipd_path: Path to a cipd executable. GetCIPDFromCache can give this.
        package: A package name.
        in_dir: The directory to create the package from.
        tags: A mapping of tags to apply to the package.
        refs: An Iterable of refs to apply to the package.
        cred_path: The path of the service account credentials.
    """
    args = [
        cipd_path,
        "create",
        "-name",
        package,
        "-in",
        in_dir,
    ]
    for key, value in tags.items():
        args.extend(["-tag", "%s:%s" % (key, value)])
    for ref in refs:
        args.extend(["-ref", ref])
    if cred_path:
        args.extend(["-service-account-json", cred_path])

    cros_build_lib.run(args, capture_output=True)
