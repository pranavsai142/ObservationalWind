# Weather conditions for:
# ISLA ROQUETA NEAR acapulco, null (HADS) 
# Elev: 351.0 ft; Lat/Lon: 16.82056/-99.90694
# CENTRAL TIME ZONE

# https://www.weather.gov/wrh/Timeseries?site=irqg3
# Downloaded data in kts

# The api api.weather.gov doesn't seem to service international observations,
# I cant find international stations on this list
# https://api.weather.gov/stations

# The api seems useful though



import pytz
from datetime import datetime
import json

KNOTS_TO_M_PER_S_CONVERSION = 0.514444
WEATHER_GOV_TIMESERIES_CSV = "isla_roqueta_otis_observations.csv"
WEATHER_GOV_WIND_FILE_NAME = "Weather_Gov_Wind.json"
ACAPULCO_LATITUDE = 16.82056
ACAPULCO_LONGITUDE = -99.90694

file = open(WEATHER_GOV_TIMESERIES_CSV)
times = []
timezone = pytz.timezone("America/Chicago")
speeds = []
gusts = []
directions = []
skipHeader = True
windDict = {"acapulco":{}}
for line in file:
    if(skipHeader):
        skipHeader = False
    else:
        data = line.split(",")
#         Remove first and last quote characters
        timeString = data[0][1:][:-1]
        time = datetime.strptime(timeString, "%Y-%m-%d %H:%M:%S")
        time = timezone.localize(time)
#         print(timeString)
#         print(datetime.timestamp(time))
        speed = float(data[1])
        gust = float(data[2])
        direction = float(data[3])
        print(speed, gust, direction)
        times.append(time.timestamp())
        speeds.append(speed * KNOTS_TO_M_PER_S_CONVERSION)
        gusts.append(gust * KNOTS_TO_M_PER_S_CONVERSION)
        directions.append(direction)
        print(time)
        
windDict["acapulco"]["times"] = times
windDict["acapulco"]["speeds"] = speeds
windDict["acapulco"]["gusts"] = gusts
windDict["acapulco"]["directions"] = directions
windDict["acapulco"]["latitude"] = ACAPULCO_LATITUDE
windDict["acapulco"]["longitude"] = ACAPULCO_LONGITUDE

with open(WEATHER_GOV_WIND_FILE_NAME, "w") as outfile:
    json.dump(windDict, outfile)
        
        
        