from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import (pyqtProperty, pyqtSignal, QDateTime, QObject, QTimer, QUrl, QThread, QVariant)
from PyQt5.QtWidgets import QStyleOptionGraphicsItem
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView
import sys
from datetime import datetime

class CountdownData(QObject):

    def __init__(self, parent=None):
        super(QObject, self).__init__(parent)
        self.time_remaining = 999

        self.t = QTimer()
        self.t.timeout.connect(self.datetimeChanged)
        self.t.start(1000)
    
    def setRemaining(self, t):
        print ("Set remaining called: {}".format(t))
        self.time_remaining = t
        self.remainingChanged.emit()

    def getRemaining(self):
        return self.time_remaining

    remainingChanged = pyqtSignal()
    remaining = pyqtProperty(int, getRemaining, setRemaining, notify=remainingChanged)

    def setName(self, t):
        print ("Set name called: {}".format(t))
        self._name = t
        self.nameChanged.emit()

    def getName(self):
        return self._name

    nameChanged = pyqtSignal()
    name = pyqtProperty(str, getName, setName, notify=nameChanged)

    
    def getDatetime(self):
        return QDateTime.currentDateTime()

    datetimeChanged = pyqtSignal()
    datetime = pyqtProperty(QDateTime, getDatetime, notify=datetimeChanged)

class CountdownTimer(QThread):
    def __init__(self, countdownObject, targetDatetime, name, *args, **kwargs):
        super(QThread, self).__init__(*args, **kwargs)
        self.countdownObject = countdownObject
        self.targetDatetime = targetDatetime
        self.name = name
        self.countdownObject.setName(name)
    
    def run(self):
        self.t = QTimer()
        self.t.timeout.connect(self.updateTimer)
        self.t.start(250)
        self.exec_()

    @pyqtSlot()
    def updateTimer(self):
        remaining = (self.targetDatetime - datetime.now()).total_seconds()
        self.countdownObject.setRemaining(remaining)


class CountdownList(QObject):
    l = []

    def append(self, c):
        self.l.append(c)
        self.changed.emit()

    def getL(self):
        return self.l

    changed = pyqtSignal()
    items = pyqtProperty(QVariant, getL, notify=changed)

class CountdownApp(QObject):
    QMLFILE = 'main.qml'
    
    def __init__(self):
        super(QObject, self).__init__()
        self.app = QGuiApplication(sys.argv)
        self.view = QQuickView()
        self.view.setResizeMode(QQuickView.SizeRootObjectToView)
        #self.view.engine().quit.connect(self.app.quit)

        self.cds = CountdownList()
        self.cdt = []
        for name, targetDatetime in {
                "silvester": datetime(2018, 1, 1, 0, 0, 0),
                "geburtstag": datetime(2018, 3, 12, 0, 0, 0)
                }.items():
            cdobj = CountdownData()
            countdown = CountdownTimer(cdobj, targetDatetime, name)
            countdown.start()
            self.cds.append(cdobj)
            self.cdt.append(countdown)

        self.view.rootContext().setContextProperty('countdowns', self.cds)
        self.view.setSource(QUrl(self.QMLFILE))

        self.t = QTimer()
        self.t.timeout.connect(self.addCountdown)
        self.t.start(10000)
        

    def run(self):
        self.view.show()
        sys.exit(self.app.exec_())

    @pyqtSlot()
    def addCountdown(self):
        for name, targetDatetime in {
                "antrittsvorlesung": datetime(2018, 1, 19, 0, 0, 0)
                }.items():
            cdobj = CountdownData()
            countdown = CountdownTimer(cdobj, targetDatetime, name)
            countdown.start()
            self.cds.append(cdobj)
            self.cdt.append(countdown)        

if __name__ == "__main__":
    c = CountdownApp()
    c.run()
