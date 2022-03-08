# Author: Felix A. Maldonado 

# This runs a simple loop to test arduino function. 
# returns delays. 

# After FALLING EDGE, there will be a pause of OFFTIME (s) after the impulse with width ONTIME (s)

from pyfirmata import Arduino
import time
import msvcrt
import numpy as np

def main(PIN=13,N_STIMS = 3, ONTIME = 0.2,OFFTIME = 5 ):

    # parameters to save for output data
    STARTTIME = time.time()
    RUNTIME = 0
    ARR_DELAY = []
    ARR_TIME = []
    COUNT = 0
    OUTPUT = []

    # setting arduino parameters
    PIN = 13
    port = 'COM5'

    # start looking for arduino
    print('Looking for arduino...')
    BOOT = time.time()
    run = True
    board = Arduino(port)

    # set initial output to low 
    board.digital[PIN].write(0)
    DELAY = time.time()-BOOT
    print('Arduino connect delay (s): %0.6f'%DELAY)
    print('Starting in 5 seconds...\n')

    # pause time for differentiation of bootup random outputs of pin13
    time.sleep(5)

    # sends stimuli and prints data while t < DURATION
    while (COUNT <= N_STIMS ):
        UP = time.time()
        board.digital[PIN].write(1)
        time.sleep(ONTIME)
        board.digital[PIN].write(0)
        time.sleep(OFFTIME)
        RUNTIME = time.time() - STARTTIME
        OUTPUT.append([(RUNTIME + DELAY),time.time() - UP - (ONTIME+OFFTIME)]) # real time sent, real delay
        COUNT += 1
        print('Stim # %0.1f sent at: %0.6f, Pulse delay(s): %0.6f'%(COUNT,RUNTIME + DELAY,(time.time() - UP - (ONTIME+OFFTIME))))
    else:
        run = False
        print('\nENDED..\n')
        print(np.asarray(OUTPUT))
        print('')

if __name__ == '__main__':
    print('\n===================================================\n')
    print('Simple code to test Tobii synchronization.\nIntented to compare time stimulus is sent and recieved.\n')
    print('Defaults to:\n- PIN = 13\n- N_STIMS = 3\n- ONTIME = 0.2 s\n- OFFTIME = 5 s\n- T = 5.2 s')
    print('===================================================\n')

    #print('\nPress ANY key to start...')
    #msvcrt.getch()
    main()



