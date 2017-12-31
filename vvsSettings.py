from yaml import load, dump, YAMLError


settings = {}

__defaultSettings = {
    'enableDebugOutputs': False,
    'enableNotifications': False,
    'notificationTimings': [
        "8:00", #Start 1st period
        "9:15", #End 1st period
        "17:00", #Start 2nd period
        "19:00" #End 2nd period
        ]
    }


#Read the settings.yml file
try:
    with open('settings.yml', 'r') as file:
        settings = load(file)
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


#print (settings)
#print (__defaultSettings)


