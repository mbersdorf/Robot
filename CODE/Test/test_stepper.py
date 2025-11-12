from gpiozero import OutputDevice
from time import sleep
from threading import Thread
# import Pins.pins as pins

class SchrittmotorTB6600:
    def __init__(self, step_pin, dir_pin, step_delay=0.001, enable_pin=None):
        """
        step_pin: GPIO-Pin für STEP
        dir_pin:  GPIO-Pin für DIR (Richtung)
        enable_pin: Optionaler GPIO-Pin für ENABLE (aktiviert Treiber)
        step_delay: Zeit zwischen den STEP-Pulsen (kleiner = schneller)
        """
        self.step = OutputDevice(step_pin)
        self.dir = OutputDevice(dir_pin)
        self.enable = OutputDevice(enable_pin) if enable_pin is not None else None
        self.step_delay = step_delay                  # Zeit zwischen STEP-Pulsen
        self._running = False
        self._thread = None

    def _run(self):
        while self._running:
            self.step.on()
            sleep(self.step_delay)
            self.step.off()
            sleep(self.step_delay)

    def start(self, direction="cw"):
        """Startet den Motor kontinuierlich in angegebener Richtung ('cw' oder 'ccw')"""
        if self._running:
            print("Motor läuft bereits.")
            return

        # Richtung setzen
        if direction == "cw":
            self.dir.off()
        else:
            self.dir.on()

        # Treiber aktivieren
        if self.enable:
            self.enable.off()  # aktiv low beim TB6600

        self._running = True
        self._thread = Thread(target=self._run, daemon=True)
        self._thread.start()
        print(f"Motor gestartet, Richtung: {direction}")

    def stop(self):
        """Stoppt den Motor"""
        self._running = False
        if self.enable:
            self.enable.on()  # deaktivieren
        print("Motor gestoppt.")

    def cleanup(self):
        """Räumt GPIOs auf"""
        self.stop()
        self.step.close()
        self.dir.close()
        if self.enable:
            self.enable.close()
        print("GPIOs freigegeben.")

    def set_speed(self, step_delay):
        """Ändert die Schrittverzögerung während der Laufzeit"""
        self.step_delay = step_delay
        print(f"Neue step_delay: {self.step_delay}")


if __name__ == "__main__":
    import time
    motor = SchrittmotorTB6600(step_pin=27, dir_pin=17) #step_delay=0.001

    # Motor rechts herum starten
    motor.start(direction="cw")
    time.sleep(2)
    motor.set_speed(0.003)
    time.sleep(2)
    motor.set_speed(0.002)
    time.sleep(2)
    motor.set_speed(0.001)
    time.sleep(2)
    motor.set_speed(0.00005)
    time.sleep(2)
    


    motor.stop()
    motor.cleanup()
