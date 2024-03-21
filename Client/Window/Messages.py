from PyQt5.QtCore import QAbstractListModel, Qt

class Messages(QAbstractListModel):
    def __init__( self, *args, **kwargs):
        super(Messages, self).__init__(*args, **kwargs)
        self.messages = []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.messages[index.row()]

    def setData(self, index, role, value):
        self._size[index.row()]

    def rowCount(self, index):
        return len(self.messages)

    def add_message(self, who, text, author, time):
        if text:
            self.messages.append((who, text, author, time))
            self.layoutChanged.emit()
