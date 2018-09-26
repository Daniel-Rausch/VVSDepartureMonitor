from vvsGuiQML import VVSQMLApp
from vvsSettings import settings

import logging


if __name__ == "__main__":

    connections = settings['connections']
    logging.basicConfig(level=settings['loggingLevel'])
    
    c = VVSQMLApp(connections)
    c.run()
