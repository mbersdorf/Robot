"""
app.py
-----------------------------------------
Hauptprogramm für den Roboter-Webserver.
Startet Flask + SocketIO, initialisiert Hardware und Threads.
"""

# ============================================================
# 🔹 Imports
# ============================================================

from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import threading
import signal
import sys


# --- Eigene Module ---
from events.init_events import register_all_events, temperature_loop
from hardware.objects import initialize_hardware
from hardware.sensors.Distance.sensor_monitor import stop_sensor_monitor, stop_thread
from hardware.sensors.cam.cam import gen_frames


# ============================================================
# 🔹 Flask- und SocketIO-Setup
# ============================================================

# Flask-App erstellen
app = Flask(__name__)

# SocketIO initialisieren (WebSocket-Kommunikation)
socketio = SocketIO(app)


# ============================================================
# 🔹 Hardware-Initialisierung
# ============================================================

# Erstellt alle Hardwareobjekte (Ventil, Walze, Bewegung, Sensoren, usw.)
# und übergibt das SocketIO-Objekt zur Statuskommunikation.
initialize_hardware(socketio)


# ============================================================
# 🔹 Events registrieren & Hintergrund-Threads starten (Absturzüberwachung, Temperatursensor)
# ============================================================

# Bindet alle WebSocket-Events (z. B. Steuerung der Walze, Ventil usw.)
# aus dem Ordner „events“ an.
register_all_events(socketio)


# ============================================================
# 🔹 Flask-Routen (HTTP)
# ============================================================

@app.route("/")
def index():
    """Startseite (GUI)"""
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    """Liefert kontinuierlichen MJPEG-Stream der Kamera"""
    return Response(
        gen_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# ============================================================
# 🔹 Signal-Handler (sauberes Beenden)
# ============================================================




def signal_handler(sig, frame):
    """Fängt SIGINT/SIGTERM ab und beendet das Programm sauber."""
    global stop_thread
    print("\n🛑 Beende Programm...")

    # Sensor-Thread stoppen
    stop_thread = True
    print("🧵 Sensor-Monitor-Thread gestoppt.")

    # GPIOs sauber freigeben
    try:
        from hardware import objects
        objects.movement.cleanup()
        objects.linmotor.cleanup()  
        objects.brush.cleanup()
        objects.valve.cleanup()
        objects.front_distance_sensor.cleanup()
        objects.back_distance_sensor.cleanup()
        print("🧹 GPIO-Pins freigegeben.")
    except Exception as e:
        print(f"Fehler beim GPIO-Cleanup: {e}")

    # App sicher beenden
    sys.exit(0)


# Registriere Signal-Handler
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


# ============================================================
# 🔹 Programmstart
# ============================================================

if __name__ == "__main__":
    # Starte Flask + SocketIO Server
    # Läuft auf allen Interfaces (0.0.0.0) und Port 5000
    # use_reloader=False verhindert doppelten Start bei Threads
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False,
        allow_unsafe_werkzeug=True
    )
