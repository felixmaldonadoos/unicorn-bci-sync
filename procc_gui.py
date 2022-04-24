from multiprocessing import Process
import tkinter as tk
import sys
from tcp2tobii import *
  
class Application(object):
    def __init__(self):
        
        # set up window
        self.top = tk.Tk()
        self.top.title('Sync Hub')
        self.top.geometry('300x200') # Size 200, 200
        
        # declare buttons and target functions
        self.startButton = tk.Button(self.top, height=4, width=20, text ="Start Run", 
        command = self.start,bg='green')
        self.stopButton = tk.Button(self.top, height=4, width=20, text ="Stop Run", 
        command = self.stop,bg='yellow')
        self.terminateButton = tk.Button(self.top, height=2, width=10, text ="Close", 
        command = self.terminateall,bg ='red')
        
        # set up buttons
        self.startButton.pack()
        self.stopButton.pack()
        self.terminateButton.pack()
        self.top.mainloop()
    
    def start(self):
        """
        connect() starts tcp2tobii connection
        """
        self.process = Process(target = connect)
        self.process.start()
        
    def connect(self):
        """
        connect tcp2tobii
        """
        tcp2tobii.connect()

    def stop(self):
        """
        this functions stops the process that was called.
        """ 
        # Popen(f"TASKKILL /F /PID {self.procc_id} /T") # windows
        print(f"Killing process")
        self.process.kill()
        
    def terminateall(self):
        """
        Terminates whole program. Similar to force quit. You can also terminate program by 
        terminating window itself (red X or circle, depends on OS)
        """ 
        print("\nTerminating program..")
        self.top.destroy()
        sys.exit(1)



if __name__ == "__main__":
    a = Application()