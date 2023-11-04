from flask import Flask, url_for, render_template
import api, image, sql


app = Flask(__name__)


@app.route("/")
def dashboard():
    #Substitui os dados dentro do html
    return render_template("index (3).html",
                           fundo = image.fundo,
                           Pluviosidade = image.icon_pluvi,
                           Luminosidade = image.icon_lum,
                           Clima= image.icones,
                           Vento = image.icon_vento,
                           UV = image.icon_uv,
                           Umidade = image.icon_umidade,
                           CO= image.icon_co,
                           Chuva = image.icon_chuva,
                           Pressao = image.icon_pressao,
                           Info = api.desc,
                           Temp = api.feels_like,
                           DataTemp = sql.Temperatura,
                           DataPluv = sql.Pluviosidade,
                           DataLum = sql.Luminosidade,
                           VentoVel = sql.Vento_vel,
                           VentoDir = sql.Vento_dir,
                           DataUV = sql.Indice_uv,
                           DataUmi = sql.Umidade,
                           DataCO = sql.CO,
                           DataChu = api.chuva,
                           DataPre = sql.Pressao,
                           Hora = sql.Hora)

if __name__ == "__main__":
    app.run(debug=True)