from wallaby.qt_combat import *
from wallaby.pf.room import *
from twisted.internet import defer

class WebHouse(QtCore.QObject):
    def __init__(self, view):
        QtCore.QObject.__init__(self)
        self._rooms = {}
        self._view = view

    @Property("QString")
    def roomName(self):
        return self._view.roomName()

    @Slot("QString", result="QString")
    def get(self, name):
        if name in self._rooms:
            room = self._rooms[name] 
        else:
            room = WebRoom(self._view, House.get(name))
            self._rooms[name] = room

        self._view.registerObject("wlbyRoom_" + name, room)
        return name

class WebRoom(QtCore.QObject):
    pillow = Signal('QString', 'QVariant')
    docPillow = Signal('QString', 'QString')
    resultPillow = Signal('QString', 'QString')

    def __init__(self, view, room):
        QtCore.QObject.__init__(self)
        self._view = view
        self._room = room

    @Property("QString")
    def name(self):
        return self._room.name()

    @Slot("QString")
    def _catch(self, pillow):
        self._room.catch(pillow, self.__catch)

    def __catch(self, pillow, feathers):
        from wallaby.common.queryResult import QueryResult
        from wallaby.common.document import Document

        if isinstance(feathers, QueryResult):
            class QueryResultWrapper(QtCore.QObject):
                value = Signal('int', 'QString', 'QVariant')

                def __init__(self, result):
                    QtCore.QObject.__init__(self)
                    self._result = result 

                @Property("int")
                def length(self):
                    return self._result.length()

                @Property("QString")
                def identifier(self):
                    return self._result.identifier()

                @Slot('int', 'QString')
                def get(self, idx, path):
                    self.deferredGet(idx, path)

                @defer.inlineCallbacks
                def deferredGet(self, idx, path):
                    value = yield self._result.deferredGetValue(idx, path)
                    self.value.emit(idx, path, value)

            self._view.registerObject("wlbyResult_" + feathers.identifier(), QueryResultWrapper(feathers))
            self.resultPillow.emit( pillow, feathers.identifier() )

        elif isinstance(feathers, Document):
            class DocumentWrapper(QtCore.QObject):
                def __init__(self, doc):
                    QtCore.QObject.__init__(self)
                    self._doc = doc 

                def document(self):
                    return self._doc

                @Slot('QString', result='QVariant')
                def get(self, path):
                    return self._doc.get(path)

                @Slot('QString', 'QVariant')
                def set(self, path, value):
                    self._doc.set(path, value)

            self._view.registerObject("wlbyDoc_" + feathers.documentID, DocumentWrapper(feathers))
            self.docPillow.emit( pillow, feathers.documentID)
        else:
            self.pillow.emit( pillow, feathers)

    @Slot("QString", "QString")
    def _throwDoc(self, pillow, _id):
        doc = self._view.registeredObject(_id)
        if doc != None:
            self._room.throw(pillow, doc.document())
        else:
            print "Doc with Id", _id, "not registered in room", self._view.roomName()

    @Slot("QString", "QVariant")
    def _throw(self, pillow, feathers):
        self._room.throw(pillow, feathers)
