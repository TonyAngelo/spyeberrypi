from models.models import Observable
import RPi.GPIO as GPIO # for the sensor
import logging

logging.basicConfig(format='%(asctime)s %(levelname)-5s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename='logs/sensor.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
            self.led.ledState(1)
        else:
            logger.info("Sensor off")
            self.set("Off")
            self.led.ledState(0)