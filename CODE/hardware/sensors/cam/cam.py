from picamera2 import Picamera2  # Import der Picamera2-Bibliothek für Raspberry Pi Kameras
import cv2                        # OpenCV für Bildverarbeitung
import time                       # Zeitfunktionen für Sleep

# ============================================================
# Kamera-Setup
# ============================================================

# Kamera-Objekt erstellen
picam2 = Picamera2()

# Konfiguration der Kamera
# - RGB888 Format (Farbformat)
# - 640x480 Pixel Auflösung
config = picam2.create_preview_configuration(
    main={"format": "RGB888", "size": (640, 480)}
)
picam2.configure(config)  # Konfiguration auf Kamera anwenden

picam2.start()            # Kamera starten
time.sleep(2)             # Kurze Wartezeit, damit die Kamera "aufwärmt"

# ============================================================
# Frame-Generator
# ============================================================

def gen_frames():
    """
    Generator-Funktion für JPEG-Frames der Kamera.

    Yield:
        bytes: JPEG-codiertes Bild, geeignet für Streaming (z.B. Flask Video Feed)
    """
    while True:
        # Bild als NumPy-Array von der Kamera erfassen
        frame = picam2.capture_array()

        # Array in JPEG konvertieren
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue  # Fehlerhafte Frames überspringen

        # Byte-Daten erzeugen
        frame_bytes = buffer.tobytes()

        # Yield für Flask Streaming:
        # multipart/x-mixed-replace Format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
