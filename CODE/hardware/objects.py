"""
hardware_init.py
Initialisiert alle Aktoren und Sensoren des Roboters.
Bindet zentrale Pin-Belegung aus pins.py ein.
"""

# ============================================================
# 🔹 Imports
# ============================================================

import hardware.Pins.pins as pins
from hardware.sensors.Distance.Infrared import E18DN80NK
from hardware.sensors.Temperature.MLX90614 import MLX90614
from hardware.actors.valve import Valve
from hardware.actors.brush import Brush
from hardware.actors.movement import Movement
from hardware.actors.linmotor import Linmotor

brush = None
valve = None
movement = None
linmotor = None
front_distance_sensor = None
back_distance_sensor = None
temperature_sensor = None



def initialize_hardware(socketio):
    """
    Initialisiert alle Hardware-Komponenten des Roboters.

    Args:
        socketio: SocketIO-Objekt für Echtzeit-Kommunikation
    """
    # ============================================================
    # 🔹 Aktoren (Outputs)
    # ============================================================


    global brush, valve, movement, linmotor, front_distance_sensor, back_distance_sensor, temperature_sensor
    movement = Movement(
        stepper_right_pins=(pins.STEP_STEPPER_RIGHT, pins.DIR_STEPPER_RIGHT),
        stepper_left_pins=(pins.STEP_STEPPER_LEFT, pins.DIR_STEPPER_LEFT), socketio=socketio
    )

    # --- Linearmotor ---
    linmotor = Linmotor(pins.LINMOTOR_PIN_ausfahren, pins.LINMOTOR_PIN_einfahren)

    # --- Wasser-Ventil ---
    valve = Valve(pins.VALVE_PIN, socketio)

    # --- Walze (Bürste) ---
    brush = Brush(pins.BRUSH_PIN, socketio)


    # ============================================================
    # 🔹 Sensoren (Inputs)
    # ============================================================

    # --- Infrarot-Abstandssensoren ---
    front_distance_sensor = E18DN80NK(pins.INFRARED_SENSOR_FRONT_PIN)
    back_distance_sensor = E18DN80NK(pins.INFRARED_SENSOR_BACK_PIN)

    # --- Temperatur-Sensor ---
    temperature_sensor = MLX90614()


    # ============================================================
    # 🔹 Übersicht aller Hardware-Objekte
    # ============================================================

    hardware = {
        "movement": movement,
        "linmotor": linmotor,
        "valve": valve,
        "brush": brush,
        "sensors": {
            "front_distance": front_distance_sensor,
            "back_distance": back_distance_sensor,
            "temperature": temperature_sensor,
        },
    }
