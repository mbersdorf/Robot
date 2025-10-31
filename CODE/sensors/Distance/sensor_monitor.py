import time
from threading import Thread
# from input.Distance.Infrared import sensor
from Pins.hardware import distance_sensor, stepper_left, stepper_right

stop_thread = False

def start_sensor_monitor(socketio):

    def monitor():
        global stop_thread
        while not stop_thread:
            try:
                # if distance_sensor.is_danger(): # evtl und bewegung nach vorne??
                    # socketio.emit("led_feedback", {"status": "blocked"})
                # else:
                    # socketio.emit("led_feedback", {"status": "active"})
                    # stepper_left.stop()
                    # stepper_right.stop()
                    
                    # if socketio:
                    # socketio.emit("led_control", {"led": "1", "action": "off"})
                        # print("block vorward") # test
                        #print("⚠️ Absturzgefahr erkannt! Bewegung nach vorne gestoppt.")
                        # socketio.emit("led_control", {"led": "2", "action": "off"})
                        # socketio.emit("led_control", {"led": "3", "action": "off"})
                        # socketio.emit("led_control", {"led": "4", "action": "off"})
                    time.sleep(0.3)
            except Exception as e:
                break
            time.sleep(0.05)

    thread = Thread(target=monitor, daemon=True)
    thread.start()
