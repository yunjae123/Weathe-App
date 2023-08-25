import datetime as dt
import requests 
from flask import Flask, render_template, request

app = Flask(__name__)

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = "a4243aa3498ba0bab7d3f32f82b18ef8"

def k_ftemp(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return fahrenheit

def k_ctemp(kelvin):
    return kelvin - 273.1

@app.route('/', methods=["GET", "POST"])

def index():
    if request.method == "POST":
        city = request.form.get("city")
    url = BASE_URL + "appid=" + API_KEY + "&q=" + city
    response = requests.get(url).json()
    fahrenheit_temp = round(k_ftemp(response["main"]["temp"]))
    celsius_temp = round(k_ctemp(response["main"]["temp"]))
    humidity = response['main']['humidity']
    local_sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
    local_sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])
    return render_template("index.html", city = city, fahrenheit_temp = fahrenheit_temp, celsius_temp = celsius_temp, humidity = humidity)

if __name__ == "__main__":
    app.run(debug=True)




