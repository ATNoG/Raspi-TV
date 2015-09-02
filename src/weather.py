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
        try:
            location = conn.execute('SELECT * FROM HTMLSettings WHERE idName=?', ('weather',)).fetchone()[1]
            observation = owm.weather_at_place(location+',pt')
        except Exception:
            observation = owm.weather_at_place('Aveiro,pt')
        weather = observation.get_weather()

        conn.execute("DELETE FROM Weather;")

        wind = weather.get_wind()
        wind = wind['speed']*10
        humidity = weather.get_humidity()
        temperature = weather.get_temperature('celsius')
        temperature = temperature['temp']
        code = weather.get_weather_code()
        sunrise = weather.get_sunrise_time('iso')
        sunrise = sunrise.split(" ")
        sunrise = sunrise[1].split("+")
        sunset = weather.get_sunset_time('iso')
        sunset = sunset.split(" ")
        sunset = sunset[1].split("+")

        conn.execute("INSERT INTO Weather VALUES (?,?,?,?,?,?)", (wind, humidity, temperature, code, sunrise[0], sunset[0]))
        conn.commit()
        conn.close()

        return {'weather': {'wind': wind,
                            'humidity': humidity,
                            'temperature': temperature,
                            'status': code,
                            'sunrise': sunrise[0],
                            'sunset': sunset[0]
                            }
                }
    except Exception, e:
        print e.message
        wind = conn.execute("SELECT Wind FROM Weather;").fetchone()
        humidity = conn.execute("SELECT Humidity FROM Weather;").fetchone()
        temperature = conn.execute("SELECT Temperature FROM Weather;").fetchone()
        status = conn.execute("SELECT Weather_Code FROM Weather;").fetchone()
        sunrise = conn.execute("SELECT Sunrise_Time FROM Weather;").fetchone()
        sunset = conn.execute("SELECT Sunset_Time FROM Weather;").fetchone()
        sunrise = sunrise[0].split(" ")
        sunrise = sunrise[1].split("+")
        sunset = sunset[0].split(" ")
        sunset = sunset[1].split("+")

        return {'weather': {'wind': wind[0],
                            'humidity': humidity[0],
                            'temperature': temperature[0],
                            'status': status[0],
                            'sunset': sunset[0],
                            'sunrise': sunrise[0]
                            }
                }