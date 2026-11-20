import csv
import requests
import sys
from pathlib import Path

CSV_PATH = Path.home() / "code" / "cs602-airports-explorer" / "airport-codes.csv"

def find_airport(ident):
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["ident"] == ident:
                return row
    return None

def parse_coordinates(text):
    lon_text, lat_text = text.split(",")   # CSV order: longitude first!
    lon = float(lon_text)
    lat = float(lat_text)
    if not (-90 <= lat <= 90):
        raise ValueError(f"Bad latitude in: {text}")
    if not (-180 <= lon <= 180):
        raise ValueError(f"Bad longitude in: {text}")
    return lat, lon

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

def get_current_weather(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,wind_speed_10m",
    }
    response = requests.get(WEATHER_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data["current"], data["current_units"]

if __name__ == "__main__":
    ident = sys.argv[1].upper() if len(sys.argv) > 1 else "KBOS"
    airport = find_airport(ident)
    if airport is None:
        print(f"No airport with code '{ident}'.")
    else:
        lat, lon = parse_coordinates(airport["coordinates"])
        try:
            current, units = get_current_weather(lat, lon)
        except requests.exceptions.RequestException as e:
            print(f"Could not get weather for {ident}: {e}")
            sys.exit(1)
        print(f"{airport['name']} ({ident}), {airport['municipality']}")
        print(f"Current temperature: {current['temperature_2m']} {units['temperature_2m']}, "
              f"wind: {current['wind_speed_10m']} {units['wind_speed_10m']}")