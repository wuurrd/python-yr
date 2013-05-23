#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from libweather import Yr as Weather
from libweather import place2url

place = Weather('Norge/Østfold/Halden/Sponvika')

temperature = place.get_temperature()

finder = place2url('Oslo')
for i in finder.find():
    print i

print temperature['value'], temperature['unit']
