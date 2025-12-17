"""
pins.py
Zentrale Definition aller GPIO-Pins und I2C-Adressen
für digitale Ein- und Ausgänge des Roboters.
"""
# ! Wichtig !
# GPIO-Pin 21 wird von anderem Programm (shutdown.py) verwendet
# nicht hier definieren oder nutzen!

# ============================================================
# 🔹 Digitale Eingänge
# ============================================================

INFRARED_SENSOR_FRONT_PIN = 22
INFRARED_SENSOR_BACK_PIN = 26


# ============================================================
# 🔹 Digitale Ausgänge
# ============================================================

# --- Stepper Motor Contorller Left ---
DIR_STEPPER_LEFT = 17
STEP_STEPPER_LEFT = 27

# --- Stepper Motor Controller Right ---
DIR_STEPPER_RIGHT = 23
STEP_STEPPER_RIGHT = 24

# --- Wassersteuerung ---
VALVE_PIN = 6

# --- Walze (Brush) ---
BRUSH_PIN = 5

# --- Linearmotor ---
LINMOTOR_PIN_ausfahren = 16
LINMOTOR_PIN_einfahren = 25

# --- LED Status ---
LED_PIN = 20

# ============================================================
# 🔹 Analoge Eingänge / I2C-Adressen
# ============================================================

# MLX90614 Infrarot-Temperatursensor
# (Default-Adresse: 0x5A)
# MLX90614_ADDRESS = 0x5A

# Register (optional, falls du direkt ausliest)
# MLX90614_TA = 0x06      # Umgebungstemperatur
# MLX90614_TOBJ1 = 0x07   # Objekttemperatur
