import time
import tkinter as tk
import sys
from subprocess import Popen
import socket
import time
from datetime import datetime
from tcp_latency import measure_latency
import RPi.GPIO as GPIO 
import re
import sys


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
    
    def temp_startog(self):
        """
        this functions starts a new process that runs our main script. 
        """ 
        print(f"{self.script}.py with process number: ",end="")
        process = Popen(["python", f"{self.script}.py"])
        self.procc_id = process.pid
        print(self.procc_id)
        return self.procc_id
        
    def stop(self):
        """
        this functions stops the process that was called.
        """ 
        # Popen(f"TASKKILL /F /PID {self.procc_id} /T") # windows
        print(f"Killing process: {self.procc_id}")
        Popen(["kill","-s","9",f"{self.procc_id}"])
        
    def terminateall(self):
        """
        Terminates whole program. Similar to force quit. You can also terminate program by 
        terminating window itself (red X or circle, depends on OS)
        """ 
        print("\nTerminating program..")
        sys.exit(1)
        self.top.destroy()

    def start():
        run = tcp2tobii()
        run.createsocket() 
        run.createfile()
        run.listen()
   

class tcp2tobii():
    def __init__(self):

        # declaring the regex pattern for IP addresses
        pattern_ip = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        
        # initializing the list object
        self.TCP_IP = "10.0.0.92" # find ip
        self.TCP_PORT = 5678 # find port num
        self.PIN_LED = 18 # find led pin

        # # file setup
        self.filename = "data/"+datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ".csv" # file with today's datetime
        self.filename = re.sub(r"\s",'_',self.filename) # sub any whitespace with underscore
        self.filename = re.sub(r":",'-',self.filename) # HH:MM:SS in .csv name causes github fetch request error

        # Print introduction and common info. 
        print("\nStarting 'unicorn-bci-sync'")
        print("Stimulation codes can be found in data/Stimulation_codes.png")
        print(f"IP to connect: {self.TCP_IP}")
        print(f"PORT to connect: {self.TCP_PORT}")
        print(f"Tobii Pin to connect: {self.PIN_LED}")

        # simple counters
        self.COUNT = 0
        self.STIMCOUNT = 0

        # GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.PIN_LED,GPIO.OUT)

    def createfile(self):
        # filename = string
        print("Creating csv...",end="")
        file = open(self.filename,"a")
        file.write("count,elapsed_time,delay_time" + "\n")
        file.close()
        print("OK.")

    def createsocket(self):

        # create socket
        print("Trying to create socket...",end="")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
        # connect to port
        print("Trying to connect to port...",end="")
        self.s.connect((self.TCP_IP, self.TCP_PORT))

        # check connection latency measure_latency(host,port,runs,timeout)
        print("Verifying initial latency...",end="")
        print(str(round(measure_latency(host=self.TCP_IP, port=self.TCP_PORT)[0],4)))

    def sendstim(self):
        # uncomment prints for visualization
        #print ("rising")
        GPIO.output(self.PIN_LED,GPIO.HIGH)
        time.sleep(0.2)
        #print("falling")
        GPIO.output(self.PIN_LED,GPIO.LOW)

    def savefile(self):
        file = open(self.filename,"a")
        file.write(str(self.STIMCOUNT) +","+ str(self.ELAPSEDTIME) + "," + str(self.DELAYTIME))
        file.write("\n")
        file.close()


    def listen(self):
        # timer
        STARTTIME = time.time()

        print("\nCOUNT, ELAPSED TIME (ms), DELAY TIME (ms):\n")

        # Stim listener run forever until CTRL+C
        while True:
            CURRENTTIME = time.time()
            data = self.s.recv(1024)
            
            if (data):
                ACQUIRETIME = time.time()
                self.COUNT += 1
                # Openvibe sends 2 stims, ignores when button is released. if odd (first) save 
                if (self.COUNT%2 == 1 ):
                    
                    # send stim
                    self.sendstim()
                    # get timestamp
                    self.ELAPSEDTIME = CURRENTTIME - STARTTIME
                    self.DELAYTIME = (ACQUIRETIME - CURRENTTIME) # not true "delay", time from previous press

                    # counter to save on file
                    self.STIMCOUNT += 1
                    print(str(self.STIMCOUNT-1).zfill(2) + f"| {round(self.ELAPSEDTIME,6)} | {round(self.DELAYTIME,6)} ",end = "" ) # dont print new line

                    # save timestamp to file
                    self.savefile()
                else:
                    pass
      
if __name__ == "__main__":
    Application()