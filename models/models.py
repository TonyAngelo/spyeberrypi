import logging
from apscheduler.scheduler import Scheduler

dayLabels=['Daily','WeekDays']
dayOptions={
    'Daily':'mon-sun',
    'WeekDays':'mon-fri'}

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
from models.planarOLED import planarDisplay
#from ipscan import find_mac_on_network

# model
class Model:
    def __init__(self):
        # check to see if values are in text file, otherwise load defaults
        try:
            f = open('spyeconfig.txt', 'r')
        # problem opening the file, load the default values
        except:
            logger.warn("Could not open spyeconfig.txt")

            self.filepath = Observable("c:/users/public/documents/spyeworks/content/")
            self.ipaddy = Observable("192.168.1.110")
            self.active = Observable("active")
            self.activedelay = Observable("0")
            self.idle = Observable("idle")
            self.daysLabel = Observable("Daily")
            self.onHour = Observable(7)
            self.onMin = Observable(0)
            self.offHour = Observable(19)
            self.offMin = Observable(0)
            self.UpdateTextFile()

            logger.warn("spyeconfig.txt created with default values.")
        else:
            logger.info("Parsing spyeconfig.txt...")

            self.filepath = Observable(f.readline()[:-1])
            self.ipaddy = Observable(f.readline()[:-1])
            # self.mac = Observable(f.readline()[:-1])
            # self.ipaddy = Observable(find_mac_on_network(self.mac.get()))
            self.active = Observable(f.readline()[:-1])
            self.activedelay = Observable(f.readline()[:-1])
            self.idle = Observable(f.readline()[:-1])
            self.daysLabel = Observable(f.readline()[:-1])
            self.onHour = Observable(int(f.readline()[:-1]))
            self.onMin = Observable(int(f.readline()[:-1]))
            self.offHour = Observable(int(f.readline()[:-1]))
            self.offMin = Observable(int(f.readline()[:-1]))
            logger.info("Parsing complete.")
            # close the file
            f.close()

        # get the current status of the sensor variable
        self.sensorstate = Sensor(23)

        # add the tv
        self.tv = planarDisplay('ttyUSB0')

        # Start the scheduler
        self.sched = Scheduler()
        self.sched.start()

        # set default turn on and turn off times
        self.days = dayOptions[self.daysLabel.get()]
        self.DisplayOnJob = self.sched.add_cron_job(self.displayPowerOn, day_of_week=self.days, hour=str(self.onHour.get()),
                                                    minute=str(self.onMin.get()))
        self.DisplayOffJob = self.sched.add_cron_job(self.displayPowerOff, day_of_week=self.days, hour=str(self.offHour.get()),
                                                     minute=str(self.offMin.get()))

        # initiate the spyeworks player
        #if len(self.ipaddy.get())==0:
            #logger.error("No IP address found for MAC %s" , self.mac.get())

        self.spyeworks = Spyeworks(self.ipaddy.get(),self.filepath.get(),
                                   self.active.get(),self.idle.get())

    ###############################################################
    ### Methods for controlling the TV
    ###############################################################

    def displayPowerOn(self):
        self.tv.power(1)

    def displayPowerOff(self):
        self.tv.power(0)

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
        self.activedelay.set(value)
        self.UpdateTextFile()

    ##########################################################
    ### Method for writing current model values to a text file
    ##########################################################

    def UpdateTextFile(self):
        logger.info("Writing to spyeconfig.txt...")
        # write the model to a text file for tracking variable changes
        f=open('spyeconfig.txt','w+')
        f.write(
            self.filepath.get() + '\n' + self.ipaddy.get() + '\n' + self.active.get() + '\n' + self.activedelay.get() + '\n' + self.idle.get() + '\n' +
            self.daysLabel.get() + '\n' + str(self.onHour.get()) + '\n' + str(self.onMin.get()) + '\n' + str(
                self.offHour.get()) + '\n' + str(self.offMin.get()) + '\n')
        f.close()
        logger.info("Writing complete.")
