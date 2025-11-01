from gpiozero import LED  # Import der gpiozero-Klasse LED für digitale Ausgänge (einfacher Digital-Output)

class Brush:
    """
    Klasse für die Steuerung der Walze (Brush).
    Kapselt die Hardwareansteuerung über einen digitalen Output.
    """

    def __init__(self, pin, socketio):
        """
        Initialisiert die Walze.

        Args:
            pin (int): GPIO-Pin, an dem die Walze angeschlossen ist.
        """
        self.pin = pin                      # Speichert den zugewiesenen GPIO-Pin
        self.output = LED(pin)              # Initialisiert den digitalen Output über gpiozero.LED
                                            # Hinweis: LED wird hier als einfacher Digital-Output genutzt
        self.is_open = False                # Zustand der Walze: False = aus, True = an
        self.socketio = socketio            # SocketIO-Objekt für Statusmeldungen
        print(f"Walze auf Pin {self.pin} initialisiert.")  # Info-Ausgabe beim Start


    def on(self):
        """
        Schaltet die Walze ein.
        """
        self.output.on()                    # Setzt den GPIO-Pin auf HIGH
        self.is_open = True                 # Aktualisiert den internen Status
        print(f"Walze eingeschaltet.")      # Ausgabe zur Statuskontrolle
        self.socketio.emit('brush_status', {'brushstatus': 'AN'})  # Status über SocketIO senden



    def off(self):
        """
        Schaltet die Walze aus.
        """
        self.output.off()                   # Setzt den GPIO-Pin auf LOW
        self.is_open = False                # Aktualisiert den internen Status
        print(f"Walze ausgeschaltet.")      # Ausgabe zur Statuskontrolle
        self.socketio.emit('brush_status', {'brushstatus': 'Aus'})  # Status über SocketIO senden


    def is_on(self):
        """
        Prüft, ob die Walze eingeschaltet ist.

        Returns:
            bool: True, wenn Walze eingeschaltet, sonst False
        """
        return self.is_open                 # Gibt den aktuellen Status zurück
    

    def cleanup(self):
        """
        Gibt die Hardware frei, schließt den GPIO-Pin.
        Sollte aufgerufen werden, wenn das Programm endet.
        """
        self.output.close()                 # Freigabe des Pins über gpiozero
        print(f"Walze freigegeben.")       # Info-Ausgabe
