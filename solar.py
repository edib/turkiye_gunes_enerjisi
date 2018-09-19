# -*- coding: utf-8 -*-
from pysolar.solar import *
from datetime import datetime,timedelta
from geopy.geocoders import Nominatim
import pandas as pd
import warnings

#Tqdm var ise import et yoksa tqdm fonksiyonunu taklit et
try:
        from tqdm import tqdm
except ModuleNotFoundError as e:
        def tqdm(iterable, *argv):
                return iterable
'''
Enum class
Zaman seviyelerini tutar
'''
class TimeResolution():
	SECONDS = 1
	MINUTES = 60
	HOURS = 3600
	DAYS = 86400

'''
Verilen base zaman üzerinden yine verilen TimeResolution kadar ileriye Zaman
üreten generator.
'''
def timeGenerator(base,TimeResolution):
	for x in range(0,31536000,TimeResolution):
		yield base + timedelta(seconds = x)

def timeMod(base,delta):
    seconds = int((base - datetime.min).total_seconds())
    return timedelta(seconds=seconds % delta.total_seconds())
#Pysolar'ın verdiği warning'i suppress etmek için eklenen ignore
warnings.filterwarnings('ignore')
geolocator = Nominatim(user_agent="turkiye_gunes_enerjisi")
cityList = pd.read_csv("tr_iller.csv",usecols=['city'])
whole_year = 24*365
my_time = datetime(2018,1,1,0,0)
print("City", "Sun Altitude","Hour,Watt/m2")
output = []
CALCULATIONRESOLUTION   = TimeResolution.MINUTES
TARGETRESOLUTION        = TimeResolution.MINUTES
TARGETPRECISION 	= 6
with open("solartimes.txt",mode='w',encoding='utf-8') as f:
    for city in tqdm(cityList['city'].values,desc="Şehirler",unit="Şehir"): #:
        location = geolocator.geocode(city)
        # calculate for every hour for 2018
        stepsGenerator = timeGenerator(my_time,CALCULATIONRESOLUTION)
        targetTimeDelta = timedelta(seconds = TARGETRESOLUTION)
        totalWattage = 0
        prev_time = 0
        for my_time in tqdm(iterable=stepsGenerator,desc=city,total=31536000/CALCULATIONRESOLUTION,ncols=100,unit="#"):
            if timeMod(my_time,targetTimeDelta).seconds == 0:
                if totalWattage >= (10 ** -TARGETPRECISION):
                    totalWattage /= (TARGETRESOLUTION / CALCULATIONRESOLUTION)
                    print((("City: {}\tSun Altitude {}\tTime: {}\tWatt/m2: {:."+str(TARGETPRECISION)+"f}").format(city, sun_alt, prev_time, totalWattage)),file=f)
                prev_time = my_time
                totalWattage = 0
            sun_alt = get_altitude(location.latitude, location.longitude, my_time)
            if sun_alt > 0 :
                totalWattage += radiation.get_radiation_direct(my_time, sun_alt)
