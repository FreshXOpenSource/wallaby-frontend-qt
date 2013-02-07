# Copyright (c) by it's authors. 
# Some rights reserved. See LICENSE, AUTHORS.

import wallaby.FXUI as FXUI

from wallaby.qt_combat import *

from wallaby.frontends.qt.widgets.labels.extendedWebView import ExtendedWebView

#============================================================================#
# The group name in designer widgetbox                                       #
#----------------------------------------------------------------------------#
DESIGNER_GROUP_NAME = "wallaby@fX"

#============================================================================#
# Plugin for CTLiveView                                                      #
#----------------------------------------------------------------------------#
class ExtendedWebViewPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):

    def __init__(self, parent=None):
        super(ExtendedWebViewPlugin, self).__init__(parent)

        self.initialized = False

    def initialize(self, formEditor):
        if self.initialized:
            return
        self.initialized = True

    def isInitialized(self):
        return self.initialized

    def isContainer(self):
        return False

    def icon(self):
        return FXUI.icon()

    def domXml(self):
        return '<widget class="ExtendedWebView" name="extendedWebView">\n</widget>\n'
    
    def group(self):
        return DESIGNER_GROUP_NAME
              
    def includeFile(self):
        return "wallaby.frontends.qt.widgets.labels.extendedWebView"

    def name(self):
        return "ExtendedWebView"

    def toolTip(self):
        return ""

    def whatsThis(self):
        return ""

    def createWidget(self, parent):
        return ExtendedWebView(parent)
