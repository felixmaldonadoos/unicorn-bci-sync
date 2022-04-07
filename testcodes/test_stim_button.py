from csv import excel
import RPi.GPIO as io # Import Raspberry Pi GPIO library
import time
import socket


# gpio setup
PINBUTTON = 10
io.setwarnings(False) # Ignore warning for now
io.setmode(io.BOARD) # Use physical pin numbering
io.setup(PINBUTTON, io.IN, pull_up_down=io.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
# time to pause
TIMEOUT = 0.25

# stimulus setup
CODE_HEX = "4f56544b5f5374696d756c6174696f6e49645f4c6162656c5f3030"
CODE_BYTES = bytes.fromhex(CODE_HEX)
print("code to send:\n")
print(CODE_BYTES)

# Server's IP and socket
TCP_IP = '10.0.0.92'
TCP_PORT = 1024

# socket setup
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while True:
    if io.input(PINBUTTON) == io.HIGH:
        print("Button was pushed!")
        s.send(33024)
        time.sleep(TIMEOUT)