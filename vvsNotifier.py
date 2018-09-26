from PyQt5.QtCore import pyqtSignal
from datetime import (datetime, time)
import logging

from vvsSettings import settings
from vvsDepartureUpdaterThread import (VVSConnectionUpdater, QVVSConnectionData)

settingsNotify = settings['notificationSettings']

try:
    import notify2
    notify2.init('VVS Monitor')
except:
    if settingsNotify['enableNotifications']:
        logging.error("Failed to load notify2 library, so the notification feature will be disabled. Note that notifications are supported on Linux only.")
        settingsNotify['enableNotifications'] = False



class VVSNotifier:

    __notifierList = []
    
    def __init__(self, connectionUpdaterThread):

        self.__connection = connectionUpdaterThread
        self.__notification = notify2.Notification("Departure " + self.__connection.getNextConnection().line,
                                              "",
                                              "notification-message-im"
                                              )
        self.__notification.timeout = settingsNotify["notificationTimeout"] * 1000
        self.__connection.updated.connect(self.processUpdate)
        

    def processUpdate(self):
        #show notifications only during certain time frames
        if settingsNotify['showNotificationOnlyDuringPeriods']:
            periods = settingsNotify['notificationPeriods']
            periodCount = int(len(periods)/2)
            currentTime = datetime.now().time()

            timeIsInPeriod = False
            for i in range(periodCount):
                start = time(*settingsNotify['notificationPeriods'][2*i])
                end = time(*settingsNotify['notificationPeriods'][2*i+1])

                if self.__time_in_range(currentTime, start, end):
                    timeIsInPeriod = True

            if not timeIsInPeriod:
                self.__notification.close()
                return
                
        
        #test for error
        if self.__connection.getNextConnection().errorInternet or self.__connection.getNextConnection().errorNotFound:
            self.__notification.close()
            return


        #Show notification only if less than x minutes remaining. Always on if x <= 0.
        if settingsNotify['showNotificationsForTimeRemaining'] > 0:
            if self.__connection.getNextConnection().minutesToDeparture > settingsNotify['showNotificationsForTimeRemaining']:
                self.__notification.close()
                return
            
        
        m = "In " + str(self.__connection.getNextConnection().minutesToDeparture) + " min\n" + "Delay " + str(self.__connection.getNextConnection().delay) + " min"
        self.__notification.message = m
        self.__notification.show()



    def __time_in_range(self, time, start, end):
        #Return true if x is in the range [start, end]
        if start < end:
            return start <= time <= end
        else:
            return start <= time or time <= end
        


    @classmethod
    def setup(cls, connectionUpdaterThreadList):
        if not settingsNotify['enableNotifications']:
            return

        for i in range(len(connectionUpdaterThreadList)):
            if i in settingsNotify['notifcationsForConnections']:
                cls.__notifierList.append(VVSNotifier(connectionUpdaterThreadList[i]))


if __name__ == "__main__":
    print("This file is not supposed to be run as main!")
