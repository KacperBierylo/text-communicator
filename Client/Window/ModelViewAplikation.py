import datetime
from PyQt5.QtWidgets import *

from Window.Messages import Messages
from Window.MessageView import MessageView
from Window.FileSelector import FileSelector
class ModelViewApliation(QMainWindow):
    ms = 0
    value = 500
    def __init__(self,ms_):
        super(ModelViewApliation, self).__init__()
        self.ms = ms_
        self.initilize()
        l = QVBoxLayout()
        h = QHBoxLayout()
        main = QVBoxLayout()
        main.addLayout(l)
        main.addLayout(h)

        self.message_input = QLineEdit("Wiadomosc")

        radioButton = QRadioButton("CBC")
        radioButton.setChecked(True)
        radioButton.counter = "CBC"
        radioButton.toggled.connect(self.ClickCBC)
        main.addWidget(radioButton)
        radioButton = QRadioButton("ECB")
        radioButton.counter = "ECB"
        radioButton.toggled.connect(self.ClickECB)
        main.addWidget(radioButton)

        self.btn1 = QPushButton("Send")
        self.btn2 = QPushButton("File") #not implement

        self.messages = QListView()
        self.messages.setResizeMode(QListView.Adjust)
        self.messages.setItemDelegate(MessageView())

        self.model = Messages()
        self.messages.setModel(self.model)

        self.btn1.pressed.connect(self.message_to)
        self.btn2.pressed.connect(self.info)

        l.addWidget(self.messages)
        h.addWidget(self.message_input)
        h.addWidget(self.btn1)
        h.addWidget(self.btn2)

        self.w = QWidget()
        self.w.setLayout(main)
        self.setCentralWidget(self.w)

    def ClickECB(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.ms.changeTypeCode("ECB")
            print("ECB")

    def ClickCBC(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.ms.changeTypeCode("CBC")
            print("CBC")

    def initilize(self):
        self.resize(500, 500)
        self.setWindowTitle("ChatApp")

    def resizeEvent(self, e):
        self.model.layoutChanged.emit()

    def message_to(self):
        author = "ME"
        time = datetime.datetime.now()
        timeConvert = time.strftime("%Y-%m-%d %H:%M:%S")
        message = self.message_input.text()
        self.model.add_message(1, message, author, timeConvert)
        self.ms.sendMessage(message,author,time)

    def message_from(self, mess, author, time:datetime.datetime):
        time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.model.add_message(0, mess, author, time)
        self.refreshWindow()

    def info(self):
        # QMessageBox.about(self, "Information", "Ta fukncje nie została jeszcze zaimplementowana")
        self.fs = FileSelector()
        filepath = self.fs.filename
        self.fs.close()
        print(filepath)
        time = datetime.datetime.now()
        timeConvert = time.strftime("%Y-%m-%d %H:%M:%S")
        self.ms.sendFile(filepath)

    def refreshWindow(self):
        if self.value == 500:
            self.resize(500, 501)
            self.value = 510
        else:
            self.resize(500,500)
            self.value = 500