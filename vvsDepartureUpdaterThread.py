#coding: utf-8
import time

from PyQt5.QtCore import *
from PyQt5.QtQml import qmlRegisterType
from vvsDepartureAPI import (connectionsData, VVSConnection, InternetConnectionError, NoVVSConnectionFoundError)


class QVVSConnectionData(QObject):

    _ = pyqtSignal()
        
    def __init__(self, station, line, direction, vvsc = None):
        super(QObject, self).__init__()
        self.__station = station
        self.__line = line
        self.__direction = direction
        
        self.vvsc = vvsc
        self.internetConError = False
        self.noConFoundError = False

    def __str__(self):
        if self.vvsc == None:
            return ""
        return self.vvsc.__str__()

    @pyqtProperty(bool, notify=_)
    def errorInternet(self):
        return self.internetConError

    @pyqtProperty(bool, notify=_)
    def errorNotFound(self):
        return self.noConFoundError

    @pyqtProperty(str, notify=_)
    def line(self):
        return self.__line

    @pyqtProperty(str, notify=_)
    def station(self):
        return self.__station

    @pyqtProperty(str, notify=_)
    def direction(self):
        return self.__direction

    @pyqtProperty(int, notify=_)
    def delay(self):
        if self.vvsc == None:
            return 0
        return self.vvsc.delay

    @pyqtProperty(str, notify=_)
    def departureDate(self):
        if self.vvsc == None:
            return ""
        return self.vvsc.getDepartureDateAsString()

    @pyqtProperty(str, notify=_)
    def departureTime(self):
        if self.vvsc == None:
            return ""
        return self.vvsc.getDepartureTimeAsString()

    @pyqtProperty(int, notify=_)
    def minutesToDeparture(self):
        if self.vvsc == None:
            return 0
        return self.vvsc.getMinutesToDeparture()
    

qmlRegisterType(QVVSConnectionData, 'QVVSConnectionData', 1, 0, 'QVVSConnectionData')    



#Updates the next connection in the background and prepares strings for the gui to display
class VVSConnectionUpdater(QThread):

    updated = pyqtSignal()

    #synchronized: if set to true, then all threads with the same update delay will update at the same time
    #updateDelay: number of seconds until next data retrieval
    #minUpdateDelay: Only used if synchronized. Sync might result in an update that is scheduled immediately after the previous one, even for large updateDelay values. This forces a minimum wait time.
    #errorDelay: Number of subsequently failed updates until an error is forwarded. Until that number is reached, the last connection that was successfully retrieved is forwarded instead.
    def __init__(self, station, line, direction, synchronized=True, updateDelay=15, minUpdateDelay=1, errorDelay=4):
        super().__init__()
        self.__connectionData = QVVSConnectionData(station, line, direction)
        
        self.__synchronized = synchronized
        self.__updateDelay = updateDelay
        self.__minUpdateDelay = minUpdateDelay
        self.__errorDelay = errorDelay

        self.__halt = False
        self.__errorCount = 0
        self.__continuousInternetConErrors = 0

        self.__nextUpdate = int(time.time())


    def stop(self):
        self.__halt = True
        

    def run(self):
        while not self.__halt:
            try:
                nextConnection = VVSConnection.getNextConnectionFromStation(self.__connectionData.station, self.__connectionData.line, self.__connectionData.direction)
            except (InternetConnectionError, NoVVSConnectionFoundError) as e:
                #print(e)
                if self.__errorCount < self.__errorDelay:
                    self.__errorCount += 1
                if type(e) == InternetConnectionError:
                    if self.__continuousInternetConErrors < self.__errorDelay:
                        self.__continuousInternetConErrors += 1
                else:
                    self.__continuousInternetConErrors = 0

                #Handle special case where the first connection try already yields an error:
                if self.__connectionData.vvsc == None:
                    self.__errorCount = self.__errorDelay
                    if type(e) == InternetConnectionError:
                        self.__continuousInternetConErrors = self.__errorDelay

                if self.__errorCount == self.__errorDelay:
                    if self.__continuousInternetConErrors == self.__errorDelay:
                        self.__connectionData.internetConError = True
                        self.__connectionData.noConFoundError = False
                    else:
                        self.__connectionData.internetConError = False
                        self.__connectionData.noConFoundError = True
                        
            else:
                #print(nextConnection)
                if(nextConnection == None):
                    print('Error: This code should never be executed. Please fix the API!')
                    continue
                self.__connectionData.vvsc = nextConnection
                self.__connectionData.internetConError = False
                self.__connectionData.noConFoundError = False
                self.__errorCount = 0
                self.__continuousInternetConErrors = 0


            #Compute next update and sleep

            currentTime = int(time.time())
            sleepTime = 0
            if self.__synchronized:
                sleepTime = self.__updateDelay - currentTime % self.__updateDelay
                if sleepTime < self.__minUpdateDelay :
                    sleepTime += self.__updateDelay
            else:
                sleepTime = self.__updateDelay
            self.__nextUpdate = currentTime + sleepTime
            
            self.updated.emit()
            self.sleep(sleepTime)


    def getTimeToNextUpdateAsPercent(self):
        currentTime = time.time()
        percentage =(self.__nextUpdate - currentTime)/self.__updateDelay
        if percentage > 1:
            return 1.0
        elif percentage < 0:
            return 0.0
        else:
            return percentage

    def getNextConnection(self):
        return self.__connectionData


    updateProgress = pyqtProperty(float, getTimeToNextUpdateAsPercent, notify=updated)
    nextConnection = pyqtProperty(QVVSConnectionData, getNextConnection, notify=updated)



    

if __name__ == '__main__':
    print("This file is not supposed to be run as main.")

    x60 = connectionsData["X60UniToLeo"]
    test = VVSConnectionUpdater(x60[0],x60[1],x60[2], synchronized = True, updateDelay = 15)
    test.start()
    time.sleep(2)
    test.stop()
    print(test.getTimeToNextUpdateAsPercent())
    test.wait()
    con = test.getNextConnection()
    print(con)
    print(con.departureDate)
    print(con.departureTime)
    print(con.minutesToDeparture)
