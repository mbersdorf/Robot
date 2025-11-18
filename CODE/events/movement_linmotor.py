from hardware import objects

def register_linmotor_events(socketio):
    @socketio.on("Lin_control")
    def handle_walze(data):
        action = data['action']
        direction = data['direction']

        if action =="off":
            objects.linmotor.stop()
        else:
            if direction == "out":
                objects.linmotor.ausfahren()
            elif direction == "in":
                objects.linmotor.einfahren()

