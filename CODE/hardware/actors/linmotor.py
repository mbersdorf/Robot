from gpiozero import LED  # Import der gpiozero-Klasse LED für digitale Ausgänge (einfacher Digital-Output)

class Linmotor:
    """
    Klasse zur Steuerung des Linearmotors.
    Kapselt die Hardwareansteuerung über einen digitalen Ausgang.
    """

    def __init__(self, pin):
        """
        Initialisiert den Linearmotor.

        Args:
            pin (int): GPIO-Pin, an dem der Linearmotor angeschlossen ist.
        """
        self.pin = pin                      # Speichert den zugewiesenen GPIO-Pin
        self.output = LED(pin)              # Initialisiert den digitalen Output über gpiozero.LED
                                            # Hinweis: LED wird hier als einfacher Digital-Output genutzt
        self.output.off()                   # Motor standardmäßig aus
        self.is_open = False                # Zustand des Motors: False = aus, True = an
        print(f"Linearmotor auf Pin {self.pin} initialisiert.")  # Info-Ausgabe beim Start
        

    def on(self):
        """
        Schaltet den Linearmotor ein.
        """
        self.output.on()                    # Setzt den GPIO-Pin auf HIGH
        self.is_open = True                 # Aktualisiert den internen Status
        print(f"Linearmotor eingeschaltet.")  # Ausgabe zur Statuskontrolle


    def off(self):
        """
        Schaltet den Linearmotor aus.
        """
        self.output.off()                   # Setzt den GPIO-Pin auf LOW
        self.is_open = False                # Aktualisiert den internen Status
        print(f"Linearmotor ausgeschaltet.")  # Ausgabe zur Statuskontrolle


    def is_on(self):
        """
        Prüft, ob der Linearmotor eingeschaltet ist.

        Returns:
            bool: True, wenn Motor eingeschaltet, sonst False
        """
        return self.is_open                 # Gibt den aktuellen Status zurück
    

    def cleanup(self):
        """
        Gibt die Hardware frei, schließt den GPIO-Pin.
        Sollte aufgerufen werden, wenn das Programm endet.
        """
        self.output.close()                 # Freigabe des Pins über gpiozero
        print(f"Linearmotor freigegeben.") # Info-Ausgabe
