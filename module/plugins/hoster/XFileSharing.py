# -*- coding: utf-8 -*-

import re

from module.plugins.internal.XFSHoster import XFSHoster, create_getInfo


class XFileSharing(XFSHoster):
    __name__    = "XFileSharing"
    __type__    = "hoster"
    __version__ = "0.60"
    __status__  = "testing"

    __pattern__ = r'^unmatchable$'
    __config__  = [("activated", "bool", "Activated", True)]

    __description__ = """XFileSharing dummy hoster plugin for hook"""
    __license__     = "GPLv3"
    __authors__     = [("Walter Purcaro", "vuolter@gmail.com")]


    URL_REPLACEMENTS = [("/embed-", "/")]


    def _log(self, level, plugintype, pluginname, messages):
        messages = (self.PLUGIN_NAME,) + messages
        return super(XFileSharing, self)._log(level, plugintype, pluginname, messages)


    def init(self):
        self.__pattern__ = self.pyload.pluginManager.hosterPlugins[self.classname]['pattern']

        self.PLUGIN_DOMAIN = re.match(self.__pattern__, self.pyfile.url).group("DOMAIN").lower()
        self.PLUGIN_NAME   = "".join(part.capitalize() for part in re.split(r'\.|\d+|-', self.PLUGIN_DOMAIN) if part != '.')


    def setup(self):
        self.chunk_limit     = -1 if self.premium else 1
        self.multiDL         = True
        self.resume_download = self.premium


    #@TODO: Recheck in 0.4.10
    def setup_base(self):
        if self.account:
            self.req     = self.pyload.requestFactory.getRequest(self.PLUGIN_NAME, self.account.user)
            self.premium = self.account.info['data']['premium']  #@NOTE: Avoid one unnecessary get_info call by `self.account.premium` here
        else:
            self.req     = self.pyload.requestFactory.getRequest(self.classname)
            self.premium = False

        super(SimpleCrypter, self).setup_base()


    #@TODO: Recheck in 0.4.10
    def load_account(self):
        class_name = self.classname
        self.__class__.__name__ = self.PLUGIN_NAME
        super(XFileSharing, self).load_account()
        self.__class__.__name__ = class_name


getInfo = create_getInfo(XFileSharing)
