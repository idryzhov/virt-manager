# Copyright (C) 2013, 2014 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.

import atexit
import imp
import logging
import os

os.environ["VIRTINST_TEST_TRACKPROPS"] = "1"
os.environ["VIRTINST_TEST_SUITE"] = "1"

import virtinst
virtinst.stable_defaults = False

from virtcli import cliconfig
# This sets all the cli bits back to their defaults
reload(cliconfig)

from tests import utils

# pylint: disable=W0212
# Access to protected member, needed to unittest stuff

# Force certain helpers to return consistent values
virtinst.util.is_blktap_capable = lambda ignore: False
virtinst.util.default_bridge = lambda ignore1: ["bridge", "eth0"]

# Setup logging
rootLogger = logging.getLogger()
for handler in rootLogger.handlers:
    rootLogger.removeHandler(handler)

logging.basicConfig(level=logging.DEBUG,
                    format="%(levelname)-8s %(message)s")

if utils.get_debug():
    rootLogger.setLevel(logging.DEBUG)
else:
    rootLogger.setLevel(logging.ERROR)

_cleanup_imports = []


def _import(name, path):
    _cleanup_imports.append(path + "c")
    return imp.load_source(name, path)


def _cleanup_imports_cb():
    for f in _cleanup_imports:
        if os.path.exists(f):
            os.unlink(f)

atexit.register(_cleanup_imports_cb)
virtinstall = _import("virtinstall", "virt-install")
virtimage = _import("virtimage", "virt-image")
virtclone = _import("virtclone", "virt-clone")
virtconvert = _import("virtconvert", "virt-convert")
virtxml = _import("virtxml", "virt-xml")

# Variable used to store a local iso or dir path to check for a distro
# Specified via 'python setup.py test_urls --path"
URLTEST_LOCAL_MEDIA = []

# Used to implement test_initrd_inject --distro
INITRD_TEST_DISTROS = []
