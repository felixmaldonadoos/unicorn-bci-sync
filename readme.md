Author: Felix A. Maldonado Osorio 

Affiliation: Drexel University, PHL, PA

# Background
This project is intended for data synchronization between OpenVibe BCI platform and Tobii eyetracker system via Arduino system. 

This project is being conducted at Drexel University's Cognitive Neuroengineering and Quantitative Experimental Research 
(CONQUER) Collaborative Laboratory under the supervision of Dr. Hasan Ayaz. 

# requirements.txt
To install requirements, run the following in your environment:
```
pip install -r requirements.txt
```
# main.py
Recieves keyboard stimulus from ```OpenVibe``` software via ```TCP``` and forwards trigger to ```Tobii``` eye-tracker system. This code waits for keyboard input and saves external stimulus' information on ```count```,```elapsed_time```, and '''delay_time'''. Timestamps can also be saved on OpenVibe directly if needed. 

- ```TCP_IP = '' ```: Server IP address. Default to ```localhost = 127.0.0.1```.
- ```TCP_PORT = 5678```: Default ```TCP Writer``` Box port. Can be changed within OpenVibe. 

How to run: (Has not been updated for app implementation)
  - You can check host port on Windows by: ```Settings>Network & internet > Wi-Fi > "your_network"``` and locate ```IPv4 address: x:x:x:x```
  - To check if connected, run ```ping -c 1 host_port``` on RaspberryPi.
      1. Tip: Use VNC Viewer or SSH to remotely connect and run scripts on RaspberryPi, removing need for monitor and peripherals. 
  - Change ```TCP_PORT = "127.0.0.1"``` and ```TCP_PORT = 5678``` to necessary values. 
  - Run ```main.py```. 
  - Send stimulus by pressing any stim label key (e.g. 'a') on host computer, RaspberryPi is listening and forwards to Tobii. Stim labels can be found at 'stim_labels.png'
  - To close:
      1. Click ```CTRL+C``` on command window. ```main.py``` will saves each timestamp instantly.

# keyboardstim.xlm
```OpenVibe``` scenario. Press any assigned key to send stmiulus to Tobii eye-tracker. List can be found in ```resources/Stim_labels.png```. 

# testcodes/
- ```test_blink.py```
Simple LED blink program on RaspberryPi. Helpful to test circuit connection to output.
- ``` test_stim_button.py```
Sends stimulus to OpenVibe when pressing button.
- ```test_tcp.py```
Connects to ```OpenVibe``` port and sends periodic stimulus to host. 
- ```ping.py``` 
(Unstable on RaspberrryPi). Sends ping to host computer. Run before ```main.py``` to ensure connectivity.

# data/
Stores test data into ```.csv``` format with columns ```count, elapsed_time, delay_time``` with date when ```main.py``` is ran.

# Next steps: 
(In no specific order)
- add functionality to run upon startup (this is done on individual RaspberryPi's)
this removes the need to need RaspberryPi peripherals to run code. 
- implement latency measurements
- update ```delay_time``` algorithm bug (calculates time from previous sent stimulus)
- create a class module

