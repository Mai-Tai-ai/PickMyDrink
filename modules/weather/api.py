import os
import requests
from dotenv import load_dotenv

from modules.weather.model import WeatherInfo

# Load the .env file
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

# Set the base URL and parameters
url = "http://api.weatherapi.com/v1/current.json"

def get_weather(city: str = "Amsterdam"):
    # Make the request
    response = requests.get(url, params={"q": city, "key": API_KEY, "aqi": "no"})
    data = response.json()

    if "current" not in data:
        return {"error": "No current weather information available."}

    weather = data["current"]
    model_data = {
        "clouds": weather["cloud"],
        "precipitation": weather["precip_mm"],
        "wind": weather["wind_kph"],
        "temperature": weather["temp_c"],
        "condition": weather["condition"]["text"].lower(),
        "is_day": weather["is_day"],
        "visibility": weather["vis_km"],
        "humidity": weather["humidity"],
        "pressure": weather["pressure_mb"]
    }

    return WeatherInfo.model_validate(model_data)


if __name__ == "__main__":
    data = get_weather()
    print(data)
