import sys
import logging
import time

from apscheduler.scheduler import Scheduler

logging.basicConfig(format='%(asctime)s %(levelname)-5s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename='logs/models.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

dayLabels=['Daily','WeekDays']
dayOptions={
    'Daily':'mon-sun',
    'WeekDays':'mon-fri'
}

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
        # default to everyday
        self.daysLabel='Daily'
        self.days=dayOptions[self.daysLabel]
        # turn on at 7am
        self.turnOnHour = 7
        self.turnOnMin = 0
        self.DisplayOnJob = self.sched.add_cron_job(self.displayPowerOn, day_of_week=self.days, hour=self.turnOnHour, minute=self.turnOnMin)

        # turn off at 7pm
        self.turnOffHour = 19
        self.turnOffMin = 0
        self.DisplayOffJob = self.sched.add_cron_job(self.displayPowerOff, day_of_week=self.days, hour=self.turnOffHour, minute=self.turnOffMin)

        # print the menu
        self.printMenu()

    def printMenu(self):
        print("""
        Timer Test Menu

            1. Set Turn On/Off Days
            2. Set Turn On Time
            3. Set Turn Off Time
            4. Get On-Off Times
            5. Quit/Exit
            """)

        # get the selection
        self.main_selection = input("Please select: ")
        print("\n")

        if self.main_selection == '1':
            print('Current Turn On/Off days:',self.daysLabel)
            print('1. Daily')
            print('2. WeekDays')
            self.newDays = input("Select which days to use: ")
            # validate entry
            if int(self.newDays)==1 or int(self.newDays)==2:
                self.daysLabel = dayLabels[int(self.newDays)]
                self.days = dayOptions[self.daysLabel]
                print('New Turn On/Off days:', self.daysLabel)
            else:
                print('Invalid entry')
            self.printMenu()
        elif self.main_selection == '2':
            print('Current Turn On time ', str(self.turnOnHour), ':', str(self.turnOnMin).zfill(2), sep='')
            self.newTurnOnHour = input("Enter new turn on hour (in 24 hour clock): ")
            # validate hour entry
            if int(self.newTurnOnHour) < 24 and int(self.newTurnOnHour) >= 0:
                self.newTurnOnMin = input("Enter new turn on minute: ")
                # validate min entry
                if int(self.newTurnOnMin) < 60 and int(self.newTurnOnMin) >= 0:
                    # assign new hour
                    self.turnOnHour = int(self.newTurnOnHour)
                    # assign new minute
                    self.turnOnMin = int(self.newTurnOnMin)
                    # cancel the old job
                    self.sched.unschedule_job(self.DisplayOnJob)
                    # schedule the new job
                    self.DisplayOnJob = self.sched.add_cron_job(self.displayPowerOn, day_of_week=self.days,
                                                                hour=self.turnOnHour, minute=self.turnOnMin)
                    # print new turn on time
                    print('New Turn On time ', str(self.turnOnHour), ':', str(self.turnOnMin).zfill(2), sep='')
                else:
                    print('Invalid Turn On Min')
            else:
                print('Invalid Turn On Hour')
            self.printMenu()
        elif self.main_selection == '3':
            print('Current Turn Off time ', str(self.turnOffHour), ':', str(self.turnOffMin).zfill(2), sep='')
            self.newTurnOffHour = input("Enter new turn off hour (in 24 hour clock): ")
            # validate hour entry
            if int(self.newTurnOffHour) < 24 and int(self.newTurnOffHour) >= 0:
                self.newTurnOffMin = input("Enter new turn off minute: ")
                # validate min entry
                if int(self.newTurnOffMin) < 60 and int(self.newTurnOffMin) >= 0:
                    # assign new hour
                    self.turnOffHour = int(self.newTurnOffHour)
                    # assign new minute
                    self.turnOffMin = int(self.newTurnOffMin)
                    # cancel the old job
                    self.sched.unschedule_job(self.DisplayOffJob)
                    # schedule the new job
                    self.DisplayOffJob = self.sched.add_cron_job(self.displayPowerOff, day_of_week=self.days,
                                                                 hour=self.turnOffHour, minute=self.turnOffMin)
                    # print new turn off time
                    print('New Turn Off time ', str(self.turnOffHour), ':', str(self.turnOffMin).zfill(2), sep='')
                else:
                    print('Invalid Turn Off Min')
            else:
                print('Invalid Turn Off Hour')
            self.printMenu()
        elif self.main_selection == '4':
            print('Turn On ',self.daysLabel,' at ',str(self.turnOnHour),':',str(self.turnOnMin).zfill(2), sep='')
            print('Turn Off ',self.daysLabel,' at ', str(self.turnOffHour), ':', str(self.turnOffMin).zfill(2), sep='')
            self.sched.print_jobs()
            self.printMenu()
        elif self.main_selection == '5':
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