import RPi.GPIO as GPIO
import os
import time

# Pin, an dem dein Schalter hängt
SWITCH_PIN = 21  

GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Kippschalter-Überwachung läuft. (STRG+C zum Beenden)")

try:
    while True:
        #print("Test")
        print(GPIO.input(SWITCH_PIN))
        # Wenn Schalter geschlossen ist
        if GPIO.input(SWITCH_PIN) == GPIO.LOW:
            print("Schalter LOW erkannt – Raspberry Pi fährt herunter.")
            #os.system("sudo shutdown now")
            #time.sleep(5)  
        time.sleep(0.2)

except KeyboardInterrupt:
    print("Beendet vom Benutzer!")

finally:
    GPIO.cleanup()



# init Event:

#from .shutdown_event import setup_shutdown_swith

# Register all Events:

#Schalter Event für Shutdown aktivieren
#setup_shutdown_switch()