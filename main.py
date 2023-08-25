import datetime as dt
import requests 

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = "a4243aa3498ba0bab7d3f32f82b18ef8"
CITY = "Denver"

def k_ftemp(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return fahrenheit


url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
response = requests.get(url).json()

fahrenheit_temp = round(k_ftemp(response["main"]["temp"]))

print(f"{CITY} is currently {fahrenheit_temp} degrees fahrenheit!")