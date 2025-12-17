from gpiozero import LED

class Valve:
    def __init__(self, pin, socketio):
        self.pin = pin
        self.output = LED(pin)  # LED steht für einfachen Digital-Output !!!
        self.is_open = False
        self.socketio = socketio
        print(f"Ventil auf Pin {self.pin} initialisiert.")

    def on(self):
        self.output.on()
        self.is_open = True
        self.socketio.emit('valve_status', {'valvestatus': 'AN'})  # Status über SocketIO senden
        print(f"Ventil eingeschaltet.")

    def off(self):
        self.output.off()
        self.is_open = False
        self.socketio.emit('valve_status', {'valvestatus': 'AUS'})  # Status über SocketIO senden
        print(f"Ventil ausgeschaltet.")

    def is_on(self):
        return self.is_open

    def cleanup(self):
        self.output.close()
        print(f"Ventil freigegeben.")
