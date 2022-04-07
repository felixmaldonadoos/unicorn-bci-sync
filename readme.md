AUTHOR: Felix A. Maldonado

AFFILIATION: Drexel University, PHL, PA

Work in progress.

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
Recieves keyboard stimulus from ```OpenVibe``` software via ```TCP``` and forwards trigger to ```Tobii``` eye-tracker system. This code waits for keyboard input and saves external stimulus' information on ```Elapsed_time``` and ```count```. Timestamps can also be saved on ```OpenVibe``` directly if needed. 

- ```TCP_IP = '' ```: Server IP address.
- ```TCP_PORT = 5678```: Default ```TCP Writer``` Box port. Can be changed within ```OpenVibe```. 

<<<<<<< HEAD
=======
# keyboardstim.xlm
```OpenVibe``` scenario. Press any assigned key to send stmiulus to Tobii eye-tracker. List can be found in ```resources/Stim_labels.png```. 
>>>>>>> 64d5a1f7dfeeb1e249c051f653d8eb568448b7d5

# /testcodes
- ```test_button_only.py```
Blinks LED upon pressing button. 
- ``` test_stim_button.py```
Sends stimulus to ```OpenVibe```. (Unstable)
- ```test_tcp.py```
Connects to ```OpenVibe``` port and sends periodic stimulus. 

# /data
Stores test data into ```.csv``` format with columns ```Elapsed_time, count``` with date when ```main.py``` was ran.

# next steps: 
(In no specific order)
- Add ```try``` and ```except``` statements that will aid startup functionality. (Such as autoconnect to wifi, autorestart if failed, etc)
- Add error handling 
- add functionality to run upon startup
this removes the need to need RaspberryPi peripherals to run code. 

How to run: 
  - Run testing.xlm on OpenVibe.
  - Run ```main.py``` and wait for device to connect. 
  - Send any stim by pressing any stim label key (e.g. 'a'). Stim labels can be found at 'stim_labels.png'
  - To close:
      1. Click CTRK+C on command window. ```main.py``` will save data automatically.
