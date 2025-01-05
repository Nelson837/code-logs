#!/usr/bin/env python3
import os
import subprocess
import requests
from datetime import datetime

# Set your API key for OpenWeatherMap
API_KEY = "e9fa5b284140437597ef45f6a648cf24"  # Replace with your API key
CITY = "Kuwait City"  # Replace with your city
GITHUB_REPO_PATH = "/path/to/your/repo"  # Replace with your local repository path

def fetch_weather():
    """Fetch the current weather for the specified city."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        return temp, weather
    else:
        raise Exception(f"Error fetching weather data: {response.status_code}")

def log_weather(temp, weather):
    """Log weather data to a file."""
    file_path = os.path.join(GITHUB_REPO_PATH, "weather_log.txt")
    with open(file_path, "a") as file:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{now} - Temperature: {temp}°C, Weather: {weather}\n")

def git_commit_push():
    """Commit and push changes to GitHub."""
    os.chdir(GITHUB_REPO_PATH)
    subprocess.run(["git", "add", "weather_log.txt"])
    commit_message = f"Weather log update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    subprocess.run(["git", "commit", "-m", commit_message])
    result = subprocess.run(["git", "push"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error pushing to GitHub:")
        print(result.stderr)
    else:
        print("Changes pushed to GitHub successfully.")

def main():
    try:
        temp, weather = fetch_weather()
        log_weather(temp, weather)
        git_commit_push()
        print("Weather log updated successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
