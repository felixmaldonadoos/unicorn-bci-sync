import socket
import time

# stimulus setup
#CODE = 'OVTK_StimulationId_Label_00'
#CODE_HEX = "4f56544b5f5374696d756c6174696f6e49645f4c6162656c5f3030"
#CODE_HEX = hex(CODE)
CODE_HEX = "0x584"
CODE_BYTES = bytes.fromhex(CODE_HEX)
print("code to send:\n")
print(CODE_BYTES)

# Server's IP and socket
TCP_IP = '10.0.0.92'
TCP_PORT = 15361

# socket setup
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while True:
    print("connected.")
    s.send(1412)
    time.sleep(3)