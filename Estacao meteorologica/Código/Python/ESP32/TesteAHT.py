import time, machine
import aht
from time import sleep

# Example SCL pin and SDA pin for WEMOS D1 mini Lite
i2c = machine.I2C(1,scl=machine.Pin(22), sda=machine.Pin(21),freq=10000)
sensor = aht.AHT2x(i2c, crc=True)
while True:
# To print one of measures:
    print("Humidade: {:.2f}".format(sensor.humidity))
    print("Temperatura: {:.2f}".format(sensor.temperature))
    print('\n')
    sleep(0.5)
    

