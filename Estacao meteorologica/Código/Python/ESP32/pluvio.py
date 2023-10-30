from machine import Pin
from utime import sleep, time
import _thread

class Pluviometro:
    def __init__(self, pino_pluvi, area = 50000):
        self.pino_pluvi = Pin(pino_pluvi, Pin.IN)
        self.area = area #area em mm²
        self.conta_pulsos = 0
        self.ultimo_tempo_pulso = 0
        self.estado_interrupcao = 0
        self.chuva_comecou = False
        self.lock = _thread.allocate_lock()
        _thread.start_new_thread(self.__monitorar_chuva, ())

    def __medir_chuva(self, pin):
        sleep(0.5)
        if not self.chuva_comecou:        
            with self.lock:
                self.chuva_comecou = True
            #print('Comecou a chover')
        with self.lock:
            self.conta_pulsos += 1
            self.ultimo_tempo_pulso = time()
        
    def volume_chuva(self):
        with self.lock:
            return self.conta_pulsos * 9.8 * 1000 / self.area

    def __monitorar_chuva(self):

        self.pino_pluvi.irq(trigger = Pin.IRQ_RISING, handler = self.__medir_chuva)

        while True:
            if time() - self.ultimo_tempo_pulso > 900:
                with self.lock:     
                    self.conta_pulsos = 0
                    self.chuva_comecou = False
            sleep(1)
