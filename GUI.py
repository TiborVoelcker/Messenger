# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtTest
from Client import Client
import sys

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_GUI()
        self.client = Client()
        self.client.IP = "127.0.0.1"
        self.client.PORT = 2000

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.config()

    def init_GUI(self):
        self.setWindowTitle = "Messenger"
        self.verticalLayout = QtWidgets.QVBoxLayout(self)

        self.chat = QtWidgets.QTextEdit(self)
        self.verticalLayout.addWidget(self.chat)
        self.chat.setReadOnly(True)

        self.input = QtWidgets.QLineEdit(self)
        self.verticalLayout.addWidget(self.input)

        self.show()

    def config(self):
        self.chat.append("Enter IP Address: ")
        self.spy = QtTest.QSignalSpy(self.input.returnPressed)
        while not self.spy.wait():
            pass
        self.client.IP = self.input.text()
        self.client.run()
        self.chat.clear()
        self.input.clear()
        self.input.returnPressed.connect(self.enter)
        self.timer.start()

    def closeEvent(self, event):
        self.client.close()
        sys.exit(event)

    def enter(self):
        message = self.input.text()
        if message:
            self.chat.append(message)
            self.input.clear()
            self.client.send(message)

    def update(self):
        message = self.client.receive()
        if message:
            self.chat.append("> " + str(message))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    tempdict = ex.__dict__
    sys.exit(app.exec_())