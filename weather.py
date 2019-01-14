from guizero import App, Text, MenuBar, Combo
import math
import requests
from datetime import datetime
from meteocalc import Temp, heat_index
import api_key


# functions

# quit function
def quit_program():
    exit()

# convert unix time to standard time
def convert_unix_time(unix_code):
    timestamp = int(unix_code)
    return(datetime.utcfromtimestamp(timestamp).strftime('%H:%M'))

# wind chill factor, v = wind speed in km, t = temp in celsius
def get_wind_chill(v, t):
    return int(13.12 + 0.6215*t -  11.37*math.pow(v, 0.16) + 0.3965*t*math.pow(v, 0.16))

# heat index
def get_heat_index(temp, humid):
    return int(heat_index(temperature=temp, humidity=humid))

# dropdown menu
def selection(selected_value):
    if selected_value == "Toronto, ON":
        display_text.value = display_info("Toronto")
    elif selected_value == "Ottawa, ON":
        display_text.value = display_info("Ottawa")
    elif selected_value == "Sydney, AUS":
        display_text.value = display_info("Sydney")

# weather gets
def get_temperature(data):
    return int(data['main']['temp'] - 273)

def get_conditions(data):
    return data['weather'][0]['description']

def get_humidity(data):
    return data['main']['humidity']

def get_sunrise(data):
    return data['sys']['sunrise']-18000

def get_sunset(data):
    return data['sys']['sunset']-18000

def get_wind_speed(data):
    return data['wind']['speed']*3.6

# displays
def display_info(city):
    # API key, request, JSON dictionary pull
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID={}'.format(city,api_key.api_key)

    res = requests.get(url)

    data = res.json()

    if get_temperature(data) > 20 and get_heat_index(get_temperature(data), get_humidity(data)) > get_temperature(data):
        text = "\nTemperature: {}\nHeat Index: {}\nConditions: {}\nSunrise: {}\nSunset: {}\nWind Speed: {:.2f}km/h\nHumidity: {}%".format(get_temperature(data),\
                 get_heat_index(get_temperature(data), get_humidity(data)), get_conditions(data),\
                convert_unix_time(get_sunrise(data)), convert_unix_time(get_sunset(data)), get_wind_speed(data), get_humidity(data))
    else:
        text = "\nTemperature: {}\nWind Chill: {}\nConditions: {}\nSunrise: {}\nSunset: {}\nWind Speed: {:.2f}km/h\nHumidity: {}%".format(get_temperature(data),\
                get_wind_chill(get_wind_speed(data), get_temperature(data)), get_conditions(data),\
                convert_unix_time(get_sunrise(data)), convert_unix_time(get_sunset(data)), get_wind_speed(data), get_humidity(data))

    return text

# end functions

# creates window, title Weather
app = App(title="Weather", width="300", height="260", bg="white")

# menu bar
menubar = MenuBar(app,
                toplevel=["File"],
                options=[
                [["Quit", quit_program]]
                ])

# displays opening message
message = Text(app,text="Choose a city to see the weather.", align="center")

# creates dropdown menu
dropdown = Combo(app, options=["","Ottawa, ON", "Toronto, ON", "Sydney, AUS"], selected="", command=selection)

display_text = Text(app)

# displays the entire app
app.display()
