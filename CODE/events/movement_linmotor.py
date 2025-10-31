from Pins.hardware import linmotor

def register_linmotor_events(socketio):
    @socketio.on("motor_control")
    def handle_walze(data):
        action = data['action']
        linmotor.on() if action == "on" else linmotor.off()
        print(f"Linmotor -> {action}")
