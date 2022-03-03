
# Author: Felix A. Maldonado
# Date: 3/2/2022

# This script connects to Unicorn Hybrid Black EEG and sends periodic stimulations to external 
# device for synchronization purposes using 2 processes. 

import msvcrt
import numpy as np
import time
import matplotlib.pyplot as plt
from pylsl import StreamInlet, resolve_stream
from multiprocessing import Process
from pyfirmata import Arduino

global aborted
aborted = False
DURATION = 10
SAMPLING_FREQUENCY = 256
DOWN_SAMP_RATIO = 256

def stream():
    # setup pylsl connection
    print('STREAM STARTED...\n\n')
    streams = resolve_stream()
    inlet = StreamInlet(streams[0])
    aborted = False
    # trigger acquisition and record time
    ABS_START_TIME = time.time()

    # create array to store signal and stimulation timestamps
    sig = []

    while not aborted:
        # get current time to print out stats at end.
        sample, timestamp = inlet.pull_sample()
        sig.append(sample)
        n_samples = len(sig)
        print(sample)
        if n_samples%(SAMPLING_FREQUENCY*DURATION+1) == 0:
            aborted = True
            ABS_STOP_TIME = time.time()

            CORRECTED_TIME = ABS_STOP_TIME - ABS_START_TIME - inlet.time_correction()
            EXPECTED_TIME = ABS_STOP_TIME - ABS_START_TIME
            print('\n\n');
            print('===============OUTPUT================')
            print('Absolute time: %0.6f'%(EXPECTED_TIME))
            print('Corrected time: %0.6f'%(CORRECTED_TIME))
            print('Absolute error: %0.6f'%(EXPECTED_TIME - CORRECTED_TIME))
            print('True fs: %0.6f'%(len(sig)/CORRECTED_TIME), end='\n')
            print('Program ended...')
            print('=====================================')
            print('\n\n');
    else:
        print('Stream ended..')
        time.sleep(1)
        return aborted

# sends arduino stimulation every second
def send_stim():
    CALL_TIME = time.time()
    #aborted = False
    board = Arduino('COM5')
    board.digital[13].write(0)
    DELAY_TIME = time.time() - CALL_TIME
    print('Board connected after %0.6f seconds..'%(DELAY_TIME)) # there is usually a ~5s delay to connect to arduino
    #maybe create a numpy array and append the first samples, by adding delay time as 0s 5*
    while ((time.time() - CALL_TIME - DELAY_TIME)<= DURATION):
        up = time.time()
        board.digital[13].write(1)    # swap with board[pin].write(0)
        time.sleep(1)
        board.digital[13].write(0)   
        time.sleep(1)  # swap with board[pin].write(1)
        print('rising to falling edge delay:', time.time()-up - 2)

    print('out of loop!')

def main():
    run = True
    processes = []
    process_stream = Process(target=stream)
    process_stim = Process(target=send_stim)
    processes.append(process_stream)
    processes.append(process_stim)

    for process in processes:
        process.start()
    run = False
    if aborted:
        print('FINAL ABORTED!')
        for process in processes:
            process.terminate()
            print('Terminating process')

if __name__ == '__main__':
    print('\nPress any key to start...')
    msvcrt.getch()
    print('\n\n');
    print('================INPUT================')
    print('=Input fs: %0.1f'%SAMPLING_FREQUENCY)
    print('=Send Tobii stim every X seconds: %0.2f'%(SAMPLING_FREQUENCY/DOWN_SAMP_RATIO))
    print('=====================================')
    print('\n\n')
    main()