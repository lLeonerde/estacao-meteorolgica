"""
Se o valor do potenciômetro estiver entre 0 - 255, acenda um LED;
Se o valor do potenciômetro estiver entre 256 - 511, acenda dois LEDs;
Se o valor do potenciômetro estiver entre512 - 767, acenda três LEDs;
Se o valor do potenciômetro estiver entre 768 - 1023, acenda quatro LEDs.

"""
import streamlit as st
from machine import ADC, Pin
from time import sleep
led = Pin(19, Pin.OUT)
led1 = Pin(21, Pin.OUT)
led2 = Pin(22, Pin.OUT)
led3 = Pin(23, Pin.OUT)
pot = ADC(Pin(15))
pot.atten(ADC.ATTN_11DB)
estado = 0
try:
    while True:
        st.header (valor)
        valor = (int(pot.read() / 4))
        print(valor)
        if valor <= 255 :
            led.value(1)
            led1.value(0)
            led2.value(0)
            led3.value(0)
        if valor >= 256 and valor <= 511 :
            led.value(1)
            led1.value(1)
            led2.value(0)
            led3.value(0)
        if valor >= 512 and valor <= 767 :
            led.value(1)
            led1.value(1)
            led2.value(1)
            led3.value(0)
        if valor >= 768 and valor <= 1023 :
            led.value(1)
            led1.value(1)
            led2.value(1)
            led3.value(1)
            
        sleep(1)
        
        
        
        
except KeyboardInterrupt:
    led.value(0)

