#coding: utf-8
import sys
from PyQt5.QtCore import QUrl, Qt, pyqtSlot, QObject, QThread
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5 import QtQuick

class QmlAusgabe(object):
    def __init__(self, pathToQmlFile="guiTest.qml"):

        #QML-Engine
        self.__appEngine = QQmlApplicationEngine()
        self.__appEngine.load(pathToQmlFile)

        self.__appWindow = self.__appEngine.rootObjects()[0]

        self.__rectangle1 = self.__appWindow.findChild(QObject, "Rectangle1")
        self.__rectangle2 = self.__appWindow.findChild(QObject, "Rectangle2")

        self.__colorState = False

    def changeColor(self):
        if self.__colorState:
            self.__rectangle1.setProperty("color", "red")
            self.__rectangle2.setProperty("color", "green")
        else:
            self.__rectangle1.setProperty("color", "yellow")
            self.__rectangle2.setProperty("color", "blue")
        self.__colorState = not self.__colorState

    def show(self):
        self.__appWindow.show()



class Controller(QThread):
    def __init__(self, windowObject):
        super().__init__()
        self.__window = windowObject

    def run(self):
        while True:
            self.sleep(1)
            self.__window.changeColor()
        



if __name__ == "__main__":
    appQueue = QApplication(sys.argv)
    qdm = QmlAusgabe()

    thread = Controller(qdm)
    thread.start()
    
    qdm.show()
    sys.exit(appQueue.exec_())
    
