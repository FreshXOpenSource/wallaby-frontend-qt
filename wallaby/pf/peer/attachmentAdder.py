# Copyright (c) by it's authors. 
# Some rights reserved. See LICENSE, AUTHORS.

from peer import *

from wallaby.qt_combat import *
from viewer import Viewer
from wallaby.backends.couchdb import *

from twisted.internet import defer

class AttachmentAdder(Peer):
    Add = Pillow.In

    def __init__(self, room, directAdd=True):
        Peer.__init__(self, room)
        self._viewer = Viewer(room, self._setID, '_id')

        self._directAdd = directAdd

        self._id = None
        self._catch(AttachmentAdder.In.Add, self._add)

    def _setID(self, value):
        self._id = value

    @defer.inlineCallbacks
    def _add(self, pillow, feather):
        if self._id != None:
            dialog = QtGui.QFileDialog()
            dialog.setDirectory(QtCore.QDir.homePath())
            dialog.setFileMode(QtGui.QFileDialog.ExistingFiles)
            if dialog.exec_():
                fileNames = dialog.selectedFiles()
                from twisted.internet import threads
                import os.path, mimetypes

                if self._directAdd and self._viewer.document().database() != None:
                    import copy
                    doc = copy.deepcopy(self._viewer.document()._data)
                    db = self._viewer.document().database()
                else:
                    doc = db = None

                for f in fileNames:
                    content = yield threads.deferToThread(self.__readFile, f)
                    name = os.path.basename(f)
                    if self._directAdd and db is not None:
                        (t, encoding) = mimetypes.guess_type(name)
                        if t != None:
                            yield db.put_attachment(doc, name, content, t)
                        else:
                            yield db.put_attachment(doc, name, content)
                    else:
                        self._viewer.document().setAttachment(name, content)

    def __readFile(self, f):
        return open(f, "rb").read()
