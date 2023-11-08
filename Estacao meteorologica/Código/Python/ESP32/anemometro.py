from machine import Pin
from utime import sleep, time
import _thread
class Encoder():
    def __init__(self,pinA, pinB):
        #ANTES QUE PERGUNTEM N FAÇO IDEIA PRA Q ESSES 2 PINOS SERVEM
        a = Pin(pinA,Pin.IN, Pin.PULL_UP)
        b = Pin(pinB,Pin.IN, Pin.PULL_UP)
        self.A = a
        self.B = b
        self.pulse = 0
        self.pulse_per_revolution = 360
        self.circumference = 0.2 #ex: 20cm diameter
        self.time = 1.0
        self.vKmph = 0
        
        _thread.start_new_thread(self.__monitoring, ())

    def __count(self,p):
        if p == self.A:
            self.pulse += 1 if self.A.value() == self.B.value() else -1
        else:
            self.pulse += 1 if self.A.value() != self.B.value() else -1

    def __monitoring(self):
        self.A.irq(trigger=Pin.IRQ_RISING or Pin.IRQ_FALLING, handler=self.__count)
        self.B.irq(trigger=Pin.IRQ_RISING or Pin.IRQ_FALLING, handler=self.__count)
        
        last_pulse = self.pulse

        sleep(time)

        pps = self.pulse - last_pulse
        rps = pps / self.pulse_per_revolution
        self.vKmph = rps * self.circumference*3.6
        
        self.pulse = 0

    def read(self):
        return self.vKmph