# AUTHOR: Felix A. Maldonado
# DATE: April 17, 2022

import socket
import time
import re
import os
import sys
from tcp_latency import measure_latency

"""
this function reads in a TCP/IP address and port from testaddress.txt and tries to connect to it and prints 
out latency values in ms. Default port is localhost 127.0.0.1 and port 5678. By default this script will try
to connect to network 3 times (RUNS)
"""
class connecttest():
    def __init__(self):

        # read file to extract IP and connections
        with open('testaddress.txt') as fh:
            fstring = fh.readlines()

        # declaring the regex pattern for IP addresses
        pattern_ip = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        
        # initializing the list object
        self.TCP_IP = pattern_ip.search(fstring[0])[0] # find ip
        self.TCP_PORT = int(re.findall('[0-9]+', fstring[1])[0]) # find port num

        print(f"IP: {self.TCP_IP}\nPORT: {self.TCP_PORT}")

    def connect(self):

        # create socket
        print("Trying to create socket...",end="")
        try: 
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("OK.")
        except socket.error as e:
            print(f"Error:{e}")
            sys.exit(1)
            
        # connect to port
        print("Trying to connect to port...",end="")
        try:
            self.s.connect((self.TCP_IP, self.TCP_PORT))
            print("OK.")
        except socket.gaierror as e:
            print(f"Address-related error connecting to server: {e}")
        except socket.error as e:
            print(f"Error: Connection Refused >> Check TCP_HOST name and if it host is running.")
        # close socket. this allows script to reinitialize socket and port (in case any fail).
        self.s.close()

    def latency(self,runs = 5):
        # unstable, trying to not use numpy due to dependency issue on raspi
        try:
            print("Calculating latency...",end = "")
            LATENCY = round(measure_latency(host=self.TCP_IP, port=self.TCP_PORT)[0],4)
            print(f"{LATENCY} ms") 
        except:
            print("Failed.")        
    
    def main(self):
        self.connect()
        self.latency()

if __name__ == "__main__":

    RUNS = 3
    m = connecttest()

    for i in range(RUNS):
        try:
            print(f"\n==== TEST TCP CONNECTION RUN {i+1 } ====")
            m.main()
        except KeyboardInterrupt:
            print("Keyboard interrupt.")
            sys.exit(1)
    print("Test connection completed.\n")
