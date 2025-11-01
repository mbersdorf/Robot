import smbus2 as smbus
import time
 
class MLX90614():
 
    MLX90614_TA    = 0x06
    MLX90614_TOBJ1 = 0x07
 
    def __init__(self, address = 0x5a, bus = 1):
        self.address = address
        self.bus = smbus.SMBus(bus)
 
    def readValue(self, registerAddress):
        error = None
        for i in range(3):
            try:
                return self.bus.read_word_data(self.address, registerAddress)
            except IOError as e:
                error = e
                time.sleep(0.1)
        if error is not None:
            raise error
        raise IOError("I2C read failed after 3 attempts")
 
    def valueToCelcius(self, value):
        return -273.15 + (value * 0.02)
 
    def readObjectTemperature(self):
        value = self.readValue(self.MLX90614_TOBJ1)
        return self.valueToCelcius(value)
 
    def readAmbientTemperature(self):
        value = self.readValue(self.MLX90614_TA)
        return self.valueToCelcius(value)
    


# if __name__ == "__main__":
#     sensor = MLX90614()
#     while True:
#         obj_temp = sensor.readObjectTemperature()
#         amb_temp = sensor.readAmbientTemperature()
#         print(f"Object Temperature: {obj_temp:.2f} °C, Ambient Temperature: {amb_temp:.2f} °C")
#         time.sleep(1)