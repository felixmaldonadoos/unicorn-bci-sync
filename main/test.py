import socket
import time
from datetime import datetime
from tcp_latency import measure_latency
import RPi.GPIO as GPIO 
import re
import sys

print("Pausing for 5 seconds.")
time.sleep(5)
print("Ended.")