from time import time
from math import pi

#----------------------------------------------#
#------------ classe Anemometro ---------------#
#----------------------------------------------#
class Anemometro:

    #--------------- CONSTRUTOR ---------------#
    def __init__(self, comprimentoHaste, ppr, fatorCorrecao):
        self.__tempoInicial = time()

        self.__tempoAnterior = time()-1
        self.__comprimentoHaste = comprimentoHaste
        self.__ppr              = ppr
        self.__fatorCorrecao    = fatorCorrecao

        self.__deslocamentoCm = 0.0
        self.__mPorSegundo    = 0.0
        self.__kmPorHora      = 0.0

    #---------------- MÉTODOS -----------------#

    #-- Método: deslocamento(difPulsos, raio, PPR)
    #-- retorna o deslocamento da concha do anemômetro, em centímetros.
    #   difPulsos: representa a quantidade de pulsos do encoder.
    #   raio: representa o cumprimento da haste da concha do anemômetro, em centímetros.
    #   PPR: representa a quantidade de pulsos por revolução que possui o encoder.
    @staticmethod
    def deslocamento(difPulsos, raio, ppr):
        return (2 * pi * raio * difPulsos / ppr)

    #-- Método: metroPorSegundo(difTempo, deslocamentoCm)
    #-- retorna o deslocamento em metros por segundo (m/s)
    #   difTempo: diferença entre a leitura anterior e a atual, em segundos.
    #   __deslocamentoCm: representa o deslocamento medido em centímetros.
    @staticmethod
    def metroPorSegundo(difTempo, deslocamentoCm, fatorCorrecao):
        difTempoH = difTempo
        return ((deslocamentoCm / 100.0 / difTempoH) * fatorCorrecao)

    #-- Método: quilometroPorHora(difTempo, deslocamentoCm)
    #-- retorna o deslocamento em KM por hora (KM/h)
    #   difTempo: diferença entre a leitura anterior e a atual, em segundos.
    #   __deslocamentoCm: representa o deslocamento medido em centímetros.
    @staticmethod
    def quilometroPorHora(difTempo, deslocamentoCm, fatorCorrecao):
        deslocamentoKm = (deslocamentoCm / 100000.0)
        difTempoH = (difTempo / 3600.0)
        return ((deslocamentoKm / difTempoH) * fatorCorrecao)

    #-- Função: convChartoInt()
    #-- Descrição: Recebe um array de caracteres, extrai sua parte
    #   numérica demarcada pelo início e fim, e retorna o valor
    #   inteiro lido.
    @staticmethod
    def convCharToInt(a, inicio, fim):
        i = fim
        total = 0
        j = 1
        algarismo = 0
        while i > inicio:
            algarismo = int(a[i])
            total = total + (algarismo * j)
            j = j * 10
            i = i - 1
        return total

    def velocidade(self, i2c, endereco, tipo=2):
        buffer = i2c.readfrom(endereco, 15)             # lê 15 bytes do Anemômetro (endereço #9)
        b = ""
        #print(buffer)

        for j in buffer:
            b = b + chr(j)

        #-- Verifica direção do vento
        self.__direcaoVento = b[9]

        #-- Quantidade de pulsos do intervalo
        pulsosAtual = self.convCharToInt(b, 9, 14)
        b = ""

        #-- Inicializa o temporizador para cálculo de velocidade
        tempoAtual = time()

        #-- Computa diferença de tempo entre os eventos
        difTempo = (tempoAtual - self.__tempoAnterior)

        #-- Diferença entre quantidade de pulsos anterior e atual
        difPulsos = pulsosAtual

        #-- Atualiza varíaveis de controle de pulso e tempo
        self.__tempoAnterior = tempoAtual

        #-- Realiza todos os cálculos de velocidade
        self.__deslocamentoCm = self.deslocamento(difPulsos, self.__comprimentoHaste, self.__ppr)
        self.__mPorSegundo    = self.metroPorSegundo(difTempo, self.__deslocamentoCm, self.__fatorCorrecao)
        self.__kmPorHora      = self.quilometroPorHora(difTempo, self.__deslocamentoCm, self.__fatorCorrecao)

        if tipo == 0:
            return self.__deslocamentoCm
        elif tipo == 1:
            return self.__mPorSegundo
        elif tipo == 2:
            return self.__kmPorHora
