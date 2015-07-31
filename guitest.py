from tkinter import *
from tkinter import ttk

root=Tk()
root.title('Spyeworks Motion Settings')
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

class MainApp:
    def __init__(self,master):
        # build spyeworks settings frame
        self.spyeTitle=Label(master,text="Spyeworks Settings", pady=3)
        self.spyeTitle.pack(side='top')
        # build player ip setting 
        self.playerIPlabel=Label(master,text="Player IP: ")
        self.playerIPlabel.pack(side='left')
        self.playerIPaddress=Label(master,textvariable=player_IP)
        self.playerIPaddress.pack(side='left')
        self.playerIPedit=Button(master,text="EDIT",command=self.edit_playerIP)
        self.playerIPedit.pack(side='left')
        # build file path setting
        self.filepathlabel=Label(master,text="Filepath: ")
        self.filepathlabel.pack(side='left')
        self.filepathaddress=Label(master,textvariable=listpath)
        self.filepathaddress.pack(side='left')
        self.filepathedit=Button(master,text="EDIT",command=self.edit_filepath)
        self.filepathedit.pack(side='left')
        # build active list setting
        self.activelistlabel=Label(master,text="Active Playlist: ")
        self.activelistlabel.pack(side='left')
        self.activelistaddress=Label(master,textvariable=active_list)
        self.activelistaddress.pack(side='left')
        self.activelistedit=Button(master,text="EDIT",command=self.edit_activelist)
        self.activelistedit.pack(side='left')
        # build idle list setting
        self.idlelistlabel=Label(master,text="Idle Playlist: ")
        self.idlelistlabel.pack(side='left')
        self.idlelistaddress=Label(master,textvariable=idle_list)
        self.idlelistaddress.pack(side='left')
        self.idlelistedit=Button(master,text="EDIT",command=self.edit_idlelist)
        self.idlelistedit.pack(side='left')
        
        # build sensor settings frame
        self.sensorTitle=Label(master,text="Sensor Settings")
        self.sensorTitle.pack(side='top')

    def edit_playerIP(self):
        player_IP.set("10.10.9.55")

    def edit_filepath(self):
        listpath.set("c:/users/desktop/")

    def edit_activelist(self):
        active_list.set("altru health systems")

    def edit_idlelist(self):
        idle_list.set("code 42")

app=MainApp(root)

#root.attributes('-fullscreen',True)
#root.bind('<KeyPress>',onKeyPress)

root.mainloop()
root.destroy()
