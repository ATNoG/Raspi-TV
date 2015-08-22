import pyowm
import sqlite3 as sql

conn = sql.connect('../db/raspi-tv.sqlite', check_same_thread=False)

# sign in at http://home.openweathermap.org/users/sign_up
# and get the API Key and paste bellow:
owm = pyowm.OWM('9a1dd6da7dec9485cacbe5ea25ed40de')

# forecast = owm.daily_forecast("Aveiro,pt")
#tomorrow = pyowm.timeutils.tomorrow()
#forecast.will_be_sunny_at(tomorrow)


def get_weather():
    try:
        location = conn.execute('SELECT * FROM HTMLSettings WHERE idName=?', ('weather',)).fetchone()[1]
        observation = owm.weather_at_place(location+',pt')
    except:
        observation = owm.weather_at_place('Aveiro,pt')

    # Search for current weather

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