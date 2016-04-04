from models import Observable
import RPi.GPIO as GPIO # for the sensor
import logging

logging.basicConfig(format='%(asctime)s %(levelname)-5s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename='logs/sensor.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

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

    def sensorChange(self,value):
        if GPIO.input(value):
            logger.info("Sensor on")
            self.set("On")
        else:
            logger.info("Sensor off")
            self.set("Off")
