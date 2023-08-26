import datetime as dt
import requests 
from flask import Flask, render_template, request
import os

app = Flask(__name__)

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = os.environ.get("OPENWEATHER_API_KEY")
DEFAULT_CITY = "denver"


def k_ftemp(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return fahrenheit

def k_ctemp(kelvin):
    return kelvin - 273.15

@app.route('/', methods=["GET", "POST"])

def index():
    city = DEFAULT_CITY
    if request.method == "POST":
        city_input = request.form.get("city")
        city = city_input.lower().capitalize() if city_input else DEFAULT_CITY.capitalize()
    url = BASE_URL + "appid=" + API_KEY + "&q=" + city
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp =  data.get("main", {}).get("temp")
        if temp:
            fahrenheit_temp = round(k_ftemp(data["main"]["temp"]))
            celsius_temp = round(k_ctemp(data["main"]["temp"]))
            humidity = data['main']['humidity']
            local_sunrise_time = dt.datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
            local_sunset_time = dt.datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])
            return render_template("index.html", city = city, fahrenheit_temp = fahrenheit_temp, celsius_temp = celsius_temp, humidity = humidity)
        else:
            return render_template("index.html", city=city, error="Temperature data is missing for this city.")
    
    elif response.status_code == 404:
        return render_template("index.html", city=city, error="City not found")
    
    else:
        return render_template("index.html", city=city, error="An unexpected error occurred.")
if __name__ == "__main__":
    app.run(debug=True)





