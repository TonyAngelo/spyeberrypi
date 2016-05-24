import logging

logging.basicConfig(format='%(asctime)s %(levelname)-5s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename='logs/models.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# data object
class Observable:
    def __init__(self, initialValue=None):
        self.data = initialValue
        self.callbacks = {}

    def addCallback(self, func):
        self.callbacks[func] = 1

    def delCallback(self, func):
        del self.callback[func]

    def _docallbacks(self):
        for func in self.callbacks:
            func(self.data)

    def set(self, data):
        self.data = data
        self._docallbacks()

    def get(self):
        return self.data

    def unset(self):
        self.data = None

from models.pir import Sensor
from models.spye import Spyeworks
#from ipscan import find_mac_on_network

# model
class Model:
    def __init__(self):
        #check to see if values are in text file, otherwise load defaults
        try:
            f=open('spyeconfig.txt','r')
        # problem opening the file, load the default values
        except:
            logger.warn("Could not open spyeconfig.txt")

            self.filepath = Observable("c:/users/public/documents/spyeworks/content/")
            self.ipaddy = Observable("192.168.1.110")
            #self.mac = Observable("00:00:00:00:00:00")
            self.active = Observable("active")
            self.activedelaytime = Observable("10")
            self.idle = Observable("idle")
            self.UpdateTextFile()

            logger.warn("spyeconfig.txt created with default values.")
        else:
            logger.info("Parsing spyeconfig.txt...")

            self.filepath = Observable(f.readline()[:-1])
            #self.mac = Observable(f.readline()[:-1])
            #self.ipaddy = Observable(find_mac_on_network(self.mac.get()))
            self.ipaddy = Observable(f.readline()[:-1])
            self.active = Observable(f.readline()[:-1])
            self.activedelaytime = Observable(f.readline()[:-1])
            self.idle = Observable(f.readline()[:-1])

            logger.info("Parsing complete.")
        # close the file
        f.close()

        # get the current status of the sensor variable
        self.sensorstate = Sensor(23)

        # initiate the spyeworks player
        #if len(self.ipaddy.get())==0:
            #logger.error("No IP address found for MAC %s" , self.mac.get())

        self.spyeworks = Spyeworks(self.ipaddy.get(),self.filepath.get(),
                                   self.active.get(),self.idle.get())

    ###############################################################
    ### Methods for the controller to update variables in the model
    ###############################################################

    def SetIP(self, value):
        self.ipaddy.set(value)
        self.UpdateTextFile()
        # also update the spyeworks player
        self.spyeworks.ipaddy=value

    def SetFilepath(self, value):
        self.filepath.set(value)
        self.UpdateTextFile()
        # also update the spyeworks player
        self.spyeworks.filepath=value

    def SetActive(self, value):
        self.active.set(value)
        self.UpdateTextFile()
        # also update the spyeworks player
        self.spyeworks.active=value

    def SetIdle(self, value):
        self.idle.set(value)
        self.UpdateTextFile()
        # also update the spyeworks player
        self.spyeworks.idle=value

    def SetActiveDelayTime(self, value):
        self.activedelaytime.set(value)
        self.UpdateTextFile()

    ##########################################################
    ### Method for writing current model values to a text file
    ##########################################################

    def UpdateTextFile(self):
        logger.info("Writing to spyeconfig.txt...")
        # write the model to a text file for tracking variable changes
        f=open('spyeconfig.txt','w+')
        f.write(self.filepath.get() + '\n' + self.ipaddy.get() + '\n' + self.active.get() + '\n' + self.activedelay.get() + '\n' + self.idle.get() + '\n')
        f.close()
        logger.info("Writing complete.")
