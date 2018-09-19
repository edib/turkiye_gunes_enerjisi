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

#df = pd.DataFrame(, index=['time'])
pd_columns=['city','time', 'watt']
geolocator = Nominatim(user_agent="test")
my_time = curr_day_starttime()
cityList = pd.read_csv("tr_iller.csv",usecols=['city'])

'''
cols = ['city', 'time', 'watt']
lst = []
for a in range(20):
    lst.append([a*3, a*4, a*5])
df1 = pd.DataFrame(lst, columns=cols)

print(df1)
df1.to_csv("datafile1", encoding='utf-8', index=False)
'''
city_row = []
for city in cityList['city'].loc[1:1].values:
        location = geolocator.geocode(city)
        min_total = 0.0000
        hourly_average = 0.0000
        my_average = 0.0000
        for hour in range(0,60*24):
                sun_alt = get_altitude(location.latitude, location.longitude, my_time)
                if (sun_alt > 0):
                        my_rad = radiation.get_radiation_direct(my_time, sun_alt)
                        #print(my_time, my_rad)
                        min_total = min_total + my_rad
                        if (hour % 60 == 0):
                                my_average = min_total / 60
                                print(my_time - timedelta(hours=1), my_average)
                                my_average = 0.0000
                city_total = hourly_average + my_average
                my_time = my_time + timedelta(minutes=1)
        city_row.append([city, my_time, city_total])
my_df = pd.DataFrame(city_row, columns=pd_columns)
print(my_df)
#my_df.to_csv("datafile", encoding='utf-8', index=False)