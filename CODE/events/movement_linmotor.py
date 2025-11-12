from hardware import objects

def register_linmotor_events(socketio):
    @socketio.on("motor_control")
    def handle_walze(data):
        action = data['action']
        objects.linmotor.ausfahren() if action == "on" else objects.linmotor.einfahren()
        print(f"Linmotor -> {action}")
