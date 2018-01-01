from vvsGuiQML import VVSQMLApp
from vvsSettings import settings


if __name__ == "__main__":

    connections = settings['connections']
    
    c = VVSQMLApp(connections)
    c.run()
