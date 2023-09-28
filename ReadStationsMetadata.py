import json

NOS_STATIONS_FILE_NAME = "NOS_Stations.json"

# Takes in Stations.csv created by deb, converted to csv. (Commas removed) 
file = open("Stations.csv")
stationsDict = {"NOS": {}}
stationsDict["NOS"] = {}
for line in file:
    data = line.split(",")
    if("NOS" in data[1]):
    	stationsDict["NOS"][data[0]] = {}
    	stationsDict["NOS"][data[0]]["id"] = data[1][4:]
    	stationsDict["NOS"][data[0]]["source"] = data[2]
    	stationsDict["NOS"][data[0]]["name"] = data[7]
    	stationsDict["NOS"][data[0]]["latitude"] = data[8]
    	stationsDict["NOS"][data[0]]["longitude"] = data[9]
    	stationsDict["NOS"][data[0]]["altitude"] = data[10]

for station in stationsDict["NOS"].keys():
	print(station)
	
with open(NOS_STATIONS_FILE_NAME, "w") as outfile:
    json.dump(stationsDict, outfile)