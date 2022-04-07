This is still under dev...

# main.py
Recieves keyboard stimulus from ```OpenVibe``` software via ```TCP``` and forwards trigger to ```Tobii``` eye-tracker system. This code waits for keyboard input and saves external stimulus' information on ```Elapsed_time``` and ```count```. Timestamps can also be saved on ```OpenVibe``` directly if needed. 

- ```TCP_IP = '' ```: Server IP address.
- ```TCP_PORT = 5678```: Default ```TCP Writer``` Box port. Can be changed within ```OpenVibe```. 


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