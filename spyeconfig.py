#########################################################################
#########################################################################
#
# Spyeworks - Configuration Script - v1
#
# This program configures the Rasberry Pi for use with the Spyeworks
# Digital Signage Player.
#
# by Tony Petrangelo
# tonypetrangelo@gmail.com
#
#########################################################################
#########################################################################

# import libraries
#from threading import Timer  # for delay timers

import sys
import logging
from models.models import Observable

dayLabels=['Daily','WeekDays']
dayOptions={
    'Daily':'mon-sun',
    'WeekDays':'mon-fri'
}

logging.basicConfig(format='%(asctime)s %(levelname)-5s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename='logs/models.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# controller, talks to views and models
class Controller:
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
            self.onoffDays = Observable("Daily")
            self.onHour = Observable("7")
            self.onMin = Observable("0")
            self.offHour = Observable("19")
            self.offMin = Observable("0")
            self.UpdateTextFile()

            logger.warn("spyeconfig.txt created with default values.")
        else:
            logger.info("Parsing spyeconfig.txt...")

            self.filepath = Observable(f.readline()[:-1])
            self.ipaddy = Observable(f.readline()[:-1])
            #self.mac = Observable(f.readline()[:-1])
            #self.ipaddy = Observable(find_mac_on_network(self.mac.get()))
            self.active = Observable(f.readline()[:-1])
            self.activedelay = Observable(f.readline()[:-1])
            self.idle = Observable(f.readline()[:-1])
            self.daysLabel = Observable(f.readline()[:-1])
            self.onHour = Observable(f.readline()[:-1])
            self.onMin = Observable(f.readline()[:-1])
            self.offHour = Observable(f.readline()[:-1])
            self.offMin = Observable(f.readline()[:-1])
            logger.info("Parsing complete.")
        # close the file
        f.close()

        # create the title/value dictionary
        self.settingsDict = {'Spyeworks IP':self.ipaddy, 'Active List':self.active, 'Active Delay':self.activedelay, 'Idle List':self.idle}

        # print the menu
        self.printMenu()

    def printMenu(self):
        print("""
        Spyeworks Motion Sensor Configuration Main Menu

            1. Change Spyeworks IP
            2. Change Active List
            3. Change Active Delay
            4. Change Idle List
            5. Change Display Turn On/Off Days
            6. Change Display Turn On Time
            7. Change Display Turn Off Time
            8. Get On-Off Times
            9. Quit/Exit
            """)

        # get the selection
        self.main_selection = input("Please select: ")
        print("\n")

        if self.main_selection == '1':
            self.printSecondMenu('Spyeworks IP', self.ipaddy.get())

        elif self.main_selection == '2':
            self.printSecondMenu('Active List', self.active.get())

        elif self.main_selection == '3':
            self.printSecondMenu('Active Delay', self.activedelay.get())

        elif self.main_selection == '4':
            self.printSecondMenu('Idle List', self.idle.get())

        elif self.main_selection == '5':
            print('Current Turn On/Off days:', self.daysLabel.get())
            print('1. Daily')
            print('2. WeekDays')
            self.newDays = input("Select which days to use: ")
            # validate entry
            if int(self.newDays) == 1 or int(self.newDays) == 2:
                self.daysLabel.set(dayLabels[int(self.newDays) - 1])
                # update the text file
                self.UpdateTextFile()
                print('New Turn On/Off days:', self.daysLabel.get())
            else:
                print('Invalid entry')
            self.printMenu()

        elif self.main_selection == '6':
            print('Current Turn On time ', str(self.onHour.get()), ':', str(self.onMin.get()).zfill(2), sep='')
            self.newOnHour = input("Enter new turn on hour (in 24 hour clock): ")
            # validate hour entry
            if int(self.newOnHour) < 24 and int(self.newOnHour) >= 0:
                self.newOnMin = input("Enter new turn on minute: ")
                # validate min entry
                if int(self.newOnMin) < 60 and int(self.newOnMin) >= 0:
                    # assign new hour
                    self.onHour.set(int(self.newOnHour))
                    # assign new minute
                    self.onMin.set(int(self.newOnMin))
                    # update the text file
                    self.UpdateTextFile()
                    # print new turn on time
                    print('New Turn On time ', str(self.onHour.get()), ':', str(self.onMin.get()).zfill(2), sep='')
                else:
                    print('Invalid Turn On Min')
            else:
                print('Invalid Turn On Hour')
            self.printMenu()

        elif self.main_selection == '7':
            print('Current Turn Off time ', str(self.offHour.get()), ':', str(self.offMin.get()).zfill(2), sep='')
            self.newOffHour = input("Enter new turn off hour (in 24 hour clock): ")
            # validate hour entry
            if int(self.newOffHour) < 24 and int(self.newOffHour) >= 0:
                self.newOffMin = input("Enter new turn off minute: ")
                # validate min entry
                if int(self.newOffMin) < 60 and int(self.newOffMin) >= 0:
                    # assign new hour
                    self.offHour.set(int(self.newOffHour))
                    # assign new minute
                    self.offMin.set(int(self.newOffMin))
                    # update the text file
                    self.UpdateTextFile()
                    # print new turn off time
                    print('New Turn Off time ', str(self.offHour.get()), ':', str(self.offMin.get()).zfill(2), sep='')
                else:
                    print('Invalid Turn Off Min')
            else:
                print('Invalid Turn Off Hour')
            self.printMenu()

        elif self.main_selection == '7':
            print('Turn On ', self.daysLabel.get(), ' at ', str(self.onHour.get()), ':', str(self.onMin.get()).zfill(2), sep='')
            print('Turn Off ', self.daysLabel.get(), ' at ', str(self.offHour.get()), ':', str(self.offMin.get()).zfill(2),
                  sep='')
            self.printMenu()

        elif self.main_selection == '9':
            sys.exit()

        else:
            print("Invalid selection.\n")
            self.printMenu()

    def printSecondMenu(self,title,value):
        print(title,'-',value)
        print("1. Change",title)
        print("2. Back to Main")

        # get the selection
        self.second_selection = input("Please select: ")
        print("\n")

        if self.second_selection == '1':
            # new input
            self.new_value = input("Enter a new value: ")
            print("\n")
            # validate new value
            self.settingsDict[title].set(self.new_value)
            self.UpdateTextFile()
            # print new value
            print("New Value entered:", self.settingsDict[title].get())
            print("\n")
            # print menu again
            self.printSecondMenu(title, self.new_value)
        elif self.second_selection == '2':
            # back to main menu
            self.printMenu()
        else:
            print("Invalid selection.\n")
            self.printSecondMenu(title, value)


    ##########################################################
    ### Method for writing current model values to a text file
    ##########################################################

    def UpdateTextFile(self):
        logger.info("Writing to spyeconfig.txt...")
        # write the model to a text file for tracking variable changes
        f = open('spyeconfig.txt', 'w+')
        f.write(
            self.filepath.get() + '\n' + self.ipaddy.get() + '\n' + self.active.get() + '\n' + self.activedelay.get() + '\n' + self.idle.get() + '\n' +
            self.daysLabel.get() + '\n' + self.onHour.get() + '\n' + self.onMin.get() + '\n' + self.offHour.get() + '\n' + self.offMin.get() + '\n')
        f.close()
        logger.info("Writing complete.")


app = Controller()

while True:
    pass