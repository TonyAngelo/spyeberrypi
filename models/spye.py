from models.models import Observable
import time # for measuring spyeworks buffer timeout
import socket # for ip comms
import chardet # for character encoding/decoding
import logging

logging.basicConfig(format='%(asctime)s %(levelname)-5s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename='logs/spye.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# spyeworks instance
class Spyeworks(Observable):
    def __init__(self,ipaddy,filepath,active,idle,initialValue="Offline"):
        Observable.__init__(self,initialValue)
        self.ipaddy=ipaddy
        self.port=8900
        self.filepath=filepath
        self.active=active
        self.idle=idle
        self.activeplaying=False
        self.idleplaying=False
        self.parse=False
        self.currentList=Observable()
        self.allLists=Observable()
        self.getCurrentList()

    def login(self,cmd=""):
        # initiate the socket
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # set the socket connect timeout
        s.settimeout(5)
        # try to connect
        logger.info("Connecting to player at %s" , self.ipaddy)
        try:
            s.connect((self.ipaddy,self.port))
        # connection error
        except:
            logger.error("Connection error: %s" , self.ipaddy)
            self.set("Connection Error")
        # socket connected
        else:
            logger.info("Connected to player at %s. Logging in..." , self.ipaddy)
            # send the login msg
            s.send(b'LOGIN\r\n')
            # receive the reply
            msg=s.recv(1024)
            # decode the reply
            msg=msg.decode('ascii')
            # if it's an OK, login is good
            if(msg[:2]=='OK'):
                logger.info("Connected and logged in to player at %s" , self.ipaddy)
                # set device to Online
                self.set("Online")
                # if there is a command
                if len(cmd)>0:
                    # send the endcoded command
                    s.send(cmd.encode())
                    # if the command needs to be parsed
                    if self.parse:
                        if self.parseType=='active':
                            # set the active string and change the flags
                            self.currentList.set(self.active)
                            self.activeplaying=True
                            self.idleplaying=False
                        elif self.parseType=='idle':
                            # set the idle string and change the flags
                            self.currentList.set(self.idle)
                            self.activeplaying=False
                            self.idleplaying=True
                        # reset the parse flag
                        self.parse=False
                        # get the strings for parsing
                        stringsForParsing=self.recv_timeout(s).split('\r\n')
                        # if we are pasring an all playlists response
                        if self.parseType=='all':
                            allListsTemp=[]
                            # loop over strings
                            for st in stringsForParsing:
                                myString=st[len(self.filepath):-12]
                                if len(myString)>0:
                                    # add response to list
                                    allListsTemp.append(myString)
                            self.allLists.set(allListsTemp)
                        # if we are parsing the current list
                        elif self.parseType=='current':
                            # loop over strings
                            for st in stringsForParsing:
                                # get the playlist response
                                myString=st[len(self.filepath):-4]
                                # if there is a response
                                if len(myString)>0:
                                    # assign response to current list
                                    self.currentList.set(myString)
            # login not okay         
            else:
                logger.error("Login error: %s" , self.ipaddy)
                # set the device to login error
                self.set("Login Error")
            # close the socket connection
            s.close()

    # routine for receiving chunks of data from a socket
    def recv_timeout(self,mySocket,timeout=.5):
        # set the socket to nonblocking
        mySocket.setblocking(0)
        # initiate the variables
        buffer=[]
        data=''
        begin=time.time()
        # start the while loop
        while 1:
            # if there is data and we've reached the timeout, end the while
            if buffer and time.time()-begin > timeout:
                break
            # if there is no data, wait for twice the timeout
            elif time.time()-begin > timeout*2:
                break
            
            # receive data
            try:
                data=mySocket.recv(8192)
            except:
                pass
            else:
                # if data received
                if data:
                    # get the encoding type
                    encoding=chardet.detect(data)['encoding']
                    # add data to buffer
                    buffer.append(data.decode(encoding))
                    # reset timeout
                    begin=time.time()

        # join the buffer for return
        return ''.join(buffer)

    def getCurrentList(self):
        self.parse=True
        self.parseType='current'
        self.login('SCP\r\n')

    def getAllPlaylists(self):
        self.parse=True
        self.parseType='all'
        self.login('DML\r\n')

    def playActive(self):
        self.parse=True
        self.parseType='active'
        self.login('SPL'+self.filepath+self.active+'.dml\r\n')

    def playIdle(self):
        self.parse=True
        self.parseType='idle'
        self.login('SPL'+self.filepath+self.idle+'.dml\r\n')
