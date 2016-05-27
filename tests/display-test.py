import sys
import logging
import serial # for 232 control

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

class planarDisplay(Observable):
    def __init__(self, device='ttyUSB0', initialValue="Off"):
        Observable.__init__(self, initialValue)
        self.ser = serial.Serial(
            port='/dev/' + device,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        logger.info("Planar OLED init")

    def power(self, value):
        if value == 1:
            self.ser.write('display.power=1\r')  # turn on display
            logger.info("Planar OLED power on sent")
            self.set("On")

            self.rxbuf = self.ser.readline()
            print(self.rxbuf)

        else:
            self.ser.write('display.power=0\r')  # turn off display
            logger.info("Planar OLED power off sent")
            self.set("Off")

            self.rxbuf = self.ser.readline()
            print(self.rxbuf)

# controller, talks to views and models
class Controller:
    def __init__(self):
        # initiate the tv
        self.tv = planarDisplay('ttyUSB0')

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