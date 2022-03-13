# Author: Felix A. Maldonado
# Date created: March 7, 2022
# Affiliation: Drexel University

# This script reads stimulation outputs from OpenVibe via LSL connection. For the function to run, 
# a scenerio with the LSL export box must be selected with stimulations as input. When running, 
# the script will listen to stimuli from OpenVibe and relay a logical 1 to Tobii via arduino for 
# a specified time ONTIME and then 0 for time OFFTIME. N_STIMS number of stimuli will be sent. 

# NOTE: Return time is relative to when script began recording. we can use this to map the first 
# point sent by creating a labeled stim on OpenVibe. Also, there is a delay calling initial 
# pylsl.StreamInlet.time_correction() but stabilizes on recurrent calls. 

import pandas as pd
import time
from pylsl import StreamInlet, resolve_stream, local_clock
from pyfirmata import Arduino
import sys
import os    
from pathlib import Path
import msvcrt as m
from datetime import datetime



# main function 
def main(PIN=12, ONTIME = 0.2):

    # arrays to store variables
    ARR_TIME = []
    ARR_ERR = []

    # used to count number of stims. 
    COUNT = 0 

    try:
        
        print('Connecting to LSL...\n')
        # start lsl stream
        streams = resolve_stream()
        inlet = StreamInlet(streams[0])
        print('Connected to LSL stream...')

        # making directory to save output 
        print('Creating output directiory cwd/test_data')
        current_directory = os.getcwd()
        PATH_OUT = os.path.join(current_directory, r'test_data')

        if not os.path.exists(PATH_OUT):
           os.makedirs(PATH_OUT)


        # start clock
        STARTTIME = local_clock()        
        print('INSTRUCTIONS:\n\nTo exit loop: \n1) Click on Python Shell and press CTRL+C \n2) send another OpenVibe stimulus (click on <KeyboardStimulator> tab and press <a> \n')
        print('Stimulation codes can be found at: stim_labels.png')

        print('\n\nPress ANY button to start listening for stimulus...\n\n')
        m.getch()
        print('COLLECTION STARTED...\n')
        print('Stim # {COUNT} recieved at {ELAPSEDTIME} s & Arduino stim sent at {RUNTIME} s with delay (Arduino - Stim): {RUNTIME - ELAPSEDTIME} s')
        # while still connected
        while True:

            # collect sample
            board.digital[PIN].write(0)
            SAMPLE, TIMESTAMP = inlet.pull_sample()

            # sample time (experimental)
            ELAPSEDTIME = (TIMESTAMP + inlet.time_correction())- STARTTIME

            # boolean to check if stim was recieved
            STIM_RECVD = (str(type(SAMPLE)) == ("<class 'list'>")) # [####] sent from OpenVibe

            # wait for stim to get recvd
            if STIM_RECVD:

                # rising time
                UP = local_clock()
                board.digital[PIN].write(1)
                time.sleep(ONTIME)
                
                # SEE NOTE 1
                board.digital[PIN].write(0)
                RUNTIME = UP - STARTTIME

                # append collected values for output
                ARR_TIME.append(RUNTIME)
                ARR_ERR.append(RUNTIME-ELAPSEDTIME)
                # add 1 to iterations

                COUNT += 1
                # may be removed for temporal resolution, need to check oscilloscope
                print(f'{COUNT} | {ELAPSEDTIME:.6f} s | {RUNTIME:.6f} s | {(RUNTIME - ELAPSEDTIME):.6f} s')
        #else:
            #board.digital[PIN].write(0) # if N_STIMS reached, bring pin to 0 and break loop
            #print('\nStream ended...\n')
            #print(OUTPUT)
    except KeyboardInterrupt:
        print('\nUser ended collection..\n\nSaving stimuli to CSV...\n')


    try:
        #create dataframe and save arrays to csv
        HEADERS = ['T_Stim_Recieved','Error_Stim_Recieved']
        df = pd.DataFrame(list(zip(ARR_TIME, ARR_ERR)),
                columns = HEADERS)
        # datetime object containing current date and time
        #now = datetime.now()
        # dd/mm/YY_H:M:S
        #DT_STRING = now.strftime("%d/%m/%Y_%H:%M:%S")
        #name = f'{PATH_OUT}_{datetime.datetime.now().strftime("%H%M_%m%d%Y")}.csv'
        FILE_OUT = os.path.join(PATH_OUT, r'stimulations.csv')
        df.to_csv(FILE_OUT)
        print('Done saving to CSV...\n\nClosing system...')
        #sys.exit(0)
    except:
        print('ERROR: Failed to save to csv file..\n\nClosing system...')
        print('\nThis is a bug. you need to delete the old files created from previous run.\n')

if __name__ == '__main__':
    print('\n===================================================')
    print('Simple code to test Tobii synchronization.\nIntented to compare time stimulus is sent and recieved.\n')
    print('Defaults to:\n- PIN = 12\n- ONTIME = 0.2 s')
    print('===================================================\n')
    # arduino params
    board = Arduino('COM5')
    print('\nConnected to arduino...\n')
    #time.sleep(5.5)
    main()

# NOTE 1
    # want to test in oscilloscope if it is makes a difference to bring 1 to 0 now or after if stmnt. 
    # i expect it slows down signal. but my read times were from before write(0), so then again there 
    # may be no delay

# NOTE 2
# def time_correction(self, timeout=FOREVER):
    # Retrieve an estimated time correction offset for the given stream.
    # The first call to this function takes several miliseconds until a 
    # reliable first estimate is obtained. Subsequent calls are instantaneous 
    # (and rely on periodic background updates). The precision of these 
    # estimates should be below 1 ms (empirically within +/-0.2 ms).