import json
import matplotlib.pyplot as plt

NOS_ADCIRC_WIND_DATA_FILE_NAME = "NOS_ADCIRC_Wind_Data.json"
NOS_WIND_FILE_NAME = "NOS_Wind.json"

adcircWindData = {}
windData = {}

with open(NOS_ADCIRC_WIND_DATA_FILE_NAME) as outfile:
    adcircWindData = json.load(outfile)
    
with open(NOS_WIND_FILE_NAME) as outfile:
    windData = json.load(outfile)
    
adcircLatitudes = []
adcircLongitudes = []
nosLatitudes = []
nosLongitudes = []
latLongStationLabels = []
for nodeIndex in adcircWindData.keys():
    adcircLatitudes.append(adcircWindData[nodeIndex]["latitude"])
    adcircLongitudes.append(adcircWindData[nodeIndex]["longitude"])
    latLongStationLabels.append(adcircWindData[nodeIndex]["stationKey"])
    
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

fig, ax = plt.subplots()
ax.scatter(adcircLongitudes, adcircLatitudes)

for stationIndex, latLongStationLabel in enumerate(latLongStationLabels):
    ax.annotate(latLongStationLabel, (adcircLongitudes[stationIndex], adcircLatitudes[stationIndex]))

plt.show()  