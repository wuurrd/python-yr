#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from libyr import Yr

temp = Yr('Ågotnes', 'en').get_temperature()

print("The temperature in %s is %s %s") % (temp['location'], temp['value'], temp['unit'])
