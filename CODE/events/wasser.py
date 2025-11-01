from hardware import objects

def register_wasser_events(socketio):
    @socketio.on("wasser_control")
    def handle_wasser(data):
        action = data['action']
        objects.valve.on() if action == "on" else objects.valve.off()
        print(f"LED Wasser -> {action}")
