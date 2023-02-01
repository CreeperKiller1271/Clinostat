from tkinter import *
import time
import motorControl

#starts the main expariment 
#gravity, eTime, dTime
def startSequence():
    #check input values
    #start thread
    sys.setup(gInput.getint(gInput.get()), tInput.getint(tInput.get()))
    sys.run()
    #hide main screen open the secondary
    startTime = time.time()
    setupFrame.pack_forget()
    rTime(startTime)
    runFrame.pack()
    return

def eStop():
    sys.stop()
    runFrame.pack_forget()
    setupFrame.pack()

def rTime(sTime):
    tString = '{:.2f}'.format(time.time() - sTime)
    tLbl.config(text=tString)
    tLbl.after(1000,rTime, sTime)

sys = motorControl.gravitySystem()

#window setup
root = Tk()
root.title("3D Clinostat")
root.option_add('*tearOff', FALSE)
root.minsize(400,300)

#contains all of the setup data
setupFrame = Frame(root)
setupFrame.pack()

#menu bar
mBar = Menu(root)
mFile = Menu(mBar)
mBar.add_cascade(menu=mFile, label="File")

#Sequence Start Button
startSequenceButton = Button(setupFrame, text = "Start", command=startSequence)
startSequenceButton.grid(row = 20, column = 2)

#Gravity Input
gInputFrame = LabelFrame(setupFrame, text="Desired Gravity(0-1)")
gInputFrame.grid(row=0, column=0, sticky=W)
gInput = Entry(gInputFrame, width=5, justify=RIGHT)
gInput.pack()

#Time Input
tInputFrame = LabelFrame(setupFrame, text="Experiment Time(hours)")
tInputFrame.grid(row=1, column=0, sticky=W)
tInput = Entry(tInputFrame, width=5, justify=RIGHT)
tInput.pack()

#Mechanical loading delay time Input
dInputFrame = LabelFrame(setupFrame, text="Delay Time(Minutes)")
dInputFrame.grid(row=2, column=0, sticky=W)
dInput = Entry(dInputFrame, width=5, justify=RIGHT)
dInput.pack()

#Homing device controlls
homeFrame = LabelFrame(setupFrame, text="Homing")
homeFrame.grid(row=5, column=0)

#Up button 
homeUp = Button(homeFrame, text = '\u25B2', command=sys.rForward, repeatdelay=100, repeatinterval=100)
homeUp.grid(row = 0, column=2)

#Down button
homeDown = Button(homeFrame, text = '\u25BC', command=sys.rBackward, repeatdelay=100, repeatinterval=100)
homeDown.grid(row = 3, column=2)

#Left button
homeLeft = Button(homeFrame, text = '\u25C0', command=sys.rLeft, repeatdelay=100, repeatinterval=100)
homeLeft.grid(row = 2, column=1)

#Right button
homeRight = Button(homeFrame, text = '\u25B6', command=sys.rRight, repeatdelay=100, repeatinterval=100)
homeRight.grid(row = 2, column=3)

#mechanical loading configuration frame
mLoadFrame = LabelFrame(setupFrame, text="Mechanical Loading")
mLoadFrame.grid(row=0, rowspan=6, column=3)

chamber1Lebel = Label(mLoadFrame, text="Chamber 1")
chamber1Lebel.grid(row=0,column=0)

chamber2Lebel = Label(mLoadFrame, text="Chamber 2")
chamber2Lebel.grid(row=1,column=0)

chamber3Lebel = Label(mLoadFrame, text="Chamber 3")
chamber3Lebel.grid(row=2,column=0)

chamber4Lebel = Label(mLoadFrame, text="Chamber 4")
chamber4Lebel.grid(row=3,column=0)

chamber5Lebel = Label(mLoadFrame, text="Chamber 5")
chamber5Lebel.grid(row=4,column=0)

chamber6Lebel = Label(mLoadFrame, text="Chamber 6")
chamber6Lebel.grid(row=5,column=0)

runFrame = Frame(root)

tLblFrame = LabelFrame(runFrame, text="Running Time")
tLblFrame.pack()
tLbl = Label(tLblFrame)
tLbl.pack()

stopSequenceButton = Button(runFrame, text = "Stop", command=eStop)
stopSequenceButton.pack()

root.config(menu=mBar)
root.mainloop()