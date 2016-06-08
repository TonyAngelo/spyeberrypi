#########################################################################
#########################################################################
#
# Spyeworks - Motion Sensor Interface - v1
#
# This program uses the Rasberry Pi to track a connected motion sensor 
# and based on it's state change the playlist on a Spyeworks Digital 
# Signage Player from an Active list to an Idle list.
#
# by Tony Petrangelo
# tonypetrangelo@gmail.com
#
#########################################################################
#########################################################################

# import libraries
from models.models import Model
from threading import Timer # for delay timers

# controller, talks to views and models
class Controller:
    def __init__(self):
        # create model and setup callbacks
        self.model = Model()
        self.model.spyeworks.addCallback(self.updatePlayerOnline)
        self.model.spyeworks.currentList.addCallback(self.updateCurrentList)
        self.model.sensorstate.addCallback(self.updateSensorState)

        # create variables for timers
        self.activeTimer=Timer(1, self.dummyFunc, ())
        #self.playIdleList=False

        # update variables with data from model
        self.updatePlayerOnline(self.model.spyeworks.get())
        self.updateSensorState(self.model.sensorstate.get())

    #################################
    ### Methods for printing to the console
    #################################

    # updates the player online status in the view
    def updatePlayerOnline(self, value):
        print("Player is "+value)
        pass

    # updates the current list status in the view
    def updateCurrentList(self, value):
        print("Current List is "+value)
        pass

    # dummy function for passing to timer thread
    def dummyFunc(self):
        pass

    # handles updates to the sensor status
    def updateSensorState(self, value):
        # updates the sensor status in the view
        print("Sensor is "+value)
        # if the sensor is activated
        if value=="On":
            # if the active timer is not active
            if self.activeTimer.isAlive()==False:
                # play the active list
                self.model.spyeworks.playActive()
                # start the active list timer
                self.activeTimer = Timer(int(self.model.activedelay.get()), self.dummyFunc, ())
                self.activeTimer.start()

app = Controller()

while True:
    pass
