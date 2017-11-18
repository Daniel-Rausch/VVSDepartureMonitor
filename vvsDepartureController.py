#coding: utf-8
import time

from PyQt5.QtCore import *

import vvsDepartureAPI
from vvsDepartureAPI import *


#Updates the next connection in the background and prepares strings for the gui to display
class VVSConnectionUpdater(QThread):
    
    def __init__(self, station, line, direction, updateDelay=10):
        super().__init__()
        self.__station = station
        self.__line = line
        self.__direction = direction
        self.__updateDelay = updateDelay

        self.__halt = False

        self.__previousConnection = None

        self.connectionStringLine = line
        self.connectionStringNextDeparture = ""


    def stop(self):
        self.__halt = True
        

    def run(self):
        while not self.__halt:
            print(self.__station)

            nextConnection = None

            try:
                nextConnection = VVSConnection.getNextConnectionFromStation(self.__station, self.__line, self.__direction)
            except (InternetConnectionError, NoVVSConnectionFoundError) as e:
                print(e)
                self.sleep(self.__updateDelay)
                continue
            print(nextConnection)
            
            self.emit(SIGNAL("updated()"))
            self.sleep(self.__updateDelay)
    



if __name__ == '__main__':
    print("This file is not supposed to be run as main.")

    x60 = vvsDepartureAPI.connectionsData["X60UniToLeo"]
    test = VVSConnectionUpdater(x60[0],x60[1],x60[2])
    test.start()
    time.sleep(10)
    test.stop()
    test.wait()
