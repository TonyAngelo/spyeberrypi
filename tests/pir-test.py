from pir import Sensor

class Controller:
    def __init__(self):
        # create model and setup callbacks
        self.sensor = Sensor(23)


app = Controller()

while True:
    pass