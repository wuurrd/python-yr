#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from libweather import Yr as Weather

place = Weather('Norge/Vestfold/Tønsberg/Tønsberg')

temperature = place.get_temperature()

print temperature['value'], temperature['unit']
