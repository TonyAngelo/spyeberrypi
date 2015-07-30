from tkinter import *

root=Tk()
root.geometry("640x480")

# sensor number used
sensor=4
# ip address of player
player_IP=StringVar()
player_IP.set("10.10.9.51")
# file path for playlists
listpath=StringVar()
listpath.set("c:/users/public/documents/spyeworks/content/")
# name of active list
active_list=StringVar()
active_list.set("code 42")
# name of idle list
idle_list=StringVar()
idle_list.set("altru health systems")
#programatic delay
active_delay_state=False
active_delay_time=30
idle_delay_state=False
idle_delay_time=30

class App:
    def __init__(self,master):
        # build spyeworks settings frame
        self.spyeframe=Frame(master)
        self.spyeframe.pack(side='top')
        self.spyeTitle=Label(self.spyeframe,text="Spyeworks Settings", pady=3)
        self.spyeTitle.pack(side='top')
        # build player ip setting 
        self.playerIPframe=Frame(self.spyeframe,width=300,bd=1)
        self.playerIPframe.pack()
        self.playerIPlabel=Label(self.playerIPframe,text="Player IP: ")
        self.playerIPlabel.pack(side='left')
        self.playerIPaddress=Label(self.playerIPframe,textvariable=player_IP)
        self.playerIPaddress.pack(side='left')
        self.playerIPedit=Button(self.playerIPframe,text="EDIT",command=self.edit_playerIP)
        self.playerIPedit.pack(side='right')
        # build file path setting
        self.filepathframe=Frame(self.spyeframe,width=300)
        self.filepathframe.pack()
        self.filepathlabel=Label(self.filepathframe,text="Filepath: ")
        self.filepathlabel.pack(side='left')
        self.filepathaddress=Label(self.filepathframe,textvariable=listpath)
        self.filepathaddress.pack(side='left')
        self.filepathedit=Button(self.filepathframe,text="EDIT",command=self.edit_filepath)
        self.filepathedit.pack(side='right')
        # build active list setting
        self.activelistframe=Frame(self.spyeframe,width=300)
        self.activelistframe.pack()
        self.activelistlabel=Label(self.activelistframe,text="Active Playlist: ")
        self.activelistlabel.pack(side='left')
        self.activelistaddress=Label(self.activelistframe,textvariable=active_list)
        self.activelistaddress.pack(side='left')
        self.activelistedit=Button(self.activelistframe,text="EDIT",command=self.edit_activelist)
        self.activelistedit.pack(side='right')
        # build idle list setting
        self.idlelistframe=Frame(self.spyeframe,width=300)
        self.idlelistframe.pack()
        self.idlelistlabel=Label(self.idlelistframe,text="Idle Playlist: ")
        self.idlelistlabel.pack(side='left')
        self.idlelistaddress=Label(self.idlelistframe,textvariable=idle_list)
        self.idlelistaddress.pack(side='left')
        self.idlelistedit=Button(self.idlelistframe,text="EDIT",command=self.edit_idlelist)
        self.idlelistedit.pack(side='right')
        
        # build sensor settings frame
        self.sensorframe=Frame(master)
        self.sensorframe.pack(side='top')
        self.sensorTitle=Label(self.sensorframe,text="Sensor Settings")
        self.sensorTitle.pack(side='top')

    def edit_playerIP(self):
        player_IP.set("10.10.9.55")

    def edit_filepath(self):
        listpath.set("c:/users/desktop/")

    def edit_activelist(self):
        active_list.set("altru health systems")

    def edit_idlelist(self):
        idle_list.set("code 42")

app=App(root)

#root.attributes('-fullscreen',True)
#root.bind('<KeyPress>',onKeyPress)

root.mainloop()
root.destroy()
