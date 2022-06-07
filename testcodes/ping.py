import platform
import socket
import sys

TCP_IP = '144.118.57.240' # dorado - personal
#TCP_IP = '144.118.56.78' # dragonfly-lab pc
TCP_PORT = 5678 # default tcp writer box

import platform    # For getting the operating system name
import subprocess  # For executing a shell command

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='linux' else '-c' # '-c' == 'unix'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0

if __name__ == "__main__":
    print(ping(TCP_IP))   