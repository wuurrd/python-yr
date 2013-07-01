#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from libyr import Yr

weather = Yr('Tønsberg', 'nb')
temperature = weather.temperature()
windspeed = weather.wind_speed()
winddirection = weather.wind_direction()
forecast = weather.forecast()

print(windspeed)
print(winddirection)
print(temperature)
print(forecast)
