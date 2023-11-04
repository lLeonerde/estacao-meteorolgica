import api

#Separa o "icon" da api em parte numériaca(para selecionar a imagem do clima) e parte escrita(para separar entre dia e noite)
dn = api.icon[-1]
icon_id = api.icon[0:2]

#links das imagens vindos do github
icon = {"01": ['https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_ClimaPrincipal/ClearSky/Day/ClearSky_Day.svg', 'https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_ClimaPrincipal/ClearSky/Night/ClearSky_Night.svg'],
        "02": ['https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_ClimaPrincipal/FewClouds/Day/FewClouds_Day.svg','https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_ClimaPrincipal/FewClouds/Night/FewClouds_Night.svg'],
        "03": ['https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_ClimaPrincipal/ScatteredClouds/ScatteredClouds.svg','https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_ClimaPrincipal/ScatteredClouds/ScatteredClouds.svg'],
        "04": ['https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_ClimaPrincipal/BrokenClouds/BrokenClouds.svg','https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_ClimaPrincipal/BrokenClouds/BrokenClouds.svg'],
        "09": ['https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_ClimaPrincipal/ShowerRain/ShowerRain.svg','https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_ClimaPrincipal/ShowerRain/ShowerRain.svg'],
        "10": ['https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_ClimaPrincipal/Rain/Day/Rain_Day.svg','https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_ClimaPrincipal/Rain/Night/Rain_Night.svg'],
        "11": ['https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_ClimaPrincipal/Thunderstorm/Thunderstorm.svg','https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_ClimaPrincipal/Thunderstorm/Thunderstorm.svg'],
        "13": ['https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_ClimaPrincipal/Snow/Snow.svg','https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_ClimaPrincipal/Snow/Snow.svg'],
        "50": ['https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_ClimaPrincipal/Mist/Mist.svg','https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_ClimaPrincipal/Mist/Mist.svg']}
icones = icon[icon_id][0]
print(icones)

#links dos icones vindos do github
if dn == "d":
    icones = icon[icon_id][0]
    icon_co = 'https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_DemaisAspectos/CO/Dia/CO_Dia.svg'
    icon_chuva = 'https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_DemaisAspectos/Chuva/Dia/Chuva_Dia.svg'
    icon_uv = 'https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_DemaisAspectos/IndiceUV/Dia/IndiceUV_Dia.svg'
    icon_lum = 'https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_DemaisAspectos/Luminosidade/Dia/Luminosidade_Dia.svg'
    icon_pluvi = 'https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_DemaisAspectos/Pluviosidade/Dia/Pluviosidade_Dia.svg'
    icon_pressao = 'https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_DemaisAspectos/Pressao/Dia/Pressao_Dia.svg'
    icon_umidade = 'https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_DemaisAspectos/Umidade/Dia/Umidade_Dia.svg'
    icon_vento = 'https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_DemaisAspectos/Vento/Dia/Vento_Dia.svg'
    fundo = '#7CBBE7'
    print("dia")
else:
    icones = icon[icon_id][1]
    icon_co = 'https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_DemaisAspectos/CO/Noite/CO_Noite.svg'
    icon_chuva = 'https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_DemaisAspectos/Chuva/Noite/Chuva_Noite.svg'
    icon_uv = 'https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_DemaisAspectos/IndiceUV/Noite/IndiceUV_Noite.svg'
    icon_lum = 'https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_DemaisAspectos/Luminosidade/Noite/Luminosidade_Noite.svg'
    icon_pluvi = 'https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_DemaisAspectos/Pluviosidade/Noite/Pluviosidade_Noite.svg'
    icon_pressao = 'https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_DemaisAspectos/Pressao/Noite/Pressao_Noite.svg'
    icon_umidade = 'https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_DemaisAspectos/Umidade/Noite/Umidade_Noite.svg'
    icon_vento = 'https://raw.githubusercontent.com/dodo-think/Interface-para-TV/f8f08cbfca81dc5e6ccc5feaf8fd4864ccaf1c68/Estac%CC%A7a%CC%83o%20Metereolo%CC%81gica/Vetores_DemaisAspectos/Vento/Noite/Vento_Noite-01.svg'
    fundo = '#282730'
    print("noite")