from hardware import objects

def register_linmotor_events(socketio):
    @socketio.on("motor_control")
    def handle_walze(data):
        action = data['action']
        objects.linmotor.on() if action == "on" else objects.linmotor.off()
        print(f"Linmotor -> {action}")
