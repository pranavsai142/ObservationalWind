import json
import haversine
import netCDF4 as nc
from datetime import datetime, timedelta

METGET_GFS_WIND_FILE_NAME = "adcirc_gfs_analysis_wind_pressure_2022121413-2022121906.nc"
METGET_GFS_RAIN_FILE_NAME = "adcirc_gfs_analysis_rain_2022121413-2022121906.nc"
NOS_STATIONS_FILE_NAME = "NOS_Stations.json"
NOS_STATION_TO_GFS_NODE_DISTANCES_FILE_NAME = "NOS_Station_To_GFS_Node_Distances.json"
NOS_GFS_NODES_FILE_NAME = "NOS_GFS_Nodes.json"
NOS_GFS_WIND_DATA_FILE_NAME = "NOS_GFS_Wind_Data.json"
NOS_GFS_RAIN_DATA_FILE_NAME = "NOS_GFS_Rain_Data.json"
NOS_GFS_NODES_WIND_DATA_FILE_NAME = "NOS_GFS_Nodes_Wind_Data.json"

def extractLatitudeIndex(nodeIndex):
    return int(nodeIndex[1: nodeIndex.find(",")])
def extractLongitudeIndex(nodeIndex):
    return int(nodeIndex[nodeIndex.find(",") + 1: nodeIndex.find(")")])
    
# METGET_GFS_FILE_NAME = input("GFS NetCDF File Name?: ")
METGET_GFS_FILE_NAME = "gfs_dec_2022_multiple_forecasts.nc"
gfsDataset = nc.Dataset(METGET_GFS_FILE_NAME)
gfsMetadata = gfsDataset.__dict__
print(gfsMetadata)
print(gfsDataset.variables)

quit()
rainDataset = nc.Dataset(METGET_GFS_FILE_NAME)
rainMetadata = rainDataset.__dict__
print(rainMetadata)
print(rainDataset.variables)

coldStartDateText = METGET_GFS_WIND_FILE_NAME[34: 42] + "T" + METGET_GFS_WIND_FILE_NAME[42:44]
coldStartDate = datetime.fromisoformat(coldStartDateText)
print("coldStartDate", coldStartDate)

print("number of timesteps")
timesteps = len(windDataset.variables["time"][:])
print(timesteps)

minT = windDataset.variables["time"][0].data
maxT = windDataset.variables["time"][-1].data

print("deltaT of data")
windDeltaT = timedelta(minutes=maxT - minT)
print(windDeltaT)

print("start of wind data (seconds since coldstart)")
startDate = coldStartDate + timedelta(minutes=float(minT))
endDate = coldStartDate + timedelta(minutes=float(maxT))
print("startDate", startDate)
print("endDate", endDate)

times = []
for index in range(timesteps):
    time = coldStartDate + timedelta(minutes=float(windDataset.variables["time"][index].data))
    times.append(time.timestamp())

# GFS Data is grid based system
print("min max latitude and longitude")
minLatitude = windDataset.variables["lat"][0].data
minLongitude = windDataset.variables["lon"][0].data
maxLatitude = windDataset.variables["lat"][-1].data
maxLongitude = windDataset.variables["lon"][-1].data

print("minLatitude", minLatitude)
print("minLongitude", minLongitude)
print("maxLatitude", maxLatitude)
print("maxLongitude", maxLongitude)

deltaLatitude = maxLatitude - minLatitude
deltaLongitude = maxLongitude - minLongitude

print("deltaLatitude", deltaLatitude)
print("deltaLongitude", deltaLongitude)

deltaNodesLatitude = len(windDataset.variables["lat"][:])
deltaNodesLongitude = len(windDataset.variables["lon"][:])

print("deltaNodesLatitude", deltaNodesLatitude)
print("deltaNodesLongitude", deltaNodesLongitude)

print("Wind at t=0, point(0, 0)")
windX000 = windDataset.variables["wind_u"][0][0][0]
windY000 = windDataset.variables["wind_v"][0][0][0]
print("windX000", windX000)
print("windY000", windY000)

# Find node indexes that are closest to NOS_Stations
# with open(NOS_STATIONS_FILE_NAME) as stations_file:
#     stationsDict = json.load(stations_file)
    
# stationToNodeDistancesDict = {}
# 
# # Set to true to recreate station to node distances calculations dictionary
# initializeStationToNodeDistancesDict = False
# if(initializeStationToNodeDistancesDict):
#     for stationKey in stationsDict["NOS"].keys():
#         stationToNodeDistancesDict[stationKey] = {}
# 
#     for longitudeIndex in range(deltaNodesLongitude):
#         for latitudeIndex in range(deltaNodesLatitude):
#             node = (float(windDataset.variables["lat"][latitudeIndex].data), float(windDataset.variables["lon"][longitudeIndex].data))
#             nodeIndex = str((latitudeIndex, longitudeIndex))
#             if(node[0] <= 90 and node[0] >= -90):
#                 for stationKey in stationsDict["NOS"].keys():
#                     stationDict = stationsDict["NOS"][stationKey]
#                     stationCoordinates = (float(stationDict["latitude"]), float(stationDict["longitude"]))
#                     distance = haversine.haversine(stationCoordinates, node)
#                     if(len(stationToNodeDistancesDict[stationKey].keys()) == 0):
#                         stationToNodeDistancesDict[stationKey]["nodeIndex"] = nodeIndex
#                         stationToNodeDistancesDict[stationKey]["distance"] = distance
#                     elif(stationToNodeDistancesDict[stationKey]["distance"] > distance):
#                         stationToNodeDistancesDict[stationKey]["nodeIndex"] = nodeIndex
#                         stationToNodeDistancesDict[stationKey]["distance"] = distance
#             else:
#                 badNodes.append(nodeIndex)
#                 print("bad node", nodeIndex, node)
#         
#     print("stationToNodeDistancesDict", stationToNodeDistancesDict)
# 
#     with open(NOS_STATION_TO_GFS_NODE_DISTANCES_FILE_NAME, "w") as outfile:
#         json.dump(stationToNodeDistancesDict, outfile)
# 
# with open(NOS_STATION_TO_GFS_NODE_DISTANCES_FILE_NAME) as outfile:
#     stationToNodeDistancesDict = json.load(outfile)
#   
# gfsNodes = {"NOS": {}}
#     
# initializeGFSNodesDict = False
# if(initializeGFSNodesDict):
#     for stationKey in stationToNodeDistancesDict.keys():
#         stationToNodeDistanceDict = stationToNodeDistancesDict[stationKey]
#         nodeIndex = stationToNodeDistanceDict["nodeIndex"]
#         gfsNodes["NOS"][nodeIndex] = {}
#         gfsNodes["NOS"][nodeIndex]["latitude"] = float(windDataset.variables["lat"][extractLatitudeIndex(nodeIndex)].data)
#         gfsNodes["NOS"][nodeIndex]["longitude"] = float(windDataset.variables["lon"][extractLongitudeIndex(nodeIndex)].data)
#         gfsNodes["NOS"][nodeIndex]["stationKey"] = stationKey
#     
#     with open(NOS_GFS_NODES_FILE_NAME, "w") as outfile:
#         json.dump(gfsNodes, outfile)
# 
# with open(NOS_GFS_NODES_FILE_NAME) as outfile:
#     gfsNodes = json.load(outfile)
# 
# initializeGFSWindDataDict = True
# if(initializeGFSWindDataDict):
#     gfsWindData = {}
#     for nodeIndex in gfsNodes["NOS"].keys():
#         gfsWindData[nodeIndex] = {}
#         gfsWindData[nodeIndex]["latitude"] = float(windDataset.variables["lat"][extractLatitudeIndex(nodeIndex)].data)
#         gfsWindData[nodeIndex]["longitude"] = float(windDataset.variables["lon"][extractLongitudeIndex(nodeIndex)].data)
#         gfsWindData[nodeIndex]["stationKey"] = gfsNodes["NOS"][nodeIndex]["stationKey"]
#         gfsWindData[nodeIndex]["times"] = times
#         windsX = []
#         windsY = []
#         for index in range(timesteps):
#             windsX.append(float(windDataset.variables["wind_u"][index][extractLongitudeIndex(nodeIndex)][extractLatitudeIndex(nodeIndex)]))
#             windsY.append(float(windDataset.variables["wind_v"][index][extractLongitudeIndex(nodeIndex)][extractLatitudeIndex(nodeIndex)]))
#         gfsWindData[nodeIndex]["windsX"] = windsX
#         gfsWindData[nodeIndex]["windsY"] = windsY
#     
#     with open(NOS_GFS_WIND_DATA_FILE_NAME, "w") as outfile:
#         json.dump(gfsWindData, outfile)
#         
# initializeGFSRainDataDict = True
# if(initializeGFSRainDataDict):
#     gfsRainData = {}
#     for nodeIndex in gfsNodes["NOS"].keys():
#         gfsRainData[nodeIndex] = {}
#         gfsRainData[nodeIndex]["latitude"] = float(rainDataset.variables["lat"][extractLatitudeIndex(nodeIndex)].data)
#         gfsRainData[nodeIndex]["longitude"] = float(rainDataset.variables["lon"][extractLongitudeIndex(nodeIndex)].data)
#         gfsRainData[nodeIndex]["stationKey"] = gfsNodes["NOS"][nodeIndex]["stationKey"]
#         gfsRainData[nodeIndex]["times"] = times
#         rains = []
#         for index in range(timesteps):
#             rains.append(float(rainDataset.variables["rain"][index][extractLongitudeIndex(nodeIndex)][extractLatitudeIndex(nodeIndex)]))
#         gfsRainData[nodeIndex]["rains"] = rains
#     
#     with open(NOS_GFS_RAIN_DATA_FILE_NAME, "w") as outfile:
#         json.dump(gfsRainData, outfile)
#     
# initializeGFSNodesWindDataDict = False
# if(initializeGFSNodesWindDataDict):
#     gfsNodesWindData = {}
#     for longitudeIndex in range(deltaNodesLongitude):
#         for latitudeIndex in range(deltaNodesLatitude):
#             nodeIndex = str((latitudeIndex, longitudeIndex))
#             gfsNodesWindData[nodeIndex] = {}
#             gfsNodesWindData[nodeIndex]["latitude"] = float(windDataset.variables["lat"][latitudeIndex].data)
#             gfsNodesWindData[nodeIndex]["longitude"] = float(windDataset.variables["lon"][longitudeIndex].data)
#             gfsNodesWindData[nodeIndex]["times"] = times
#             windsX = []
#             windsY = []
#             for index in range(timesteps):
#                 windsX.append(windDataset.variables["wind_u"][index][longitudeIndex][latitudeIndex])
#                 windsY.append(windDataset.variables["wind_v"][index][longitudeIndex][latitudeIndex])
#             gfsNodesWindData[nodeIndex]["windsX"] = windsX
#             gfsNodesWindData[nodeIndex]["windsY"] = windsY
#     
#     with open(NOS_GFS_NODES_WIND_DATA_FILE_NAME, "w") as outfile:
#         json.dump(gfsNodesWindData, outfile)