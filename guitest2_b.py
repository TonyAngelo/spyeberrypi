from tkinter import *

root=Tk()
root.title('Spyeworks Motion Settings')
root.geometry("640x480")

mainframe=Frame(root)
mainframe.grid(column=0,row=0,sticky=(N,W,E,S))
mainframe.columnconfigure(0,weight=1)
mainframe.rowconfigure(0,weight=1)

##setup variables
# sensor number used
sensor_status=StringVar()
sensor_status.set("Idle")
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
active_delay_state=IntVar()
active_delay_time=IntVar()
idle_delay_state=IntVar()
idle_delay_time=IntVar()

def edit_playerIP():
    pass

def edit_filepath():
    pass

def edit_activelist():
    pass

def edit_idlelist():
    pass

def edit_activedelay():
    pass

def edit_idledelay():
    pass

TITLE_COLUMN=3
LABEL_COLUMN=1
EDIT_COLUMN=5

nRowNum=1
playerSettingstitle=Label(mainframe,text="Spyeworks Player Settings")
playerSettingstitle.grid(column=TITLE_COLUMN,row=nRowNum)

nRowNum=2
playerIPlabel=Label(mainframe,text="Player IP: ").grid(column=LABEL_COLUMN,row=nRowNum,sticky=E)
playerIPactual=Label(mainframe,textvariable=player_IP).grid(column=3,row=nRowNum,sticky=W)
playerIPedit=Button(mainframe,text="EDIT",command=edit_playerIP).grid(column=EDIT_COLUMN,row=nRowNum)

nRowNum=3
filepathlabel=Label(mainframe,text="Filepath: ").grid(column=LABEL_COLUMN,row=nRowNum,sticky=E)
filepathactual=Label(mainframe,textvariable=listpath).grid(column=3,row=nRowNum,sticky=W)
filepathedit=Button(mainframe,text="EDIT",command=edit_filepath).grid(column=EDIT_COLUMN,row=nRowNum)

nRowNum=4
activelistlabel=Label(mainframe,text="Active Playlist: ").grid(column=LABEL_COLUMN,row=nRowNum,sticky=E)
activelistactual=Label(mainframe,textvariable=active_list).grid(column=3,row=nRowNum,sticky=W)
activelistedit=Button(mainframe,text="EDIT",command=edit_activelist).grid(column=EDIT_COLUMN,row=nRowNum)

nRowNum=5
idlelistlabel=Label(mainframe,text="Idle Playlist: ").grid(column=LABEL_COLUMN,row=nRowNum,sticky=E)
idlelistactual=Label(mainframe,textvariable=idle_list).grid(column=3,row=nRowNum,sticky=W)
idlelistedit=Button(mainframe,text="EDIT",command=edit_idlelist).grid(column=EDIT_COLUMN,row=nRowNum)

nRowNum=6
divider=Frame(mainframe,height=4).grid(row=nRowNum)

nRowNum=7
sensorSettingstitle=Label(mainframe,text="Motion Sensor Settings")
sensorSettingstitle.grid(column=TITLE_COLUMN,row=nRowNum)

nRowNum=8
setsensorlabel=Label(mainframe,text="Sensor Status: ").grid(column=LABEL_COLUMN,row=nRowNum,sticky=E)
setsensoractual=Label(mainframe,textvariable=sensor_status).grid(column=3,row=nRowNum,sticky=W)

nRowNum=9
activedelaylabel=Label(mainframe,text="Active Delay Enable").grid(column=LABEL_COLUMN,row=nRowNum,sticky=E)
activedelaycheck=Checkbutton(mainframe,variable=active_delay_state).grid(column=2,row=nRowNum,sticky=W)
activedelaytimelabel=Label(mainframe,text="Delay Time").grid(column=3,row=nRowNum,sticky=E)
activedelaytime=Label(mainframe,textvariable=str(active_delay_time)).grid(column=4,row=nRowNum,sticky=W)
activedelayedit=Button(mainframe,text="EDIT",command=edit_activedelay).grid(column=EDIT_COLUMN,row=nRowNum)

nRowNum=10
idledelaylabel=Label(mainframe,text="Idle Delay Enable").grid(column=LABEL_COLUMN,row=nRowNum,sticky=E)
idledelaycheck=Checkbutton(mainframe,variable=idle_delay_state).grid(column=2,row=nRowNum,sticky=W)
idledelaytimelabel=Label(mainframe,text="Delay Time").grid(column=3,row=nRowNum,sticky=E)
idledelaytime=Label(mainframe,textvariable=str(idle_delay_time)).grid(column=4,row=nRowNum,sticky=W)
idledelayedit=Button(mainframe,text="EDIT",command=edit_idledelay).grid(column=EDIT_COLUMN,row=nRowNum)


for child in mainframe.winfo_children(): child.grid_configure(padx=5,pady=5)

root.mainloop()
