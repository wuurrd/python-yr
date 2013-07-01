#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils import Connect, Location
import datetime, json
import xml.etree.cElementTree as et

class Yr:
    def __init__(self, location, language):
        self.location = (location.decode('utf-8'))
        self.language = (language)

    def temperature(self):
        """
        Get temperature from yr and return it.
        """
        location = (Location(self.location, self.language).find())
        data = (Connect(location).read())
        data = (et.fromstring(data)) 
        out = []
        for temperature in data[5].iter('temperature'):
            if temperature.attrib:
                out.append({
                    'unit': temperature.attrib['unit'],
                    'value': temperature.attrib['value'],
                    'location': self.location,
                 })
                return json.dumps(out)

    def wind_speed(self):
        """
        Get wind speed from yr.
        """
        location = (Location(self.location, self.language).find())
        data = (Connect(location).read())
        data = (et.fromstring(data))
        out = []
        for wind in data[5].iter('windSpeed'):
            if wind.attrib:
                out.append({
                    'location': self.location,
                    'mps': wind.attrib['mps'],
                    'unit': str('mps'),
                    'name': wind.attrib['name'],
                })
                return json.dumps(out)

    def wind_direction(self):
        """
        Get wind direction from yr.
        """
        location = Location(self.location, self.language).find()
        data = (Connect(location).read())
        data = (et.fromstring(data))
        out = []
        for wind in data[5].iter('windDirection'):
            if wind.attrib:
                out.append({
                    'location': self.location,
                    'deg': wind.attrib['deg'],
                    'code': wind.attrib['code'],
                    'name': wind.attrib['name'],
                })
                return json.dumps(out)

    def forecast(self):
        location = Location(self.location, self.language).find()
        data = (Connect(location).read())
        data = (et.fromstring(data))
        days = []
        for items in data[5][0].iter('text'):
            for child in items[0]:
                days.append({
                    'from': child.get('from'), 
                    'to': child.get('to'), 
                    child[0].tag: child[0].text, 
                    child[1].tag: child[1].text,
                    'location': self.location,
                })
            return json.dumps(days)
