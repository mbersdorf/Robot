from Pins.hardware import brush

def register_walze_events(socketio):
    @socketio.on("walze_control")
    def handle_walze(data):
        action = data['action']
        brush.on() if action == "on" else brush.off()
        print(f"LED Walze -> {action}")
