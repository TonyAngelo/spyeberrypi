import RPi.GPIO as GPIO
import time
import socket

# sensor number used
sensor=4
# ip address of player
player_IP="10.10.9.51"
# file path for playlists
listpath="c:/users/public/documents/spyeworks/content/"
# name of active list
active_list="code 42"
# name of idle list
idle_list="altru health systems"
#programatic delay
active_delay_state=False
active_delay_time=30
idle_delay_state=False
idle_delay_time=30

# function for playing spyeworks list
def fnPlayList(player,path,name):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((player,8900))
    s.send(b'LOGIN\r\n')
    msg=s.recv(1024)
    if(msg.decode('ascii')[:2]=='OK'):
        cmd='SPL'+path+name+'.dml\r\n'
        s.send(cmd.encode())
    s.close()

# sensor setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor,GPIO.IN,GPIO.PUD_DOWN)
# setup sensor states
prev_state=False
curr_state=False
# start sensor loop
while True:
    time.sleep(0.1)
    prev_state=curr_state
    curr_state=GPIO.input(sensor)
    if curr_state!=prev_state:
        if curr_state:
            fnPlayList(player_IP,listpath,active_list) # active list
            if active_delay_state:
                time.sleep(active_delay_time)
        else:
            fnPlayList(player_IP,listpath,idle_list) # idle list
            if idle_delay_state:
                time.sleep(idle_delay_time)
