import socket
import time
from datetime import datetime
# import RPi.GPIO as GPIO 
import re
import sys


global run 
run = True

def checkifconnected(s):
    try:
        s.sendall(b"ping")
        print("still connected")
    except:
        # 
        return False

def createsocket(TCP_IP = "127.0.0.1",TCP_PORT = 5678):

    # create socket
    print("Trying to create socket...",end="")
    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("OK.")
    except socket.error as e:
        print(f"Error creating socket: {e}")
        return not run
    except KeyboardInterrupt:
        print("User terminated program.")
        sys.exit(1)
        return not run
  
    # connect to port
    for i in range(5):
        print("Trying to connect to port...",end="")
        try:
            s.connect((TCP_IP, TCP_PORT))
            print("OK.")
        except socket.gaierror as e:
            print(f"Address-related error connecting to server: {e}")
            
        except socket.error as e:
            print(f"Connection error: {e}")
        except KeyboardInterrupt: 
            sys.exit(1)  
            print("User ended program.")
    else:
        print("failed to connect to port. ")
        return not run
        
    


def listen(s):

        # timer
        COUNT = 0 
        STIMCOUNT = 0 
        STARTTIME = time.time()

        print("\nCOUNT, ELAPSED TIME (ms), DELAY TIME (ms):\n")

        CURRENTTIME = time.time()
      
        data = s.recv(1024)
    
        if (data):
            ACQUIRETIME = time.time()
            COUNT += 1
            # Openvibe sends 2 stims, ignores when button is released. if odd (first) save 
            if (COUNT%2 == 1 ):
                
                # # send stim
                # sendstim()
                # get timestamp
                ELAPSEDTIME = CURRENTTIME - STARTTIME
                DELAYTIME = (ACQUIRETIME - CURRENTTIME) # not true "delay", time from previous press

                # counter to save on file
                STIMCOUNT += 1
                print(str(STIMCOUNT-1).zfill(2) + f"| {round(ELAPSEDTIME,6)} | {round(DELAYTIME,6)} ",end = "" ) # dont print new line

                # save timestamp to file
                #savefile()
            
            

if __name__ == "__main__":
    while run: # try to connect 5 times
        try:
            listen(s)
        except:
            print("failed to listen")
        try:
            createsocket()
        except:
            print("failed to create socket")
        


