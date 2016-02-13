import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
    if(GPIO.input(17) !=1):
        print("Button 1 pressed")
    else:
        print("fuck off.")
