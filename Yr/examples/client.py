#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from libyr import Yr

weather = Yr('Ørje kirke', 'en')
temperature = weather.temperature()
windspeed = weather.wind_speed()

print("The wind in %s is %s %s") % (windspeed['location'], windspeed['mps'], windspeed['unit'])
print("The temperature in %s is %s %s") % (temperature['location'], temperature['value'], temperature['unit'])
