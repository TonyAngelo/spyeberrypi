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

            logger.info("Parsing complete.")
        # close the file
        f.close()

        # print the menu
        self.printMenu()

    def printMenu(self):
        print("""
                1. Change Spyeworks IP
                2. Change Active List
                3. Change Active Delay
                4. Change Idle List
                5. Quit/Exit
                """)

        # get the selection
        self.main_selection = input("Please select:")

        if self.main_selection == '1':
            self.printSecondMenu('Spyeworks IP', self.ipaddy)
        elif self.main_selection == '2':
            self.printSecondMenu('Active List', self.active)
        elif self.main_selection == '3':
            self.printSecondMenu('Active Delay', self.activedelay)
        elif self.main_selection == '4':
            self.printSecondMenu('Idle List', self.idle)
        elif self.main_selection == '5':
            sys.exit()
        else:
            print("Invalid selection.\n")
            self.printMenu()

    def printSecondMenu(self,title,value):
        print(title,'-',value)
        print("1. Change",title)
        print("2. Back to Main")

        # get the selection
        self.second_selection = input("Please select:")

        if self.second_selection == '1':
            # new input
            self.new_value = input("Enter a new value:")
            # validate new value
            print("New Value entered:", self.new_value)
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
            self.mac.get() + '\n' + self.filepath.get() + '\n' + self.active.get() + '\n' + self.idle.get() + '\n' + self.sensorenable.get() + '\n' +
            self.activelist.get() + '\n' + self.activedelaytime.get() + '\n' + self.idlelist.get() + '\n' + self.idledelaytime.get() + '\n')
        f.close()
        logger.info("Writing complete.")


app = Controller()

while True:
    pass