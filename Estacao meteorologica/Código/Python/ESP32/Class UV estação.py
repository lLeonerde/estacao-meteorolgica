from machine import ADC, Pin
from time import sleep

class uv_sensor:
    def __init__(self,pin):
        self.adc = ADC(Pin(pin))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)
        
    def ler_valor(self):
        return self.adc.read()

    def converter_val_uv(self):
        val_sensorV = (self.adc.read() * 3.3)/4095 #valor em volts
        valor_sensorMV = round(((self.adc.read() * 3.3)/4095) * 1000,4)
        return val_sensorV,valor_sensorMV
    
    def mostrarUV_index(self):
        valor_sensorMV = round(((self.adc.read() * 3.3)/4095) * 1000,4)
        if valor_sensorMV <50:
            UV_index = 0
        elif valor_sensorMV <227:
            UV_index = 1
        elif valor_sensorMV <318:
            UV_index = 2
        elif valor_sensorMV <408:
            UV_index = 3
        elif valor_sensorMV <503:
            UV_index = 4
        elif valor_sensorMV <606:
            UV_index = 5
        elif valor_sensorMV <696:
            UV_index = 6
        elif valor_sensorMV <795:
            UV_index = 7
        elif valor_sensorMV <881:
            UV_index = 8
        elif valor_sensorMV <976:
            UV_index = 9
        elif valor_sensorMV <1079:
            UV_index = 10
        else:
            UV_index = 11
        return UV_index