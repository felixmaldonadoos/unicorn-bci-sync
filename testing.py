import socket
import time
from datetime import datetime
import RPi.GPIO as GPIO 
import re
import sys
import ping

class tcp2tobii(TCP_IP = '127.0.0.1',TCP_PORT = 5678):

    def __init__(self):
        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT
        self.PIN_LED = 18
        # file setup
        self.filename = "data/"+datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ".csv"
        self.filename = re.sub(r"\s",'_',filename) # sub any whitespace with underscore
        self.filename = re.sub(r":",'-',filename) # HH:MM:SS in .csv name causes github fetch request error

        # Print introduction and common info. 
        print("\nStarting 'unicorn-bci-sync'")
        print("Stimulation codes can be found in data/Stimulation_codes.png")
        print(f"IP to connect: {self.TCP_IP}")
        print(f"PORT to connect: {self.TCP_PORT}")

    def createfile(self):
        # filename = string
        print(f"Creating file in path: {self.filename}")
        print("Creating csv...",end="")
        file = open(self.filename,"a")
        file.write("count,elapsed_time,delay_time" + "\n")
        file.close()
        print("OK.")

    def createsocket(self):

        # create socket
        print("Trying to create socket...",end="")
        try: 
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("OK.")
        except socket.error as e:
            print(f"Error creating socket: {e}")

    def connectport(self):
        # connect to port
        print("Trying to connect to port...",end="")
        try:
            s.connect((TCP_IP, TCP_PORT))
            print("OK.")
        except socket.gaierror as e:
            print(f"Address-related error connecting to server: {e}")
            sys.exit(1)
        except socket.error as e:
            print(f"Connection error: {e}")
            sys.exit(1)
        print("OK.")

    def sendstim(self):
        # uncomment prints for visualization
        #print ("rising")
        GPIO.output(self.PIN_LED,GPIO.HIGH)
        time.sleep(0.2)
        #print("falling")
        GPIO.output(self.PIN_LED,GPIO.LOW)

    def savefile(self):
        try:
            file = open(filename,"a")
            file.write(str(self.STIMCOUNT) +","+ str(self.ELAPSEDTIME) + "," + str(self.DELAYTIME))
            file.write("\n")
            file.close()
            print("Y")
        except:
            print("X")

    def run(self):
        createsocket() 
        createfile()
        connectport()

        try:
            main()
        except KeyboardInterrupt:
            print("\nForced Interrupt.")
            sys.exit(1)
        except:
            print("Unknown error!")
            sys.exit(1)

    def main():

        # counters
        STARTTIME = time.time()
        count = 0
        STIMCOUNT = 0

        print("\nCOUNT, ELAPSED TIME (ms), DELAY TIME (ms):\n")

        # Stim listener run forever until CTRL+C
        while True:
            CURRENTTIME = time.time()
            data = s.recv(1024)
            
            if (data):
                ACQUIRETIME = time.time()
                self.count += 1
                # Openvibe sends 2 stims, ignores when button is released. if odd (first) save 
                if (self.count%2 == 1 ):
                    
                    # send stim
                    sendstim()
                    
                    # get timestamp
                    self.ELAPSEDTIME = CURRENTTIME - STARTTIME
                    self.DELAYTIME = (ACQUIRETIME - CURRENTTIME) # not true "delay", time from previous press

                    # counter to save on file
                    self.STIMCOUNT += 1
                    print(str(self.STIMCOUNT-1).zfill(2) + f"| {round(self.ELAPSEDTIME,6)} | {round(self.DELAYTIME,6)} ",end = "" ) # dont print new line

                    # save timestamp to file
                    savefile()
                else:
                    pass
  
if __name__ == "__main__":
    run = tcp2tobii()
    run.run()