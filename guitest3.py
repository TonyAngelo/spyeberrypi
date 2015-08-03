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
        # check to see if values are in text file, otherwise load defaults
        self.ipaddy = Observable("192.168.1.110")
        self.filepath = Observable("c:/users/public/documents/spyeworks/content/")
        self.active = Observable("active")
        self.idle = Observable("idle")
        self.UpdateTextFile()

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

    def UpdateTextFile(self):
        # write the model to a text file for tracking variable changes
        pass


# main view
class View(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        self.title('Spyeworks Motion Settings')
        self.geometry("640x480")
        
        LABEL_COL=1
        VALUE_COL=2
        BTN_COL=3
        VALUE_WIDTH=50
        # ip address section
        nRowNum=1
        self.IPlabel = tk.Label(self, text='IP Address')
        self.IPlabel.grid(column=LABEL_COL,row=nRowNum,sticky=tk.E)
        self.IPActual = tk.Label(self, width=VALUE_WIDTH)
        self.IPActual.grid(column=VALUE_COL,row=nRowNum,sticky=tk.W)
        self.editIPButton = tk.Button(self, text='EDIT', width=8)
        self.editIPButton.grid(column=BTN_COL,row=nRowNum)
        # filepath section
        nRowNum=2
        tk.Label(self, text='Filepath').grid(column=LABEL_COL,row=nRowNum,sticky=tk.E)
        self.FilepathActual = tk.Label(self, width=VALUE_WIDTH)
        self.FilepathActual.grid(column=VALUE_COL,row=nRowNum,sticky=tk.W)
        self.editFilepathButton = tk.Button(self, text='EDIT', width=8)
        self.editFilepathButton.grid(column=BTN_COL,row=nRowNum)
        # active section
        nRowNum=3
        tk.Label(self, text='Active').grid(column=LABEL_COL,row=nRowNum,sticky=tk.E)
        self.ActiveActual = tk.Label(self, width=VALUE_WIDTH)
        self.ActiveActual.grid(column=VALUE_COL,row=nRowNum,sticky=tk.W)
        self.editActiveButton = tk.Button(self, text='EDIT', width=8)
        self.editActiveButton.grid(column=BTN_COL,row=nRowNum)
        # idle section
        nRowNum=4
        tk.Label(self, text='Idle').grid(column=LABEL_COL,row=nRowNum,sticky=tk.E)
        self.IdleActual = tk.Label(self, width=VALUE_WIDTH)
        self.IdleActual.grid(column=VALUE_COL,row=nRowNum,sticky=tk.W)
        self.editIdleButton = tk.Button(self, text='EDIT', width=8)
        self.editIdleButton.grid(column=BTN_COL,row=nRowNum)
    
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


# popup window for setting the players ip address
class FilepathChangerWidget(BasicChangerWidget):
    def __init__(self, master, app, title, currlabel, newlabel):
        BasicChangerWidget.__init__(self, master, app, title, currlabel, newlabel)
        self.okButton.config(command=self.validateFilepath)

    # validates the value entered to see if it is a valid ip address
    def validateFilepath(self):
        # if filepath is valid
        self.app.newFilepath(self.value.get())
        self.destroy()


# popup window for setting the active list
class ActiveChangerWidget(BasicChangerWidget):
    def __init__(self, master, app, title, currlabel, newlabel):
        BasicChangerWidget.__init__(self, master, app, title, currlabel, newlabel)
        self.okButton.config(command=self.validateActive)

    # validates the value entered to see if it is a valid ip address
    def validateActive(self):
        # if filepath is valid
        self.app.newActive(self.value.get())
        self.destroy()

# popup window for setting the active list
class IdleChangerWidget(BasicChangerWidget):
    def __init__(self, master, app, title, currlabel, newlabel):
        BasicChangerWidget.__init__(self, master, app, title, currlabel, newlabel)
        self.okButton.config(command=self.validateIdle)

    # validates the value entered to see if it is a valid ip address
    def validateIdle(self):
        # if filepath is valid
        self.app.newIdle(self.value.get())
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

        # create main view and link edit btns to funcs
        self.view = View(root)
        self.view.editIPButton.config(command=self.editIP)
        self.view.editFilepathButton.config(command=self.editFilepath)
        self.view.editActiveButton.config(command=self.editActive)
        self.view.editIdleButton.config(command=self.editIdle)

        # update variables
        self.updateIP(self.model.ipaddy.get())
        self.updateFilepath(self.model.filepath.get())
        self.updateActive(self.model.active.get())
        self.updateIdle(self.model.idle.get())
        
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


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = Controller(root)
    root.mainloop()
