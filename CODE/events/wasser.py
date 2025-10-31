from Pins.hardware import valve

def register_wasser_events(socketio):
    @socketio.on("wasser_control")
    def handle_wasser(data):
        action = data['action']
        valve.on() if action == "on" else valve.off()
        print(f"LED Wasser -> {action}")
