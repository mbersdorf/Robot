from flask import Flask, render_template, Response
from flask_socketio import SocketIO
from events.init_events import register_all_events, temperature_loop
import threading
from sensors.Distance.sensor_monitor import start_sensor_monitor, stop_thread
import signal
import sys
from sensors.cam.cam import gen_frames

app = Flask(__name__)
socketio = SocketIO(app)

# WebSocket-Events auslagern
register_all_events(socketio)

sensor_thread = start_sensor_monitor(socketio)

# Route für die Startseite
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



# Signalhandler für sauberes Beenden
def signal_handler(sig, frame):
    global stop_thread
    print("Beende Programm...")
    stop_thread = True          # Thread stoppen
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    # Starte den Temperatur-Thread
    temp_thread = threading.Thread(target=temperature_loop, args=(socketio,), daemon=True)
    temp_thread.start()

    socketio.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=False)
