
import mysql.connector

#Se conecta ao banco de dados
con = mysql.connector.connect(host='localhost', database = 'db_ajax', user = 'root', password = 'Agostinho!2023')

#Busca a conecção com o banco de dados
if con.is_connected():
    db_info = con.get_server_info()
    print("Conexão  realizada:", db_info)
    cursor = con.cursor()
    comando = 'SELECT * FROM db_milan.leituras order by id desc limit 0,1;'
    cursor.execute(comando)
    a = cursor.fetchall()
    b = a[0]
    c = list(b)
#Dentro do banco de dados retornam os seguintes dados
    Temperatura = c[1]
    Umidade = c[2]
    Pressao = round(c[3]/101327.389, 2)
    Altitude = c[4]
    Indice_uv = c[5]
    CO = c[6]
    Vento_vel = c[7]
    Vento_dir = c[8][-1]
    Pluviosidade = c[9]
    Luminosidade = c[10]
    Hora = c[11]
    #print(Temperatura,Umidade,Pressao,Altitude,Indice_uv,CO,Vento_vel,Vento_dir,Pluviosidade,Luminosidade,Hora)
else:
    print('erro')
