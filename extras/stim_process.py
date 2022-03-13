import numpy as np
import time
from pylsl import StreamInlet, resolve_stream, local_clock
from multiprocessing import Process, Value, Array
from pyfirmata import Arduino

streams = resolve_stream()
inlet = StreamInlet(streams[0])
count = 0
STARTTIME = local_clock()
PREVIOUS = 0
while count < 10:
    sample, timestamp = inlet.pull_sample()
    ELAPSED = timestamp - STARTTIME
    print(f'Stim recieved at t(s): {ELAPSED}')
    print(ELAPSED - PREVIOUS - 10)
    # at the end, assign current time as previous, in order to get delay
    PREVIOUS = timestamp - STARTTIME
    count += 1