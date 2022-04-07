import socket
import time

# socket setup
TCP_IP = '10.0.0.92'
TCP_PORT = 5678 # default tcp writer box

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

# counter
count = 0
# check if odd
isOdd = count%2 == 1 

# wait for stim to be recieved
while True:
    
    data = s.recv(1024)
    #I WANT TO DIFFERENTIATE HERE
    if (data):
        count += 1
        print(data)
        if (count%2 == 1):
            #print(data)
            print("SEND STIM")
        else:
            pass

def 
