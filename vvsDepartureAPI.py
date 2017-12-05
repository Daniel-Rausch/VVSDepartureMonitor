#coding: utf-8
import requests
import datetime
import time
from vvsEfa import get_EFA_from_VVS, parse_efa



connectionsData= {
    'X60UniToLeo': ['5006021', 'X60', 'Leonberg Bf'],
    '92UniToLeo': ['5006008', '92', 'Rotebühlplatz']
    }


class NoVVSConnectionFoundError(Exception):
    pass

class InternetConnectionError(Exception):
    pass



class VVSConnection:
    
    def __init__(self, dictFromVVSApi):
        self.line = dictFromVVSApi['number']
        self.station = dictFromVVSApi['stopName']
        self.direction = dictFromVVSApi['direction']
        self.departure = dictFromVVSApi['departureTime']
        self.delay = dictFromVVSApi['delay']



    def __str__(self):
        output = ('Line: ' + self.line + "  |  " +
                  'Station: ' + self.station + "  |  " +
                  'Direction: ' + self.direction + "  |  " +
                  'Departure: ' + self.getDepartureDateAsString() + "  |  " +
                  'Delay: ' + str(self.delay))
        return output



    def getDepartureDateAsString(self):
        return self.departure.strftime("%Y-%m-%d %H:%M:%S")



    def getDepartureTimeAsString(self):
        return self.departure.strftime("%H:%M:%S")



    def getMinutesToDeparture(self):
        currentTime = datetime.datetime.now()
        #print(currentTime)
        #print(self.departure)

        difference = self.departure - currentTime
        return int(difference.total_seconds()/60)



    #Throws InternetConnectionError and NoVVSConnectionFoundError
    @staticmethod
    def getNextConnectionFromStation(station, line, direction):
        #Get data about station from online API
        data = []
        try:
            data = parse_efa(get_EFA_from_VVS(station))
        except (ConnectionError, requests.exceptions.HTTPError) as e:
            raise InternetConnectionError('Could not retrieve data from the VVS API.')
        #print(data)
        
        #Filter interesting connections from the list
        filteredConnections = []
        for connectionDict in data:
            #print(connectionDict)
            
            #Check whether connection matches the requested line and direction
            if str(connectionDict['number']) == line and str(connectionDict['direction']) == direction:
                
                #Make a sanity check to filter out past connections
                newVVSConnectionObject = VVSConnection(connectionDict)
                if newVVSConnectionObject.getMinutesToDeparture() < -1:
                    continue
                
                #Add connection to list of potential connections
                filteredConnections.append(newVVSConnectionObject)
        #print(filteredConnections)
        
        if len(filteredConnections) == 0:
            raise NoVVSConnectionFoundError('The VVS API did not return any connections that matched the search criteria.')
        
        filteredConnections.sort(key=lambda x: x.getMinutesToDeparture())
        
        return filteredConnections[0]
        



def main():
    while True:
        try:
            connectionData = connectionsData['X60UniToLeo']
            nextConnection = VVSConnection.getNextConnectionFromStation(connectionData[0], connectionData[1], connectionData[2])
            print(nextConnection)
            print("Minutes left: " + str(nextConnection.getMinutesToDeparture()))
        except (InternetConnectionError, NoVVSConnectionFoundError) as e:
            print("Error: Could not retrieve X60 data")
            
        try:
            connectionData = connectionsData['92UniToLeo']
            nextConnection = VVSConnection.getNextConnectionFromStation(connectionData[0], connectionData[1], connectionData[2])
            print(nextConnection)
            print("Minutes left: " + str(nextConnection.getMinutesToDeparture()))
        except (InternetConnectionError, NoVVSConnectionFoundError) as e:
            print("Error: Could not retrieve 92 data")

        time.sleep(15)
        print("\n-------------------------------------\n")




if __name__ == '__main__':
    main()
