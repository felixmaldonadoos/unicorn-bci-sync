# from link: 
# https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(PINBUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
# time to pause
TIMEOUT = 0.25
while True: # Run forever
    if GPIO.input(10) == GPIO.HIGH:
        print("Button was pushed!")
        time.sleep(TIMEOUT)