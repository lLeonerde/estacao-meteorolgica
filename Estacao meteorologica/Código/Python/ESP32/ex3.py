"""
Usando um potenciômetro, faça com que ele controle a luminosidade de um LED, com a variação do valor.
"""

from machine import Pin, PWM, ADC
from time import sleep

pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)

while True:
    valor = (int(pot.read() / 4))
    led = PWM(Pin(2), freq=20000, duty=0)
    led.duty(valor)
    
