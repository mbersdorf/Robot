from flask import request
from Pins.hardware import front_distance_sensor, back_distance_sensor, movement


def register_movement_button_events(socketio):
    @socketio.on("led_control")
    def handle_led(data):
        led_id = data['led']
        action = data['action']

        handle_movement(led_id, action)   

    @socketio.on('connect')
    def handle_connect():
        print(f"✅ Verbunden: {request.remote_addr}")

    @socketio.on('disconnect')
    def handle_disconnect():
        print(f"❌ Verbindung getrennt: {request.remote_addr}")

    def handle_movement(led_id, action):
        front_blocked = front_distance_sensor.is_danger()
        back_blocked = back_distance_sensor.is_danger()

        # Mappe Bewegungsrichtungen auf Funktionen
        actions = {
            "1": movement.move_forward,
            "2": movement.move_backward,
            "3": movement.turn_left,
            "4": movement.turn_right
        }

        # Standard: wenn "off" -> stop
        if action == "off":
            movement.stop()
            return

        # Blockade-Logik
        if led_id == "1" and front_blocked:
            print("🚫 Bewegung nach vorne blockiert (Frontsensor aktiv)")
            movement.stop()
            return
        if led_id == "2" and back_blocked:
            print("🚫 Bewegung nach hinten blockiert (Rücksensor aktiv)")
            movement.stop()
            return

        # Drehungen immer erlaubt
        if led_id in ("3", "4") or (led_id == "1" and not front_blocked) or (led_id == "2" and not back_blocked):
            action_func = actions.get(led_id)
            if action_func:
                action_func()
            else:
                movement.stop()