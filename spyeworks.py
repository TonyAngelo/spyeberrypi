import socket # for connecting with ip devices
import chardet

# data object
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

# spyeworks instance of the observable class
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
        self.login()

    def login(self,cmd=""):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(5)
        try:
            s.connect((self.ipaddy,self.port))
        except:
            # connection error
            self.set("Connection Error")
        else:
            s.send(b'LOGIN\r\n')
            msg=s.recv(1024)
            msg=msg.decode('ascii')
            print("Msg:"+msg)
            if(msg[:2]=='OK'):
                self.set("Online")
                if len(cmd)>0:
                    s.send(cmd.encode())
                    if self.parse:
                        self.parse=False
                        msg=s.recv(1024)
                        encoding=chardet.detect(msg)['encoding']
                        stringToParse=msg.decode(encoding)
                        print("Msg:"+stringToParse[len(self.filepath):-4])
                        #print("Msg:"+msg)
            else:
                self.set("Login Error")
            s.close()

    def getCurrentList(self):
        self.parse=True
        self.login('SCP\r\n')

    def playActive(self):
        self.login('SPL'+self.filepath+self.active+'.dml\r\n')
        print("Play Active")
        #self.currentlist=self.active
        self.activeplaying=True
        self.idleplaying=False

    def playIdle(self):
        self.login('SPL'+self.filepath+self.idle+'.dml\r\n')
        print("Play Idle")
        #self.currentlist=self.idle
        self.activeplaying=False
        self.idleplaying=True

def updatePlayerOnline(value):
    print(value)


spyeworks = Spyeworks("10.10.9.51",
                    "c:/users/public/documents/spyeworks/content/",
                    "code 42","jamf")

spyeworks.addCallback(updatePlayerOnline)




