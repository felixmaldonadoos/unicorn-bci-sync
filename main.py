# Author: Felix A. Maldonado
# Date created: April 6, 2022

import socket
import time
from datetime import datetime
import RPi.GPIO as GPIO 

# socket setup
TCP_IP = '10.0.0.92'
TCP_PORT = 5678 # default tcp writer box

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

# GPIO setup
PINLED = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PINLED,GPIO.OUT)

# wait for stim to be recieved
def main():
    
    # counters
    STARTTIME = time.time()
    count = 0
    stimcount = 0

    while True:
        CURRENTTIME = time.time()
        data = s.recv(1024)
        #I WANT TO DIFFERENTIATE HERE
        if (data):
            count += 1
            if (count%2 == 1 ):
                sendstim()
                
                # get timestamp
                ELAPSEDTIME = CURRENTTIME - STARTTIME

                #print(data)
                stimcount += 1
                print(stimcount-1)

                # open and save timestamp to file
                file = open(filename,"a")
                file.write(str(ELAPSEDTIME) + "," + str(stimcount))
                file.write("\n")
                file.close()
                
        
            else:
                pass

def sendstim():
    # uncomment prints for visualization
    #print ("rising")
    GPIO.output(PINLED,GPIO.HIGH)
    time.sleep(0.2)
    #print("falling")
    GPIO.output(PINLED,GPIO.LOW)

if __name__ == "__main__":
    # create new file date and time of when it was ran
    filename = "data/"+datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ".csv"
    file = open(filename,"a")
    # header
    file.write( "Elapsed_time,count" + "\n")
    #file.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ",count" + "\n")
    file.close()

    main()
