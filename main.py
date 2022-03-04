
# Author: Felix A. Maldonado
# Date: 3/2/2022

# This script connects to Unicorn Hybrid Black EEG and sends periodic stimulations to external 
# device for synchronization purposes using 2 processes. 
#import pandas as pd 
import msvcrt
import numpy as np
import time
import os
from pylsl import StreamInlet, resolve_stream
from multiprocessing import Process, Value, Array
from pyfirmata import Arduino

#===========================================================
global aborted
DURATION = 10
SAMPLING_FREQUENCY = 256
DOWN_SAMP_RATIO = 256
#===========================================================
def stream():
    try:
    # setup pylsl connection
        print('Trying to connect to stream...\n')
        streams = resolve_stream()
        inlet = StreamInlet(streams[0])
    except:
        print('No device found...\n\nMake sure the following are met: \n- Native bluetooth driver is turned off \n- Unicorn is connected \n- OpenVibe is Connected and Playing\n')
        return
    # trigger acquisition and record time
    ABS_START_TIME = time.time()

    # create array to store signal and stimulation timestamps
    sig = []

    aborted = False
    while not aborted:
        # get current time to print out stats at end.
        sample, timestamp = inlet.pull_sample()
        sig.append(sample)

        n_samples = len(sig)

        #print(sample) #works to here 2:36pm
        if n_samples%(SAMPLING_FREQUENCY*DURATION) == 0:
            aborted = True
            ABS_STOP_TIME = time.time()

            CORRECTED_TIME = ABS_STOP_TIME - ABS_START_TIME - inlet.time_correction()
            EXPECTED_TIME = ABS_STOP_TIME - ABS_START_TIME
            print('\nOpenVibe LSL stream ended..\n')
            print('===============OUTPUT================')
            print('Absolute time: %0.6f'%(EXPECTED_TIME))
            print('Corrected time: %0.6f'%(CORRECTED_TIME))
            print('Absolute error: %0.6f'%(EXPECTED_TIME - CORRECTED_TIME))
            print('Number of Samples: %0.6f'%(len(sig)))
            print('True fs: %0.6f'%(len(sig)/CORRECTED_TIME), end='\n')
            print('=====================================\n')
        
    else:
        return aborted,sig,CORRECTED_TIME, EXPECTED_TIME

#===========================================================
# sends arduino stimulation every second
#===========================================================
CALL_TIME = time.time()
def send_stim():
    try:
        board = Arduino('COM5')
    except:
        print('\nERROR: Arduino not connected...\n')
        print('\nContinuing data collection without external stimuli...\n')
    else:
        run = True
        #board = Arduino('COM5') # takes approx 5.002-5.0004 second delay to connect
        board.digital[13].write(0)
        DELAY_TIME = time.time() - CALL_TIME
        print('\nArduino connected after %0.6f seconds..\n'%(DELAY_TIME)) # there is usually a ~5s delay to connect to arduino
        #maybe create a numpy array and append the first samples, by adding delay time as 0s 5*
        while ((time.time() - CALL_TIME - DELAY_TIME)<= DURATION):
        #while not aborted:
            up = time.time()
            board.digital[13].write(1)    
            time.sleep(1)
            board.digital[13].write(0)   
            time.sleep(1) 
            print('rising to falling edge delay:', time.time()-up - 2)
            # cut fist sig[-Delay*fps::] 
        else:
            RUNTIME = time.time() - CALL_TIME - DELAY_TIME
            print('\nArduino Runtime: %d seconds\n'%RUNTIME)
            print('There is a lag in deactivation that needs to be quantified..\n')
            return DELAY_TIME,RUNTIME # add to final csv 

#===========================================================
# main function
#===========================================================
def main():
    run = True

    #ret_value = Value("f",1.1,lock=False)
    processes = []
    process_stream = Process(target=stream)
    process_stim = Process(target=send_stim)
    #process_info = Process(target=send_info)
    processes.append(process_stream)
    processes.append(process_stim)
    #processes.append(process_info)

    for process in processes:
        process.start()

#===========================================================
# not implemented yet, will do after delays are quantified 
# and corrected in the numpy array
#===========================================================
def save_to_csv(**kwargs):
    for arg in kwargs.values:
        if arg[1] == True:
            pd.DataFrame(np_array).to_csv("path/to/file.csv")

if __name__ == '__main__':
    print('\nPress any key to start...')
    msvcrt.getch()
    print('');
    print('================INPUT================')
    print('=Input fs: %0.1f'%SAMPLING_FREQUENCY)
    print('=Send Tobii stim every X seconds: %0.2f'%(SAMPLING_FREQUENCY/DOWN_SAMP_RATIO))
    print('=====================================\n')
    main()
    
#===========================================================
# Comments to add in the future:
#===========================================================
# make a concurrent.futures.processpool to extract sig and delay arrays, to save to csv