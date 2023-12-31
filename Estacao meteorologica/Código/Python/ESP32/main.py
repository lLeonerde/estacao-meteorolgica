
###################################################################
#==                                                             ==#
#==  Projeto....: Estação Meteorológica                         ==#
#==  Instituição: FATEC-JD - Sistemas Embarcados                ==#
#==  Data.......: Novembro/2023                                 ==#
#==                                                             ==#
#==  Trabalho da disciplina Projeto Integrador II               ==#
#==                                                             ==#
#==  Mediante o conhecimento adquirido nas disciplinas Banco de ==# 
#==  dados, Programação para Sistemas Embarcados I,  Eletrônica ==#
#==  Digital II e Engenharia de Software I,  revisar  o projeto ==#
#==  Estação Meteorológica FATEC anterior e apresentar uma nova ==#                                                                                                       ==#
#==  proposta com base no microcontrolador ESP32,   sensores  e ==#
#==  barramento I2C.                                            ==#
#==                                                             ==#
###################################################################



#== Importação de classes gerais
from machine import Pin, I2C, reset, ADC
from time import time, sleep



#== Classes específicas do projeto (sensores)

from mpl3115a2 import MPL3115A2     # Pressão e altitude
from aht import AHT2x               # Temperatura e umidade
import bh1750                       # Luminosidade
from MQ7 import MQ7                 # Sensor de Gás (carbono)
from sensorUV import uv_sensor      # Sensor Ultravioleta
from pluvio import Pluviometro      # Sensor para mediçao de chuva
from RosaVentop import RdV
from anemometro import Encoder

#== Classes para configuração do ESP32 como servidor WEB E mqtt
from umqtt.simple import MQTTClient
import usocket as socket
import network
import gc



#==============================================#
#=========== Bloco de Funções =================#
#==============================================#

#-- Função: localizaDispI2C()
#-- Descrição: Localiza dispositivos I2C na rede e retorna uma
#   lista contendo os dispositivos encontrados
def localizaDispI2C():
    print('Procura por dispositivos I2C na rede...')
    dispositivos = i2c.scan()
    if len(dispositivos) == 0:
        print("Nenhum dispositivo encontrado!")
    else:
        print('Quantidade de dispositivos I2C encontrados:',len(dispositivos))

    for dispositivo in dispositivos: 
        print("Endereço decimal: ",dispositivo," | Endereço hexadecimal: ",hex(dispositivo))
    return dispositivos


#==============================================#
#==============================================#
#============= Programa Principal =============#
#==============================================#

#-- Instancia objeto I2C com os pinos SCL e SDA definidos CCS811
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
#-- A lista "dispositivos" recebe um array de dispositivos encontrados
dispositivos = localizaDispI2C()

# Sensores e as portas utilizadas no ESP
co_sens = 4
uv_sens = 2
anemometro_sens = (14,27,26)
Ms,Sm,Ls = anemometro_sens
encoderA, encoderB = (19,23)
pluvio = 13


CO = MQ7(co_sens)
UV = uv_sensor(uv_sens)
Rosaventop = RdV(Ms,Sm,Ls)
PLV = Pluviometro(pluvio)
Enc = Encoder(encoderA,encoderB)

gc.collect()


print("Iniciando WiFi...")
estacao = network.WLAN(network.STA_IF)
estacao.active(False)
estacao.active(True)

estacao.connect('','')

while estacao.isconnected() == False:
    sleep(0.25)
print(estacao.ifconfig())

#servidor = 'test.mosquitto.org' 
servidor = 'broker.emqx.io'
topic = '/bmp_bh_sht'
#servidor='192.168.128.116'
cliente = MQTTClient('NodeMCU', servidor, 1883)
print('Conexao realizada.')

#==============================================#
#=============  Loop principal ================#
#==============================================#

try:
    #-- Caso tenha sido encontrado algum dispositivo...
    if len(dispositivos) >= 0:
        i = 0

        #-- Loop infinito caso exista algum dispositivo...
        while (True):
            
            estacao.ative(False)

            #-- Varre todos os dispositivos da rede e "pega" o 
            #   que eles estão escrevendo no intervalo de 1 segundo
            for i in dispositivos:
            #==============================================#
            #======= Bloco de tratamento do sensor     ====#
            #======= AHT (umidade e temperatura)     ======#
            #==============================================#

                if i == 0x38:
                    aht = AHT2x(i2c, crc=True)
                    print("Umidade...................: {:2.2f}%".format(aht.humidity))
                    print("Temperatura...............: {:2.2f}ºC".format(aht.temperature))
                    #print("_________________________________________")
                    
            #==============================================#
            #======= Bloco de tratamento do sensor     ====#
            #======= MPL3115A2 (pressão e altitude)  ======#
            #==============================================#

                elif (i == 0x60):
                    print('teste')
                    mpl = MPL3115A2(i2c, mode=MPL3115A2.PRESSURE)   #modo pressão 
                    pressao = mpl.pressure()
                    temperatura = mpl.temperature()
                    print("Pressão atmosférica.......: {:2.2f}pa".format(pressao))

                    mpl = MPL3115A2(i2c, mode=MPL3115A2.ALTITUDE)   #modo altímetro 
                    altitude = mpl.altitude() 
                    print("Altitude..................: {:2.2f}m ".format(altitude))
                    #print("_________________________________________") 
                    
            #==============================================#
            #======= Bloco de tratamento do sensor     ====#
            #======= BH1750 (Luminosidade)           ======#
            #==============================================#
                
                elif ((i == 0x23) or (i == 0x5C)):
                    
                    captura = bh1750.BH1750(i2c)
                    mesure_lux = captura.leitura_lux(bh1750.MODE_CONTINU_HAUTE_RESOLUTION)
                    if (captura.detect()):
                        while True:
                            mesure_lux = captura.leitura_lux(bh1750.MODE_CONTINU_HAUTE_RESOLUTION)
                            if mesure_lux >= 0:
                                print("Luminosidade..............: {} lux".format(mesure_lux))
                                
                                break
                            sleep(0.2)
                            
            #==============================================#
            #===== Bloco de tratamento do Anemômetro ======#
            #==============================================#

            Wind_speed = Enc.read()
            print(f"Eu sou a velocidade............:{Wind_speed}\n")

            #==============================================#
            #======= Bloco de tratamento do sensor ========#
            #======= Rosa dos ventos               ========#
            #==============================================#

            Wind_direction = Rosaventop.read()
            print(f"Direção do vento..............: {Wind_direction}\n")


            #========================================================#
            #======= Bloco de tratamento do sensor reed-switch   ====#
            #======= Pluviometro (Precipitação pluviométrica)    ====#
            #========================================================#

            chuva_mm = PLV.volume_chuva()
            print(f"mm chuva..............: {chuva_mm}\n")
            #==============================================#
            #======= Bloco de tratamento do sensor     ====#
            #======= MQ7 (CO)                          ====#
            #==============================================#

            taxa_CO = CO.read()
            print(f"Co..............: {taxa_CO}\n")

            #==============================================#
            #======= Bloco de tratamento do sensor     ====#
            #======= Uv (uv)(n sei o nome)             ====#
            #==============================================#

            UV_indice = UV.mostrarUV_index()
            print(f"Uv..............: {UV_indice}")
            print("_________________________________________")

            # Enviando dados pelo MQTT
            
            estacao.ative(True)
            estacao.connect('','')

            while estacao.isconnected() == False:
                sleep(0.25)
            print(estacao.ifconfig())


            print('Publicando no servidor MQTT') 
            cliente.connect()
            test = '{"temperatura" : ' + str(aht.temperature) + ', "umidade" : ' + str(aht.humidity) + ', "nivel_co" : ' + str(taxa_CO) + ', "pressao" : ' + str(pressao) + ', "altitude" : ' + str(altitude) + ', "luminosidade" : ' + str(mesure_lux)  + ', "Indice_UV" : ' + str(UV_indice) + ', "Volume_chuva" : ' +  str(chuva_mm) + ', "Velocidade_vento" : ' + str(Wind_speed) + ', "Dir_vento" : ' + str(Wind_direction) + '}'
            print(test)
            cliente.publish(topic.encode(), test.encode())
            cliente.disconnect()
            gc.collect()
            
            print ('Envio realizado.') 
        
            sleep(20)
except Exception as Err:
#except OSError as Err:
    print("Provável erro de comunicação com o dispositivo:",i)
    #resetar()
    #pass
    print("Erro:", Err, "\n", "Tipo do erro: ", type(Err).__name__)

except KeyboardInterrupt:
  s.close()
  estacao.active(False)




