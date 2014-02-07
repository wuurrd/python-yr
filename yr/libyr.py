#!/usr/bin/env python3
from utils import Connect, Location, Cache
import datetime, json
import xml.etree.cElementTree as et

class Yr:
    def __init__(self, location, language):
        self.location = (location)
        self.language = (language)
        self.yr_credit = {"text": "Værvarsel fra yr.no, levert av NRK og Meteorologisk institutt", 
                            "url": "http://www.yr.no/", }

    def temperature(self):
        """
        Get temperature from yr and return it.
        """
        getlocation = (Location(self.location, self.language).find())
        cache = Cache(getlocation, "temperature")
        if cache.exists() and cache.is_fresh():
            return json.loads(cache.read())
        
        data = (Connect(getlocation).read())
        data = (et.fromstring(data)) 
        out = {}
        for parent in data[5].iter('temperature'):
            if parent.attrib:
                out['data'] = (parent.attrib)
        out['credit'] = (self.yr_credit)
        cache.write(json.dumps(out))
        return out

    def wind_speed(self):
        """
        Get wind speed from yr.
        """
        getlocation = (Location(self.location, self.language).find())
        cache = Cache(getlocation, "windspeed")
        if cache.exists() and cache.is_fresh():
            return json.loads(cache.read())

        data = (Connect(getlocation).read())
        data = (et.fromstring(data))
        out = {}
        for parent in data[5].iter('windSpeed'):
            if parent.attrib:
                out['data'] = (parent.attrib)
        out['credit'] = (self.yr_credit)
        cache.write(json.dumps(out))
        return out

    def wind_direction(self):
        """
        Get wind direction from yr.
        """
        getlocation = (Location(self.location, self.language).find())
        cache = Cache(getlocation, "wind_direction")
        if cache.exists() and cache.is_fresh():
            return json.loads(cache.read())

        data = (Connect(getlocation).read())
        data = (et.fromstring(data))
        out = {}
        for parent in data[5].iter('windDirection'):
            if parent.attrib:
                out['data'] = (parent.attrib)
        out['credit'] = (self.yr_credit)
        cache.write(json.dumps(out))
        return out

    def forecast(self):
        getlocation = (Location(self.location, self.language).find())
        cache = Cache(getlocation, "forecast")
        if cache.exists() and cache.is_fresh():
            return json.loads(cache.read())

        data = (Connect(getlocation).read())
        data = (et.fromstring(data))
        days = []
        for parent in data[5][0].iter('text'):
            for child in parent[0]:
                days.append({
                    'from': child.get('from'), 
                    'to': child.get('to'), 
                    child[0].tag: child[0].text, 
                    child[1].tag: child[1].text,
                })
        out = {}
        out['data'] = (days)
        out['credit'] = (self.yr_credit)
        cache.write(json.dumps(out))
        return out

    def observations(self):
        getlocation = (Location(self.location, self.language).find())
        cache = Cache(getlocation, "observations")
        if cache.exists() and cache.is_fresh():
            return json.loads(cache.read())

        data = (Connect(getlocation).read())
        data = (et.fromstring(data))
        observations = {}
        observations['data'] = {}
        for parent in data[6].iter('weatherstation'):
            stno = parent.attrib['stno']
            observations['data'][stno] = parent.attrib
            for child in parent:
                tag = child.tag
                observations['data'][stno][tag] = child.attrib
        observations['credit'] = self.yr_credit
        cache.write(json.dumps(observations))
        return observations

    def location_info(self):
        getlocation = (Location(self.location, self.language).find())
        cache = Cache(getlocation, "location")
        if cache.exists() and cache.is_fresh():
            return json.loads(cache.read())

        data = (Connect(getlocation).read())
        data = (et.fromstring(data))
        location_list = []
        location = {}
        #TODO: Make this more nice :-)
        for parent in data[0]:
            if parent.attrib:
                location_list.append(parent.attrib)
            else:
                location_list.append({
                    parent.tag: parent.text
                })
        location['data'] = location_list
        location['credit'] = self.yr_credit
        cache.write(json.dumps(location))
        return location
