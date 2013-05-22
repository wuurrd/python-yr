#!/usr/local/bin/python
from libweather import Yr as Weather

weather = Weather("Skien")
print(weather.return_place())
