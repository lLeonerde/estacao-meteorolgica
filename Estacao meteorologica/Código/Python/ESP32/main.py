
###################################################################
#==                                                             ==#
#==  Projeto....: Estação Meteorológica                         ==#
#==  Instituição: FATEC-JD - Sistemas Embarcados                ==#
#==  Data.......: Junho/2023                                    ==#
#==                                                             ==#
#==  Trabalho da disciplina Projeto Integrador II               ==#
#==                                                             ==#
#==  Mediante o conhecimento adquirido nas disciplinas Banco de ==# 
#==  dados, Programação para Sistemas Embarcados I,  Eletrônica ==#
#==  Digital II e Engenharia de Software I,  revisar  o projeto ==#
#==  Estação Meteorológica FATEC anterior e apresentar uma nova ==#                                                                                                       ==#
#==  proposta com base no microcontrolador ESP32,   sensores,   ==#
#==  barramento I2C e MQTT.                                     ==#
#==                                                             ==#
###################################################################

#== Importação de classes gerais
from machine import Pin, I2C, reset
from time import time, sleep
#from time import ctime

#== Classes específicas do projeto (sensores)
from anemometro import Anemometro   # Velocidade do vento
from mpl3115a2 import MPL3115A2     # Pressão e altitude
from aht import AHT2x               # Temperatura e umidade
from ccs811 import CCS811           # Nível de Co2 e VTOC
from RoTW import RoTW               # Rosa dos Ventos
import bh1750                       # Luminosidade
#from pluviometro import Pluviometro

#== Classes para configuração do ESP32 ou como servidor Web ou broker MQTT
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
transicao = ""

gc.collect()
strBufTransmissao = ["0.0", "0.0", "N", "57", "22", "0.97", "716.4", "0.0", "0.0"]

# Dicionario dos sensores e seus topicos mqtt 
dict_mqtt_topicos = {
    'anemometro_m_seg': 'estacao/anem/m',
    'anemometro_km_h': 'estacao/anem/km',
    'direcao_vento': 'estacao/direcao_vento',
    'umidade': 'estacao/umidade',
    'temperatura': 'estacao/temperatura',
    'pressao': 'estacao/pressao',
    'altitude': 'estacao/altitude',
    'nivel_co2': 'estacao/nivel_co2',
    'luminosidade': 'estacao/luminosidade',
    'pluviometro': 'estacao/pluviometro'}

# Dicionario vazio a ser preenchido
dict_sensores = {}

html = """<!DOCTYPE html>
<html>
  <head>
    <title>NodeMCU LED</title>
    <meta charset="utf-8">
  </head>
  <body>
    <form>
      <p align="center">""" + str(strBufTransmissao) + """</p>
    </form>
  </body>
</html>
"""
print("Iniciando WiFi...")
estacao = network.WLAN(network.STA_IF)

# Ativa e desativa AP para evitar problemas de conexao
estacao.active(False)
estacao.active(True)

estacao.connect('SSIDexemplo', 'senha')
#estacao.connect('Soares','Jomi11022016')

while estacao.isconnected() == False:
    pass
print(estacao.ifconfig())

''' # partes do servidor WEB comentadas para evitar problemas com MQTT
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
'''

# Ao inves deste, foi utilizado um broker interno (o Aedes) do Node-RED
#servidor = 'test.mosquitto.org' 
servidor = 'IPexemplo' 
#servidor='192.168.128.116'
cliente = MQTTClient('estacao-fatec', servidor, 1883)
print('Conexao realizada.')

#==============================================#
#=============  Loop principal ================#
#==============================================#

try:
    #-- Caso tenha sido encontrado algum dispositivo...
    if len(dispositivos) > 0:
        i = 0
        taxaCO2 = CCS811(i2c)     # Instancia os objetos utilizados para CCS811

        #-- Loop infinito caso exista algum dispositivo...
        while (True):
            ''' # partes do servidor WEB comentadas para evitar problemas com MQTT
            conexao, endereco = s.accept()
            print("Conexao de %s" % str(endereco))
            requisicao = conexao.recv(1024)
            requisicao = str(requisicao)
            print("Conteudo = %s" % requisicao)
 
            conexao.send('HTTP/1.1 200 OK\n')
            conexao.send('Content-Type: text/html\n')
            conexao.send('Connection: close\n\n')
'''
            #-- Varre todos os dispositivos da rede e "pega" o 
            #   que eles estão escrevendo no intervalo de 1 segundo
            for i in dispositivos:
                #print('entrou no for')
            #==============================================#
            #===== Bloco de tratamento do Anemômetro ======#
            #==============================================#
            
                # ! Para cada sensor i2c, eh atribuido um endereço hexadecimal
                if i == 0x9:

                    #-- Constantes para cálculo de velocidade do anemômetro
                    PPR            = 1
                    COMPR_HASTE    = 15
                    FATOR_CORRECAO = 3.001

                    #-- Instancia os objetos utilizados no anemômetro
                    anemometro = Anemometro(COMPR_HASTE, PPR, FATOR_CORRECAO);

                    anemometro.velocidade(i2c, i)

                    #-- Gera a saída pelo terminal para conferência
                    #print("Direção do vento...........:", anemometro.__direcaoVento)
                    print("Deslocamento da roda.......:{:7.2f}cm".format(anemometro.__deslocamentoCm))
                    #print("Velocidade do vento........:{:7.2f}m/s".format(anemometro.__mPorSegundo))
                    #print("Velocidade do vento........:{:7.2f}Km/h".format(anemometro.__kmPorHora))
                    #print("_________________________________________")
                    dict_sensores['anem_m_seg'] = str(anemometro.__mPorSegundo)
                    dict_sensores['anem_km_h'] = str(anemometro.__kmPorHora)

            #==============================================#
            #======= Bloco de tratamento dos sensores  ====#
            #======= TCRT5000 e LM339                ======#
            #======= Rosa dos ventos               ========#
            #==============================================#

                elif i == 0xA:
                    direcao_vento = RoTW(i2c, 10, 0)
                    direcao = direcao_vento.lerValor()
                    if direcao != "":
                        transicao = direcao
                    print("Direção do vento..........: ",transicao)
#                     print("_________________________________________")
                    dict_sensores['direcao_vento']=str(direcao)

            #==============================================#
            #======= Bloco de tratamento do sensor     ====#
            #======= AHT (umidade e temperatura)     ======#
            #==============================================#

                elif i == 0x38:
                    aht = AHT2x(i2c, crc=True)
                    print("Umidade...................: {:2.2f}%".format(aht.humidity))
                    print("Temperatura...............: {:2.2f}ºC".format(aht.temperature))
                    #print("_________________________________________")
                    dict_sensores['umidade']=str(aht.humidity)
                    dict_sensores['temperatura']=str(aht.temperature)

            #==============================================#
            #======= Bloco de tratamento do sensor     ====#
            #======= MPL3115A2 (pressão e altitude)  ======#
            #==============================================#

                elif (i == 0x60):
                    mpl = MPL3115A2(i2c, mode=MPL3115A2.PRESSURE)   #modo pressão 
                    pressao = mpl.pressure()
                    #temperatura = mpl.temperature()
                    print("Pressão atmosférica.......: {:2.2f}pa".format(pressao))

                    mpl = MPL3115A2(i2c, mode=MPL3115A2.ALTITUDE)   #modo altímetro 
                    altitude = mpl.altitude() 
                    print("Altitude..................: {:2.2f}m ".format(altitude))
                    #print("_________________________________________")
                    dict_sensores['pressao']=str(pressao)
                    dict_sensores['altitude']=str(altitude)

            #==============================================#
            #======= Bloco de tratamento do sensor     ====#
            #======= CCS811 (CO2 e Gases voláteis)   ======#
            #==============================================#

                elif (i == 0x5a):
                    if taxaCO2.data_ready():
                        print(f"CO2........................: {taxaCO2.eCO2:.0f} ppm, tVOC: {taxaCO2.tVOC:.0f} ppb")
                        dict_sensores['nivel_co2']= str(taxaCO2.eCO2);

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
                            if mesure_lux > 0:
                                print("Luminosidade..............: {} lux".format(mesure_lux))
                                print("_________________________________________")
                                break
                            sleep(0.2)
                    dict_sensores['luminosidade']= str(mesure_lux);
                    #print("Luminosidade: {}".format(mesure_lux))

            #========================================================#
            #======= Bloco de tratamento do sensor reed-switch   ====#
            #======= Pluviometro (Precipitação pluviométrica)    ====#
            #========================================================#
                ''' # Biblioteca ctime, nao funciona no micropython, somente em python convencional
                    # Caso for necessario, utilizar modulo RTC i2c, com memoria EEPROM
                pluv = Pluviometro(23, 0.7859503363)
                pluv.iniciar_medicao()
                   
                tempo_atual = ((ctime().split())[3]).split(':')
                hora = int(tempo_atual[0])
                minunto = int(tempo_atual[1])
                
                if (hora == 23) and (minunto >= 59):
                    pluv._set_cont_pulso(0)
                '''
# COLOCAR AQUI o HTML caso for necessario
            html = """<!DOCTYPE html><html><head><title></title><meta charset="utf-8"></head><body><form><p align="center">""" + str(strBufTransmissao) + """</p></form></body></html>"""
            #conexao.sendall(html)
            #conexao.close()
            
            print('Publicando no servidor MQTT') 
            
            cliente.connect()
            
            # lista que recebe o valor medido pelos sensores
            conteudo=[
                dict_sensores['anem_m_seg'],
                dict_sensores['anem_km_h'],
                dict_sensores['direcao_vento'],
                dict_sensores['umidade'],
                dict_sensores['temperatura'],
                dict_sensores['pressao'],
                dict_sensores['altitude'],
                dict_sensores['nivel_co2'],
                dict_sensores['luminosidade'],
                dict_sensores['pluviometro']
            ]
            
            #json = '{"anem_m_seg" : ' + conteudo[0]  + ', "anem_km_h" : ' + conteudo[1] + '}' 
                        
            cliente.publish(dict_mqtt_topicos['anemometro_m_seg'].encode(), conteudo[0].encode())
            cliente.publish(dict_mqtt_topicos['anemometro_km_h'].encode(), conteudo[1].encode()) 
            cliente.publish(dict_mqtt_topicos['direcao_vento'].encode(), conteudo[2].encode())
            cliente.publish(dict_mqtt_topicos['umidade'].encode(), conteudo[3].encode())
            cliente.publish(dict_mqtt_topicos['temperatura'].encode(), conteudo[4].encode())
            cliente.publish(dict_mqtt_topicos['pressao'].encode(), conteudo[5].encode())
            cliente.publish(dict_mqtt_topicos['altitude'].encode(), conteudo[6].encode())
            cliente.publish(dict_mqtt_topicos['nivel_co2'].encode(), conteudo[7].encode())
            cliente.publish(dict_mqtt_topicos['luminosidade'].encode(), conteudo[8].encode())
            cliente.publish(dict_mqtt_topicos['pluviometro'].encode(), conteudo[9].encode())


            
            cliente.disconnect() 

            print ('Envio realizado.') 
            
            # Envia valores a cada 3 segundos
            gc.collect()
            sleep(3)
except Exception as Err:
#except OSError as Err:
    print("Provável erro de comunicação com o dispositivo:",i)
    #pass
    #print("Erro:", Err, "\n", "Tipo do erro: ", type(Err).__name__)

except KeyboardInterrupt:
  s.close()
  estacao.active(False)

