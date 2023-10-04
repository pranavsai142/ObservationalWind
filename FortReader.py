import netCDF4 as nc
import haversine
import json
from datetime import datetime, timedelta


# Here I will write about the fort files

# Fort 74 contains an hour by hour forecast with the wind vector x and y components

# The time is measured in seconds coldstartdate + time = time of forecast
# To access metadata of fort files, use dataset.__dict__ variable on netCDF dataset
# key rundes contains information with coldstart date
# To see dimensions of variables, use dataset.dimensions
# To see information on variables, use dataset.variables
# To get data for a variable, use dataset.variables["time"]

FORT_74_FILE_NAME = "fort.74.nc"
NOS_STATIONS_FILE_NAME = "NOS_Stations.json"
NOS_STATIONS_TO_NODE_DISTANCE_FILE_NAME = "NOS_StationsToNodeDistance.json"

windDataset = nc.Dataset(FORT_74_FILE_NAME)
windMetadata = windDataset.__dict__

windRunDescription = windMetadata["rundes"]
windRunDescriptionColdStartIndex = windRunDescription.find("cs:")
coldStartDateText = windRunDescription[windRunDescriptionColdStartIndex + 3: windRunDescriptionColdStartIndex + 17]
# Insert a T to make date text a valid iso format
coldStartDateText = coldStartDateText[0: 8] + "T" + coldStartDateText[8:]
coldStartDate = datetime.fromisoformat(coldStartDateText)
print("coldStartDate", coldStartDate)

minT = windDataset.variables["time"][0].data
maxT = windDataset.variables["time"][-1].data

print("deltaT of data")
windDeltaT = timedelta(seconds=maxT - minT)
print(windDeltaT)

print("start of wind data (seconds since coldstart)")
startDate = coldStartDate + timedelta(seconds=int(minT))
endDate = coldStartDate + timedelta(seconds=int(maxT))
print("startDate", startDate)
print("endDate", endDate)

# Grid origin is top right? Maybe not, Node based system!
# y is latitude, x is longitude
node0 = (float(windDataset.variables["y"][0].data), float(windDataset.variables["x"][0].data))
print("node0 (lat, long)", node0)

numberOfNodes = windDataset.variables["x"].shape[0]

print("number of nodes", numberOfNodes)

print("wind at node0")

windX0 = windDataset.variables["windx"][0][0]
windY0 = windDataset.variables["windy"][0][0]

print("windX0", windX0)
print("windY0", windY0)

# Find node indexes that are closest to NOS_Stations
with open(NOS_STATIONS_FILE_NAME) as stations_file:
    stationsDict = json.load(stations_file)
    
# Initialize stationToNodeDistanceDict
stationToNodeDistanceDict = {}
for stationKey in stationsDict["NOS"].keys():
    stationToNodeDistanceDict[stationKey] = {}

# Nodes with ..interesting.. latitude and longitude
badNodes = []

for nodeIndex in range(numberOfNodes):
    node = (float(windDataset.variables["y"][nodeIndex].data), float(windDataset.variables["x"][nodeIndex].data))
    if(node[0] <= 90 and node[0] >= -90 and node[1] <= 90 and node[1] >= -90):
        for stationKey in stationsDict["NOS"].keys():
            stationDict = stationsDict["NOS"][stationKey]
            stationCoordinates = (float(stationDict["latitude"]), float(stationDict["longitude"]))
            distance = haversine.haversine(stationCoordinates, node)
            if(len(stationToNodeDistanceDict[stationKey].keys()) == 0):
                stationToNodeDistanceDict[stationKey]["nodeIndex"] = nodeIndex
                stationToNodeDistanceDict[stationKey]["distance"] = distance
            elif(stationToNodeDistanceDict[stationKey]["distance"] > distance):
                stationToNodeDistanceDict[stationKey]["nodeIndex"] = nodeIndex
                stationToNodeDistanceDict[stationKey]["distance"] = distance
    else:
        badNodes.append(nodeIndex)
        print("bad node", nodeIndex, node)
    
#     Print progress
    if(nodeIndex % 50000 == 0):
        print("on node", nodeIndex, node)
        
print("stationToNodeDistanceDict", stationToNodeDistanceDict)

with open(NOS_STATIONS_TO_NODE_DISTANCE_FILE_NAME, "w") as outfile:
    json.dump(stationToNodeDistanceDict, outfile)
    