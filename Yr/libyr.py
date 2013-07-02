#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils import Connect, Location, Cache
import datetime, json
import xml.etree.cElementTree as et

class Yr:
    def __init__(self, location, language):
        self.location = (location.decode('utf-8'))
        self.language = (language)
        self.yr_credit = {}
        self.yr_credit['credit'] = { "text": "Værvarsel fra yr.no, levert av NRK og Meteorologisk institutt", 
                            "url": "http://www.yr.no/", }

    def temperature(self):
        """
        Get temperature from yr and return it.
        """
        cache = Cache(self.location, "temperature")
        if cache.exists() and cache.is_fresh():
            return json.loads(cache.read())

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
            out.append(self.yr_credit)
            cache.write(json.dumps(out))
            return json.dumps(out)

    def wind_speed(self):
        """
        Get wind speed from yr.
        """
        cache = Cache(self.location, "windspeed")
        if cache.exists() and cache.is_fresh():
            return json.loads(cache.read())

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
            out.append(self.yr_credit)
            cache.write(json.dumps(out))
            return json.dumps(out)

    def wind_direction(self):
        """
        Get wind direction from yr.
        """
        cache = Cache(self.location, "wind_direction")
        if cache.exists() and cache.is_fresh():
            return json.loads(cache.read())

        location = Location(self.location, self.language).find()
        data = (Connect(location).read())
        data = (et.fromstring(data))
        out = []
        for parent in data[5].iter('windDirection'):
            if parent.attrib:
                out.append({
                    'location': self.location,
                    'deg': parent.attrib['deg'],
                    'code': parent.attrib['code'],
                    'name': parent.attrib['name'],
                })
            out.append(self.yr_credit)
            cache.write(json.dumps(out))
            return json.dumps(out)

    def forecast(self):
        cache = Cache(self.location, "forecast")
        if cache.exists() and cache.is_fresh():
            return json.loads(cache.read())

        location = Location(self.location, self.language).find()
        data = (Connect(location).read())
        data = (et.fromstring(data))
        days = []
        for parent in data[5][0].iter('text'):
            for child in parent[0]:
                days.append({
                    'from': child.get('from'), 
                    'to': child.get('to'), 
                    child[0].tag: child[0].text, 
                    child[1].tag: child[1].text,
                    'location': self.location,
                })
        days.append(self.yr_credit)
        cache.write(json.dumps(days))
        return json.dumps(days)

    def observations(self):
        cache = Cache(self.location, "observations")
        if cache.exists() and cache.is_fresh():
            return json.loads(cache.read())

        location = Location(self.location, self.language).find()
        data = (Connect(location).read())
        data = (et.fromstring(data))
        observations = {}
        obs_list = []
        for parent in data[6].iter('weatherstation'):
            stno = parent.attrib['stno']
            observations[stno] = parent.attrib
            for child in parent:
                tag = child.tag
                observations[stno][tag] = child.attrib
        observations['credit'] = self.yr_credit
        cache.write(json.dumps(observations))
        return json.dumps(observations)
