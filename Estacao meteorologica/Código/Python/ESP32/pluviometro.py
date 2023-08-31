from machine import Pin
from time import sleep, time


class Pluviometro(object):
    def __init__(self, pino, valor_uni):
        self._pluviometro = Pin(pino, Pin.IN)
        self._cont_pulso = 0
        self._valor_mm_unitario = valor_uni
        self._valor_mm = 0
        self._valor_pluv = 0
        self._anterior = 0
        
    # Funções para setar os valores
    def _set_anterior(self, valor):
        self._anterior = valor
    
    def _set_cont_pulso(self, valor):
        self._cont_pulso = valor
     
    def _set_valor_mm(self, valor):
        self._valor_mm = valor
        
    def _set_valor_pluv(self, valor):
        self._valor_pluv = valor
       
    def _set_valor_mm_unitario(self, valor):
        self._valor_mm_unitario = valor
    
    
    # Funções para obter os valores
    def _get_anterior(self):
        return self._anterior
    
    def _get_cont_pulso(self):
        return self._cont_pulso
        
    def _get_valor_mm(self):
        return self._valor_mm
        
    def _get_valor_mm_unitario(self):
        return self._valor_mm_unitario
        
    def _get_valor_pluv(self):
        return self._valor_pluv
    
    
    def iniciar_medicao(self):
        self._set_valor_pluv(self._pluviometro.value())
        if self._get_valor_pluv() and self._get_anterior() == 0:
            self._set_cont_pulso(self._get_cont_pulso() + 1)
            self._set_valor_mm(self._get_cont_pulso() * self._get_valor_mm_unitario())
        self._set_anterior(self._get_valor_pluv())
        return self._get_valor_mm()
        

'''pluviometro = Pluviometro(13, 0.7859503363)
while True:
    valor = pluviometro.iniciar_medicao()
    print(f'Pluviômetro: {valor}mm')
    print()
    sleep(0.2)'''


# Interromper em uma determinada hora e minuto 
'''from time import ctime

while True:
    tempo_atual = ((ctime().split())[3]).split(':')
    hora = int(tempo_atual[0])
    minunto = int(tempo_atual[1])
    if (hora == 10) and (minunto >= 50):
        # No caso do pluviometro, resetar o contador de pulsos para
        # iniciar a contagem do dia seguinte
        break
    print(f'{hora}:{minunto}')'''
    
        
        
        
        
        
        
