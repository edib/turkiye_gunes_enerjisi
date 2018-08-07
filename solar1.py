# -*- coding: utf-8 -*-
from pysolar.solar import *
from datetime import datetime, timedelta
from tqdm import tqdm

from geopy.geocoders import Nominatim
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
class timeResolution():
	SECONDS = 1
	MINUTES = 60
	HOURS = 3600
	DAYS = 86400

def timeGenerator(base,timeResolution):
	for x in range(0,31536000,timeResolution):
		yield base + timedelta(seconds = x)

		
geolocator = Nominatim(user_agent="test")

cityList = pd.read_csv("tr_iller.csv",usecols=['city'])
whole_year = 24*365
my_time = datetime(2018,1,1,0,0)
print("City", "Sun Altitude","Hour,Watt/m2")
output = []
selectedTimeResolution = timeResolution.MINUTES
with open("/dev/null",mode='w',encoding='utf-8') as f:
        for city in tqdm(cityList['city'].values,desc="Şehirler",unit="Şehir"): #:
                location = geolocator.geocode(city)
                # calculate for every hour for 2018
                t = timeGenerator(my_time,selectedTimeResolution)
                for my_time in tqdm(iterable=t,desc=city,total=31536000/selectedTimeResolution,unit="#"):
                        sun_alt = get_altitude(location.latitude, location.longitude, my_time)
                        if sun_alt > 0 :
                                print(("Time: {}\tCity: {}\tWatt/m2: {}".format(my_time, city, radiation.get_radiation_direct(my_time, sun_alt))),file=f)
                        #else:
                        #        print(("City: {}\tTime: {}\tWatt/m2: {}".format(city, sun_alt, my_time, 0)),file=f)