#!/usr/bin/env python3
import os
import subprocess
import requests
from datetime import datetime

# Fetch API key and city from environment variables (set these in GitHub Secrets or Actions)
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")  # Use GitHub Secrets to store API key
CITY = os.getenv("CITY", "London")  # Default to "Kuwait City" if not set in Secrets
GITHUB_REPO_PATH = os.getenv("GITHUB_REPO_PATH", "/path/to/your/repo")  # Replace with your actual repo path

def fetch_weather():
    """Fetch the current weather for the specified city."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        weather = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]
        wind_deg = data["wind"]["deg"]
        visibility = data["visibility"]
        return {
            "temp": temp,
            "feels_like": feels_like,
            "temp_min": temp_min,
            "temp_max": temp_max,
            "humidity": humidity,
            "pressure": pressure,
            "weather": weather,
            "wind_speed": wind_speed,
            "wind_deg": wind_deg,
            "visibility": visibility
        }
    else:
        raise Exception(f"Error fetching weather data: {response.status_code}")

def log_weather(weather_data):
    """Log weather data to a file."""
    file_path = os.path.join(GITHUB_REPO_PATH, "weather_log.txt")
    with open(file_path, "a") as file:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{now} - Weather Update:\n")
        file.write(f"Temperature: {weather_data['temp']}°C\n")
        file.write(f"Feels Like: {weather_data['feels_like']}°C\n")
        file.write(f"Min Temp: {weather_data['temp_min']}°C, Max Temp: {weather_data['temp_max']}°C\n")
        file.write(f"Humidity: {weather_data['humidity']}%\n")
        file.write(f"Pressure: {weather_data['pressure']} hPa\n")
        file.write(f"Weather: {weather_data['weather']}\n")
        file.write(f"Wind Speed: {weather_data['wind_speed']} m/s, Wind Direction: {weather_data['wind_deg']}°\n")
        file.write(f"Visibility: {weather_data['visibility']} meters\n")
        file.write("-" * 40 + "\n")

def git_commit_push():
    """Commit and push changes to GitHub with detailed commit message."""
    os.chdir(GITHUB_REPO_PATH)
    
    # Staging the file
    subprocess.run(["git", "add", "weather_log.txt"])
    
    # Creating a detailed commit message
    commit_message = (
        f"Weather Log Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Logged temperature, humidity, pressure, wind speed, and other weather details.\n"
        f"Weather conditions: Light rain, cloudy skies with temperatures ranging from 11-13°C."
    )
    
    # Committing the changes
    subprocess.run(["git", "commit", "-m", commit_message])
    
    # Pushing the changes to GitHub
    result = subprocess.run(["git", "push"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error pushing to GitHub:")
        print(result.stderr)
    else:
        print("Changes pushed to GitHub successfully.")

def main():
    try:
        weather_data = fetch_weather()
        log_weather(weather_data)
        git_commit_push()
        print("Weather log updated successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()



##
