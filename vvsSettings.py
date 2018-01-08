from yaml import load, dump, YAMLError


settings = {}

__defaultSettings = {
    'connections': [
        ['5006021', 'X60', 'Leonberg Bf'], #Station ID, Line name, Direction
        ['5006008', '92', 'Rotebühlplatz']
        ],
    'updateDelay': 10, #Time in seconds between updates
    'notificationSettings':{
        'enableNotifications': False,
        'notifcationsForConnections': [0,1], #List of connections (identified by their position in the connections list) for which notifications should be enabled, starting from 0.
        'notificationTimeout': 20, #Timeout in seconds
        'showNotificationOnlyDuringPeriods': True,
        'notificationPeriods': [
            [8,0], #Start 1st period, represented as (hours, minutes)
            [9,0], #End 1st period
            [17,40], #Start 2nd period
            [19,0], #End 2nd period
        ],
        'showNotificationsForTimeRemaining': 15 #Notifications are shown only if less than x minutes remain. Set to <=0 for always on.
    },
    'enableDebugOutputs': False,
    }


#Read the settings.yml file
try:
    with open('settings.yml', 'r') as file:
        settings = load(file)
        if settings is None:
            settings = {}
except YAMLError as e:
    print('Error: Your settings.yaml file could not be parsed. Using default config. Try fixing or deleting your settings.yml file to get rid of this error.')
    settings = __defaultSettings
except FileNotFoundError as e:
    with open('settings.yml', 'w') as file:
        file.write(dump(__defaultSettings))
    settings = __defaultSettings
else:
    
    #If some options were not present in the settings.yml file, use the default instead
    for key in __defaultSettings:
        if key not in settings:
            settings[key] = __defaultSettings[key]

    for key in __defaultSettings:
        if type(__defaultSettings[key]) is dict:
            for keyLayer2 in __defaultSettings[key]:
                if keyLayer2 not in settings[key]:
                    settings[key][keyLayer2] = __defaultSettings[key][keyLayer2]


#print (settings)
#print (__defaultSettings)


