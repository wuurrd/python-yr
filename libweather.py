#!/usr/local/bin/python
api_url = ("http://www.yr.no/sted/Norge/Telemark/Skien/Skien/varsel_time_for_time.xml")

class Yr:
    def __init__(self, place):
        self.place = place
    
    def return_place(self):
        return(self.place)
