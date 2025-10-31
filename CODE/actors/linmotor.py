from gpiozero import LED

class Linmotor:
    def __init__(self, pin):
        self.pin = pin
        self.output = LED(pin)  # LED steht für einfachen Digital-Output !!!
        self.output.off()
        self.is_open = False
        print(f"Linearmotor auf Pin {self.pin} initialisiert.")

    def on(self):
        self.output.on()
        self.is_open = True
        print(f"Linearmotor eingeschaltet.")

    def off(self):
        self.output.off()
        self.is_open = False
        print(f"Linearmotor ausgeschaltet.")

    def is_on(self):
        return self.is_open

    def cleanup(self):
        self.output.close()
        print(f"Linearmotor freigegeben.")