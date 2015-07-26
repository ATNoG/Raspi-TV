import pyowm

# sign in at http://home.openweathermap.org/users/sign_up
# and get the API Key and paste bellow:
owm = pyowm.OWM('9a1dd6da7dec9485cacbe5ea25ed40de')

# forecast = owm.daily_forecast("Aveiro,pt")
#tomorrow = pyowm.timeutils.tomorrow()
#forecast.will_be_sunny_at(tomorrow)


def get_weather():
    # Search for current weather
    observation = owm.weather_at_place('Aveiro,pt')
    weather = observation.get_weather()
    return {'weather': {'wind': weather.get_wind(),
                        'humidity': weather.get_humidity(),
                        'temperature': weather.get_temperature('celsius'),
                        # http://openweathermap.org/weather-conditions
                        'weather_code': weather.get_weather_code()
                        }
            }

if __name__ == '__main__':
    resp = get_weather()
    print resp