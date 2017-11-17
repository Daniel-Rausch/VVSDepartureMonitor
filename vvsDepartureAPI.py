#coding: utf-8
import urllib.request
import json
import datetime
import time



connectionsData= {'X60UniToLeo': ['5006021', 'X60', 'Leonberg Bf'],
          '92UniToLeo': ['5006008', '92', 'Rotebühlplatz']}


class NoVVSConnectionFoundError(Exception):
    pass

class InternetConnectionError(Exception):
    pass



class VVSConnection:
    
    def __init__(self, dictFromVVSApi):
        self.line = str(dictFromVVSApi['number'])
        self.station = str(dictFromVVSApi['stopName'])
        self.direction = str(dictFromVVSApi['direction'])
        self.departure = datetime.datetime(int(dictFromVVSApi['departureTime']['year']),
                                           int(dictFromVVSApi['departureTime']['month']),
                                           int(dictFromVVSApi['departureTime']['day']),
                                           int(dictFromVVSApi['departureTime']['hour']),
                                           int(dictFromVVSApi['departureTime']['minute']))
        self.delay = int(dictFromVVSApi['delay'])



    def __str__(self):
        output = ('Line: ' + self.line + "  |  " +
                  'Station: ' + self.station + "  |  " +
                  'Direction: ' + self.direction + "  |  " +
                  'Departure: ' + self.getDepartureAsString() + "  |  " +
                  'Delay: ' + str(self.delay))
        return output



    def getDepartureAsString(self):
        return self.departure.strftime("%Y-%m-%d %H:%M:%S")



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
        data = ""
        dataFormatted = {}
        try:
            hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}
            request = urllib.request.Request("https://efa-api.asw.io/api/v1/station/" + station + "/departures/?format=json", headers = hdr)
            f = urllib.request.urlopen(request, None, 5)
            data = f.read().decode('UTF-8')
            dataFormatted = json.loads(data)
        except Exception as e:
            raise InternetConnectionError('Could not retrieve data from the VVS API.')
        #print(dataFormatted)
        
        #Filter interesting buses from the list
        filteredConnections = []
        for connectionDict in dataFormatted:
            #print(connectionDict)
            
            #Check whether bus matches the requested line and direction
            if str(connectionDict['number']) == line and str(connectionDict['direction']) == direction:
                
                #Make a sanity check to filter out past buses
                newVVSConnectionObject = VVSConnection(connectionDict)
                if newVVSConnectionObject.getMinutesToDeparture() < -1:
                    continue
                
                #Add bus to list of potential buses
                filteredConnections.append(newVVSConnectionObject)
        #print(filteredConnections)
        
        if len(filteredConnections) == 0:
            raise NoVVSConnectionFoundError('The VVS API did not return any connections that matched the search criteria.')
        
        #Find next vehicle from the list. This is just a sanity check, the list is most likely already sorted.
        nextConnectionIndex = VVSConnection.__findNextConnectionFromList(filteredConnections)
        #print(nextConnectionIndex)
        #print(filteredConnections[nextConnectionIndex])
        return filteredConnections[nextConnectionIndex]
        


    #Currently assumes that all buses in busList depart in the future
    @staticmethod
    def __findNextConnectionFromList(connectionsList):
        if len(connectionsList) == 1:
            return 0

        nextConnectionIndex = 0
        for i in range(1, len(connectionsList)):
            nextConnection = connectionsList[nextConnectionIndex]
            otherConnection = connectionsList[i]
            difference = (otherConnection.departure - nextConnection.departure).total_seconds()
            if difference < 0:
                nextConnectionIndex = i
        return nextConnectionIndex
    




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

        time.sleep(30)
        print("\n-------------------------------------\n")




if __name__ == '__main__':
    main()
