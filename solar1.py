from pysolar.solar import *
from datetime import datetime, timedelta

from geopy.geocoders import Nominatim
import pandas as pd


geolocator = Nominatim(user_agent="test")

cityList = pd.read_csv("tr_iller.csv",usecols=['city'])
whole_year = 24*365
my_time = datetime(2018,1,1,0,0)
print("City", "Sun Altitude","Hour,Watt/m2")
for city in cityList['city'].values:
	location = geolocator.geocode(city)
	# calculate for every hour for 2018
	for hour in range(0,whole_year): 
		my_time = my_time + timedelta(hours=1)
		sun_alt = get_altitude(location.latitude, location.longitude, my_time)
		if sun_alt > 0: 
			print("City: {}, Sun Altitude {}, Hour: {}, Watt/m2: {}".format(city, sun_alt, my_time, 
				radiation.get_radiation_direct(my_time, sun_alt)))
		else:
			print(0)