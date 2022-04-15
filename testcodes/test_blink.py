import RPi.GPIO as GPIO
import time

# GPIO setup
PINLED = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PINLED,GPIO.OUT)

# loop forever
while True:
    print ("LED on")
    GPIO.output(18,GPIO.HIGH)
    time.sleep(1)
    print("LED off")
    GPIO.output(18,GPIO.LOW)
    time.sleep(1)
