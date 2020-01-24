# Copyright (C) 2013, 2014 Red Hat, Inc.
#
# This work is licensed under the GNU GPLv2 or later.
# See the COPYING file in the top-level directory.

import atexit
import imp
import os

# Need to do this before any tests or virtinst import
os.environ["VIRTINST_TEST_SUITE"] = "1"
# Need to do this before we import argcomplete
os.environ.pop("_ARC_DEBUG", None)

# pylint: disable=wrong-import-position
from virtinst import buildconfig
from virtinst import log, reset_logging
# This sets all the cli bits back to their defaults
imp.reload(buildconfig)

from tests import utils

virtinstall = None
virtclone = None
virtxml = None


def setup_logging():
    import logging
    reset_logging()

    fmt = "%(levelname)-8s %(message)s"
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(logging.Formatter(fmt))
    if utils.clistate.debug:
        streamHandler.setLevel(logging.DEBUG)
    else:
        streamHandler.setLevel(logging.ERROR)
    log.addHandler(streamHandler)
    log.setLevel(logging.DEBUG)


def setup_cli_imports():
    _cleanup_imports = []

    def _cleanup_imports_cb():
        for f in _cleanup_imports:
            if os.path.exists(f):
                os.unlink(f)

    def _import(name, path):
        _cleanup_imports.append(path + "c")
        return imp.load_source(name, path)

    global virtinstall
    global virtclone
    global virtxml
    atexit.register(_cleanup_imports_cb)
    virtinstall = _import("virtinstall", "virt-install")
    virtclone = _import("virtclone", "virt-clone")
    virtxml = _import("virtxml", "virt-xml")
