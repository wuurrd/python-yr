#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from libyr import Yr

weather = Yr('Porsgrunn', 'nb')
temperature = weather.temperature()
windspeed = weather.wind_speed()
winddirection = weather.wind_direction()

print("linje 1", windspeed)
print("linje 2", winddirection)
print("linje 3", temperature)
print("Temperatur: %s %s, vind: %s, %s %s").encode("utf-8") % (temperature['value'], temperature['unit'], windspeed['name'], windspeed['mps'], windspeed['unit'])
