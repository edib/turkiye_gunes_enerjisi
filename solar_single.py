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
print("City", "Sun Altitude","Hour,Watt/m2")
city = "Ankara"
location = geolocator.geocode(city)
hourly_avereage = 0.0000
for hour in range(0,60*24): 
        sun_alt = get_altitude(location.latitude, location.longitude, my_time)
        
        if sun_alt > 0:
                hourly_avereage = hourly_avereage 
                + radiation.get_radiation_direct(my_time, sun_alt)
                #if hour % 60 == 0:
                print("City: {}, Sun Altitude {}, Hour: {}, Watt/m2: {}"
                        .format(city, sun_alt, my_time, hourly_avereage/60 ))
                #hourly_avereage = 0
        my_time = my_time + timedelta(minutes=1)
