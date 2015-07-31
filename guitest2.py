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

mainframe=ttk.Frame(root,padding="3 3 12 12")
mainframe.grid(column=0,row=0,sticky=(N,W,E,S))
mainframe.columnconfigure(0,weight=1)
mainframe.rowconfigure(0,weight=1)
