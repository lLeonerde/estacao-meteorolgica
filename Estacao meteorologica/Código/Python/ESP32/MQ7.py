from machine import Pin, ADC
import math
class MQ7():
    def __init__(self, pin, volt = 3.3, atten = 4096):
        self.atten = atten
        self.volt = volt
        self.max = 150
        co = ADC(Pin(pin))
        co.atten(ADC.ATTN_11DB)
        self.co = co
        

   
    def read(self):
        co = self.co.read()
        sensorVolt = co/self.atten * self.volt
        ppm = self.max * sensorVolt / self.volt
        
        return ppm
    
   