import requests
import os
from dotenv import load_dotenv
 
load_dotenv()
 
def get_weather(city: str) -> dict:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
   
    try:
        response = requests.get(url)
        data= response.json()
       
        if data.get("cod") != 200:
            return {"error": data.get("message", "An error occurred while fetching weather data.")}
       
        return {
            "city": city,
            "temp_celsius": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"]
        }
    except Exception as e:
        return {"error": str(e)}
 

