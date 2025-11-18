from flask import request
from threading import Thread
from hardware import objects



def register_movement_button_events(socketio):
    @socketio.on("led_control")
    def handle_led(data):
        led_id = data['led']
        action = data['action']

        handle_movement(led_id, action)

    @socketio.on("set_speed")
    def handle_set_speed(data):
        speed_percent = int(data['speed'])
        
        min_delay = 0.0001   # 100%
        max_delay = 0.001     # 0%
        # lineare Interpolation, invertiert
        step_delay = max_delay - (speed_percent / 100) * (max_delay - min_delay)

        objects.movement.set_speed(step_delay)
        print(f"Setze Geschwindigkeit auf {speed_percent}% -> step_delay: {step_delay:.6f}s")


    @socketio.on('connect')
    def handle_connect():
        print(f"✅ Verbunden: {request.remote_addr}")


    @socketio.on('disconnect')
    def handle_disconnect():
        print(f"❌ Verbindung getrennt: {request.remote_addr}")


# Logik zur Handhabung der Bewegung

    def handle_movement(led_id, action):
        front_blocked = objects.front_distance_sensor.is_danger()
        back_blocked = objects.back_distance_sensor.is_danger()

        # Mappe Bewegungsrichtungen auf Funktionen
        actions = {
            "1": objects.movement.move_forward,
            "2": objects.movement.move_backward,
            "3": objects.movement.turn_right,
            "4": objects.movement.turn_left
        }

        # Standard: wenn "off" -> stop
        if action == "off":
            objects.movement.stop()
            return

        # Blockade-Logik
        if led_id == "1" and front_blocked:
            print("🚫 Bewegung nach vorne blockiert (Frontsensor aktiv)")
            objects.movement.stop()
            return
        if led_id == "2" and back_blocked:
            print("🚫 Bewegung nach hinten blockiert (Rücksensor aktiv)")
            objects.movement.stop()
            return

        # Drehungen immer erlaubt
        if led_id in ("3", "4") or (led_id == "1" and not front_blocked) or (led_id == "2" and not back_blocked):
            action_func = actions.get(led_id)
            if action_func:
                action_func()
            else:
                objects.movement.stop()

