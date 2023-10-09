import json
import math
import numpy as np
import matplotlib.pyplot as plt

NOS_ADCIRC_WIND_DATA_FILE_NAME = "NOS_ADCIRC_Wind_Data.json"
NOS_GFS_WIND_DATA_FILE_NAME = "NOS_GFS_Wind_Data.json"
NOS_ADCIRC_NODES_WIND_DATA_FILE_NAME = "NOS_ADCIRC_Nodes_Wind_Data.json"
NOS_WIND_FILE_NAME = "NOS_Wind.json"
NOS_STATIONS_FILE_NAME = "NOS_Stations.json"

def extractLatitudeIndex(nodeIndex):
    return int(nodeIndex[1: nodeIndex.find(",")])
def extractLongitudeIndex(nodeIndex):
    return int(nodeIndex[nodeIndex.find(",") + 1: nodeIndex.find(")")])

adcircStationsWindData = {}
gfsStationsWindData = {}
adcircNodesWindData = {}
windData = {}
stationsData = {}

with open(NOS_ADCIRC_WIND_DATA_FILE_NAME) as outfile:
    adcircStationsWindData = json.load(outfile)
    
with open(NOS_GFS_WIND_DATA_FILE_NAME) as outfile:
    gfsStationsWindData = json.load(outfile)
    
with open(NOS_ADCIRC_NODES_WIND_DATA_FILE_NAME) as outfile:
    adcircNodesWindData = json.load(outfile)
    
with open(NOS_WIND_FILE_NAME) as outfile:
    windData = json.load(outfile)
    
with open(NOS_STATIONS_FILE_NAME) as outfile:
    stationsData = json.load(outfile)["NOS"]
    
adcircStationsLatitudes = []
adcircStationsLongitudes = []
nosLatitudes = []
nosLongitudes = []
stationLabels = []
stationADCIRCNodeLabels = []
adcircStationsTimes = []
adcircStationsWindDirections = []
adcircStationsWindSpeeds = []
nosTimes = []
nosWindDirections = []
nosWindSpeeds = []
for nodeIndex in adcircStationsWindData.keys():
    stationKey = adcircStationsWindData[nodeIndex]["stationKey"]
    if(stationKey in windData.keys()):
        stationADCIRCNodeLabels.append(nodeIndex)
        adcircStationsLatitudes.append(adcircStationsWindData[nodeIndex]["latitude"])
        adcircStationsLongitudes.append(adcircStationsWindData[nodeIndex]["longitude"])
        adcircStationWindsX = adcircStationsWindData[nodeIndex]["windsX"]
        adcircStationWindsY = adcircStationsWindData[nodeIndex]["windsY"]
        adcircStationTimes = []
        adcircStationWindDirections = []
        adcircStationWindSpeeds = []
        for index in range(len(adcircStationsWindData[nodeIndex]["times"])):
            adcircStationTimes.append(adcircStationsWindData[nodeIndex]["times"][index])
            adcircWindX = adcircStationsWindData[nodeIndex]["windsX"][index]
            adcircWindY = adcircStationsWindData[nodeIndex]["windsY"][index]
            adcircWindSpeed = math.sqrt(adcircWindX**2 + adcircWindY**2)
            adcircWindDirection = math.degrees(math.acos(adcircWindX / adcircWindSpeed))
            adcircWindDirection = (270 - math.atan(adcircWindY / adcircWindX) * 180/math.pi) % 360
            adcircStationWindDirections.append(adcircWindDirection)
            adcircStationWindSpeeds.append(adcircWindSpeed)
        
        adcircStationsTimes.append(adcircStationTimes)
        adcircStationsWindDirections.append(adcircStationWindDirections)
        adcircStationsWindSpeeds.append(adcircStationWindSpeeds)
        stationLabels.append(stationsData[stationKey]["name"])
        nosLatitudes.append(float(stationsData[stationKey]["latitude"]))
        nosLongitudes.append(float(stationsData[stationKey]["longitude"]))
        print(windData[stationKey]["times"])
        nosTimes.append(windData[stationKey]["times"])
        nosWindDirections.append(windData[stationKey]["directions"])
        nosWindSpeeds.append(windData[stationKey]["speeds"])

gfsStationsLatitudes = []
gfsStationsLongitudes = []
stationGFSNodeLabels = []
gfsStationsTimes = []
gfsStationsWindDirections = []
gfsStationsWindSpeeds = []
for nodeIndex in gfsStationsWindData.keys():
    stationKey = gfsStationsWindData[nodeIndex]["stationKey"]
    if(stationKey in windData.keys()):
        stationGFSNodeLabels.append(nodeIndex)
        gfsStationsLatitudes.append(gfsStationsWindData[nodeIndex]["latitude"])
        gfsStationsLongitudes.append(gfsStationsWindData[nodeIndex]["longitude"])
        gfsStationWindsX = gfsStationsWindData[nodeIndex]["windsX"]
        gfsStationWindsY = gfsStationsWindData[nodeIndex]["windsY"]
        gfsStationTimes = []
        gfsStationWindDirections = []
        gfsStationWindSpeeds = []
        for index in range(len(gfsStationsWindData[nodeIndex]["times"])):
            gfsStationTimes.append(gfsStationsWindData[nodeIndex]["times"][index])
            gfsWindX = gfsStationsWindData[nodeIndex]["windsX"][index]
            gfsWindY = gfsStationsWindData[nodeIndex]["windsY"][index]
            gfsWindSpeed = math.sqrt(gfsWindX**2 + gfsWindY**2)
            gfsWindDirection = math.degrees(math.acos(gfsWindX / gfsWindSpeed))
            gfsWindDirection = (270 - math.atan(gfsWindY / gfsWindX) * 180/math.pi) % 360
            gfsStationWindDirections.append(gfsWindDirection)
            gfsStationWindSpeeds.append(gfsWindSpeed)
        
        gfsStationsTimes.append(gfsStationTimes)
        gfsStationsWindDirections.append(gfsStationWindDirections)
        gfsStationsWindSpeeds.append(gfsStationWindSpeeds)

# Print 10th wind entry for 0th station
print(nosTimes[0][10])
print(nosWindDirections[0][10])
print(nosWindSpeeds[0][10])

# Print 10th wind entry for 0th station node
print(adcircStationsTimes[0][10])
print(adcircStationsWindDirections[0][10])
print(adcircStationsWindSpeeds[0][10])

# Print 10th wind entry for 0th station gfs node
print(gfsStationsTimes[0][10])
print(gfsStationsWindDirections[0][10])
print(gfsStationsWindSpeeds[0][10])

adcircNodesLatitudes = []
adcircNodesLongitudes = []
adcircNodeLabels = []
for nodeIndex in adcircNodesWindData.keys():
    adcircNodeLabels.append(nodeIndex)
    adcircNodesLatitudes.append(adcircNodesWindData[nodeIndex]["latitude"])
    adcircNodesLongitudes.append(adcircNodesWindData[nodeIndex]["longitude"])
    
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
ax.scatter(nosLongitudes, nosLatitudes)
ax.scatter(adcircStationsLongitudes, adcircStationsLatitudes)
ax.scatter(gfsStationsLongitudes, gfsStationsLatitudes)

for index, stationLabel in enumerate(stationLabels):
    ax.annotate(stationLabel, (nosLongitudes[index], nosLatitudes[index]))
    ax.annotate(stationADCIRCNodeLabels[index], (adcircStationsLongitudes[index], adcircStationsLatitudes[index]))
    ax.annotate(stationGFSNodeLabels[index], (gfsStationsLongitudes[index], gfsStationsLatitudes[index]))
    
plt.title("nos station points and closest gfs and adcirc nodes in rivc1 mesh plotted")
plt.xlabel("longitude")
plt.ylabel("latitude")

# Plot collection of points off adcirc mesh
fig, ax = plt.subplots()
ax.scatter(adcircNodesLongitudes, adcircNodesLatitudes)

for index, nodeLabel in enumerate(adcircNodeLabels):
    ax.annotate(nodeLabel, (adcircNodesLongitudes[index], adcircNodesLatitudes[index]))
plt.title("adcirc assorted nodes in rivc1 mesh plotted")
plt.xlabel("longitude")
plt.ylabel("latitude")

# Plot wind speed over time
for index in range(len(adcircStationsTimes)):
    fig, ax = plt.subplots()
    ax.scatter(adcircStationsTimes[index], adcircStationsWindSpeeds[index], marker=".")
    ax.scatter(gfsStationsTimes[index], gfsStationsWindSpeeds[index], marker=".")
    ax.scatter(nosTimes[index], nosWindSpeeds[index], marker=".")
    plt.title(stationLabels[index] + " station observational vs ADCIRC Wind Speed")
    plt.xlabel("time")
    plt.ylabel("wind speed (kts)")
        
# Plot wind direction over time
for index in range(len(adcircStationsTimes)):
    fig, ax = plt.subplots()
    ax.scatter(adcircStationsTimes[index], adcircStationsWindDirections[index], marker=".")
    ax.scatter(gfsStationsTimes[index], gfsStationsWindDirections[index], marker=".")
    ax.scatter(nosTimes[index], nosWindDirections[index], marker=".")
    plt.title(stationLabels[index] + " station observational vs ADCIRC Wind Direction")
    plt.xlabel("time")
    plt.ylabel("wind direction (compass)")

plt.show()