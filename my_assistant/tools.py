from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from my_assistant.memory import search_memory,save_memory,erase_all_memories
import requests

def get_current_datetime(timezone: str) -> str:
    """Returns the current date and time for a given timezone."""

    try:
        current_time = datetime.now(ZoneInfo(timezone))

        return current_time.strftime(
            "%A, %B %d, %Y at %I:%M %p"
        )

    except ZoneInfoNotFoundError:
        return (
            f"I couldn't find the timezone '{timezone}'. "
            "Please provide a valid IANA timezone, "
            "such as 'Asia/Kolkata', 'Asia/Tokyo', "
            "or 'America/New_York'."
        )

def calculator(a: float, b: float, operation: str) -> float:
    """This Performs the basic arithmetic operations"""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            return "Cannot divide by zero."
        return a / b
    return "Invalid Operation."

def search_long_term_memory(query: str) -> str:
    """Search the user's long-term memories for information relevant to the query."""

    results = search_memory(query)

    if not results:
        return "No relevant memories found."

    memories = ["Relevant memories:"]

    for i, result in enumerate(results, start=1):
        memories.append(
            f"{i}.\n"
            f"Text: {result.payload['text']}\n"
            f"Type: {result.payload['type']}\n"
            f"Created: {result.payload['created_at']}\n"
            f"Metadata: {result.payload['metadata']}\n"
            f"Similarity: {result.score}"
        )

    return "\n\n".join(memories)

from my_assistant.memory import save_memory


def save_long_term_memory(
    text: str,
    memory_type: str = "general",
    metadata: dict | None = None,
) -> str:
    """Save useful, long-term information about the user to long-term memory."""

    save_memory(
        text=text,
        memory_type=memory_type,
        metadata=metadata,
    )

    return "Memory saved successfully."


def erase_long_term_memory() -> str:
    """Erase all long-term memories. Use only when the user explicitly asks to forget all stored memories."""

    erase_all_memories()

    return "All long-term memories have been erased."



def get_weather(city: str) -> str:
    """Gets the current weather for a given city."""

    try:
        # Step 1: Convert city name into latitude and longitude
        geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

        geocoding_response = requests.get(
            geocoding_url,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json",
            },
            timeout=10,
        )

        geocoding_response.raise_for_status()

        location_data = geocoding_response.json()

        if "results" not in location_data:
            return f"I couldn't find the city '{city}'."

        location = location_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]
        city_name = location["name"]
        country = location.get("country", "")

        # Step 2: Get current weather using coordinates
        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_response = requests.get(
            weather_url,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
                "timezone": "auto",
            },
            timeout=10,
        )

        weather_response.raise_for_status()

        weather_data = weather_response.json()

        current = weather_data["current"]

        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        wind_speed = current["wind_speed_10m"]
        weather_code = current["weather_code"]

        # Convert weather code into a readable description
        weather_description = get_weather_description(weather_code)

        return (
            f"Current weather in {city_name}, {country}:\n"
            f"Condition: {weather_description}\n"
            f"Temperature: {temperature}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind speed: {wind_speed} km/h"
        )

    except requests.exceptions.RequestException:
        return "Sorry, I couldn't retrieve the weather information right now."

    except (KeyError, IndexError):
        return "Sorry, I received an unexpected response from the weather service."


def get_weather_description(weather_code: int) -> str:
    """Converts Open-Meteo weather codes into readable descriptions."""

    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }

    return weather_codes.get(
        weather_code,
        "Unknown weather condition"
    )
