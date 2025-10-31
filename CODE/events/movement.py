from flask import request
from Pins.hardware import distance_sensor, stepper_left, stepper_right

def register_led_events(socketio):
    @socketio.on("led_control")
    def handle_led(data):
        led_id = data['led']
        action = data['action']

        if distance_sensor.is_danger():
            if led_id == "1" and action == "on": #vor
                print("⚠️ LED-Aktion abgebrochen: Absturzgefahr erkannt!")
            if led_id == "2": #zurück
                if action == "on":
                    stepper_left.start(direction="ccw")
                    stepper_right.start(direction="ccw")
                else:
                    stepper_left.stop()
                    stepper_right.stop()

            if led_id == "3": #drehung links
                if action == "on":
                    stepper_left.start(direction="ccw")
                    stepper_right.start(direction="cw")
                else:
                    stepper_left.stop()
                    stepper_right.stop()
                    
            if led_id == "4": #drehung rechts
                if action == "on":
                    stepper_left.start(direction="ccw")
                    stepper_right.start(direction="cw")
                else:
                    stepper_left.stop()
                    stepper_right.stop()
            return  # Keine LED-Aktion bei Gefahr

        else:
            if led_id == "1": #vor
                if action == "on":
                    stepper_left.start(direction="cw")
                    stepper_right.start(direction="cw")
                else:
                    stepper_left.stop()
                    stepper_right.stop()

            if led_id == "2": #zurück
                if action == "on":
                    stepper_left.start(direction="ccw")
                    stepper_right.start(direction="ccw")
                else:
                    stepper_left.stop()
                    stepper_right.stop()

            if led_id == "3": #drehung links
                if action == "on":
                    stepper_left.start(direction="ccw")
                    stepper_right.start(direction="cw")
                else:
                    stepper_left.stop()
                    stepper_right.stop()
                    
            if led_id == "4": #drehung rechts
                if action == "on":
                    stepper_left.start(direction="ccw")
                    stepper_right.start(direction="cw")
                else:
                    stepper_left.stop()
                    stepper_right.stop()

        # print(f"LED {led_id} {'eingeschaltet' if action == 'on' else 'ausgeschaltet'}")


    @socketio.on('connect')
    def handle_connect():
        print(f"✅ Verbunden: {request.remote_addr}")

    @socketio.on('disconnect')
    def handle_disconnect():
        print(f"❌ Verbindung getrennt: {request.remote_addr}")
