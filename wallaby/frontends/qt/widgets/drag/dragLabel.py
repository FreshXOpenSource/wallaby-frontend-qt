# Copyright (c) by it's authors. 
# Some rights reserved. See LICENSE, AUTHORS.

import wallaby.FX as FX

from wallaby.qt_combat import *

from dragLogic import *

class DragLabel(QtGui.QLabel, DragLogic):

    def __init__(self, *args):
        QtGui.QLabel.__init__(self, *args)
        DragLogic.__init__(self)

    def mousePressEvent(self, event):
        DragLogic.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        DragLogic.mouseMoveEvent(self, event)
