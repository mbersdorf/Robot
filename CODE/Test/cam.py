from flask import Flask, Response
import cv2
from picamera2 import Picamera2
from threading import Thread
import time

app = Flask(__name__)

# --- Kamera Setup ---
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
picam2.configure(config)
picam2.start()
time.sleep(2)  # Kamera aufwärmen

def gen_frames():
    """Generator, der JPEG-Frames von der Kamera liefert"""
    while True:
        frame = picam2.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video-Feed Route"""
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    """Startseite"""
    return "<h1>Pi Camera Streaming</h1><img src='/video_feed' />"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

