import datetime as dt
import requests 
from flask import Flask, render_template, request
import os
# from dotenv import load_dotenv
# load_dotenv()

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

def get_weather_data(data):
    current_fahrenheit_temp = round(k_ftemp(data["main"]["temp"]))
    current_celsius_temp = round(k_ctemp(data["main"]["temp"]))
    max_ftemp = round(k_ftemp(data["main"]["temp_max"]))
    min_ftemp = round(k_ftemp(data["main"]["temp_min"]))
    max_ctemp = round(k_ctemp(data["main"]["temp_max"]))
    min_ctemp = round(k_ctemp(data["main"]["temp_min"]))
    humidity = data['main'].get("humidity")
    wind_speed = data["wind"].get("speed")
    visibility = data.get("visibility")
    local_sunrise_time = dt.datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
    local_sunset_time = dt.datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])
    return {
        "current_fahrenheit_temp": current_fahrenheit_temp,
        "current_celsius_temp": current_celsius_temp,
        "max_ftemp": max_ftemp,
        "min_ftemp": min_ftemp,
        "max_ctemp": max_ctemp,
        "min_ctemp": min_ctemp,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "visibility": visibility,
        "local_sunrise_time": local_sunrise_time,
        "local_sunset_time": local_sunset_time
    }

@app.route('/', methods=["GET", "POST"])

def index():
    city = DEFAULT_CITY.capitalize()
    if request.method == "POST":
        city_input = request.form.get("city")
        city = city_input.lower().capitalize() if city_input else DEFAULT_CITY.capitalize()
    url = f"{BASE_URL}appid={API_KEY}&q={city}"
    response = requests.get(url)
    print(response.json())

    if response.status_code == 200:
        data = response.json()
        temp =  data.get("main", {}).get("temp")
        if temp:
            weather_data = get_weather_data(data)
            return render_template("index.html", city = city, **weather_data) 
        else:
            return render_template("index.html", city=city, error="Temperature data is missing for this city.")
    
    elif response.status_code == 404:
        return render_template("index.html", city=city, error="City not found")
    
    else:
        return render_template("index.html", city=city, error="An unexpected error occurred.")
    
if __name__ == "__main__":
    app.run(debug=True)




