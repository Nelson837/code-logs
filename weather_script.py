#!/usr/bin/env python3
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from datetime import datetime

# Fetch API key and city from environment variables (set these in GitHub Secrets or Actions)
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
CITY = os.getenv("CITY", "London")
EMAIL = "nelsonviofficial@gmail.com"  # Replace with your personal email
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = os.getenv("EMAIL_USER")  # Your email address, set in GitHub Secrets
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Email password or app-specific password, set in GitHub Secrets

def fetch_weather():
    """Fetch the current weather for the specified city."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["name"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "temp_min": data["main"]["temp_min"],
            "temp_max": data["main"]["temp_max"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "weather": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "wind_deg": data["wind"]["deg"],
            "visibility": data["visibility"]
        }
    else:
        raise Exception(f"Error fetching weather data: {response.status_code}")

def send_email(weather_data):
    """Send an HTML email with weather data."""
    # Email content
    subject = f"Daily Weather Report for {weather_data['city']} - {datetime.now().strftime('%Y-%m-%d')}"
    body = f"""
    <html>
    <body>
        <h1 style="color: #0073e6;">🌤 Daily Weather Report for {weather_data['city']} 🌤</h1>
        <p>Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <table style="border-collapse: collapse; width: 100%; text-align: left;">
            <tr style="background-color: #f2f2f2;">
                <th style="padding: 8px; border: 1px solid #ddd;">Description</th>
                <th style="padding: 8px; border: 1px solid #ddd;">Details</th>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">Temperature</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{weather_data['temp']}°C</td>
            </tr>
            <tr style="background-color: #f9f9f9;">
                <td style="padding: 8px; border: 1px solid #ddd;">Feels Like</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{weather_data['feels_like']}°C</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">Min / Max Temp</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{weather_data['temp_min']}°C / {weather_data['temp_max']}°C</td>
            </tr>
            <tr style="background-color: #f9f9f9;">
                <td style="padding: 8px; border: 1px solid #ddd;">Humidity</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{weather_data['humidity']}%</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">Pressure</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{weather_data['pressure']} hPa</td>
            </tr>
            <tr style="background-color: #f9f9f9;">
                <td style="padding: 8px; border: 1px solid #ddd;">Weather</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{weather_data['weather']}</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">Wind</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{weather_data['wind_speed']} m/s, {weather_data['wind_deg']}°</td>
            </tr>
            <tr style="background-color: #f9f9f9;">
                <td style="padding: 8px; border: 1px solid #ddd;">Visibility</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{weather_data['visibility']} meters</td>
            </tr>
        </table>
        <p>Stay safe and have a great day! 🌈</p>
    </body>
    </html>
    """

    # Create the email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL
    msg.attach(MIMEText(body, "html"))

    # Send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, EMAIL, msg.as_string())

def main():
    try:
        weather_data = fetch_weather()
        send_email(weather_data)
        print("Weather email sent successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
