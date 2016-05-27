import sys
import logging
import time

from apscheduler.scheduler import Scheduler

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

# controller, talks to views and models
class Controller:
    def __init__(self):

        # Start the scheduler
        self.sched = Scheduler()
        self.sched.start()

        # set default turn on and turn off times
        # turn on at 7am
        self.turnOnHour=7
        self.turnOnMin=0

        self.sched.add_cron_job(self.displayPowerOn, day_of_week='mon-fri', hour=self.turnOnHour, minute=self.turnOnMin)

        # turn off at 7pm
        self.turnOffHour = 19
        self.turnOffMin = 0
        self.sched.add_cron_job(self.displayPowerOff, day_of_week='mon-fri', hour=self.turnOffHour, minute=self.turnOffMin)

        # print the menu
        self.printMenu()

    def printMenu(self):
        print("""
        Timer Test Menu

            1. Set Turn On Time
            2. Set Turn Off Time
            3. Get On-Off Times
            4. Quit/Exit
            """)

        # get the selection
        self.main_selection = input("Please select: ")
        print("\n")

        if self.main_selection == '1':

            self.printMenu()
        elif self.main_selection == '2':

            self.printMenu()
        elif self.main_selection == '3':
            self.sched.print_jobs()
            self.printMenu()
        elif self.main_selection == '4':
            sys.exit()
        else:
            print("Invalid selection.\n")
            self.printMenu()

    def displayPowerOn(self):
        print("Display On")

    def displayPowerOff(self):
        print("Display Off")


app = Controller()

while True:
    pass