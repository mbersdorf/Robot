import time
import threading
from hardware import objects



def temperature_loop(socketio):
    while True:
        try:
            obj_temp = objects.temperature_sensor.readObjectTemperature()
            socketio.emit('temperature_update', {'value': obj_temp})
        except Exception as e:
            print(f"Fehler beim Lesen der Temperatur: {e}")
        time.sleep(1)
