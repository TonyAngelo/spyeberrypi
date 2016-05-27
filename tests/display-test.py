import sys
import logging

sys.path.append("..")

from models import planarOLED

logging.basicConfig(format='%(asctime)s %(levelname)-5s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename='logs/models.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)


# controller, talks to views and models
class Controller:
    def __init__(self):
        # initiate the tv
        self.tv = planarOLED.planarDisplay('ttyUSB0')

        # print the menu
        self.printMenu()

    def printMenu(self):
        print("""
        TV Test Menu

            1. Turn On TV
            2. Turn Off TV
            3. Quit/Exit
            """)

        # get the selection
        self.main_selection = input("Please select: ")
        print("\n")

        if self.main_selection == '1':
            self.tv.power(1)
        elif self.main_selection == '2':
            self.tv.power(0)
        elif self.main_selection == '3':
            sys.exit()
        else:
            print("Invalid selection.\n")
            self.printMenu()


app = Controller()

while True:
    pass