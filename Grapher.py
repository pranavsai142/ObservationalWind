import json
import math
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

NOS_ADCIRC_WIND_DATA_FILE_NAME = "NOS_ADCIRC_Wind_Data.json"
NOS_FLOODWATER_WIND_DATA_FILE_NAME = "NOS_Floodwater_Wind_Data.json"
NOS_GFS_DEB_WIND_DATA_FILE_NAME = "NOS_GFS_DEB_Wind_Data.json"
NOS_GFS_WIND_DATA_FILE_NAME = "NOS_GFS_Wind_Data.json"
NOS_GFS_RAIN_DATA_FILE_NAME = "NOS_GFS_Rain_Data.json"
NOS_ADCIRC_NODES_WIND_DATA_FILE_NAME = "NOS_ADCIRC_Nodes_Wind_Data.json"
NOS_FLOODWATER_NODES_WIND_DATA_FILE_NAME = "NOS_Floodwater_Nodes_Wind_Data.json"
NOS_WIND_FILE_NAME = "NOS_Wind.json"
NOS_STATIONS_FILE_NAME = "NOS_Stations.json"
START_DATE = datetime(year=2023, month=9, day=14)
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


adcircStationsWindData = {}
floodwaterStationsWindData = {}
gfsStationsWindData = {}
gfsDebStationsWindData = {}
gfsStationsRainData = {}
adcircNodesWindData = {}
floodwaterNodesWindData = {}
windData = {}
stationsData = {}

with open(NOS_ADCIRC_WIND_DATA_FILE_NAME) as outfile:
    adcircStationsWindData = json.load(outfile)
    
with open(NOS_FLOODWATER_WIND_DATA_FILE_NAME) as outfile:
    floodwaterStationsWindData = json.load(outfile)
    
with open(NOS_GFS_WIND_DATA_FILE_NAME) as outfile:
    gfsStationsWindData = json.load(outfile)
    
with open(NOS_GFS_DEB_WIND_DATA_FILE_NAME) as outfile:
    gfsDebStationsWindData = json.load(outfile)
    
with open(NOS_GFS_RAIN_DATA_FILE_NAME) as outfile:
    gfsStationsRainData = json.load(outfile)
    
with open(NOS_ADCIRC_NODES_WIND_DATA_FILE_NAME) as outfile:
    adcircNodesWindData = json.load(outfile)
    
with open(NOS_FLOODWATER_NODES_WIND_DATA_FILE_NAME) as outfile:
    floodwaterNodesWindData = json.load(outfile)
    
with open(NOS_WIND_FILE_NAME) as outfile:
    windData = json.load(outfile)
    
with open(NOS_STATIONS_FILE_NAME) as outfile:
    stationsData = json.load(outfile)["NOS"]
    
adcircStationsLatitudes = []
adcircStationsLongitudes = []
adcircStationsNodeLabels = []
adcircStationsTimes = []
adcircStationsWindDirections = []
adcircStationsWindSpeeds = []
for nodeIndex in adcircStationsWindData.keys():
    stationKey = adcircStationsWindData[nodeIndex]["stationKey"]
    if(stationKey in windData.keys()):
        adcircStationsNodeLabels.append(nodeIndex)
        adcircStationsLatitudes.append(adcircStationsWindData[nodeIndex]["latitude"])
        adcircStationsLongitudes.append(adcircStationsWindData[nodeIndex]["longitude"])
        adcircStationWindsX = adcircStationsWindData[nodeIndex]["windsX"]
        adcircStationWindsY = adcircStationsWindData[nodeIndex]["windsY"]
        adcircStationTimes = []
        adcircStationWindDirections = []
        adcircStationWindSpeeds = []
        for index in range(len(adcircStationsWindData[nodeIndex]["times"])):
            adcircStationTimes.append(unixTimeToDeltaHours(adcircStationsWindData[nodeIndex]["times"][index]))
            adcircWindX = adcircStationsWindData[nodeIndex]["windsX"][index]
            adcircWindY = adcircStationsWindData[nodeIndex]["windsY"][index]
            adcircWindSpeed = vectorSpeed(adcircWindX, adcircWindY)
            adcircWindDirection = vectorDirection(adcircWindX, adcircWindY)
            adcircStationWindDirections.append(adcircWindDirection)
            adcircStationWindSpeeds.append(adcircWindSpeed)
        
        adcircStationsTimes.append(adcircStationTimes)
        adcircStationsWindDirections.append(adcircStationWindDirections)
        adcircStationsWindSpeeds.append(adcircStationWindSpeeds)
        
floodwaterStationsLatitudes = []
floodwaterStationsLongitudes = []
floodwaterStationsNodeLabels = []
floodwaterStationsTimes = []
floodwaterStationsWindDirections = []
floodwaterStationsWindSpeeds = []
for nodeIndex in floodwaterStationsWindData.keys():
    stationKey = floodwaterStationsWindData[nodeIndex]["stationKey"]
    if(stationKey in windData.keys()):
        floodwaterStationsNodeLabels.append(nodeIndex)
        floodwaterStationsLatitudes.append(floodwaterStationsWindData[nodeIndex]["latitude"])
        floodwaterStationsLongitudes.append(floodwaterStationsWindData[nodeIndex]["longitude"])
        floodwaterStationWindsX = floodwaterStationsWindData[nodeIndex]["windsX"]
        floodwaterStationWindsY = floodwaterStationsWindData[nodeIndex]["windsY"]
        floodwaterStationTimes = []
        floodwaterStationWindDirections = []
        floodwaterStationWindSpeeds = []
        for index in range(len(floodwaterStationsWindData[nodeIndex]["times"])):
            floodwaterStationTimes.append(unixTimeToDeltaHours(floodwaterStationsWindData[nodeIndex]["times"][index]))
            floodwaterWindX = floodwaterStationsWindData[nodeIndex]["windsX"][index]
            floodwaterWindY = floodwaterStationsWindData[nodeIndex]["windsY"][index]
            floodwaterWindSpeed = vectorSpeed(floodwaterWindX, floodwaterWindY)
            floodwaterWindDirection = vectorDirection(floodwaterWindX, floodwaterWindY)
            floodwaterStationWindDirections.append(floodwaterWindDirection)
            floodwaterStationWindSpeeds.append(floodwaterWindSpeed)
        
        floodwaterStationsTimes.append(floodwaterStationTimes)
        floodwaterStationsWindDirections.append(floodwaterStationWindDirections)
        floodwaterStationsWindSpeeds.append(floodwaterStationWindSpeeds)

nosLatitudes = []
nosLongitudes = []
stationLabels = []
gfsStationsLatitudes = []
gfsStationsLongitudes = []
gfsStationsNodeLabels = []
gfsStationsTimes = []
gfsStationsWindDirections = []
gfsStationsWindSpeeds = []
gfsStationsRains = []
nosTimes = []
nosWindDirections = []
nosWindSpeeds = []
nosStationsHeights = []
for nodeIndex in gfsStationsWindData.keys():
    stationKey = gfsStationsWindData[nodeIndex]["stationKey"]
    if(stationKey in windData.keys()):
        gfsStationsNodeLabels.append(nodeIndex)
        gfsStationsLatitudes.append(gfsStationsWindData[nodeIndex]["latitude"])
        gfsStationsLongitudes.append(gfsStationsWindData[nodeIndex]["longitude"])
        gfsStationWindsX = gfsStationsWindData[nodeIndex]["windsX"]
        gfsStationWindsY = gfsStationsWindData[nodeIndex]["windsY"]
        gfsStationTimes = []
        gfsStationWindDirections = []
        gfsStationWindSpeeds = []
        gfsStationRains = []
        for index in range(len(gfsStationsWindData[nodeIndex]["times"])):
            gfsStationTimes.append(unixTimeToDeltaHours(gfsStationsWindData[nodeIndex]["times"][index]))
            gfsWindX = gfsStationsWindData[nodeIndex]["windsX"][index]
            gfsWindY = gfsStationsWindData[nodeIndex]["windsY"][index]
            gfsWindSpeed = vectorSpeed(gfsWindX, gfsWindY)
            gfsWindDirection = vectorDirection(gfsWindX, gfsWindY)
            gfsStationWindDirections.append(gfsWindDirection)
            gfsStationWindSpeeds.append(gfsWindSpeed)
            gfsStationRains.append(gfsStationsRainData[nodeIndex]["rains"][index])
        
        gfsStationsTimes.append(gfsStationTimes)
        gfsStationsWindDirections.append(gfsStationWindDirections)
        gfsStationsWindSpeeds.append(gfsStationWindSpeeds)
        gfsStationsRains.append(gfsStationRains)
        stationLabels.append(stationsData[stationKey]["name"])
        nosLatitudes.append(float(stationsData[stationKey]["latitude"]))
        nosLongitudes.append(float(stationsData[stationKey]["longitude"]))
        nosStationTimes = []
        nosStationWindSpeeds = []
        nosStationHeights = []
        for index in range(len(windData[stationKey]["times"])):
            nosStationTimes.append(unixTimeToDeltaHours(windData[stationKey]["times"][index]))
            nosStationWindSpeed = windData[stationKey]["speeds"][index]
            nosStationHeight = windData[stationKey]["heights"][index]
            nosStationAltitude = None
            nosStationWindSpeeds.append(extrapolateWindToTenMeterHeight(nosStationWindSpeed, nosStationAltitude))
            nosStationHeights.append(nosStationHeight)
        nosTimes.append(nosStationTimes)
        nosWindSpeeds.append(nosStationWindSpeeds)
        nosWindDirections.append(windData[stationKey]["directions"])
        nosStationsHeights.append(nosStationHeights)
   
# gfsDebStationsLatitudes = []
# gfsDebStationsLongitudes = []
# gfsDebStationsNodeLabels = []
# gfsDebStationsTimes = []
# gfsDebStationsWindDirections = []
# gfsDebStationsWindSpeeds = []     
# for nodeIndex in gfsDebStationsWindData.keys():
#     stationKey = gfsDebStationsWindData[nodeIndex]["stationKey"]
#     if(stationKey in windData.keys()):
#         gfsDebStationsNodeLabels.append(nodeIndex)
#         gfsDebStationsLatitudes.append(gfsDebStationsWindData[nodeIndex]["latitude"])
#         gfsDebStationsLongitudes.append(gfsDebStationsWindData[nodeIndex]["longitude"])
#         gfsDebStationWindsX = gfsDebStationsWindData[nodeIndex]["windsX"]
#         gfsDebStationWindsY = gfsDebStationsWindData[nodeIndex]["windsY"]
#         gfsDebStationTimes = []
#         gfsDebStationWindDirections = []
#         gfsDebStationWindSpeeds = []
#         for index in range(len(gfsDebStationsWindData[nodeIndex]["times"])):
#             gfsDebStationTimes.append(unixTimeToDeltaHours(gfsDebStationsWindData[nodeIndex]["times"][index]))
#             gfsDebWindX = gfsDebStationsWindData[nodeIndex]["windsX"][index]
#             gfsDebWindY = gfsDebStationsWindData[nodeIndex]["windsY"][index]
#             gfsDebWindSpeed = vectorSpeed(gfsDebWindX, gfsDebWindY)
#             gfsDebWindDirection = vectorDirection(gfsDebWindX, gfsDebWindY)
#             gfsDebStationWindDirections.append(gfsDebWindDirection)
#             gfsDebStationWindSpeeds.append(gfsDebWindSpeed)
#         
#         gfsDebStationsTimes.append(gfsDebStationTimes)
#         gfsDebStationsWindDirections.append(gfsDebStationWindDirections)
#         gfsDebStationsWindSpeeds.append(gfsDebStationWindSpeeds)

numberOfStations = len(nosTimes)
# numberOfStations = 7

# Print 10th wind entry for 0th station
print(nosTimes[0][10])
print(nosWindDirections[0][10])
print(nosWindSpeeds[0][10])

# Print 10th wind entry for 0th station node
print(adcircStationsTimes[0][10])
print(adcircStationsWindDirections[0][10])
print(adcircStationsWindSpeeds[0][10])

print(floodwaterStationsTimes[0][10])
print(floodwaterStationsWindDirections[0][10])
print(floodwaterStationsWindSpeeds[0][10])

# Print 10th wind entry for 0th station gfs node
print(gfsStationsTimes[0][10])
print(gfsStationsWindDirections[0][10])
print(gfsStationsWindSpeeds[0][10])
# print(gfsStationsRains[0][10])

# Print 10th wind entry for 0th station gfs deb node
# print(gfsDebStationsTimes[0][10])
# print(gfsDebStationsWindDirections[0][10])
# print(gfsDebStationsWindSpeeds[0][10])

adcircNodesLatitudes = []
adcircNodesLongitudes = []
adcircNodeLabels = []
for nodeIndex in adcircNodesWindData.keys():
    adcircNodeLabels.append(nodeIndex)
    adcircNodesLatitudes.append(adcircNodesWindData[nodeIndex]["latitude"])
    adcircNodesLongitudes.append(adcircNodesWindData[nodeIndex]["longitude"])
    
floodwaterNodesLatitudes = []
floodwaterNodesLongitudes = []
floodwaterNodeLabels = []
for nodeIndex in floodwaterNodesWindData.keys():
    floodwaterNodeLabels.append(nodeIndex)
    floodwaterNodesLatitudes.append(floodwaterNodesWindData[nodeIndex]["latitude"])
    floodwaterNodesLongitudes.append(floodwaterNodesWindData[nodeIndex]["longitude"])
    
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
ax.scatter(adcircStationsLongitudes, adcircStationsLatitudes, label="rivc1")
ax.scatter(gfsStationsLongitudes, gfsStationsLatitudes, label="GFS")
ax.scatter(floodwaterStationsLongitudes, floodwaterStationsLatitudes, label="ec95d")
# ax.scatter(gfsDebStationsLongitudes, gfsDebStationsLatitudes, label="GFS DEB")
ax.scatter(nosLongitudes, nosLatitudes, label="Buoy")
ax.legend(loc="lower right")

for index, stationLabel in enumerate(stationLabels):
    ax.annotate(stationLabel, (nosLongitudes[index], nosLatitudes[index]))
    ax.annotate(adcircStationsNodeLabels[index], (adcircStationsLongitudes[index], adcircStationsLatitudes[index]))
    ax.annotate(floodwaterStationsNodeLabels[index], (floodwaterStationsLongitudes[index], floodwaterStationsLatitudes[index]))
    ax.annotate(gfsStationsNodeLabels[index], (gfsStationsLongitudes[index], gfsStationsLatitudes[index]))
#     ax.annotate(gfsDebStationsNodeLabels[index], (gfsDebStationsLongitudes[index], gfsDebStationsLatitudes[index]))

    
plt.title("nos station points and closest gfs, adcirc (asgs, floodwater) in mesh plotted")
plt.xlabel("longitude")
plt.ylabel("latitude")

# Plot collection of points off rivc1 mesh
fig, ax = plt.subplots()
ax.scatter(adcircNodesLongitudes, adcircNodesLatitudes)

for index, nodeLabel in enumerate(adcircNodeLabels):
    ax.annotate(nodeLabel, (adcircNodesLongitudes[index], adcircNodesLatitudes[index]))
plt.title("assorted nodes in rivc1 mesh plotted")
plt.xlabel("longitude")
plt.ylabel("latitude")

# Plot collection of points off ec95d mesh
fig, ax = plt.subplots()
ax.scatter(floodwaterNodesLongitudes, floodwaterNodesLatitudes)

for index, nodeLabel in enumerate(floodwaterNodeLabels):
    ax.annotate(nodeLabel, (floodwaterNodesLongitudes[index], floodwaterNodesLatitudes[index]))
plt.title("assorted nodes in ec95d mesh plotted")
plt.xlabel("longitude")
plt.ylabel("latitude")


# Plot wind speed over time
for index in range(numberOfStations):
    fig, ax = plt.subplots()
    ax.scatter(adcircStationsTimes[index], adcircStationsWindSpeeds[index], marker=".", label="ASGS")
    ax.scatter(floodwaterStationsTimes[index], floodwaterStationsWindSpeeds[index], marker=".", label="Floodwater (left)")
#     ax.scatter(gfsDebStationsTimes[index], gfsDebStationsWindSpeeds[index], marker=".", label="GFS DEB")
    ax.scatter(gfsStationsTimes[index], gfsStationsWindSpeeds[index], marker=".", label="GFS")
    ax.scatter(nosTimes[index], nosWindSpeeds[index], marker=".", label="Buoy")
    ax.legend(loc="lower right")
    plt.title(stationLabels[index] + " station observational vs forecast wind speed")
    plt.xlabel("Hours since " + START_DATE.strftime(DATE_FORMAT))
    plt.ylabel("wind speed (m/s)")
        
# Plot wind direction over time
for index in range(numberOfStations):
    fig, ax = plt.subplots()
    ax.scatter(adcircStationsTimes[index], adcircStationsWindDirections[index], marker=".", label="ASGS")
    ax.scatter(floodwaterStationsTimes[index], floodwaterStationsWindDirections[index], marker=".", label="Floodwater (left)")
#     ax.scatter(gfsDebStationsTimes[index], gfsDebStationsWindDirections[index], marker=".", label="GFS DEB")
    ax.scatter(gfsStationsTimes[index], gfsStationsWindDirections[index], marker=".", label="GFS")
    ax.scatter(nosTimes[index], nosWindDirections[index], marker=".", label="Buoy")
    ax.legend(loc="lower right")
    plt.title(stationLabels[index] + " station observational vs forecast wind direction")
    plt.xlabel("Hours since " + START_DATE.strftime(DATE_FORMAT))
    plt.ylabel("wind direction (compass)")
    
# for index in range(numberOfStations):
#     fig, ax = plt.subplots()
#     ax.scatter(gfsStationsTimes[index], gfsStationsRains[index], marker=".", label="GFS")
#     ax.legend(loc="upper right")
#     plt.title(stationLabels[index] + " station forecasted rain")
#     plt.xlabel("Hours since " + START_DATE.strftime(DATE_FORMAT))
#     plt.ylabel("rain accumlation over 1 hr (mm)")
# 
# for index in range(numberOfStations):
#     fig, ax = plt.subplots()
#     ax.scatter(nosTimes[index], nosStationsHeights[index], marker=".", label="Buoy")
#     ax.legend(loc="upper right")
#     plt.title(stationLabels[index] + " station water level height above reference")
#     plt.xlabel("Hours since " + START_DATE.strftime(DATE_FORMAT))
#     plt.ylabel("height (meters)")
    
plt.show()