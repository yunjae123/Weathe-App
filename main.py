import datetime as dt
import requests 

BASE_URL = "http://api.openweathermap.org/data/3.0/weather?"
API_KEY = "a4243aa3498ba0bab7d3f32f82b18ef8"
CITY = "Denver"

url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY

response = requests.get(url)