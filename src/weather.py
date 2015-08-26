import pyowm
import sqlite3 as sql
import requests

# forecast = owm.daily_forecast("Aveiro,pt")
#tomorrow = pyowm.timeutils.tomorrow()
#forecast.will_be_sunny_at(tomorrow)


def get_weather():

    try:
        response = requests.get("https://www.google.pt")
        # sign in at http://home.openweathermap.org/users/sign_up
        # and get the API Key and paste bellow:
        owm = pyowm.OWM('9a1dd6da7dec9485cacbe5ea25ed40de')
        # Search for current weather
        observation = owm.weather_at_place('Aveiro,pt')
        weather = observation.get_weather()

        db = sql.connect('../db/raspi-tv.sqlite')
        db.execute("DELETE FROM Weather;")

        wind = weather.get_wind()
        wind = wind['speed']*10
        humidity = weather.get_humidity()
        temperature = weather.get_temperature('celsius')
        temperature = temperature['temp']
        code = weather.get_weather_code()

        db.execute("INSERT INTO Weather VALUES (?,?,?,?)", (wind, humidity, temperature, code))
        db.commit()
        db.close()

        return {'weather': {'wind': wind,
                            'humidity': humidity,
                            'temperature': temperature,
                            'status': code
                            }
                }
    except Exception:
        db = sql.connect('../db/raspi-tv.sqlite')
        wind = db.execute("SELECT Wind FROM Weather;").fetchone()
        humidity = db.execute("SELECT Humidity FROM Weather;").fetchone()
        temperature = db.execute("SELECT Temperature FROM Weather;").fetchone()
        status = db.execute("SELECT Weather_Code FROM Weather;").fetchone()

        return {'weather': {'wind': wind[0],
                            'humidity': humidity[0],
                            'temperature': temperature[0],
                            'status': status[0]
                            }
                }
