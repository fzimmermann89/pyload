# -*- coding: utf-8 -*-

from module.plugins.internal.MultiHoster import MultiHoster, create_getInfo
from module.plugins.internal.utils import json


class NoPremiumPl(MultiHoster):
    __name__    = "NoPremiumPl"
    __type__    = "hoster"
    __version__ = "0.07"
    __status__  = "testing"

    __pattern__ = r'https?://direct\.nopremium\.pl.+'
    __config__  = [("activated", "bool", "Activated", True),
                   ("use_premium" , "bool", "Use premium account if available"    , True),
                   ("revertfailed", "bool", "Revert to standard download if fails", True)]

    __description__ = """NoPremium.pl multi-hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("goddie", "dev@nopremium.pl")]


    API_URL = "http://crypt.nopremium.pl"

    API_QUERY = {'site'    : "nopremium",
                 'output'  : "json",
                 'username': "",
                 'password': "",
                 'url'     : ""}

    ERROR_CODES = {0 : "Incorrect login credentials",
                   1 : "Not enough transfer to download - top-up your account",
                   2 : "Incorrect / dead link",
                   3 : "Error connecting to hosting, try again later",
                   9 : "Premium account has expired",
                   15: "Hosting no longer supported",
                   80: "Too many incorrect login attempts, account blocked for 24h"}


    def prepare(self):
        super(NoPremiumPl, self).prepare()

        data = self.account.get_data()

        self.usr = data['usr']
        self.pwd = data['pwd']


    def run_file_query(self, url, mode=None):
        query = self.API_QUERY.copy()

        query['username'] = self.usr
        query['password'] = self.pwd
        query['url']      = url

        if mode == "fileinfo":
            query['check'] = 2
            query['loc']   = 1

        self.log_debug(query)

        return self.load(self.API_URL, post=query)


    def handle_free(self, pyfile):
        try:
            data = self.run_file_query(pyfile.url, 'fileinfo')

        except Exception:
            self.temp_offline("Query error #1")

        try:
            parsed = json.loads(data)

        except Exception:
            self.temp_offline("Data not found")

        self.log_debug(parsed)

        if "errno" in parsed.keys():
            if parsed['errno'] in self.ERROR_CODES:
                #: Error code in known
                self.fail(self.ERROR_CODES[parsed['errno']])
            else:
                #: Error code isn't yet added to plugin
                self.fail(parsed['errstring'] or
                          _("Unknown error (code: %s)") % parsed['errno'])

        if "sdownload" in parsed:
            if parsed['sdownload'] == "1":
                self.fail(
                    _("Download from %s is possible only using NoPremium.pl website \
                    directly") % parsed['hosting'])

        pyfile.name = parsed['filename']
        pyfile.size = parsed['filesize']

        try:
            self.link = self.run_file_query(pyfile.url, 'filedownload')

        except Exception:
            self.temp_offline("Query error #2")


getInfo = create_getInfo(NoPremiumPl)
