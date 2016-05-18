import RPi.GPIO as GPIO # for the sensor
import logging

logging.basicConfig(format='%(asctime)s %(levelname)-5s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename='logs/sensor.log', level=logging.DEBUG)
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

class LED(Observable):
    def __init__(self, port=1, initialValue="Off"):
        Observable.__init__(self, initialValue)
        self.port = port
        logger.info("LED init")
        GPIO.setup(self.port, GPIO.OUT)
        GPIO.output(self.port, GPIO.LOW)

    def ledState(self,value):
        if value==1:
            GPIO.output(self.port, GPIO.HIGH)
        else:
            GPIO.output(self.port, GPIO.LOW)


# sensor instance of the observable class
class Sensor(Observable):
    def __init__(self, sensor=1, initialValue="Off"):
        Observable.__init__(self,initialValue)
        self.sensor=sensor
        logger.info("Sensor init")
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.sensor,GPIO.IN,GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.sensor,GPIO.BOTH,self.sensorChange)

        self.led = LED(24)

    def sensorChange(self,value):
        if GPIO.input(value):
            logger.info("Sensor on")
            self.set("On")
            self.led(1)
        else:
            logger.info("Sensor off")
            self.set("Off")
            self.led(0)

class Controller:
    def __init__(self):
        # create model and setup callbacks
        self.sensor = Sensor(23)


app = Controller()

while True:
    pass