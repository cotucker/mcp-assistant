from typing import Any
import httpx
import logging
import random
import requests
import os
import pyperclip

from dotenv import load_dotenv
from google import genai
from google.genai import types
from mcp.server.fastmcp import FastMCP
from urllib3 import response

# Initialize FastMCP server
mcp = FastMCP("weather")



load_dotenv()

# Constants
NWS_API_BASE = "https://api.weather.gov"
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
USER_AGENT = "weather-app/1.0"
client = genai.Client(api_key=GEMINI_API_KEY)


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}"""

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get current weather for a location.

    Args:
        location: Location to get weather for
    """
    print('Location: .f,gmlkfdsgkldsfjglksdg')
    response = requests.get(f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}&aqi=no')
    data = response.json()
    location_from_response = str(data['location']['name']) + ', ' + str(data['location']['country'])
    current = data['current']
    weather = f"""
Current Weather for {location_from_response}:
Temperature: {current['temp_c']}°C
Feels like: {current['feelslike_c']}°C
Wind: {current['wind_kph']} kph {current['wind_dir']}
Humidity: {current['humidity']}%
Condition: {current['condition']['text']}
Pressure: {current['pressure_mb']} mb"""
    return weather



@mcp.tool()
def roll_dice(n_dice: int) -> str:
    """Roll `n_dice` 6-sided dice and return the results.
    
    Args:
        n_dice: Number of dice to roll
    """
    result = 'Result 🎲: '
    for _ in range(n_dice):
        result += str(random.randint(1, 6)) + ' '
    return result

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
        {period['name']}:
        Temperature: {period['temperature']}°{period['temperatureUnit']}
        Wind: {period['windSpeed']} {period['windDirection']}
        Forecast: {period['detailedForecast']}
        """
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)


@mcp.tool()
async def answer_question(question: str) -> str:
    """Answer a question using the data provided in the clipboard.

    Args:
        question: Question to answer
    """
    prompt = f"""  
You are a chatbot agent answeering questions.
Your task is to answer the question provided in the <DATA> section.

<DATA>
<QUESTION>{question}</QUESTION>
</DATA>

ANSWER:
"""

    grounding_tool = types.Tool(
        google_search=types.GoogleSearch()
    )

    contents = types.Content(
        role="user",
        parts=[types.Part(text=prompt)]
    )

    config = types.GenerateContentConfig(
        tools=[grounding_tool]
    )    

    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = contents,
        config = config,
    )

    return response.text


@mcp.tool()
async def interact_with_copied_text(action: str) -> str:
    """Interact with the clipboard text.

    Args:
        text: Text to interact with
    """
    prompt_text=pyperclip.paste()
    prompt_action = action

    prompt = f"""  
You are a chatbot agent performing actions with text .
Your task is to perform the action with text using the data provided in the <DATA> section.

<DATA>
<TEXT>{prompt_text}</TEXT>
<ACTION>{prompt_action}</ACTION>
</DATA>

RESULT: 
"""

    grounding_tool = types.Tool(
        google_search=types.GoogleSearch()
    )

    contents = types.Content(
        role="user",
        parts=[types.Part(text=prompt)]
    )

    config = types.GenerateContentConfig(
        tools=[grounding_tool]
    )    

    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = contents,
        config = config,
    )

    return response.text



if __name__ == "__main__":
    # Initialize and run the server
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Starting weather service")
    mcp.run(transport='stdio')