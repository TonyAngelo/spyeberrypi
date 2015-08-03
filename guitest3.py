import tkinter as tk

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


# model
class Model:
    def __init__(self):
        #check to see if values are in text file, otherwise load defaults
        try:
            f=open('spyeconfig.txt','r')
        except:
            self.ipaddy = Observable("192.168.1.110")
            self.filepath = Observable("c:/users/public/documents/spyeworks/content/")
            self.active = Observable("active")
            self.idle = Observable("idle")
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
            self.activedelay = Observable(f.readline()[:-1])
            self.activedelaytime = Observable(f.readline()[:-1])
            self.idledelay = Observable(f.readline()[:-1])
            self.idledelaytime = Observable(f.readline()[:-1])

        f.close()
        self.sensor = Observable("Off")

    def SetIP(self, value):
        self.ipaddy.set(value)
        self.UpdateTextFile()

    def SetFilepath(self, value):
        self.filepath.set(value)
        self.UpdateTextFile()

    def SetActive(self, value):
        self.active.set(value)
        self.UpdateTextFile()

    def SetIdle(self, value):
        self.idle.set(value)
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

    def UpdateTextFile(self):
        # write the model to a text file for tracking variable changes
        f=open('spyeconfig.txt','w+')
        f.write(self.ipaddy.get()+'\n'+self.filepath.get()+'\n'+self.active.get()+'\n'+self.idle.get()+'\n'+
            self.activedelay.get()+'\n'+self.activedelaytime.get()+'\n'+self.idledelay.get()+'\n'+self.idledelaytime.get()+'\n')
        f.close()


# main view
class View(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        self.title('Spyeworks Motion Settings')
        self.geometry("640x480")
        # grid constants
        SPACE_COL=0
        LABEL_COL=1
        VALUE_COL=2
        LABEL2_COL=3
        VALUE2_COL=4
        BTN_COL=6
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
        # ip address section
        nRowNum=nRowNum+1
        tk.Label(self, text='IP Address').grid(column=LABEL_COL,row=nRowNum,sticky=tk.E)
        self.IPActual = tk.Label(self, width=VALUE_WIDTH)
        self.IPActual.grid(column=VALUE_COL,row=nRowNum,sticky=tk.W)
        self.editIPButton = tk.Button(self, text='EDIT', width=EDIT_WIDTH)
        self.editIPButton.grid(column=BTN_COL,row=nRowNum)
        # filepath section
        nRowNum=nRowNum+1
        tk.Label(self, text='Filepath').grid(column=LABEL_COL,row=nRowNum,sticky=tk.E)
        self.FilepathActual = tk.Label(self, width=VALUE_WIDTH)
        self.FilepathActual.grid(column=VALUE_COL,row=nRowNum,sticky=tk.W)
        self.editFilepathButton = tk.Button(self, text='EDIT', width=EDIT_WIDTH)
        self.editFilepathButton.grid(column=BTN_COL,row=nRowNum)
        # active section
        nRowNum=nRowNum+1
        tk.Label(self, text='Active').grid(column=LABEL_COL,row=nRowNum,sticky=tk.E)
        self.ActiveActual = tk.Label(self, width=VALUE_WIDTH)
        self.ActiveActual.grid(column=VALUE_COL,row=nRowNum,sticky=tk.W)
        self.editActiveButton = tk.Button(self, text='EDIT', width=EDIT_WIDTH)
        self.editActiveButton.grid(column=BTN_COL,row=nRowNum)
        # idle section
        nRowNum=nRowNum+1
        tk.Label(self, text='Idle').grid(column=LABEL_COL,row=nRowNum,sticky=tk.E)
        self.IdleActual = tk.Label(self, width=VALUE_WIDTH)
        self.IdleActual.grid(column=VALUE_COL,row=nRowNum,sticky=tk.W)
        self.editIdleButton = tk.Button(self, text='EDIT', width=EDIT_WIDTH)
        self.editIdleButton.grid(column=BTN_COL,row=nRowNum)
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
        self.titlespacerlabel.grid(column=SPACE_COL,row=nRowNum)
        # sensor status
        nRowNum=nRowNum+1
        tk.Label(self, text='Sensor').grid(column=LABEL_COL,row=nRowNum,sticky=tk.E)
        self.SensorStatus = tk.Label(self, width=VALUE_WIDTH)
        self.SensorStatus.grid(column=VALUE_COL,row=nRowNum,sticky=tk.W)
        # active delay settings
        nRowNum=nRowNum+1
        tk.Label(self,text="Active Delay Enable").grid(column=LABEL_COL,row=nRowNum,sticky=tk.E)
        self.ActiveDelayCheck=tk.Checkbutton(self,onvalue="T", offvalue="F")
        self.ActiveDelayCheck.grid(column=VALUE_COL,row=nRowNum,sticky=tk.W)
        tk.Label(self,text="Delay Time").grid(column=LABEL2_COL,row=nRowNum,sticky=tk.E)
        self.ActiveDelayTime=tk.Label(self)
        self.ActiveDelayTime.grid(column=VALUE2_COL,row=nRowNum,sticky=tk.W)
        self.editActiveDelayTimeButton=tk.Button(self,text="EDIT", width=EDIT_WIDTH)
        self.editActiveDelayTimeButton.grid(column=BTN_COL,row=nRowNum)
        # idle delay settings
        nRowNum=nRowNum+1
        tk.Label(self,text="Idle Delay Enable").grid(column=LABEL_COL,row=nRowNum,sticky=tk.E)
        self.IdleDelayCheck=tk.Checkbutton(self,onvalue="T", offvalue="F")
        self.IdleDelayCheck.grid(column=VALUE_COL,row=nRowNum,sticky=tk.W)
        tk.Label(self,text="Delay Time").grid(column=LABEL2_COL,row=nRowNum,sticky=tk.E)
        self.IdleDelayTime=tk.Label(self)
        self.IdleDelayTime.grid(column=VALUE2_COL,row=nRowNum,sticky=tk.W)
        self.editIdleDelayTimeButton=tk.Button(self,text="EDIT", width=EDIT_WIDTH)
        self.editIdleDelayTimeButton.grid(column=BTN_COL,row=nRowNum)


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

    # # changes active list displayed to current
    # def updateActiveDelay(self, value):
    #     # self.ActiveDelayCheck.config(text=value) 
    #     pass

    # changes active list delay time displayed to current
    def updateActiveDelayTime(self, value):
        self.ActiveDelayTime.config(text=value)

    # # changes idle list displayed to current
    # def updateIdleDelay(self, value):
    #     # self.IdleDelayCheck.config(text=value) 
    #     pass 

    # changes idle list delay time displayed to current
    def updateIdleDelayTime(self, value):
        self.IdleDelayTime.config(text=value) 


# basic popup class for edting variables
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
        self.model.ipaddy.addCallback(self.updateIP)
        self.model.filepath.addCallback(self.updateFilepath)
        self.model.active.addCallback(self.updateActive)
        self.model.idle.addCallback(self.updateIdle)
        self.model.sensor.addCallback(self.updateSensor)
        # self.model.activedelay.addCallback(self.updateActiveDelay)
        self.model.activedelaytime.addCallback(self.updateActiveDelayTime)
        # self.model.idledelay.addCallback(self.updateIdleDelay)
        self.model.idledelaytime.addCallback(self.updateIdleDelayTime)

        self.ActiveDelay=tk.StringVar()
        self.ActiveDelay.set(self.model.activedelay.get())
        self.IdleDelay=tk.StringVar()
        self.IdleDelay.set(self.model.idledelay.get())

        # create main view and link edit btns to funcs
        self.view = View(root)
        self.view.editIPButton.config(command=self.editIP)
        self.view.editFilepathButton.config(command=self.editFilepath)
        self.view.editActiveButton.config(command=self.editActive)
        self.view.editIdleButton.config(command=self.editIdle)
        self.view.ActiveDelayCheck.config(variable=self.ActiveDelay,command=self.updateActiveDelay)
        self.view.editActiveDelayTimeButton.config(command=self.editActiveDelayTime)
        self.view.IdleDelayCheck.config(variable=self.IdleDelay,command=self.updateIdleDelay)
        self.view.editIdleDelayTimeButton.config(command=self.editIdleDelayTime)

        # update variables
        self.updateIP(self.model.ipaddy.get())
        self.updateFilepath(self.model.filepath.get())
        self.updateActive(self.model.active.get())
        self.updateIdle(self.model.idle.get())
        self.updateSensor(self.model.sensor.get())
        # self.updateActiveDelay(self.model.activedelay.get())
        self.updateActiveDelayTime(self.model.activedelaytime.get())
        # self.updateIdleDelay(self.model.idledelay.get())
        self.updateIdleDelayTime(self.model.idledelaytime.get())
        
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
    def updateSensor(self, value):
        self.view.updateSensor(value)

    # updates the active delay in the view
    def updateActiveDelay(self):
        self.model.SetActiveDelay(self.ActiveDelay.get())
        print(self.ActiveDelay.get())

    # updates the active delay time in the view
    def updateActiveDelayTime(self, value):
        self.view.updateActiveDelayTime(value)

    # updates the idle delay in the view
    def updateIdleDelay(self):
        self.model.SetIdleDelay(self.IdleDelay.get())
        print(self.IdleDelay.get())

    # updates the idle delay time in the view
    def updateIdleDelayTime(self, value):
        self.view.updateIdleDelayTime(value)


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = Controller(root)
    root.mainloop()
