import json
import math
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

WEATHER_GOV_GFS_WIND_DATA_FILE_NAME = "Weather_Gov_GFS_Nodes_Wind_Data.json"
WEATHER_GOV_WIND_FILE_NAME = "Weather_Gov_Wind.json"
START_DATE = datetime(year=2023, month=10, day=22)
# START_DATE = datetime(year=2022, month=12, day=20)
DATE_FORMAT = "%m/%d/%y-%HZ"

def extractLatitudeIndex(nodeIndex):
    return int(nodeIndex[1: nodeIndex.find(",")])
    
def extractLongitudeIndex(nodeIndex):
    return int(nodeIndex[nodeIndex.find(",") + 1: nodeIndex.find(")")])
    
def vectorSpeed(x,y):
    return math.sqrt(x**2 + y**2)
    
def vectorDirection(x,y):
    degrees = math.degrees(math.atan2(y,x))
    if(degrees < 0):
        return degrees + 360
    return degrees
    
def unixTimeToDeltaHours(timestamp):
    delta = datetime.fromtimestamp(timestamp) - START_DATE
    return delta.total_seconds()/3600
    
def extrapolateWindToTenMeterHeight(windVelocity, altitude):
    return windVelocity
#     WIND_PROFILE_EXPONENT = 0.11
#     return windVelocity * ((10.0/altitude)**WIND_PROFILE_EXPONENT)


gfsNodesWindData = {}
windData = {}
    
with open(WEATHER_GOV_GFS_WIND_DATA_FILE_NAME) as outfile:
    gfsNodesWindData = json.load(outfile)
    
with open(WEATHER_GOV_WIND_FILE_NAME) as outfile:
    windData = json.load(outfile)

weatherGovLatitudes = []
weatherGovLongitudes = []
stationLabels = []
gfsNodesLatitudes = []
gfsNodesLongitudes = []
gfsNodesLabels = []
gfsNodesTimes = []
gfsNodesWindDirections = []
gfsNodesWindSpeeds = []
weatherGovTimes = []
weatherGovWindDirections = []
weatherGovWindSpeeds = []

weatherGovLatitudes.append(windData["acapulco"]["latitude"])
weatherGovLongitudes.append(windData["acapulco"]["longitude"])
stationLabels.append("acapulco")
times = []
for time in windData["acapulco"]["times"]:
    times.append(unixTimeToDeltaHours(time))
weatherGovTimes.append(times)
weatherGovWindDirections.append(windData["acapulco"]["directions"])
weatherGovWindSpeeds.append(windData["acapulco"]["speeds"])

for nodeIndex in gfsNodesWindData.keys():
    gfsNodesLabels.append(nodeIndex)
    gfsNodesLatitudes.append(gfsNodesWindData[nodeIndex]["latitude"])
    gfsNodesLongitudes.append(gfsNodesWindData[nodeIndex]["longitude"])
    gfsStationWindsX = gfsNodesWindData[nodeIndex]["windsX"]
    gfsStationWindsY = gfsNodesWindData[nodeIndex]["windsY"]
    gfsStationTimes = []
    gfsStationWindDirections = []
    gfsStationWindSpeeds = []
    gfsStationRains = []
    for index in range(len(gfsNodesWindData[nodeIndex]["times"])):
        gfsStationTimes.append(unixTimeToDeltaHours(gfsNodesWindData[nodeIndex]["times"][index]))
        gfsWindX = gfsNodesWindData[nodeIndex]["windsX"][index]
        gfsWindY = gfsNodesWindData[nodeIndex]["windsY"][index]
        gfsWindSpeed = vectorSpeed(gfsWindX, gfsWindY)
        gfsWindDirection = vectorDirection(gfsWindX, gfsWindY)
        gfsStationWindDirections.append(gfsWindDirection)
        gfsStationWindSpeeds.append(gfsWindSpeed)
    
    gfsNodesTimes.append(gfsStationTimes)
    gfsNodesWindDirections.append(gfsStationWindDirections)
    gfsNodesWindSpeeds.append(gfsStationWindSpeeds)
   
# Print 10th wind entry for 0th station
print(weatherGovTimes[0][10])
print(weatherGovWindDirections[0][10])
print(weatherGovWindSpeeds[0][10])

# Print 10th wind entry for 0th station gfs node
print(gfsNodesTimes[0][10])
print(gfsNodesWindDirections[0][10])
print(gfsNodesWindSpeeds[0][10])
    
# setting the size of the map
# fig = plt.figure(figsize=(12,9))
# m = Basemap(projection = 'mill', llcrnrlat = -90, urcrnrlat = 90, llcrnrlon = -180, urcrnrlon = 180, resolution = 'c')
# drawing the coastline
# m.drawcoastlines()
# m.drawcountries(color='gray')
# m.drawstates(color='gray')
# 
# plotting the map
# m.scatter(adcircLongitudes, adcircLat, latlon = True, s = 10, c = 'red', marker = 'o', alpha = 1)
# 
# plt.show()

# Plot lat long points of nodes and stations in wind data

fig, ax = plt.subplots()
ax.scatter(gfsNodesLongitudes, gfsNodesLatitudes, label="GFS")
ax.scatter(weatherGovLongitudes, weatherGovLatitudes, label="WeatherGov")
ax.legend(loc="lower right")

for index, gfsNodeLabel in enumerate(gfsNodesLabels):
    ax.annotate(stationLabels[0], (weatherGovLongitudes[0], weatherGovLatitudes[0]))
    ax.annotate(gfsNodeLabel, (gfsNodesLongitudes[index], gfsNodesLatitudes[index]))
    
# plt.title("nos station points and closest gfs, adcirc (asgs, floodwater) in mesh plotted")
plt.title("weather gov station points and gfs nodes in mesh plotted")
plt.xlabel("longitude")
plt.ylabel("latitude")


# Plot wind speed over time
for index in range(3,7):
    fig, ax = plt.subplots()
    ax.scatter(gfsNodesTimes[index], gfsNodesWindSpeeds[index], marker=".", label="GFS")
    ax.scatter(weatherGovTimes[0], weatherGovWindSpeeds[0], marker=".", label="WeatherGov")
    ax.legend(loc="lower right")
    plt.title(gfsNodesLabels[index] + " node observational vs forecast wind speed")
    plt.xlabel("Hours since " + START_DATE.strftime(DATE_FORMAT))
    plt.ylabel("wind speed (m/s)")
        
# Plot wind direction over time
for index in range(3,7):
    fig, ax = plt.subplots()
    ax.scatter(gfsNodesTimes[index], gfsNodesWindDirections[index], marker=".", label="GFS")
    ax.scatter(weatherGovTimes[0], weatherGovWindDirections[0], marker=".", label="WeatherGov")
    ax.legend(loc="lower right")
    plt.title(gfsNodesLabels[index] + " node observational vs forecast wind direction")
    plt.xlabel("Hours since " + START_DATE.strftime(DATE_FORMAT))
    plt.ylabel("wind direction (compass)")
    
plt.show()