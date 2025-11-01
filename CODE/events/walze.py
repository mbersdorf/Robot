from hardware import objects

def register_walze_events(socketio):
    @socketio.on("walze_control")
    def handle_walze(data):
        action = data['action']
        objects.brush.on() if action == "on" else objects.brush.off()
        print(f"LED Walze -> {action}")
