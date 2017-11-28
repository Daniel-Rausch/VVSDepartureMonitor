from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import (pyqtProperty, pyqtSignal, QDateTime, QObject, QTimer, QUrl, QThread, QVariant)
from PyQt5.QtWidgets import QStyleOptionGraphicsItem
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView
import sys
from datetime import datetime
from vvsDepartureUpdaterThread import VVSConnectionUpdater
from vvsDepartureAPI import connectionsData

class VVSApp(QObject):
    QMLFILE = 'gui.qml'

    CONNECTIONS = (connectionsData['X60UniToLeo'], connectionsData['92UniToLeo'])
    
    def __init__(self):
        super(QObject, self).__init__()
        self.app = QGuiApplication(sys.argv)
        self.view = QQuickView()
        self.view.setResizeMode(QQuickView.SizeRootObjectToView)

        self.con = []
        for connection in self.CONNECTIONS:
            updaterThread = VVSConnectionUpdater(connection[0], connection[1], connection[2])
            updaterThread.start()
            self.con.append(updaterThread)
            #print(connection)
        #self.con = VVSConnectionUpdater('5006021', 'X60', 'Leonberg Bf')
        #self.con.start()

        #print(self.con)

        self.view.rootContext().setContextProperty('con', self.con)
        self.view.setSource(QUrl(self.QMLFILE))
        

    def run(self):
        self.view.showFullScreen()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    c = VVSApp()
    c.run()
