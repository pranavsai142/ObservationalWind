import json
import math
import numpy as np
import matplotlib.pyplot as plt

NOS_ADCIRC_WIND_DATA_FILE_NAME = "NOS_ADCIRC_Wind_Data.json"
NOS_ADCIRC_NODES_WIND_DATA_FILE_NAME = "NOS_ADCIRC_Nodes_Wind_Data.json"
NOS_WIND_FILE_NAME = "NOS_Wind.json"
NOS_STATIONS_FILE_NAME = "NOS_Stations.json"

adcircStationsWindData = {}
adcircNodesWindData = {}
windData = {}
stationsData = {}

with open(NOS_ADCIRC_WIND_DATA_FILE_NAME) as outfile:
    adcircStationsWindData = json.load(outfile)
    
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
nodeLabels = []
adcircStationsTimes = []
adcircStationsWindDirections = []
adcircStationsWindSpeeds = []
nosTimes = []
nosWindDirections = []
nosWindSpeeds = []
for nodeIndex in adcircStationsWindData.keys():
    stationKey = adcircStationsWindData[nodeIndex]["stationKey"]
    if(stationKey in windData.keys()):
        nodeLabels.append(nodeIndex)
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
            adcircWindDirection = math.degrees(math.atan(adcircWindY / adcircWindX))
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
    
# Print 10th wind entry for 0th station
print(nosTimes[0][10])
print(nosWindDirections[0][10])
print(nosWindSpeeds[0][10])

# Print 10th wind entry for 0th station node
print(adcircStationsTimes[0][10])
print(adcircStationsWindDirections[0][10])
print(adcircStationsWindSpeeds[0][10])

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
ax.scatter(nosLongitudes + adcircStationsLongitudes, nosLatitudes + adcircStationsLatitudes)

for index, stationLabel in enumerate(stationLabels):
    ax.annotate(stationLabel, (nosLongitudes[index], nosLatitudes[index]))

# plt.show()

# Plot collection of points off adcirc mesh
fig, ax = plt.subplots()
ax.scatter(adcircNodesLongitudes, adcircNodesLatitudes)

for index, nodeLabel in enumerate(adcircNodeLabels):
    ax.annotate(nodeLabel, (adcircNodesLongitudes[index], adcircNodesLatitudes[index]))

# plt.show()

# Plot wind speed over time for station 0
fig, ax = plt.subplots()
ax.scatter(adcircStationsTimes[12], adcircStationsWindSpeeds[12])
ax.scatter(nosTimes[12], nosWindSpeeds[12], marker=".")

plt.show()