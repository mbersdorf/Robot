from gpiozero import LED

class Brush:
    def __init__(self, pin):
        self.pin = pin
        self.output = LED(pin)  # LED steht für einfachen Digital-Output !!!
        self.is_open = False
        print(f"Walze auf Pin {self.pin} initialisiert.")

    def on(self):
        self.output.on()
        self.is_open = True
        print(f"Walze eingeschaltet.")

    def off(self):
        self.output.off()
        self.is_open = False
        print(f"Walze ausgeschaltet.")

    def is_on(self):
        return self.is_open

    def cleanup(self):
        self.output.close()
        print(f"Walze freigegeben.")
