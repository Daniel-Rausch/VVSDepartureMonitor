#coding: utf-8
import time

from PyQt5.QtCore import *

import vvsDepartureAPI
from vvsDepartureAPI import *




#Updates the next connection in the background and prepares strings for the gui to display
class VVSConnectionUpdater(QThread, QObject):

    updated = pyqtSignal()

    #updateDelay = number of seconds until next data retrieval
    #errorDelay = Number of subsequently failed updates until an error is forwarded. Until that number is reached, the last connection that was successfully retrieved is forwarded instead.
    def __init__(self, station, line, direction, updateDelay=15, errorDelay=4):
        super().__init__()
        self.__station = station
        self.__line = line
        self.__direction = direction
        self.__updateDelay = updateDelay
        self.__errorDelay = errorDelay

        self.__halt = False

        self.__cachedConnection = None
        self.__errorCount = 0
        self.__continuousInternetConErrors = 0

        currentTime = int(time.time())
        difference = updateDelay - currentTime%updateDelay
        self.__nextUpdate = currentTime + difference


    def stop(self):
        self.__halt = True
        

    def run(self):
        while not self.__halt:
            try:
                nextConnection = VVSConnection.getNextConnectionFromStation(self.__station, self.__line, self.__direction)
            except InternetConnectionError as e:
                #print(e)
                if self.__errorCount < self.__errorDelay:
                    self.__errorCount += 1
                if self.__continuousInternetConErrors < self.__errorDelay:
                    self.__continuousInternetConErrors += 1
            except NoVVSConnectionFoundError as e:
                #print(e)
                if self.__errorCount < self.__errorDelay:
                    self.__errorCount += 1
                self.__continuousInternetConErrors = 0
            else:
                print(nextConnection)
                if(nextConnection == None):
                    print('Error: This code should never be executed. Please fix the API!')
                    continue
                self.__cachedConnection = nextConnection
                self.__errorCount = 0
                self.__continuousInternetConErrors = 0

            currentTime = int(time.time())
            difference = self.__updateDelay - currentTime%self.__updateDelay
            self.__nextUpdate = currentTime + difference
            
            self.updated.emit()
            self.sleep(difference)


    def getNextConnection(self):
        if self.__cachedConnection == None:
            raise NoVVSConnectionFoundError()
        elif self.__errorCount == self.__errorDelay:
            if self.__continuousInternetConErrors == self.__errorDelay:
                raise InternetConnectionError()
            raise NoVVSConnectionFoundError()
        return self.__cachedConnection


    def getTimeToNextUpdateAsPercent(self):
        currentTime = time.time()
        percentage = (self.__nextUpdate - currentTime)/self.__updateDelay
        if percentage > 1:
            return 1.0
        elif percentage < 0:
            return 0.0
        else:
            return percentage



if __name__ == '__main__':
    print("This file is not supposed to be run as main.")

    x60 = vvsDepartureAPI.connectionsData["X60UniToLeo"]
    test = VVSConnectionUpdater(x60[0],x60[1],x60[2], updateDelay = 5)
    test.start()
    time.sleep(12)
    test.stop()
    print(test.getTimeToNextUpdateAsPercent())
    test.wait()
    print(test.getNextConnection())
