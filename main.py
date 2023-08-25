import datetime as dt
import requests 
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')

def index():
    return "Hello World!!!"

if __name__ == "__main__":
    app.run(debug=True)


BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = "a4243aa3498ba0bab7d3f32f82b18ef8"
CITY = "Seoul"

def k_ftemp(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return fahrenheit

def k_ctemp(kelvin):
    return kelvin - 273.1


url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
response = requests.get(url).json()

fahrenheit_temp = round(k_ftemp(response["main"]["temp"]))
celsius_temp = round(k_ctemp(response["main"]["temp"]))
humidity = response['main']['humidity']
local_sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
local_sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])

# print(f"{CITY} is currently {fahrenheit_temp}°F or {celsius_temp}°C.")
# print(f"The humidity in {CITY} is currently {humidity}%.")

