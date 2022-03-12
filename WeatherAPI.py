import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


API_key_weather = os.getenv("API_key_weather")

user_city = input('Enter city: ')
user_country = input('Country[ example: ph, kr, jp, au, us and etc.]: ')
weather_data = \
    requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={user_city},{user_country}&'
                 f'appid={API_key_weather}&units=imperial')

data = weather_data.json()
with open('weatherData.json', 'w') as f:
    json.dump(data, f, indent=2)  #To provide a json file of weather_data variable. because request.get(url)
                                # returns json format
if data['cod'] == '404':
    print(f"{user_city} City doesn't exist")

elif data['cod'] == 200:
    wd_main = data['weather'][0]['main']
    wd_description = data['weather'][0]['description']
    wd_temp_F = data['main']['temp'] #will return Fahrenheit becuase of &units=imperial on url
    wd_humidity = data['main']['humidity']
    wd_wind = data['wind']['speed']
    wd_sunrise = data['sys']['sunrise']
    wd_sunset = data['sys']['sunset']
    wd_dt = data['dt']

    #code below: converts Fahrenheit into Celsius.
    wd_temp_convert = (wd_temp_F - 32)*5/9
    wd_temp_C = round(wd_temp_convert, 2) #round off 2 decimal point.

    #This API (https://openweathermap.org/) gives Unix Epoch timestamp e.g 1644573532 data for sunset and sunrise.
    #The code below will convert it into readable datetime format. [Month(Name) day,year hour:minute:second AM/PM]
    wd_sunrise2 = int(wd_sunrise)
    wd_sunset2 = int(wd_sunset)
    srise = datetime.fromtimestamp(wd_sunrise2).strftime('%B %d,%Y %I:%M:%S %p')
    sset = datetime.fromtimestamp(wd_sunset2).strftime('%B %d,%Y %I:%M:%S %p')

    #wind speed: meter/sec to km/hr
    wd_wind_converted = wd_wind * (1/1000) * (60) * (60)
    wd_wind_converted = round(wd_wind_converted, 2)

    #dt: Date of calculation of data based from the API
    wd_dt = int(wd_dt)
    wd_dt2 = datetime.fromtimestamp(wd_dt).strftime('%B %d,%Y %I:%M:%S %p')
    print('----------------------------------------------------------')
    print(f"{datetime.now().strftime('%B %d,%Y %I:%M:%S %p')}")
    print(f"{user_city},{data['sys']['country']}")
    print('----------------------------------------------------------')
    print(f'Date of calculation of data: {wd_dt2}')
    print(f'The weather today is: {wd_main}, {wd_description}')
    print(f"Current temperature: {wd_temp_F} °F or {wd_temp_C} °C")
    print(f'Wind speed: {wd_wind_converted} km/hr')
    print(f"Humidity: {wd_humidity}%")
    print(f"Sunrise Time: {srise}")
    print(f"Sunset Time: {sset}")


    print(f'\nOther Information:\n')
    for key,value in data['main'].items():
        temp_value = ['temp','temp_min','temp_max','feels_like']
        if key in temp_value:
            value = (value - 32)*5/9
            value = (round(value, 2))
            value = f'{value} °C'
        print(key, value)




# print(weather_data.status_code) #status code. e.g. (200=OK) (404 = Not found)
# print(json.dumps(data, indent=2)) #to check the dictionary but the oject are string
