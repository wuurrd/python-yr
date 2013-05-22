#!/usr/bin/python
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from libweather import Yr as Weather

temperature = Weather("Norge/Oslo/Oslo/Oslo").get_temperature()
print(temperature)
