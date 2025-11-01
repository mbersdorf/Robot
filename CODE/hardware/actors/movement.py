from gpiozero import OutputDevice
from time import sleep
from threading import Thread

# ============================================================
# TB6600 Steppertreiber
# ============================================================

class TB6600:
    """
    Klasse für den Steppertreiber TB6600.
    Steuert einen einzelnen Schrittmotor über STEP, DIR und optional ENABLE.
    """

    def __init__(self, step_pin, dir_pin, enable_pin=None, step_delay=0.001):
        """
        Initialisiert den Steppertreiber.

        Args:
            step_pin (int): GPIO-Pin für STEP
            dir_pin (int): GPIO-Pin für DIR (Richtung)
            enable_pin (int, optional): GPIO-Pin für ENABLE (aktiviert Treiber)
            step_delay (float, optional): Zeit zwischen STEP-Pulsen (kleiner = schneller)
        """
        self.step = OutputDevice(step_pin)             # STEP-Pin als digitaler Ausgang
        self.dir = OutputDevice(dir_pin)               # DIR-Pin als digitaler Ausgang
        self.enable = OutputDevice(enable_pin) if enable_pin is not None else None
        self.step_delay = step_delay                   # Zeit zwischen STEP-Pulsen
        self._running = False                          # Interner Status, ob Motor läuft
        self._thread = None                            # Thread, der Motor-Puls erzeugt


    def _run(self):
        """
        Endlosschleife für STEP-Pulse.
        Läuft in einem separaten Thread.
        """
        while self._running:
            self.step.on()
            sleep(self.step_delay)
            self.step.off()
            sleep(self.step_delay)


    def start(self, direction="cw"):
        """
        Startet den Motor kontinuierlich in angegebener Richtung.

        Args:
            direction (str): 'cw' für clockwise, 'ccw' für counter-clockwise
        """
        if self._running:
            print("Motor läuft bereits.")
            return

        # Richtung setzen
        if direction == "cw":
            self.dir.off()
        else:
            self.dir.on()

        # Treiber aktivieren (TB6600 = aktiv low)
        if self.enable:
            self.enable.off()

        # Motor starten
        self._running = True
        self._thread = Thread(target=self._run, daemon=True)
        self._thread.start()
        print(f"Motor gestartet, Richtung: {direction}")


    def stop(self):
        """
        Stoppt den Motor.
        """
        self._running = False
        if self.enable:
            self.enable.on()  # Treiber deaktivieren
        print("Motor gestoppt.")

    def cleanup(self):
        """
        Räumt GPIOs auf und stoppt Motor.
        """
        self.stop()
        self.step.close()
        self.dir.close()
        if self.enable:
            self.enable.close()
        print("GPIOs freigegeben.")


# ============================================================
# Movement-Klasse für den Roboter
# ============================================================

class Movement:
    """
    Steuerung des Roboter-Antriebs mit zwei Steppermotoren (links/rechts).
    Bietet Bewegungsfunktionen: vorwärts, rückwärts, drehen, stoppen.
    """

    def __init__(self, stepper_right_pins, stepper_left_pins, socketio):
        """
        Initialisiert die beiden Steppermotoren.

        Args:
            stepper_right_pins (tuple): (STEP_PIN, DIR_PIN) für rechten Motor
            stepper_left_pins (tuple): (STEP_PIN, DIR_PIN) für linken Motor
        """
        self.stepper_left = TB6600(*stepper_left_pins)
        self.stepper_right = TB6600(*stepper_right_pins)
        self.state = "stopped"  # interner Status: 'stopped', 'moving_forward', etc.
        self.socketio = socketio

    def move_forward(self):
        """Fährt den Roboter vorwärts."""
        self.stepper_left.start(direction="cw")
        self.stepper_right.start(direction="cw")
        self._set_state("moving_forward")
        self.socketio.emit('movement_status', {'status': 'VORWÄRTS'})  # Status über SocketIO senden

    def move_backward(self):
        """Fährt den Roboter rückwärts."""
        self.stepper_left.start(direction="ccw")
        self.stepper_right.start(direction="ccw")
        self._set_state("moving_backward")
        self.socketio.emit('movement_status', {'status': 'RÜCKWÄRTS'})

    def turn_left(self):
        """Dreht den Roboter nach links."""
        self.stepper_left.start(direction="ccw")
        self.stepper_right.start(direction="cw")
        self._set_state("turning_left")
        self.socketio.emit('movement_status', {'status': 'LINKS DREHEN'})

    def turn_right(self):
        """Dreht den Roboter nach rechts."""
        self.stepper_left.start(direction="cw")
        self.stepper_right.start(direction="ccw")
        self._set_state("turning_right")
        self.socketio.emit('movement_status', {'status': 'RECHTS DREHEN'})

    def stop(self):
        """Stoppt beide Motoren."""
        self.stepper_left.stop()
        self.stepper_right.stop()
        self._set_state("stopped")
        self.socketio.emit('movement_status', {'status': 'STOPP'})  # Status über SocketIO senden

    def _set_state(self, state):
        """
        Aktualisiert den internen Status und gibt ihn aus.

        Args:
            state (str): neuer Bewegungszustand
        """
        self.state = state
        print(f"Movement state: {self.state}")

    def get_movement(self):
        """
        Gibt den aktuellen Bewegungsstatus zurück.

        Returns:
            str: Aktueller Bewegungszustand
        """
        return self.state
    
    def cleanup(self):
        """
        Gibt die Hardware frei, stoppt Motoren.
        """
        self.stepper_left.cleanup()
        self.stepper_right.cleanup()
        print("Movement GPIOs freigegeben.")
    

