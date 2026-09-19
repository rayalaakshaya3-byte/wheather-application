from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get('OPENWEATHER_API_KEY')
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error_message = None

    if request.method == 'POST':
        if not API_KEY:
            return render_template('index.html', weather=None, error='Weather API key is not configured. Set OPENWEATHER_API_KEY and restart the app.')
        city = request.form.get('city')
        if city:
            # Parameters for the API request
            params = {
                'q': city,
                'appid': API_KEY,
                'units': 'metric'  # Use 'imperial' for Fahrenheit
            }
            try:
                response = requests.get(BASE_URL, params=params)
                data = response.json()

                if response.status_code == 200:
                    weather_data = {
                        'city': data['name'],
                        'country': data['sys']['country'],
                        'temperature': round(data['main']['temp']),
                        'feels_like': round(data['main']['feels_like']),
                        'humidity': data['main']['humidity'],
                        'description': data['weather'][0]['description'].title(),
                        'icon': data['weather'][0]['icon'],
                        'wind_speed': data['wind']['speed']
                    }
                else:
                    error_message = data.get('message', 'City not found. Please try again.').title()
            except requests.exceptions.RequestException:
                error_message = 'Failed to connect to weather service. Please check your network connection.'

    return render_template('index.html', weather=weather_data, error=error_message)

if __name__ == '__main__':
    app.run(debug=True)
