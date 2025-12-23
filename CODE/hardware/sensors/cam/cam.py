from picamera2 import Picamera2
import cv2
import time

picam2 = None
camera_available = False


def init_camera():
    global picam2, camera_available

    try:
        picam2 = Picamera2()
        config = picam2.create_preview_configuration(
            main={"format": "RGB888", "size": (640, 480)}
        )
        picam2.configure(config)
        picam2.start()
        time.sleep(2)

        camera_available = True
        print("📷 Kamera erfolgreich initialisiert")

    except Exception as e:
        picam2 = None
        camera_available = False
        print(f"⚠️ Keine Kamera gefunden: {e}")


def gen_frames():
    """
    Generator für MJPEG-Stream.
    Funktioniert auch, wenn keine Kamera vorhanden ist.
    """

    # Lazy Init → Kamera erst beim ersten Zugriff starten
    if not camera_available:
        init_camera()

    if not camera_available:
        # Kein Kamera-Stream → leere Antwort oder Platzhalter
        while True:
            time.sleep(1)
            yield b''

    while True:
        frame = picam2.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        frame_bytes = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n'
        )
