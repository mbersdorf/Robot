import RPi.GPIO as GPIO
import os

class LED_PI_Status:
    """
    Klasse zur Steuerung der LED-Statusanzeige des Raspberry Pi.
    """
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

        # Initialer Status: LED an
        # LED leuchtet sobald programm startet
        # und bis der shutdown stattfindet
        GPIO.output(self.pin, GPIO.HIGH)



