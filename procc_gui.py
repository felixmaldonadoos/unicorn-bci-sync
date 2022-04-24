from multiprocessing import Process
from tkinter import *
from tcp2tobii import *
  
class Application(object):
    def __init__(self,script):
        
        # set up window
        self.script = script
        self.top = tk.Tk()
        self.top.title('Sync Hub')
        self.top.geometry('300x200') # Size 200, 200
        
        # set up processes
        self.p1 = Process(target = connect)
        self.p2 = Process(target = stop)

        # declare buttons and target functions
        self.startButton = tk.Button(self.top, height=4, width=20, text ="Start Run", 
        command = self.p1.start,bg='green')
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
        connect()
  
    def stop(self):
        """
        this functions stops the process that was called.
        """ 
        # Popen(f"TASKKILL /F /PID {self.procc_id} /T") # windows
        print(f"Killing process")
        self.p1.kill()
        
    def terminateall(self):
        """
        Terminates whole program. Similar to force quit. You can also terminate program by 
        terminating window itself (red X or circle, depends on OS)
        """ 
        print("\nTerminating program..")
        sys.exit(1)
        self.top.destroy()



if __name__ == "__main__":
    a = Application()