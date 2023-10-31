from machine import ADC, Pin
from utime import sleep
import _thread


#Inicio class rosa dos ventos
class Rosa_dos_ventos:
    def __init__(self, pinMs, pinSm,pinLs):
        pinMs = ADC(Pin(pinMs))
        pinSm = ADC(Pin(pinSm))
        pinLs = ADC(Pin(pinLs))
        pinMs.width(ADC.WIDTH_12BIT) 
        pinMs.atten(ADC.ATTN_0DB)
        pinSm.width(ADC.WIDTH_12BIT) 
        pinSm.atten(ADC.ATTN_0DB)
        pinLs.width(ADC.WIDTH_12BIT) 
        pinLs.atten(ADC.ATTN_0DB)

        #Possições com base no circuito
        self.positions = ["S","Ne","E","Se","Nw","W","Sw","N"]
        self.actualPosition = ""
        self.pinMs = pinMs
        self.pinSm = pinSm
        self.pinLs = pinLs
        _thread.start_new_thread(self.__monitoring, ())

    #thread pra monitorar a posição (atualiza a cada 10 sec)
    def __monitoring(self):
        while True:
            Ms = self.pinMs.read()
            Sm = self.pinSm.read()
            Ls = self.pinLs.read()
            try:
                val = int(f"{Ms}{Sm}{Ls}",2)
                self.actualPosition = self.positions[val]
            except:
                self.actualPosition = "Cannot find any position. Verify the sensor"
            sleep(10)

    #retorna a posição atual
    def read(self):
        return self.actualPosition