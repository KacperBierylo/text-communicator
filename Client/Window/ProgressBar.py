# importing libraries
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
from PyQt5.QtWidgets import QApplication

class ProgressBar(QWidget):

    def __init__(self):
        super().__init__()

        # calling initUI method
        self.initUI()

    # method for creating widgets
    def initUI(self):
        # creating progress bar
        self.pbar = QProgressBar(self)

        # setting its geometry
        self.pbar.setGeometry(30, 40, 200, 25)

        # creating push button
        #self.btn = QPushButton('Start', self)

        # changing its position
        #self.btn.move(40, 80)

        # adding action to push button
        #self.btn.clicked.connect(self.doAction)

        # setting window geometry
        self.setGeometry(300, 300, 280, 170)

        # setting window action
        self.setWindowTitle("Wysylanie")

        # showing all the widgets
        self.show()
    # when button is pressed this method is being called
    def setValue(self, value):
        # setting for loop to set value of progress bar
        for i in range(101):
            QApplication.processEvents()
            self.pbar.setValue(value)



