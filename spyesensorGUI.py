# load imports
import tkinter as tk
import RPi.GPIO as GPIO
import time
import socket

# model object
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

class Sensor(Observable):
    def __init__(self, sensor=1, initialValue="Off"):
        Observable.__init__(self,initialValue)
        self.sensor=sensor
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensor,GPIO.IN,GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.sensor,GPIO.BOTH,self.sensorChange)

    def sensorChange(self,value):
        if GPIO.input(value):
            self.set("On")
        else:
            self.set("Off")

class Spyeworks(Observable):
    def __init__(self,ipaddy,filepath,active,idle,initialValue="Offline"):
        Observable.__init__(self,initialValue)
        self.ipaddy=ipaddy
        self.port=8900
        self.filepath=filepath
        self.active=active
        self.idle=idle
        self.login()

    def login(self,cmd=""):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((self.ipaddy,self.port))
        s.send(b'LOGIN\r\n')
        msg=s.recv(1024)
        if(msg.decode('ascii')[:2]=='OK'):
            self.set("Online")
            if len(cmd)>0:
                s.send(cmd.encode())
        else:
            self.set("Offline")
        s.close()

    def playActive(self):
        login('SPL'+self.filepath+self.active+'.dml\r\n')

    def playIdle(self):
        login('SPL'+self.filepath+self.idle+'.dml\r\n')

# model
class Model:
    def __init__(self):
        #check to see if values are in text file, otherwise load defaults
        try:
            f=open('spyeconfig.txt','r')
        # problem opening the file, load the default values
        except:
            self.ipaddy = Observable("192.168.1.110")
            self.filepath = Observable("c:/users/public/documents/spyeworks/content/")
            self.active = Observable("active")
            self.idle = Observable("idle")
            self.sensorenable = Observable("T")
            self.activedelay = Observable("F")
            self.activedelaytime = Observable("30")
            self.idledelay = Observable("F")
            self.idledelaytime = Observable("30")
            self.UpdateTextFile()
        else:
            self.ipaddy = Observable(f.readline()[:-1])
            self.filepath = Observable(f.readline()[:-1])
            self.active = Observable(f.readline()[:-1])
            self.idle = Observable(f.readline()[:-1])
            self.sensorenable = Observable(f.readline()[:-1])
            self.activedelay = Observable(f.readline()[:-1])
            self.activedelaytime = Observable(f.readline()[:-1])
            self.idledelay = Observable(f.readline()[:-1])
            self.idledelaytime = Observable(f.readline()[:-1])
        # close the file
        f.close()

        # get the current status of the sensor variable
        self.sensorstate = Sensor(4)

        # initiate the spyeworks player
        self.spyeworks = Spyeworks(self.ipaddy.get(),self.filepath.get(),
                                   self.active.get(),self.idle.get())

    ###############################################################
    ### Methods for the controller to update variables in the model
    ###############################################################

    def SetIP(self, value):
        self.ipaddy.set(value)
        self.UpdateTextFile()
        # also update the spyeworks player
        self.spyeworks.ipaddy=value

    def SetFilepath(self, value):
        self.filepath.set(value)
        self.UpdateTextFile()
        # also update the spyeworks player
        self.spyeworks.filepath=value

    def SetActive(self, value):
        self.active.set(value)
        self.UpdateTextFile()
        # also update the spyeworks player
        self.spyeworks.active=value

    def SetIdle(self, value):
        self.idle.set(value)
        self.UpdateTextFile()
        # also update the spyeworks player
        self.spyeworks.idle=value

    def SetSensorEnable(self,value):
        self.sensorenable.set(value)
        self.UpdateTextFile()

    def SetActiveDelay(self, value):
        self.activedelay.set(value)
        self.UpdateTextFile()

    def SetActiveDelayTime(self, value):
        self.activedelaytime.set(value)
        self.UpdateTextFile()

    def SetIdleDelay(self, value):
        self.idledelay.set(value)
        self.UpdateTextFile()

    def SetIdleDelayTime(self, value):
        self.idledelaytime.set(value)
        self.UpdateTextFile()

    ##########################################################
    ### Method for writing current model values to a text file
    ##########################################################

    def UpdateTextFile(self):
        # write the model to a text file for tracking variable changes
        f=open('spyeconfig.txt','w+')
        f.write(self.ipaddy.get()+'\n'+self.filepath.get()+'\n'+self.active.get()+'\n'+self.idle.get()+'\n'+self.sensorenable.get()+'\n'+
            self.activedelay.get()+'\n'+self.activedelaytime.get()+'\n'+self.idledelay.get()+'\n'+self.idledelaytime.get()+'\n')
        f.close()


# main view
class View(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        self.title('Spyeworks Motion Settings')
        self.geometry("800x600")
        self.grid_columnconfigure(7, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # grid constants
        SPACE_COL=0
        LABEL_COL=1
        VALUE_COL=2
        LABEL2_COL=2
        VALUE2_COL=3
        BTN_COL=4
        VALUE_WIDTH=50
        EDIT_WIDTH=8
        # spacer
        nRowNum=0
        self.titlespacerlabel = tk.Label(self, text='     ')
        self.titlespacerlabel.grid(column=SPACE_COL,row=nRowNum)
        # spyeworks title
        nRowNum=nRowNum+1
        self.spyetitlelabel = tk.Label(self, text='Spyeworks Settings')
        self.spyetitlelabel.grid(column=VALUE_COL,row=nRowNum)
        # spacer
        nRowNum=nRowNum+1
        self.titlespacerlabel = tk.Label(self, text='     ')
        self.titlespacerlabel.grid(column=SPACE_COL,row=nRowNum)
        # spyeworks online status
        nRowNum=nRowNum+1
        self.spyeworksonline = tk.Label(self)
        self.spyeworksonline.grid(column=VALUE_COL,row=nRowNum)
        # spacer
        nRowNum=nRowNum+1
        self.titlespacerlabel = tk.Label(self, text='     ')
        self.titlespacerlabel.grid(column=SPACE_COL,row=nRowNum)
        # ip address section
        nRowNum=nRowNum+1
        tk.Label(self, text='IP Address:').grid(column=LABEL_COL,row=nRowNum,sticky=tk.E,padx=5,pady=5)
        self.IPActual = tk.Label(self)
        self.IPActual.grid(column=VALUE_COL,row=nRowNum,sticky=tk.W)
        self.editIPButton = tk.Button(self, text='EDIT', width=EDIT_WIDTH)
        self.editIPButton.grid(column=BTN_COL,row=nRowNum,sticky=tk.E)
        # filepath section
        nRowNum=nRowNum+1
        tk.Label(self, text='Filepath:').grid(column=LABEL_COL,row=nRowNum,sticky=tk.E,padx=5,pady=5)
        self.FilepathActual = tk.Label(self)
        self.FilepathActual.grid(column=VALUE_COL,row=nRowNum,sticky=tk.W)
        self.editFilepathButton = tk.Button(self, text='EDIT', width=EDIT_WIDTH)
        self.editFilepathButton.grid(column=BTN_COL,row=nRowNum,sticky=tk.E)
        # active section
        nRowNum=nRowNum+1
        tk.Label(self, text='Active List:').grid(column=LABEL_COL,row=nRowNum,sticky=tk.E,padx=5,pady=5)
        self.ActiveActual = tk.Label(self)
        self.ActiveActual.grid(column=VALUE_COL,row=nRowNum,sticky=tk.W)
        self.editActiveButton = tk.Button(self, text='EDIT', width=EDIT_WIDTH)
        self.editActiveButton.grid(column=BTN_COL,row=nRowNum,sticky=tk.E)
        # idle section
        nRowNum=nRowNum+1
        tk.Label(self, text='Idle List:').grid(column=LABEL_COL,row=nRowNum,sticky=tk.E,padx=5,pady=5)
        self.IdleActual = tk.Label(self)
        self.IdleActual.grid(column=VALUE_COL,row=nRowNum,sticky=tk.W)
        self.editIdleButton = tk.Button(self, text='EDIT', width=EDIT_WIDTH)
        self.editIdleButton.grid(column=BTN_COL,row=nRowNum,sticky=tk.E)
        # spacer
        nRowNum=nRowNum+1
        self.titlespacer2label = tk.Label(self, text='     ')
        self.titlespacer2label.grid(column=SPACE_COL,row=nRowNum)
        # motion title
        nRowNum=nRowNum+1
        self.motiontitlelabel = tk.Label(self, text='Motion Settings')
        self.motiontitlelabel.grid(column=VALUE_COL,row=nRowNum)
        # spacer
        nRowNum=nRowNum+1
        self.titlespacerlabel = tk.Label(self, text='     ')
        self.titlespacerlabel.grid(column=5,row=nRowNum)
        # sensor status
        nRowNum=nRowNum+1
        tk.Label(self, text='Sensor Enabled:').grid(column=LABEL_COL,row=nRowNum,sticky=tk.E,padx=5,pady=5)
        self.SensorEnable = tk.Checkbutton(self,onvalue="T", offvalue="F")
        self.SensorEnable.grid(column=VALUE_COL,row=nRowNum,sticky=tk.W)
        tk.Label(self, text='Sensor State:').grid(column=LABEL2_COL,row=nRowNum,sticky=tk.E,padx=5,pady=5)
        self.SensorStatus = tk.Label(self)
        self.SensorStatus.grid(column=VALUE2_COL,row=nRowNum,sticky=tk.W)
        # active delay settings
        nRowNum=nRowNum+1
        tk.Label(self,text="Active Delay Enable").grid(column=LABEL_COL,row=nRowNum,sticky=tk.E,padx=5,pady=5)
        self.ActiveDelayCheck=tk.Checkbutton(self,onvalue="T", offvalue="F")
        self.ActiveDelayCheck.grid(column=VALUE_COL,row=nRowNum,sticky=tk.W)
        tk.Label(self,text="Active Delay Time:").grid(column=LABEL2_COL,row=nRowNum,sticky=tk.E,padx=5,pady=5)
        self.ActiveDelayTime=tk.Label(self)
        self.ActiveDelayTime.grid(column=VALUE2_COL,row=nRowNum,sticky=tk.W,padx=5,pady=5)
        self.editActiveDelayTimeButton=tk.Button(self,text="EDIT", width=EDIT_WIDTH)
        self.editActiveDelayTimeButton.grid(column=BTN_COL,row=nRowNum,sticky=tk.E)
        # idle delay settings
        nRowNum=nRowNum+1
        tk.Label(self,text="Idle Delay Enable").grid(column=LABEL_COL,row=nRowNum,sticky=tk.E,padx=5,pady=5)
        self.IdleDelayCheck=tk.Checkbutton(self,onvalue="T", offvalue="F")
        self.IdleDelayCheck.grid(column=VALUE_COL,row=nRowNum,sticky=tk.W)
        tk.Label(self,text="Idle Delay Time:").grid(column=LABEL2_COL,row=nRowNum,sticky=tk.E,padx=5,pady=5)
        self.IdleDelayTime=tk.Label(self)
        self.IdleDelayTime.grid(column=VALUE2_COL,row=nRowNum,sticky=tk.W,padx=5,pady=5)
        self.editIdleDelayTimeButton=tk.Button(self,text="EDIT", width=EDIT_WIDTH)
        self.editIdleDelayTimeButton.grid(column=BTN_COL,row=nRowNum,sticky=tk.E)

    #####################################################################
    ### Methods used by the controller for updating variables in the view
    #####################################################################

    # changes the ip address displayed to current 
    def updateOnline(self, value):
        self.spyeworksonline.config(text="Player is "+value) 

    # changes the ip address displayed to current 
    def updateIP(self, value):
        self.IPActual.config(text=value) 

    # changes the filepath displayed to current
    def updateFilepath(self, value):
        self.FilepathActual.config(text=value) 

    # changes the active playlist displayed to current
    def updateActive(self, value):
        self.ActiveActual.config(text=value) 

    # changes the idle playlist displayed to current
    def updateIdle(self, value):
        self.IdleActual.config(text=value) 

    # changes the sensor state displayed to current
    def updateSensor(self, value):
        self.SensorStatus.config(text=value) 

    # changes active list delay time displayed to current
    def updateActiveDelayTime(self, value):
        self.ActiveDelayTime.config(text=value)

    # changes idle list delay time displayed to current
    def updateIdleDelayTime(self, value):
        self.IdleDelayTime.config(text=value) 


# basic popup class for editing variables
class BasicChangerWidget(tk.Toplevel):
    def __init__(self, master, app, title, currlabel, newlabel):
        # initiate the popup as a toplevel object, keep track of the app and set the geometry and title
        tk.Toplevel.__init__(self, master)
        self.app=app
        self.geometry('%dx%d+%d+%d' % (300,200,250,125))
        self.title(title)
        # display the current ip label and value
        self.currlabel=tk.Label(self, text=currlabel).pack(padx=5,pady=5)
        self.curractual=tk.Label(self)
        self.curractual.pack(padx=5,pady=5)
        # display the new ip label and value
        self.value=tk.StringVar(None)
        self.newlabel=tk.Label(self,text=newlabel).pack(padx=5,pady=5)
        self.newentry=tk.Entry(self, textvariable=self.value)
        self.newentry.pack(padx=5,pady=5)
        # display the ok button
        self.okButton = tk.Button(self, text='OK', width=8)
        self.okButton.pack(padx=5,pady=5)

# popup window for setting the players ip address
class IPChangerWidget(BasicChangerWidget):
    def __init__(self, master, app, title, currlabel, newlabel):
        BasicChangerWidget.__init__(self, master, app, title, currlabel, newlabel)
        self.okButton.config(command=self.validateIP)

    # validates the value entered to see if it is a valid ip address
    def validateIP(self):
        # if IP is valid
        self.app.newIP(self.value.get())
        self.destroy()

# popup window for setting the filepath
class FilepathChangerWidget(BasicChangerWidget):
    def __init__(self, master, app, title, currlabel, newlabel):
        BasicChangerWidget.__init__(self, master, app, title, currlabel, newlabel)
        self.okButton.config(command=self.validateFilepath)

    # validates the value entered to see if it is a valid filepath
    def validateFilepath(self):
        # if filepath is valid
        self.app.newFilepath(self.value.get())
        self.destroy()

# popup window for setting the active list
class ActiveChangerWidget(BasicChangerWidget):
    def __init__(self, master, app, title, currlabel, newlabel):
        BasicChangerWidget.__init__(self, master, app, title, currlabel, newlabel)
        self.okButton.config(command=self.validateActive)

    # validates the value entered to see if it is a valid active list
    def validateActive(self):
        # if list name is valid
        self.app.newActive(self.value.get())
        self.destroy()

# popup window for setting the idle list
class IdleChangerWidget(BasicChangerWidget):
    def __init__(self, master, app, title, currlabel, newlabel):
        BasicChangerWidget.__init__(self, master, app, title, currlabel, newlabel)
        self.okButton.config(command=self.validateIdle)

    # validates the value entered to see if it is a valid idle list
    def validateIdle(self):
        # if list name is valid
        self.app.newIdle(self.value.get())
        self.destroy()

# popup window for setting the active list delay time
class ActiveDelayTimeChangerWidget(BasicChangerWidget):
    def __init__(self, master, app, title, currlabel, newlabel):
        BasicChangerWidget.__init__(self, master, app, title, currlabel, newlabel)
        self.okButton.config(command=self.validateActiveDelayTime)

    # validates the value entered to see if it is a valid delay time
    def validateActiveDelayTime(self):
        # if delay time is valid
        self.app.newActiveDelayTime(self.value.get())
        self.destroy()

# popup window for setting the idle list delay time
class IdleDelayTimeChangerWidget(BasicChangerWidget):
    def __init__(self, master, app, title, currlabel, newlabel):
        BasicChangerWidget.__init__(self, master, app, title, currlabel, newlabel)
        self.okButton.config(command=self.validateIdleDelayTime)

    # validates the value entered to see if it is a valid delay time
    def validateIdleDelayTime(self):
        # if delay time is valid
        self.app.newIdleDelayTime(self.value.get())
        self.destroy()


# controller, talks to views and models
class Controller:
    def __init__(self, root):

        # create modle and setup callbacks
        self.model = Model()
        self.model.spyeworks.addCallback(self.updatePlayerOnline)
        self.model.ipaddy.addCallback(self.updateIP)
        self.model.filepath.addCallback(self.updateFilepath)
        self.model.active.addCallback(self.updateActive)
        self.model.idle.addCallback(self.updateIdle)
        self.model.sensorstate.addCallback(self.updateSensorState)
        self.model.activedelaytime.addCallback(self.updateActiveDelayTime)
        self.model.idledelaytime.addCallback(self.updateIdleDelayTime)

        # create variables for tracking checkboxs
        self.ActiveDelay=tk.StringVar()
        self.ActiveDelay.set(self.model.activedelay.get())
        self.IdleDelay=tk.StringVar()
        self.IdleDelay.set(self.model.idledelay.get())
        self.SensorEnable=tk.StringVar()
        self.SensorEnable.set(self.model.sensorenable.get())

        # create main view and link edit btns to funcs
        self.view = View(root)
        self.view.editIPButton.config(command=self.editIP)
        self.view.editFilepathButton.config(command=self.editFilepath)
        self.view.editActiveButton.config(command=self.editActive)
        self.view.editIdleButton.config(command=self.editIdle)
        self.view.SensorEnable.config(variable=self.SensorEnable,command=self.updateSensorEnable)
        self.view.ActiveDelayCheck.config(variable=self.ActiveDelay,command=self.updateActiveDelay)
        self.view.editActiveDelayTimeButton.config(command=self.editActiveDelayTime)
        self.view.IdleDelayCheck.config(variable=self.IdleDelay,command=self.updateIdleDelay)
        self.view.editIdleDelayTimeButton.config(command=self.editIdleDelayTime)

        # update variables with data from model
        self.updatePlayerOnline(self.model.spyeworks.get())
        self.updateIP(self.model.ipaddy.get())
        self.updateFilepath(self.model.filepath.get())
        self.updateActive(self.model.active.get())
        self.updateIdle(self.model.idle.get())
        self.updateSensorState(self.model.sensorstate.get())
        self.updateActiveDelayTime(self.model.activedelaytime.get())
        self.updateIdleDelayTime(self.model.idledelaytime.get())
    
    #################################################################
    ### Methods for launching the changer popup for changing settings
    #################################################################

    # launches the popup for editing the players ip address
    def editIP(self):
        self.editIP = IPChangerWidget(self.view,self,"Set IP Address","Current IP", "New IP")
        self.editIP.curractual.config(text=self.model.ipaddy.get())

    # launches the popup for editing the filepath
    def editFilepath(self):
        self.editFilepath = FilepathChangerWidget(self.view,self,"Set Filepath","Current Filepath", "New Filepath")
        self.editFilepath.curractual.config(text=self.model.filepath.get())

    # launches the popup for editing the active list
    def editActive(self):
        self.editActive = ActiveChangerWidget(self.view,self,"Set Active List","Current Active List", "New Active List")
        self.editActive.curractual.config(text=self.model.active.get())

    # launches the popup for editing the idle list
    def editIdle(self):
        self.editIdle = IdleChangerWidget(self.view,self,"Set Idle List","Current Idle List", "New Idle List")
        self.editIdle.curractual.config(text=self.model.idle.get())

    # launches the popup for editing the active delay time
    def editActiveDelayTime(self):
        self.editActiveDelayTime = ActiveDelayTimeChangerWidget(self.view,self,"Set Active Delay Time","Current Active Delay Time", "New Active Delay Time")
        self.editActiveDelayTime.curractual.config(text=self.model.activedelaytime.get())

    # launches the popup for editing the idle delay time
    def editIdleDelayTime(self):
        self.editIdleDelayTime = IdleDelayTimeChangerWidget(self.view,self,"Set Idle Delay Time","Current Idle Delay Time", "New Idle Delay Time")
        self.editIdleDelayTime.curractual.config(text=self.model.idledelaytime.get())

    ##################################
    ### Methods for updating the model
    ##################################

    # sets the new ip address returned from the validate ip function
    def newIP(self, value):
        self.model.SetIP(value)

    # sets the new filepath returned from the validate filepath function
    def newFilepath(self, value):
        self.model.SetFilepath(value)

    # sets the new active list returned from the validate active function
    def newActive(self, value):
        self.model.SetActive(value)

    # sets the new idle list returned from the validate idle function
    def newIdle(self, value):
        self.model.SetIdle(value)

    # sets the new idle list returned from the validate idle function
    def newActiveDelayTime(self, value):
        self.model.SetActiveDelayTime(value)

    # sets the new idle list returned from the validate idle function
    def newIdleDelayTime(self, value):
        self.model.SetIdleDelayTime(value)
    
    #################################
    ### Methods for updating the view
    #################################

    # updates the player online status in the view
    def updatePlayerOnline(self, value):
        self.view.updateOnline(value)

    # updates the ip address in the view
    def updateIP(self, value):
        self.view.updateIP(value)

    # updates the filepath in the view
    def updateFilepath(self, value):
        self.view.updateFilepath(value)

    # updates the active list in the view
    def updateActive(self, value):
        self.view.updateActive(value)

    # updates the idle list in the view
    def updateIdle(self, value):
        self.view.updateIdle(value)

    # updates the sensor status in the view
    def updateSensorEnable(self):
        self.model.SetSensorEnable(self.SensorEnable.get())

    # updates the sensor status in the view
    def updateSensorState(self, value):
        self.view.updateSensor(value)

    # updates the active delay in the view
    def updateActiveDelay(self):
        self.model.SetActiveDelay(self.ActiveDelay.get())

    # updates the active delay time in the view
    def updateActiveDelayTime(self, value):
        self.view.updateActiveDelayTime(value)

    # updates the idle delay in the view
    def updateIdleDelay(self):
        self.model.SetIdleDelay(self.IdleDelay.get())

    # updates the idle delay time in the view
    def updateIdleDelayTime(self, value):
        self.view.updateIdleDelayTime(value)


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = Controller(root)
    root.mainloop()
