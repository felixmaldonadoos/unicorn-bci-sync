
# Author: Felix A. Maldonado
# Date: 3/2/2022 9:44 AM

# This script connects to Unicorn Hybrid Black EEG and sends periodic stimulations to external 
# device for synchronization purposes.

import msvcrt
import numpy as np
import time
from pylsl import StreamInlet, resolve_stream

DURATION = 3
SAMPLING_FREQUENCY = 256
DOWN_SAMP_RATIO = 256


def main():
    # setup pylsl connection
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
        print('0')
        sample, timestamp = inlet.pull_sample()
        sig.append(sample)
        n_samples = len(sig)
        print(sig)

        if SAMPLING_FREQUENCY%n_samples==0:
            
            send_stim()
            stim.append(time.time() - ABS_START_TIME) # dont save curr_time = time.time() to save cpu resources
            #print(stim[-1] - stim[0]) # print last sent stim
            pass

        if n_samples%(SAMPLING_FREQUENCY*DURATION) == 0:
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