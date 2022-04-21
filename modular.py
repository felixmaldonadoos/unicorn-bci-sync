from testing import tcp2tobii
from tkinter import *
import sys

def main():
    global aborted; 
    aborted = False
    run = tcp2tobii()
    run.createsocket() 
    run.createfile()
    try:
        run.listen()
    except KeyboardInterrupt:         
        print("\nForced Interrupt.")
          

if __name__ == "__main__":
    root=Tk() 
    root.geometry('800x800') 
    var1=StringVar()  
    b1=Button(root,text='press', command=main) 
    b1.pack() 
    b2=Button(root,text='press2', command=root.destroy) 
    b2.pack() 
    l1=Label(root, textvariable=var1) 
    l1.pack() 
    root.mainloop() 