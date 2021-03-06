# -*- coding: utf-8 -*-

import re

from module.plugins.internal.XFSHoster import XFSHoster, create_getInfo


class RarefileNet(XFSHoster):
    __name__    = "RarefileNet"
    __type__    = "hoster"
    __version__ = "0.12"
    __status__  = "testing"

    __pattern__ = r'http://(?:www\.)?rarefile\.net/\w{12}'
    __config__  = [("activated", "bool", "Activated", True)]

    __description__ = """Rarefile.net hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("zoidberg", "zoidberg@mujmail.cz")]


    PLUGIN_DOMAIN = "rarefile.net"

    LINK_PATTERN = r'<a href="(.+?)">\1</a>'


getInfo = create_getInfo(RarefileNet)
