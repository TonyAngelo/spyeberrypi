from models.models import Observable
import serial # for 232 control
import logging

logging.basicConfig(format='%(asctime)s %(levelname)-5s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename='../logs/sensor.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

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

    def power(self, value):
        if value == 1:
            self.ser.write(b"display.power=1\r")  # turn on display
            logger.info("Planar OLED power on sent")

        else:
            self.ser.write(b"display.power=0\r")  # turn off display
            logger.info("Planar OLED power off sent")