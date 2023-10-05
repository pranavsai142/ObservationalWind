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
NOS_STATION_TO_NODE_DISTANCES_FILE_NAME = "NOS_Station_To_Node_Distances.json"
NOS_ADCIRC_NODES_FILE_NAME = "NOS_ADCIRC_Nodes.json"
NOS_ADCIRC_WIND_DATA_FILE_NAME = "NOS_ADCIRC_Wind_Data.json"

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

print("number of timesteps")
timesteps = len(windDataset.variables["time"][:])
print(timesteps)

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
    
stationToNodeDistancesDict = {}

# Set to true to recreate station to node distances calculations dictionary
initializeStationToNodeDistancesDict = False
if(initializeStationToNodeDistancesDict):
    for stationKey in stationsDict["NOS"].keys():
        stationToNodeDistancesDict[stationKey] = {}

    # Nodes with ..interesting.. latitude and longitude
    badNodes = []

    for nodeIndex in range(numberOfNodes):
        node = (float(windDataset.variables["y"][nodeIndex].data), float(windDataset.variables["x"][nodeIndex].data))
        if(node[0] <= 90 and node[0] >= -90 and node[1] <= 90 and node[1] >= -90):
            for stationKey in stationsDict["NOS"].keys():
                stationDict = stationsDict["NOS"][stationKey]
                stationCoordinates = (float(stationDict["latitude"]), float(stationDict["longitude"]))
                distance = haversine.haversine(stationCoordinates, node)
                if(len(stationToNodeDistancesDict[stationKey].keys()) == 0):
                    stationToNodeDistancesDict[stationKey]["nodeIndex"] = nodeIndex
                    stationToNodeDistancesDict[stationKey]["distance"] = distance
                elif(stationToNodeDistancesDict[stationKey]["distance"] > distance):
                    stationToNodeDistancesDict[stationKey]["nodeIndex"] = nodeIndex
                    stationToNodeDistancesDict[stationKey]["distance"] = distance
        else:
            badNodes.append(nodeIndex)
            print("bad node", nodeIndex, node)
    
    #     Print progress
        if(nodeIndex % 50000 == 0):
            print("on node", nodeIndex, node)
        
    print("stationToNodeDistancesDict", stationToNodeDistancesDict)

    with open(NOS_STATION_TO_NODE_DISTANCES_FILE_NAME, "w") as outfile:
        json.dump(stationToNodeDistancesDict, outfile)

with open(NOS_STATION_TO_NODE_DISTANCES_FILE_NAME) as outfile:
    stationToNodeDistancesDict = json.load(outfile)
  
adcircNodes = {"NOS": {}}
    
initializeAdcircNodesDict = False
if(initializeAdcircNodesDict):
    for stationKey in stationToNodeDistancesDict.keys():
        stationToNodeDistanceDict = stationToNodeDistancesDict[stationKey]
        nodeIndex = stationToNodeDistanceDict["nodeIndex"]
        adcircNodes["NOS"][nodeIndex] = {}
        adcircNodes["NOS"][nodeIndex]["latitude"] = float(windDataset.variables["y"][nodeIndex].data)
        adcircNodes["NOS"][nodeIndex]["longitude"] = float(windDataset.variables["x"][nodeIndex].data)
        adcircNodes["NOS"][nodeIndex]["stationKey"] = stationKey
    
    with open(NOS_ADCIRC_NODES_FILE_NAME, "w") as outfile:
        json.dump(adcircNodes, outfile)

with open(NOS_ADCIRC_NODES_FILE_NAME) as outfile:
    adcircNodes = json.load(outfile)

adcircWindData = {}
for nodeIndex in adcircNodes["NOS"].keys():
    adcircWindData[nodeIndex] = {}
    adcircWindData[nodeIndex]["latitude"] = float(windDataset.variables["y"][int(nodeIndex)].data)
    adcircWindData[nodeIndex]["longitude"] = float(windDataset.variables["x"][int(nodeIndex)].data)
    adcircWindData[nodeIndex]["stationKey"] = adcircNodes["NOS"][nodeIndex]["stationKey"]
    windsX = []
    windsY = []
    for index in range(timesteps):
        windsX.append(windDataset.variables["windx"][index][int(nodeIndex)])
        windsY.append(windDataset.variables["windy"][index][int(nodeIndex)])
    adcircWindData[nodeIndex]["windsX"] = windsX
    adcircWindData[nodeIndex]["windsY"] = windsY
    
with open(NOS_ADCIRC_WIND_DATA_FILE_NAME, "w") as outfile:
    json.dump(adcircWindData, outfile)

    
  
