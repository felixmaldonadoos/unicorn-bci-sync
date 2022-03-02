
# Author: Felix A. Maldonado
# Date: 3/2/2022 9:44 AM

# This script connects to Unicorn Hybrid Black EEG and sends periodic stimulations to external 
# device for synchronization purposes.

import msvcrt
import numpy as np
import time
import matplotlib.pyplot as plt
from pylsl import StreamInlet, resolve_stream
import threading

global aborted
DURATION = 3
SAMPLING_FREQUENCY = 256
DOWN_SAMP_RATIO = 256

plt.style.use('dark_background')

def stream():
    # setup pylsl connection
    print('here')
    streams = resolve_stream()
    inlet = StreamInlet(streams[0])

    # trigger acquisition and record time
    aborted = False
    ABS_START_TIME = time.time()

    # create array to store signal and stimulation timestamps
    sig = []
    stim = []

    while not aborted:
        # get current time to print out stats at end.
        sample, timestamp = inlet.pull_sample()
        sig.append(sample)
        n_samples = len(sig)
        #print(sample[-1])
        if n_samples%(SAMPLING_FREQUENCY*DURATION) == 0:
            aborted = True
            run = False
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


# sends arduino stimulation every second
def send_stim():
    ABS_START_TIME = time.time()
    print(1)            # swap with board[pin].write(1)
    time.sleep(1)  
    while ((time.time() - ABS_START_TIME)<= 3):
        print(0)        # swap with board[pin].write(0)
        time.sleep(1)
        print(1)
        time.sleep(1)   # swap with board[pin].write(1)

    
def main():
    aborted = False
    run = True
    thread_data = threading.Thread(target=stream,daemon=True)
    thread_stim = threading.Thread(target=stream,daemon=True)
    
    thread_data.start()
    thread_stim.start()
    run = False
    if aborted:
        thread_data.join()
        thread_stim.join()


if __name__ == '__main__':
    print('Press any key to start...')
    msvcrt.getch()
    print('\n\n');
    print('================INPUT================')
    print('=Input fs: %0.1f'%SAMPLING_FREQUENCY)
    print('=Send Tobii stim every X seconds: %0.2f'%(SAMPLING_FREQUENCY/DOWN_SAMP_RATIO))
    print('=====================================')
    print('\n\n');

    main()
