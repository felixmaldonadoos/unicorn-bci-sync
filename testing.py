import socket
import time
from datetime import datetime
from tcp_latency import measure_latency
import RPi.GPIO as GPIO 
import re
import sys

class tcp2tobii():

    def __init__(self):
        # read file to extract IP and connections
        with open('address.txt') as fh:
            fstring = fh.readlines()

        # declaring the regex pattern for IP addresses
        pattern_ip = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        
        # initializing the list object
        self.TCP_IP = pattern_ip.search(fstring[0])[0] # find ip
        self.TCP_PORT = int(re.findall('[0-9]+', fstring[1])[0]) # find port num
        self.PIN_LED = int(re.findall('[0-9]+', fstring[2])[0]) # find led pin

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
        try: 
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("OK.")
        except socket.error as e:
            print(f"Error creating socket: {e}")
            sys.exit(1)
            
        # connect to port
        print("Trying to connect to port...",end="")
        try:
            self.s.connect((self.TCP_IP, self.TCP_PORT))
            print("OK.")
        except socket.gaierror as e:
            print(f"Address-related error connecting to server: {e}")
            sys.exit(1)
        except socket.error as e:
            print(f"Connection error: {e}")
            sys.exit(1)
        print("OK.")

        # check connection latency measure_latency(host,port,runs,timeout)
        print("Verifying initial latency...",end="")
        try:
            latency = str(round(measure_latency(host=self.TCP_IP, port=self.TCP_PORT)[0],4))
        except IndexError:
            print("Seems IP or port were disconnected.")
        print(latency)

    def sendstim(self):
        # uncomment prints for visualization
        #print ("rising")
        GPIO.output(self.PIN_LED,GPIO.HIGH)
        time.sleep(0.2)
        #print("falling")
        GPIO.output(self.PIN_LED,GPIO.LOW)

    def savefile(self):
        try:
            file = open(self.filename,"a")
            file.write(str(self.STIMCOUNT) +","+ str(self.ELAPSEDTIME) + "," + str(self.DELAYTIME))
            file.write("\n")
            file.close()
            print("Y")
        except:
            print("X")

    def is_still_connected(self):
        # not yet implemented
        try:
            self.s.sendall(b"ping")
            return True
        except:
            return False


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
        


def main():
    run = tcp2tobii()
    run.createsocket() 
    run.createfile()
    
    try:
        run.listen()
    except KeyboardInterrupt:
        print("\nForced Interrupt.")
        sys.exit(1)
    
if __name__ == "__main__":
    main()