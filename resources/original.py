# Author: Felix A. Maldonado
# Date created: April 6, 2022

import socket
import time
from datetime import datetime
import RPi.GPIO as GPIO 
import re
import sys
import ping

# wait for stim to be recieved
def main():

    # counters
    STARTTIME = time.time()
    count = 0
    STIMCOUNT = 0

    print("\nStimulus list:\n")

    # Stim listener run forever until CTRL+C
    while True:
        CURRENTTIME = time.time()
        data = s.recv(1024)
        
        if (data):
            ACQUIRETIME = time.time()
            count += 1
            # Openvibe sends 2 stims, ignores when button is released. if odd (first) save 
            if (count%2 == 1 ):
                
                # send stim
                sendstim()
                
                # get timestamp
                ELAPSEDTIME = CURRENTTIME - STARTTIME
                DELAYTIME = (ACQUIRETIME - CURRENTTIME) # not true "delay", time from previous press

                # counter to save on file
                STIMCOUNT += 1
                ELAPSEDTIME_ROUNDED = str(ELAPSEDTIME).zfill(8)
                print( str(STIMCOUNT-1).zfill(2) + f"| {round(ELAPSEDTIME,6)} | {round(DELAYTIME,6)} ",end = "" ) # dont print new line

                # save timestamp to file
                savefile(ELAPSEDTIME,DELAYTIME,STIMCOUNT)
            else:
                pass

def sendstim():
    # uncomment prints for visualization
    #print ("rising")
    GPIO.output(PINLED,GPIO.HIGH)
    time.sleep(0.2)
    #print("falling")
    GPIO.output(PINLED,GPIO.LOW)

def savefile(ELAPSEDTIME, DELAYTIME, STIMCOUNT):
    try:
        file = open(filename,"a")
        file.write(str(STIMCOUNT) +","+ str(ELAPSEDTIME) + "," + str(DELAYTIME))
        file.write("\n")
        file.close()
        print("Y")
    except:
        print("X")

def createfile(filename):
    # filename = string
    print(f"Creating file in path: {filename}")
    print("Creating csv...",end="")
    file = open(filename,"a")
    file.write("count,elapsed_time,delay_time" + "\n")
    file.close()
    print("OK.")

# file setup
filename = "data/"+datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ".csv"
filename = re.sub(r"\s",'_',filename) # sub any whitespace with underscore
filename = re.sub(r":",'-',filename) # HH:MM:SS in .csv name causes github fetch request error

# socket setup
TCP_IP = '127.0.0.1' # localhost
TCP_PORT = 5678 # default tcp writer box

# GPIO setup
PINLED = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PINLED,GPIO.OUT)

if __name__ == "__main__":
    
    # Print introduction and common info. 
    print("\nStarting 'unicorn-bci-sync'")
    print("Stimulation codes can be found in data/Stimulation_codes.png")
    print(f"IP to connect: {TCP_IP}")
    print(f"PORT to connect: {TCP_PORT}")

    # create file with datetime
    createfile(filename)
    
    # connect to socket
    print("Trying to create socket...",end="")
    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("OK.")
    except socket.error as e:
        print(f"Error creating socket: {e}")

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

    # start main program
    try:
        print("Starting main...")
        main()
    except KeyboardInterrupt:
        print("\nForced Interrupt.")