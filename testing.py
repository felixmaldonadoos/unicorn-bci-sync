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

import time
from pylsl import StreamInlet, resolve_stream, local_clock
#from multiprocessing import Process, Value, Array
from pyfirmata import Arduino

# stream params
streams = resolve_stream()
inlet = StreamInlet(streams[0])

# main function 
def main(PIN=13,N_STIMS = 5, ONTIME = 0.2,OFFTIME = 5):
    STARTTIME = local_clock()
    COUNT = 0 
    #SAMPLE = None
    #STIM_RECVD = (str(type(SAMPLE)) == ("<class 'list'>")) # [####] sent from OpenVibe
    while COUNT < N_STIMS:
        # collect sample
        board.digital[PIN].write(0)
        SAMPLE, TIMESTAMP = inlet.pull_sample()
        # sample time (experimental)
        ELAPSEDTIME = (TIMESTAMP + inlet.time_correction())- STARTTIME
        #DELAY = inlet.time_correction()
        STIM_RECVD = (str(type(SAMPLE)) == ("<class 'list'>")) # [####] sent from OpenVibe
        if STIM_RECVD:
            UP = local_clock()
            board.digital[PIN].write(1)
            time.sleep(ONTIME)
            #board.digital[PIN].write(0)
            RUNTIME = UP - STARTTIME
            COUNT += 1
            # may be removed for temporal resolution, need to check oscilloscope
            print(f'{COUNT} | {ELAPSEDTIME:.6f} s | {RUNTIME:.6f} s | {(RUNTIME - ELAPSEDTIME):.6f} s')
    else:
        print('\nStream ended...\n')
        #print(OUTPUT)

if __name__ == '__main__':
    print('\n===================================================\n')
    print('Simple code to test Tobii synchronization.\nIntented to compare time stimulus is sent and recieved.\n')
    print('Defaults to:\n- PIN = 13\n- N_STIMS = 5\n- ONTIME = 0.2 s')
    print('===================================================\n')
    # arduino params
    board = Arduino('COM5')
    print('\nConnected to arduino...\nPausing for 5.5 seconds...\n')
    print('Stim # {COUNT} recieved at {ELAPSEDTIME} s & Arduino stim sent at {RUNTIME} s with delay (Arduino - Stim): {RUNTIME - ELAPSEDTIME} s\n')
    time.sleep(5.5)
    main()


## PS ON pylsl DOCUMENTATION
#
#        def time_correction(self, timeout=FOREVER):
#            Retrieve an estimated time correction offset for the given stream.
#            The first call to this function takes several miliseconds until a 
#            reliable first estimate is obtained. Subsequent calls are instantaneous 
#            (and rely on periodic background updates). The precision of these 
#            estimates should be below 1 ms (empirically within +/-0.2 ms).