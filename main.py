# Required Libraries
# import os
# import pytz
import pyowm
import streamlit as st
# import requests
from matplotlib import dates, rcParams
from datetime import datetime
import matplotlib.pyplot as plt

# city = "delhi"
# API_key = ""
# base_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_key}"
# data = requests.get(base_url)
# json = data.json()
# data1 = json['list']
# print(data1[0]['main']['temp'])
# print(data1[1]['main']['temp'])
# j = json['main']
# print(json)
# j = json['main']['temp']
# for i in data:
#     print(i)
# json = list(data)
# print(json[5])

# print(j)

# OR
#################################################################################
# # OWM API Key
#
owm = pyowm.OWM("861e0910dc1ecd1c58b5e20d16d3461d")
#
# Title
st.set_page_config(layout="centered")
st.title("5 Day Weather Forecast ☀️")

st.write('##### 📌 Made By Sahil Raj Kumar')
st.write("#### Write the name of a City and select the Temperature Unit and Graph Type")

# Location text input
place = st.text_input("NAME OF THE CITY 🏙️", "")

# select box unit graph type
unit = st.selectbox("Select Temperature Unit 🌡️", ("Celsius", "Fahrenheit"))
graph_type = st.selectbox("Select Graph Type 📈", ("Line Graph", "Bar Graph"))

# Submit Button
b = st.button("SUBMIT")
# warning
st.set_option('deprecation.showPyplotGlobalUse', False)

# Plotting Graphs
def plot_line(days, min_t, max_t):
    days = dates.date2num(days)
    rcParams['figure.figsize'] = 6, 4
    plt.plot(days, max_t, color='black', linestyle='solid', linewidth=1, marker='o', markerfacecolor='green',
             markersize=7)
    plt.plot(days, min_t, color='black', linestyle='solid', linewidth=1, marker='o', markerfacecolor='blue',
             markersize=7)
    plt.ylim(min(min_t) - 4, max(max_t) + 4)  # ylimits
    plt.xticks(days)  # x_axis
    x_y_axis = plt.gca()  # get current axis
    xaxis_format = dates.DateFormatter('%d/%m')

    x_y_axis.xaxis.set_major_formatter(xaxis_format)
    plt.grid(True, color='brown')
    plt.legend(["Maximum Temperature", "Minimum Temperature"], bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xlabel('Dates(dd/mm)', size=12)
    plt.ylabel('Temperature', size=12)
    plt.title('5-Day Weather Forecast', size=15)

    for i in range(6):
        plt.text(days[i], min_t[i] - 1.5, min_t[i],
                 horizontalalignment='center',
                 verticalalignment='bottom',
                 color='black')
    for i in range(6):
        plt.text(days[i], max_t[i] + 0.5, max_t[i],
                 horizontalalignment='center',
                 verticalalignment='bottom',
                 color='black')
    # plt.show()
    # plt.savefig('figure_line.png')
    st.pyplot()
    plt.clf()


def plot_bars(days, min_t, max_t):
    # print(days)
    days = dates.date2num(days)
    rcParams['figure.figsize'] = 6, 4
    min_temp_bar = plt.bar(days - 0.2, min_t, width=0.4)
    max_temp_bar = plt.bar(days + 0.2, max_t, width=0.4)
    plt.xticks(days)
    x_y_axis = plt.gca()
    xaxis_format = dates.DateFormatter('%d/%m')

    x_y_axis.xaxis.set_major_formatter(xaxis_format)
    plt.legend(["Maximum Temperature", "Minimum Temperature"], bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xlabel('Dates(dd/mm)', size=12)
    plt.ylabel('Temperature', size=12)
    plt.title('5-Day Weather Forecast', size=15)

    for bar_chart in [min_temp_bar, max_temp_bar]:
        for index, bar in enumerate(bar_chart):
            height = bar.get_height()
            xpos = bar.get_x() + bar.get_width() / 2.0
            ypos = height
            label_text = str(int(height))
            plt.text(xpos, ypos, label_text,
                     horizontalalignment='center',
                     verticalalignment='bottom',
                     color='black')
    st.pyplot()
    plt.clf()


# Main function
def weather_detail(place, unit, g_type):
    mgr = owm.weather_manager()
    days = []
    dates_2 = []
    min_t = []
    max_t = []
    forecaster = mgr.forecast_at_place(place, '3h')
    forecast = forecaster.forecast
    obs = mgr.weather_at_place(place)
    weather = obs.weather
    temperature1 = weather.temperature(unit='celsius')['temp']
    if unit == 'Celsius':
        unit_c = 'celsius'
    else:
        unit_c = 'fahrenheit'

    for weather in forecast:
        day = datetime.utcfromtimestamp(weather.reference_time())  # 2022-11-04 15:00:00..
        date1 = day.date()  # 2022-11-04...
        if date1 not in dates_2:
            dates_2.append(date1)
            min_t.append(None)
            max_t.append(None)
            days.append(date1)
        temperature = weather.temperature(unit_c)['temp']
        if not min_t[-1] or temperature < min_t[-1]:
            min_t[-1] = temperature
        if not max_t[-1] or temperature > max_t[-1]:
            max_t[-1] = temperature

    obs = mgr.weather_at_place(place)
    weather = obs.weather
    st.write(f"## 📍 Weather at {place[0].upper() + place[1:]} currently: ")
    if unit_c == 'celsius':
        st.write(f"### 🌡️ Temperature: {temperature1} °C")
    else:
        st.write(f"### 🌡️  Temperature: {temperature1} F")
    st.write(f"### ☁️ Sky: {weather.detailed_status}")
    st.write(f"### 🌪  Wind Speed: {round(weather.wind(unit='km_hour')['speed'])} km/h")
    st.write(f"### ⛅️Sunrise Time : {weather.sunrise_time(timeformat='iso')} GMT")
    st.write(f"### ☁️  Sunset Time : {weather.sunset_time(timeformat='iso')} GMT")

    # Expected Temperature Alerts
    st.write("## ❄️Expected Temperature Changes/Alerts: ")
    if forecaster.will_have_fog():
        st.write("#### ▶️FOG ALERT🌁!!")
    if forecaster.will_have_rain():
        st.write("#### ▶️RAIN ALERT☔!!")
    if forecaster.will_have_storm():
        st.write("#### ▶️STORM ALERT⛈️!!")
    if forecaster.will_have_snow():
        st.write("#### ▶️ SNOW ALERT❄️!!")
    if forecaster.will_have_tornado():
        st.write("#### ▶️TORNADO ALERT🌪️!!")
    if forecaster.will_have_hurricane():
        st.write("#### ▶️HURRICANE ALERT🌀")
    if forecaster.will_have_clear():
        st.write("#### ▶️CLEAR WEATHER PREDICTED🌞!!")
    if forecaster.will_have_clouds():
        st.write("#### ▶️CAN HAVE CLOUDY SKIES⛅")

    st.write('                ')
    st.write('                ')

    if g_type == "Line Graph":
        plot_line(days, min_t, max_t)
    elif g_type == "Bar Graph":
        plot_bars(days, min_t, max_t)

    # To give max and min temperature
    i = 0
    st.write(f"## 📆 Date :  Max - Min  ({unit})")
    for obj in days:
        ta = (obj.strftime("%d/%m"))
        st.write(f'#### ➡️ {ta} :\t   ({max_t[i]} - {min_t[i]})')
        i += 1


if b:
    if place != "":
        try:
            weather_detail(place, unit, graph_type)

        except:
            st.warning("Please enter a Valid city name", icon="⚠️")

# # st.write(w)
# #
# # def forecast1(city, t="3h"):
# #     daily_forecast = mgr.forecast_at_place(city, t)
# #     forecast = daily_forecast.forecast
# #     a = []
# #     for i in forecast:
# #         a.append(i)
# #     return forecast
#
# # def forecast1(city, t="3h"):
# #     daily_forecast = mgr.forecast_at_place(city, t)
# #     forecast = daily_forecast.forecast
# #     return forecast
# #
#
# # print(forecast1('Tokyo,JP'))
# mgr = owm.weather_manager()
# daily_forecast = mgr.forecast_at_place('Tokyo,JP', "3h")
# forecast = daily_forecast.forecast
#
# for i in forecast:
#     print(i)
# #
# observation = mgr.weather_at_place('Tokyo,JP')
# weather = observation.weather
# print(weather)
# temp = weather.temperature("celsius")
# print(temp)
# #
# #
# # st.write(temp)
# # print(forecast)
# # print(dir(forecast))
# # print(dir(weather))
