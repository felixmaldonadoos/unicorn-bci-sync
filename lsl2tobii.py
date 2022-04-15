# Author: Felix A. Maldonado
# Date created: April 13, 2022

# takes input lsl stimulation markers from mentalab and forwards
# to tobii eye-tracker.

from pylsl import StreamInlet, resolve_stream
import time
from datetime import datetime
import RPi.GPIO as GPIO 
import re

# wait for stim to be recieved
def main():

    # counters
    STARTTIME = time.time()
    count = 0
    stimcount = 0

    print("\nStimulus list:\n")

    # Stim listener run forever until CTRL+C
    while True:
        CURRENTTIME = time.time()
        DATA, TIMESTAMP = inlet.pull_sample()

        # boolean to check if stim was recieved
        STIM_RECVD = (str(type(SAMPLE)) == ("<class 'list'>")) # [####] sent from OpenVibe

        # wait for stim to get recvd
        if STIM_RECVD:

            # send stim
            sendstim()
            
            # get timestamp
            ELAPSEDTIME = CURRENTTIME - STARTTIME

            # counter to save on file
            stimcount += 1
            print( f"{ELAPSEDTIME} |"+ str(stimcount-1))

            # save timestamp to file
            file = open(filename,"a")
            file.write(str(ELAPSEDTIME) + "," + str(stimcount))
            file.write("\n")
            file.close()

def sendstim():
    # uncomment prints for visualization
    #print ("rising")
    GPIO.output(PINLED,GPIO.HIGH)
    time.sleep(0.2)
    #print("falling")
    GPIO.output(PINLED,GPIO.LOW)


# GPIO setup
PINLED = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PINLED,GPIO.OUT)

if __name__ == "__main__":
    # create new file date and time of when it was ran
    filename = "data/"+datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ".csv"
    filename = re.sub(r"\s",'_',filename) # sub any whitespace with underscore
    filename = re.sub(r":",'-',filename) # HH:MM:SS in .csv name causes github fetch request error
    
    # Print introduction and common info. 
    print("\nStarting 'unicorn-bci-sync' LSL to Tobii")
    print("Stimulation codes can be found in data/Stimulation_codes.png")

    # create file with datetime
    print(f"Creating file in path: {filename}")
    file = open(filename,"a")

    # header
    file.write( "elapsed_time,count" + "\n")
    file.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ",count" + "\n")
    file.close()
    print("File created and saved.")
    
    # connect to socket
    try: 
        print("Trying to connect to strean.")
        streams = resolve_stream()
        inlet = StreamInlet(streams[0]) # need to check which stream is marker. mentalab produces 3
        print("Connected.")
    except:
        print("Failed.")

    
    try:
        print("Starting main...")
        main()
    except:
        print("\nForced Interrupt.")