from gpiozero import InputDevice
import time

class E18DN80NK:
    """
    Klasse zur Ansteuerung eines E18-DN80NK IR-Näherungssensors
    über den Raspberry Pi mit gpiozero.
    """

    def __init__(self, pin: int, pull_up: bool = True):
        """
        Initialisiert den Sensor.
        :param pin: GPIO-Pin-Nummer (BCM)
        :param pull_up: True, wenn interner Pull-up genutzt werden soll
        """
        self.sensor = InputDevice(pin, pull_up=pull_up)

    def is_safe(self) -> bool:
        """True, wenn Fläche erkannt (kein Absturzrisiko)"""
        return self.sensor.value == 1

    def is_danger(self) -> bool:
        """True, wenn Absturzgefahr erkannt"""
        return self.sensor.value == 0


# Beispielverwendung
# if __name__ == "__main__":
#     sensor = E18DN80NK(pin=23)
#     while True:
#         if sensor.is_safe():
#             print("Sicher: Fläche erkannt")
#         else:
#             print("Gefahr: Kein Untergrund erkannt!")
#         time.sleep(0.5)



