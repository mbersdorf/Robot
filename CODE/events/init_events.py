from .movement_events import register_movement_button_events
from .walze import register_walze_events
from .wasser import register_wasser_events
from .temperature import temperature_loop
from .movement_linmotor import register_linmotor_events
from hardware.sensors.Distance.sensor_monitor import start_sensor_monitor
import threading

def register_all_events(socketio):
    register_movement_button_events(socketio)
    register_walze_events(socketio)
    register_wasser_events(socketio)
    register_linmotor_events(socketio)

    # Temperatur-Loop in eigenem Thread starten
    threading.Thread(target=temperature_loop, args=(socketio,), daemon=True).start()

    # Sensorüberwachung starten (Abgrundsensoren)
    start_sensor_monitor()
