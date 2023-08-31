from machine import I2C, Pin 
from mpl3115a2 import MPL3115A2 
from time import sleep 


i2c = I2C(1, sda = Pin(21), scl = Pin(22), freq=10000) 

def altimetro(): 
    mpl = MPL3115A2(i2c, mode=MPL3115A2.ALTITUDE)#modo altímetro 
    altitude = mpl.altitude() 
    return altitude  

def barometro(): 
    mpl = MPL3115A2(i2c, mode=MPL3115A2.PRESSURE)#modo altímetro 
    pressao = mpl.pressure() 
    temperatura = mpl.temperature() 
    return pressao 


while True: 
    print(f'Altitude: {altimetro():.2f}m') 
    print(f'Pressão atmosférica: {barometro()}pa') 
    print('\n') 
    sleep(0.5) 

 