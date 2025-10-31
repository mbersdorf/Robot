from threading import Thread
from Pins.hardware import front_distance_sensor, back_distance_sensor
import time
from Pins.hardware import movement

stop_thread = False
sensor_block_forward = False
sensor_block_backward = False


def start_sensor_monitor(socketio):
    def monitor():
        global stop_thread, sensor_block
        while not stop_thread:
            sensor_block_forward = front_distance_sensor.is_danger()
            sensor_block_backward = back_distance_sensor.is_danger()
            movement_status = movement.get_movement()
            if sensor_block_forward and movement_status == "moving_forward" or sensor_block_backward and movement_status == "moving_backward":
                movement.stop()
            time.sleep(0.05)

    thread = Thread(target=monitor, daemon=True)
    thread.start()

