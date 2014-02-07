#!/usr/bin/env python3

import os.path, sys
parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parent_directory)
from libyr import Yr
#import json

#weather = Yr('Norge/Telemark/Skien/Skien', 'nb')
weather = Yr('Czech_Republic/Prague/Prague')
#temperature = weather.temperature()
#windspeed = weather.wind_speed()
#winddirection = weather.wind_direction()
#forecast = weather.forecast()
#observations = weather.observations()

#print('wind speed:', windspeed)
#print('wind direction:', winddirection)
#print('temperature:', temperature)
#print('forecast:', forecast)
#print('observations:', observations)
#print(json.dumps(observations, indent=4))

x = weather.xmltosoup()
x = str(x.forecast.tabular.time)
print(x)

#x = weather.xmlsource()
#print(x)
x = weather.xmltodict(x)
print(x)
x = weather.xmltojson(x)
print(x)
