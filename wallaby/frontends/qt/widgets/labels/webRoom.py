from wallaby.qt_combat import *

class WebRoom(QtCore.QObject):
    pillow = Signal('QString', 'QVariant')

    def __init__(self, room):
        QtCore.QObject.__init__(self)
        self._room = room

    @Property("QString")
    def room(self):
        return self._room.roomName()

    @Slot("QString")
    def _catch(self, pillow):
        self._room.catch(pillow, self.__catch)

    def __catch(self, pillow, feathers):
        from wallaby.common.document import Document
        if isinstance(feathers, Document):
            self.pillow.emit( pillow, feathers._data)
        else:
            self.pillow.emit( pillow, feathers)

    @Slot("QString", "QVariant")
    def _throw(self, pillow, feathers):
        self._room.throw(pillow, feathers)
