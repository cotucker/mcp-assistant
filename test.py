import requests, os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

def get_weather(location: str) -> str:
    """Get current weather for a location.

    Args:
        location: Location to get weather for
    """
    print('Location: .f,gmlkfdsgkldsfjglksdg')
    response = requests.get(f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}&aqi=no')
    data = response.json()
    print('JSON\n' + str(data))
    location_from_response = str(data['location']['name']) + ', ' + str(data['location']['country'])
    current = data['current']
    weather = f"""
    Current Weather for {location_from_response}:
    Temperature: {current['temp_c']}°C
    Feels like: {current['feelslike_c']}°C
    Wind: {current['wind_kph']} kph {current['wind_dir']}
    Humidity: {current['humidity']}%
    Condition: {current['condition']['text']}
    Pressure: {current['pressure_mb']} mb
    """
    return weather

if __name__ == '__main__':
    print(get_weather('Minsk'))