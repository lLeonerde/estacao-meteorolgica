from machine import Pin, I2C

class RoTW(object):
    def __init__(self, i2c, endereco, compensacao):
        self.__endereco = endereco
        self.__compensacao = compensacao
        #self.__i2c = I2C(scl = Pin(22), sda = Pin(21), freq=400000) # configuração do i2c para o RoTW
        self.__i2c = i2c
        self.__habilitar = False
        #verificação para ver se o RoTW foi encontrado
        if endereco in self.__i2c.scan():
            #print("RoTW encontrado")
            self.__habilitar = True
        else:
            print("RoTW não encontrado")
            
    def lerValor(self):
        if self.__habilitar == True:
            self.__i2c.scan()
            self.__direcao = int.from_bytes(self.__i2c.readfrom(self.__endereco, 1, 2), "BIG") # lê o valor do i2c, e converte para graus, de 0 a 360
            #print (self.__direcao)
            #print (self.__i2c.readfrom(self.__endereco, 1, 2))
            if self.__direcao == 1:
                orientacao = "N"
            elif self.__direcao == 2:
                orientacao = "NE"
            elif self.__direcao == 4:
                orientacao = "E"
            elif self.__direcao == 8:
                orientacao = "SE"
            elif self.__direcao == 16:
                orientacao = "S"
            elif self.__direcao == 32:
                orientacao = "SW"
            elif self.__direcao == 64:
                orientacao = "W"
            elif self.__direcao == 128:
                orientacao = "NW"
            else:
                orientacao= ""

            return orientacao
        else:
            return 0
            
        
