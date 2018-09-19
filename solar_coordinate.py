from pysolar.solar import *
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
import pandas as pd


class timeResolution():
        SECONDS = 1
        MINUTES = 60
        HOURS = 3600
        DAYS = 86400

def timeGenerator(base,timeResolution):
        for x in range(0,31536000,timeResolution):
                yield base + timedelta(seconds = x)

def curr_day_starttime():
        now = datetime.now()
        return datetime(now.year,now.month,now.day,0,0)

geolocator = Nominatim(user_agent="test")
my_time = curr_day_starttime()
print(my_time)
cityList = pd.read_csv("tr_iller.csv",usecols=['city'])

for city in cityList['city'].loc[1:1].values:
       	location = geolocator.geocode(city)
        for min in range(0,60*24):
                sun_alt = get_altitude(location.latitude, location.longitude, my_time)
                sun_azim = -(get_azimuth(location.latitude, location.longitude, my_time))
                my_time = my_time + timedelta(seconds = 60)
                if (sun_alt > 0):
                        print(sun_alt, sun_azim)