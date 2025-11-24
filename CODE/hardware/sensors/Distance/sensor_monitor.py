from threading import Thread                  # Import für parallele Threads
from hardware import objects  # Hardware-Sensoren importieren
import time                                   # Zeitfunktionen (sleep)
from hardware import objects                 # Roboter-Bewegung importieren

# ============================================================
# Globale Steuerungsvariablen
# ============================================================

stop_thread = False            # Flag, um den Monitor-Thread sauber zu stoppen
sensor_block_forward = False   # Speichert, ob der Vorwärtsweg blockiert ist
sensor_block_backward = False  # Speichert, ob der Rückwärtsweg blockiert ist

# ============================================================
# Funktion: Sensor-Monitor starten
# ============================================================

def start_sensor_monitor():
    """
    Startet einen Hintergrund-Thread, der kontinuierlich die
    Abstandssensoren überprüft und den Roboter bei Gefahr stoppt.
    """
    """Startet den Hintergrundthread zur Sensorüberwachung."""
    global thread
    thread = Thread(target=monitor, daemon=True)
    thread.start()

    # ============================================================
    # Monitor-Funktion (läuft im Thread)
    # ============================================================
def monitor():
    global stop_thread, sensor_block_forward, sensor_block_backward

    while not stop_thread:  # Endlosschleife, läuft bis stop_thread = True
        try:
            # Prüfen, ob Fall erkannt wurde
            sensor_block_forward = objects.front_distance_sensor.is_danger()
            sensor_block_backward = objects.back_distance_sensor.is_danger()

            # Aktuellen Bewegungsstatus des Roboters abfragen
            movement_status = objects.movement.get_movement()

            # Wenn Fallerkennung UND Roboter in diese Richtung fährt → stoppen
            if (sensor_block_forward and movement_status == "moving_forward") \
                or (sensor_block_backward and movement_status == "moving_backward"):
                objects.movement.stop()  # Roboter sofort stoppen

            time.sleep(0.1)  # Kurze Pause, um CPU nicht zu blockieren
        except Exception as e:
            print(f"[SensorMonitor] Fehler: {e}")
            break
    

def stop_sensor_monitor():
    """Beendet den Sensorüberwachungs-Thread kontrolliert."""
    global stop_thread, thread
    stop_thread = True
    if thread and thread.is_alive():
        thread.join(timeout=1.0)
    print("✅ Sensor-Monitor gestoppt.")