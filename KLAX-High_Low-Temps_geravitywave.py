# KLAX_High_Low_Temperature.py
# Bringing you the weather forecast with sass and style

import requests
from datetime import datetime
from config import BASE_URL, HEADERS, TIMEOUT

# KLAX coordinates - serving you LA glamour vibes from the get-go
DEFAULT_LAT = 33.9416  # Latitude of KLAX (Los Angeles International Airport)
DEFAULT_LON = -118.4085  # Longitude of KLAX (because even coordinates need precision!)


def get_high_low_temperature(lat=DEFAULT_LAT, lon=DEFAULT_LON):
    """
    Fetches the high and low temperatures forecasted for KLAX for today,
    categorizing periods by isDaytime for high/low temperatures.

    Parameters:
    - lat (float): Latitude of the location (default is KLAX latitude).
    - lon (float): Longitude of the location (default is KLAX longitude).
    """
    # Step 1: Get the forecast URL for KLAX
    point_url = f"{BASE_URL}/points/{lat},{lon}"
    response = requests.get(point_url, headers=HEADERS, timeout=TIMEOUT)

    if response.status_code != 200:
        print("💔 Error: Couldn't fetch point metadata. It's not giving what it should give.")
        print("Response:", response.text)
        return

    # Extract the forecast URL directly from the JSON response
    point_data = response.json()
    forecast_url = point_data.get("forecast")

    # Debug output if forecast URL is missing
    if not forecast_url:
        print("🚨 Error: 'forecast' URL not found in point metadata. The drama!")
        print("Debug info: Full point_data response:", point_data)
        return

    # Yaaas, we stan a successful API pull!
    print(f"🎯 Debug: Snatched the forecast URL: {forecast_url}")

    # Step 2: Get the forecast data
    forecast_response = requests.get(forecast_url, headers=HEADERS, timeout=TIMEOUT)
    if forecast_response.status_code != 200:
        print("💔 Error: Couldn't fetch forecast data. The tea is piping cold.")
        print("Response:", forecast_response.text)
        return

    # Access periods
    forecast_data = forecast_response.json()
    periods = forecast_data.get("periods", [])

    # Debug moment: Confirming we got the goods
    print(f"✨ Debug: Retrieved {len(periods)} fabulous forecast periods.")  # Debugging output

    if not periods:
        print("Error: No forecast periods found. Where’s the data?")
        print("Debug info: Full forecast data response:", forecast_data)
        return

    # Today's date
    today_date = datetime.now().date()
    high_temp = None
    low_temp = None

    # Step 3: Identify today's daytime and nighttime blocks
    for period in periods:
        # Parse period start time and check if it's today
        period_start = datetime.strptime(period["startTime"], '%Y-%m-%dT%H:%M:%S%z')
        period_date = period_start.date()

        # Check if the period is for today
        if period_date == today_date:
            print(
                f"Processing period: {period['name']}, isDaytime: {period['isDaytime']}, Temperature: {period['temperature']}°F")
            temperature = period["temperature"]

            # Assign high for daytime and low for nighttime
            if period["isDaytime"]:
                high_temp = temperature
            else:
                low_temp = temperature

    # Display the results
    if high_temp is not None and low_temp is not None:
        # Serving you the full weather fantasy
        print(f"Forecasted high temperature for KLAX today: {high_temp}°F")
        print(f"Forecasted low temperature for KLAX tonight: {low_temp}°F")
    else:
        print("No forecast data available for the specified day. Weather, where you at?!")


def save_timestamp():
    """
    Saves the current timestamp to a file each time the script runs.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Log it like it's hot
    with open("run_timestamps.txt", "a") as file:
        file.write(f"Script run on: {timestamp}\n")
    print(f"Timestamp saved: {timestamp} (Because receipts matter)")


if __name__ == "__main__":
    get_high_low_temperature()
    save_timestamp()
