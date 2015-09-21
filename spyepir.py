###############################################################
###
###   Raspberry pi motion control of Spyeworks, console version
###
###############################################################

# import libraries
import RPi.GPIO as GPIO # for the sensor
import time # for time delays
import socket # for ip comms

# sensor number used
sensor=14
# sensor setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor,GPIO.IN,GPIO.PUD_DOWN)
# setup sensor states
prev_state=False
curr_state=False

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

# function for writing variables to text file
def UpdateTextFile():
    # write the model to a text file for tracking variable changes
    f=open('spyeconfig.txt','w+')
    f.write(player_IP+'\n'+listpath+'\n'+active_list+'\n'+idle_list+'\n'+active_delay_state+'\n'+
        active_delay_time+'\n'+idle_delay_state+'\n'+idle_delay_time+'\n')
    f.close()

#check to see if values are in text file, otherwise load defaults
try:
    f=open('spyeconfig.txt','r')
# problem opening the file, load the default values
except:
    player_IP = "192.168.1.110"
    listpath = "c:/users/public/documents/spyeworks/content/"
    active_list = "active"
    idle_list = "idle"
    active_delay_state = "F"
    active_delay_time = "0"
    idle_delay_state = "T"
    idle_delay_time = "10"
    UpdateTextFile()
else:
# load the values from the file
    player_IP = f.readline()[:-1]
    listpath = f.readline()[:-1]
    active_list = f.readline()[:-1]
    idle_list = f.readline()[:-1]
    active_delay_state = f.readline()[:-1]
    active_delay_time = f.readline()[:-1]
    idle_delay_state = f.readline()[:-1]
    idle_delay_time = f.readline()[:-1]
# close the file
f.close()

# start sensor loop
while True:
    # wait a beat
    time.sleep(0.1)
    # update the previous sensor state variable
    prev_state=curr_state
    # get the current state
    curr_state=GPIO.input(sensor)
    # if the current state is different from the previous
    if curr_state!=prev_state:
        # if the sensor was activated
        if curr_state:
            # if the active delay timer is enabled
            if active_delay_state=="T":
                # wait for the delay length
                time.sleep(int(active_delay_time))
            # play the list
            fnPlayList(player_IP,listpath,active_list)
        # if the sensor went to idle
        else:
            # if the idle delay is enabled
            if idle_delay_state=="T":
                # wait for the delay length
                time.sleep(int(idle_delay_time))
            # play list
            fnPlayList(player_IP,listpath,idle_list)