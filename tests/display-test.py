import sys
import logging
import time
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
            baudrate=19200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        logger.info("Planar OLED init")
        self.getPower()

    def rxBufParse(self):
        self.rxbuf = self.ser.readline()

        if self.rxbuf.find('DISPLAY.POWER:0'): # power off feedback
            self.set("Off")
            print('Power Off')
        elif self.rxbuf.find('DISPLAY.POWER:1'): # power on feedback
            self.set("On")
            print('Power Off')

    def getPower(self):
        self.ser.write(b"display.power=1\r")  # turn on display
        logger.info("Planar OLED power get sent")
        time.sleep(1)
        self.rxBufParse()

    def power(self, value):
        if value == 1:
            self.ser.write(b"display.power=1\r")  # turn on display
            logger.info("Planar OLED power on sent")
            time.sleep(1)
            self.rxBufParse()

        else:
            self.ser.write(b"display.power=0\r")  # turn off display
            logger.info("Planar OLED power off sent")
            time.sleep(1)
            self.rxBufParse()

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
            time.sleep(10)
            self.printMenu()
        elif self.main_selection == '2':
            self.tv.power(0)
            time.sleep(10)
            self.printMenu()
        elif self.main_selection == '3':
            sys.exit()
        else:
            print("Invalid selection.\n")
            self.printMenu()


app = Controller()

while True:
    pass