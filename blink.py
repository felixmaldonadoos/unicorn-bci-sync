# Author: Felix A. Maldonado 

# This runs a simple loop to test arduino function. 
# returns delays. 

from pyfirmata import Arduino
import time
import msvcrt
import numpy as np


def main(N_STIMS = 10, DURATION = 10, DC_RATIO = 0.5):
    ONTIME = DC_RATIO
    OFFTIME = 1 - ONTIME
    print('Looking for arduino...')
    BOOT = time.time()
    pin = 13
    port = 'COM5'
    run = True
    # board parameters
    board = Arduino(port)

    # set initial output to low 
    board.digital[pin].write(0)
    DELAY = time.time()-BOOT
    print('Arduino connect delay (s): %0.6f'%DELAY)
    print('Starting...\n')

    # parameters to save for output data
    STARTTIME = time.time()
    RUNTIME = 0
    ARR_DELAY = []
    ARR_TIME = []
    COUNT = 0
    OUTPUT = []
    # sends stimuli and prints data while t < DURATION
    while (RUNTIME < DURATION ):
        UP = time.time()
        board.digital[pin].write(1)
        time.sleep(ONTIME)
        board.digital[pin].write(0)
        time.sleep(OFFTIME)
        RUNTIME = time.time() - STARTTIME
        OUTPUT.append([(time.time()-STARTTIME),time.time() - UP - 1]) # real time sent, real delay
        COUNT += 1
        print('Stim # %0.1f sent at: %0.6f, Pulse delay(s): %0.6f'%(COUNT,RUNTIME,(time.time() - UP - 1)))
    else:
        run = False
        print('Average pulse delay (s): %0.6f'%(np.asarray(ARR_DELAY).mean()))
        print('\nENDED..\n')
        print(np.asarray(OUTPUT))



if __name__ == '__main__':
    print('\n===================================================')
    print('BLINKING ARDUINO LED FROM PIN 13 ..')
    print('Simple code to test Tobii synchronization.')
    print('Default sends 10 pulses, T = 1s at 50% duty cycle.')
    print('===================================================\n')


    #print('\nPress ANY key to start...')
    #msvcrt.getch()
    main()



