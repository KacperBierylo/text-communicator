from PyQt5.QtCore import QPoint, QMargins, Qt
from PyQt5.QtGui import QColor, QTextOption, QTextDocument
from PyQt5.QtWidgets import QStyledItemDelegate

USER_ME = 0
USER_THEM = 1

BUBBLE_COLORS = {USER_ME: "#4299f5", USER_THEM: "#f5da42"}
USER_TRANSLATE = {USER_ME: QPoint(0, 0), USER_THEM: QPoint(0, 0)}

BUBBLE_PADDING = QMargins(15, 5, 15, 5)
TEXT_PADDING = QMargins(25, 15, 25, 15)

class MessageView(QStyledItemDelegate):
    _font = None

    def paint(self, painter, option, index):
        painter.save()
        user, text, author, time = index.model().data(index, Qt.DisplayRole)

        trans = USER_TRANSLATE[user]
        painter.translate(trans)

        bubblerect = option.rect.marginsRemoved(BUBBLE_PADDING)
        textrect = option.rect.marginsRemoved(TEXT_PADDING)

        painter.setPen(Qt.NoPen)
        color = QColor(BUBBLE_COLORS[user])
        painter.setBrush(color)
        painter.drawRoundedRect(bubblerect, 10, 10)

        toption = QTextOption()
        toption.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)

        message = text + "\n\n" + author + " " + time
        doc = QTextDocument(message)
        doc.setTextWidth(textrect.width())
        doc.setDefaultTextOption(toption)
        doc.setDocumentMargin(0)

        painter.translate(textrect.topLeft())
        doc.drawContents(painter)
        painter.restore()

    def sizeHint(self, option, index):
        _, text, author, time = index.model().data(index, Qt.DisplayRole)
        textrect = option.rect.marginsRemoved(TEXT_PADDING)

        toption = QTextOption()
        toption.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)

        message = text + "\n\n" + author + " " + time
        doc = QTextDocument(message)
        doc.setTextWidth(textrect.width())
        doc.setDefaultTextOption(toption)
        doc.setDocumentMargin(0)

        textrect.setHeight(doc.size().height())
        textrect = textrect.marginsAdded(TEXT_PADDING)
        return textrect.size()