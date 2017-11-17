#coding: utf-8
import sys
from PyQt5.QtCore import QUrl, Qt, pyqtSlot, QObject
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5 import QtQuick

from threading import Thread
from time import sleep

class QmlAusgabe(object):
    def __init__(self, pathToQmlFile="guiTest.qml"):

        #QML-Engine
        self.__appEngine = QQmlApplicationEngine()
        self.__appEngine.load(pathToQmlFile)

        self.__appWindow = self.__appEngine.rootObjects()[0]

        self.__rectangle1 = self.__appWindow.findChild(QObject, "Rectangle1")
        self.__rectangle2 = self.__appWindow.findChild(QObject, "Rectangle2")

    def changeColor(self):
        self.__rectangle1.setProperty("color", "yellow")
        self.__rectangle2.setProperty("color", "blue")

    def show(self):
        self.__appWindow.show()

if __name__ == "__main__":
    appQueue = QApplication(sys.argv)
    qdm = QmlAusgabe()
    qdm.show()
    #sys.exit(appQueue.exec_())

    t = Thread(target=appQueue.exec_, args=())
    t.start()
    sleep(5)
    qdm.changeColor()
    input()
    
