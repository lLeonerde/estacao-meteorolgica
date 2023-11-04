import requests as rq


#Chama a API OpenWeather
Api_Key = "3a599b913beb503d727f1a910208aa07"
city = "jundiaí"
link = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={Api_Key}&lang=pt_br"
link2 = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&cnt=1&appid={Api_Key}"
request = rq.get(link)
request_dic = request.json()
request2 = rq.get(link2 )
request_dic2 = request2.json()

#Busca os intens nescessários dentro do json da API
desc = request_dic["weather"][0]["description"].title()
feels_like = int(round(request_dic["main"]["feels_like"]-273.15, 0))
id= request_dic["weather"][0]["id"]
icon= request_dic["weather"][0]["icon"]
chuva =str(request_dic2['list'][0]['pop']*100)+' %'
print(id, icon, chuva , feels_like, desc)