import RPi.GPIO as GPIO
import time


time.sleep(1)
GPIO.setmode(GPIO.BCM)

GPIO.setup(9, GPIO.OUT)

try:
	p = GPIO.PWM(9, 5)
	time.sleep(0.1)
finally:
	GPIO.cleanup()

