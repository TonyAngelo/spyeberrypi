from tkinter import *

class App(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent=parent
        self.initUI()

    def initUI(self):
        self.parent.title("My App")
        self.pack(fill=BOTH,expand=1)

def main():
    root=Tk()
    root.geometry("640x480")
    app=App(root)
    root.mainloop()

if __name__=='__main__':
    main()
