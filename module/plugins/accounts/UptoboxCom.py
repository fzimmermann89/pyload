# -*- coding: utf-8 -*-

import re
import urlparse

from module.common.json_layer import json_loads
from module.plugins.internal.XFSAccount import XFSAccount


class UptoboxCom(XFSAccount):
    __name__    = "UptoboxCom"
    __type__    = "account"
    __version__ = "0.15"
    __status__  = "testing"

    __description__ = """Uptobox.com account plugin"""
    __license__     = "GPLv3"
    __authors__     = [("benbox69", "dev@tollet.me")]


    PLUGIN_DOMAIN = "uptobox.com"
    PLUGIN_URL    = "http://uptobox.com/"
    LOGIN_URL     = "https://login.uptobox.com/"


    def signin(self, user, password, data):
        if self.COOKIES:
            self.set_xfs_cookie()

        html = self.load(self.LOGIN_URL, cookies=self.COOKIES)

        if re.search(self.LOGIN_SKIP_PATTERN, html):
            self.skip_login()

        html = self.load(urlparse.urljoin(self.LOGIN_URL, "logarithme"),
                         post={'op'      : "login",
                               'redirect': self.PLUGIN_URL,
                               'login'   : user,
                               'password': password},
                         cookies=self.COOKIES)

        if json_loads(html).get('error'):
            self.fail_login()
