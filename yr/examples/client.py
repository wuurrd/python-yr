#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from libyr import Yr
import json

weather = Yr('Oslo', 'nb')
temperature = weather.temperature()
windspeed = weather.wind_speed()
winddirection = weather.wind_direction()
forecast = weather.forecast()
observations = weather.observations()

print "wind speed:", windspeed
print "wind direction:", winddirection
print "temperature:", temperature
print "forecast", forecast
print "observations", observations
print json.dumps(temperature, indent=4)
