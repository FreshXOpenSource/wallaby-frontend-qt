# Copyright (c) by it's authors. 
# Some rights reserved. See LICENSE, AUTHORS.

import codecs
import wallaby.FX as FX
import wallaby.FXUI as FXUI

from wallaby.qt_combat import *

from ..baseWidget import *
from ..logics import *

from wallaby.pf.peer.viewer import *
from webRoom import WebRoom

import copy

class ExtendedWebView(QtWebKit.QWebView, BaseWidget, EnableLogic, ViewLogic, TriggeredPillowsLogic):
    __metaclass__ = QWallabyMeta

    triggers = Meta.property("list", readOnly=True, default=["", "clicked"])
    templateName = Meta.property("string")

    ignoreSSLErrors = Meta.property("bool")

    def __init__(self, *args):
        QtWebKit.QWebView.__init__(self, *args)
        BaseWidget.__init__(self, QtWebKit.QWebView, *args)
        EnableLogic.__init__(self)
        ViewLogic.__init__(self, Viewer, self._setData)
        TriggeredPillowsLogic.__init__(self)

        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)

        self.linkClicked.connect(self._linkActivated)

        self._webRoom = WebRoom(self)

        self.page().mainFrame().javaScriptWindowObjectCleared.connect(self._registerObjects)
        self._registerObjects()

        palette = self.palette()
        palette.setBrush(QtGui.QPalette.Base, QtCore.Qt.transparent)
        self.page().setPalette(palette)
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent, False)

        self._index = "<html><body>Template not found</body></html>"
        self._content = ""
        self._content_js = ""
        self._scripts = {}
        self._styles = {}

        self.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.page().settings().setAttribute(QtWebKit.QWebSettings.JavascriptEnabled, True)
        self.page().settings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
        self.page().settings().setAttribute(QtWebKit.QWebSettings.XSSAuditingEnabled, False)
        self.page().settings().setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls, True)

    def _registerObjects(self):
        self.page().mainFrame().addToJavaScriptWindowObject("wallaby", self._webRoom)

    def _linkActivated(self, url):
        link = unicode(url.toString())
        if link.startswith('wlby://'):
            link = link.replace('wlby://', '')
            args = None
            if '/' in link:
                args = link.split('/')
                cmd = args.pop(0)
                self._triggeredValue = args
                self.trigger("clicked")

    def deregister(self, remove=False):
        EnableLogic.deregister(self, remove)
        ViewLogic.deregister(self, remove)
        TriggeredPillowsLogic.deregister(self, remove)

    # Proxy for webRoom
    def catch(self, pillow, cb):
        House.get(self.room).catch(pillow, cb)

    def throw(self, pillow, feathers):
        House.get(self.room).throw(pillow, feathers)

    def roomName(self):
        return self.room

    def register(self):
        EnableLogic.register(self)
        ViewLogic.register(self, raw=True)
        TriggeredPillowsLogic.register(self)

        import os.path
        if self.templateName is not None and FXUI.app is not None and os.path.exists(os.path.join(FX.appPath, "templates", self.templateName, "index.html")):
            self._index = codecs.open(os.path.join(FX.appPath, "templates", self.templateName, "index.html"), "r", "utf-8").read()

            if os.path.exists(os.path.join(FX.appPath, "templates", self.templateName, "content.html")):
                self._content = codecs.open(os.path.join(FX.appPath, "templates", self.templateName, "content.html"), "r", "utf-8").read()

            if os.path.exists(os.path.join(FX.appPath, "templates", self.templateName, "content.js")):
                self._content_js = codecs.open(os.path.join(FX.appPath, "templates", self.templateName, "content.js"), "r", "utf-8").read()

            import pystache
            self._index = pystache.render(unicode(self._index), {"scripts": self._scripts, "styles": self._styles})

        if os.path.exists(os.path.join(FX.appPath, "templates", self.templateName, "index.html")):
            url = QtCore.QUrl.fromLocalFile(os.path.abspath(os.path.join(FX.appPath, "templates", self.templateName, "index.html")))
            self.setHtml(unicode(self._index), url)
            
        else:
            self.setHtml(unicode(self._index))

        if self.ignoreSSLErrors:
            self.page().networkAccessManager().sslErrors.connect(self._sslErrorHandler)

    def _sslErrorHandler(self, reply, errorList):
        # Ignore SSL Error!! Fix Me
        reply.ignoreSslErrors()
        return
    
    def _setData(self, _data):
        data = _data
        if isinstance(_data, dict):
            data = []
            for key in sorted(_data.keys()):
                data.append({"key": key, "value": _data[key]})

        import pystache
        page = pystache.render(unicode(self._content), {"data": data})

        e = self.page().mainFrame().findFirstElement('#content')
        e.setInnerXml(page)

        if self._content_js != None:
            self.page().mainFrame().evaluateJavaScript(self._content_js)
