# importing the module
import re

# opening and reading the file

def findaddress():
    with open('address.txt') as fh:
        fstring = fh.readlines()

    # declaring the regex pattern for IP addresses
    pattern_ip = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    
    # initializing the list object
    TCP_IP = pattern_ip.search(fstring[0])[0]
    TCP_PORT = re.findall('[0-9]+', fstring[1])[0]
    PIN_LED = re.findall('[0-9]+', fstring[2])[0]
    return TCP_IP, TCP_PORT,PIN_LED

print(findaddress())
