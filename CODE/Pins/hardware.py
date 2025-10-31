import Pins.pins as pins
from gpiozero import LED
from sensors.Distance.Infrared import E18DN80NK
from sensors.Temperature.MLX90614 import MLX90614
from actors.valve import Valve
from actors.brush import Brush
from actors.stepper import SchrittmotorTB6600
from actors.linmotor import Linmotor

# ----Output----

# Stepper init
stepper_left = SchrittmotorTB6600(step_pin=pins.STEP_STEPPER_Left, dir_pin=pins.DIR_STEPPER_Left, step_delay=0.001)
stepper_right = SchrittmotorTB6600(step_pin=pins.STEP_STEPPER_Right, dir_pin=pins.DIR_STEPPER_Right, step_delay=0.001)

# Actor init
linmotor = Linmotor(pins.linmotor_pin)  # Linearmotor



valve = Valve(pins.valve_pin)  # Wasser
brush = Brush(pins.brush_pin)   # Walze



# ----Input----
# Sensoren initialisieren

# Abstandssensorobjekt
distance_sensor = E18DN80NK(pins.infrared_sensor_pin)

# Temperatursensorobjekt
temperature_sensor = MLX90614()