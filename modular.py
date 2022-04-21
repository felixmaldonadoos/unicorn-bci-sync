from testing import tcp2tobii
from tkinter import *

def main():
    global aborted; aboted = False
    run = tcp2tobii()
    run.createsocket() 
    run.createfile()
    
    try:
        run.listen()
    except KeyboardInterrupt:
        print("\nForced Interrupt.")
        sys.exit(1)

    
if __name__ == "__main__":
    root=Tk() 
    root.geometry('800x800') 
    var1=StringVar()  
    b1=Button(root,text='press', command=main) 
    b1.pack() 
    b2=Button(root,text='press2', command=my_process2) 
    b2.pack() 
    l1=Label(root, textvariable=var1) 
    l1.pack() 
    root.mainloop() 