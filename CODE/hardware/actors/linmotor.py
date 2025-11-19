from gpiozero import LED  # Import der gpiozero-Klasse LED für digitale Ausgänge (einfacher Digital-Output)

class Linmotor:
    """
    Klasse zur Steuerung des Linearmotors.
    Kapselt die Hardwareansteuerung über einen digitalen Ausgang.
    """

    def __init__(self, pin_ausfahren, pin_einfahren, socketio):
        """
        Initialisiert den Linearmotor.

        Args:
            pin (int): GPIO-Pin, an dem der Linearmotor angeschlossen ist.
            socketio: SocketIO-Objekt für Statusmeldungen
        """
        self.pin_ausfahren = pin_ausfahren                      # Speichert den zugewiesenen GPIO-Pin //ausfahren
        self.pin_einfahren = pin_einfahren                      # Speichert den zugewiesenen GPIO-Pin //einfahren
        self.socketio = socketio                                # SocketIO-Objekt für Statusmeldungen 
        self.output_ausfahren = LED(pin_ausfahren)              # Initialisiert den digitalen Output über gpiozero.LED
        self.output_einfahren = LED(pin_einfahren)              # Hinweis: LED wird hier als einfacher Digital-Output genutzt

        #Initialer Zustand: Motor aus                                    
        self.output_ausfahren.off()                   
        self.output_einfahren.off()
        #self.is_open = False                # Zustand des Motors: False = aus, True = an
        # print(f"Linearmotor auf Pin {self.pin} initialisiert.")  # Info-Ausgabe beim Start
        

    def ausfahren(self):
        """
        Schaltet den Linearmotor ein.
        """
        self.output_ausfahren.on()                    # Setzt den GPIO-Pin auf HIGH
        self.output_einfahren.off()
        #self.is_open = True                 # Aktualisiert den internen Status
        self.socketio.emit('lin_status', {'linstatus': 'Ausfahren'})  # Status über SocketIO senden
        print(f"Linearmotor ausfahren.")  # Ausgabe zur Statuskontrolle


    def einfahren(self):
        """
        Schaltet den Linearmotor aus.
        """
        self.output_ausfahren.off()                   # Setzt den GPIO-Pin auf LOW
        self.output_einfahren.on()
        #self.is_open = False                # Aktualisiert den internen Status
        self.socketio.emit('lin_status', {'linstatus': 'Einfahren'})  # Status über SocketIO senden
        print(f"Linearmotor einfahren.")  # Ausgabe zur Statuskontrolle

    def stop(self):
        """
        Stoppt den Linearmotor.
        """
        self.output_ausfahren.off()                   # Setzt den GPIO-Pin auf LOW
        self.output_einfahren.off()
        #self.is_open = False                # Aktualisiert den internen Status
        self.socketio.emit('lin_status', {'linstatus': 'Stopp'})  # Status über SocketIO senden
        print(f"Linearmotor gestoppt.")  # Ausgabe zur Statuskontrolle


    # def is_on(self):
    #     """
    #     Prüft, ob der Linearmotor eingeschaltet ist.

    #     Returns:
    #         bool: True, wenn Motor eingeschaltet, sonst False
    #     """
    #     return self.is_open                 # Gibt den aktuellen Status zurück
    

    def cleanup(self):
        """
        Gibt die Hardware frei, schließt den GPIO-Pin.
        Sollte aufgerufen werden, wenn das Programm endet.
        """
        self.output_einfahren.close()                 # Freigabe des Pins über gpiozero
        self.output_ausfahren.close()
        print(f"Linearmotor freigegeben.") # Info-Ausgabe
