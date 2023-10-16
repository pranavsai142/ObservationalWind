# Queries NOAA NOS buoys and saves the data
# Pranav 9/25/2023
# Fuck matlab

import scipy.io
from urllib.request import urlretrieve
from urllib.error import HTTPError
from datetime import datetime, timedelta
import json
from Encoders import NumpyEncoder
        
NOS_STATIONS_FILE_NAME = "NOS_Stations.json"
NOS_WIND_FILE_NAME = "NOS_Wind.json"

with open(NOS_STATIONS_FILE_NAME) as stations_file:
    stationsDict = json.load(stations_file)

# stationIds = [8413320, 8443970, 8447435, 8449130, 8447930, 8452660, 8510560, 8418150, 8419870, 8454049, 8454000, 8461490, 8411060, 8531680, 8534720, 8452944]
# stationNames = ['Bar Harbor', 'Boston', 'Chatham', 'Nantucket', 'Woods Hole', 'Newport', 'Montauk', 'Portland', 'Seavey Island, ME', 'Quonset Point', 'Providence', 'New London', 'Cutler Faris Wharf', 'Sandy Hook', 'Altlantic City', 'Conimicut Light'] 
stationIds = [8413320, 8447435, 8449130, 8452660, 8418150, 8454049, 8454000, 8411060, 8531680, 8452944]
stationNames = ['Bar Harbor', 'Chatham', 'Nantucket', 'Newport', 'Portland', 'Quonset Point', 'Providence', 'Cutler Faris Wharf', 'Sandy Hook', 'Conimicut Light'] 

startDate = "20230914"
endDate = "20230919"
dateStartFormat = "2023-09-14"

altitudeStartDate = "2023-09-14T00:00:00Z"
altitudeEndDate = "2023-09-19T23:59:00Z"
    
badStations = []
windDict = {}
for key in stationsDict["NOS"].keys():
    stationDict = stationsDict["NOS"][key]
    stationId = stationDict["id"]
    stationName = stationDict["name"]
    url = "https://opendap.co-ops.nos.noaa.gov/erddap/tabledap/IOOS_Wind.mat?STATION_ID%2Ctime%2CWind_Speed%2CWind_Direction%2CWind_Gust&STATION_ID%3E=%22" + stationId + "%22&BEGIN_DATE%3E=%22" + startDate + "%22&END_DATE%3E=%22" + endDate + "%22&time%3E=" + dateStartFormat + "T00%3A00%3A00Z"
    altitudeURL = "https://opendap.co-ops.nos.noaa.gov/ioos-dif-sos/SOS?service=SOS&request=GetObservation&version=1.0.0&observedProperty=water_surface_height_above_reference_datum&offering=urn:ioos:station:NOAA.NOS.CO-OPS:" + stationId + "&responseFormat=text/csv&eventTime=" + altitudeStartDate + "/" + altitudeEndDate + "&unit=Meters"
    matFilename = stationDict["id"] + ".mat"
    altitudeFilename = stationDict["id"] + "_altitude.csv"
    try:
#     Once mat files are downloaded once, comment out this line to stop querying the API
    	urlretrieve(url, matFilename)
    	urlretrieve(altitudeURL, altitudeFilename)
    	data = scipy.io.loadmat(matFilename)
    	unixTimes = data["IOOS_Wind"]["time"][0][0].flatten()
    	windDirections = data["IOOS_Wind"]["Wind_Direction"][0][0].flatten()
    	windSpeeds = data["IOOS_Wind"]["Wind_Speed"][0][0].flatten()
    	windGusts = data["IOOS_Wind"]["Wind_Gust"][0][0].flatten()
    	windDict[key] = {}
    	windDict[key]["times"] = unixTimes
    	windDict[key]["directions"] = windDirections
    	windDict[key]["speeds"] = windSpeeds
    	windDict[key]["gusts"] = windGusts
    	
    	
    	file = open(altitudeFilename)
    	csvAltitudeTimes = []
    	csvAltitudeValues = []
    	skipHeader = True
    	for line in file:
    		if(skipHeader):
    			skipHeader = False
    		else:
    			data = line.split(",")
#     			print(data)
    			altitudeFormattedTime = data[4]
    			year = int(altitudeFormattedTime[0:4])
    			month = int(altitudeFormattedTime[5:7])
    			day = int(altitudeFormattedTime[8:10])
    			hour = int(altitudeFormattedTime[11:13])
    			minute = int(altitudeFormattedTime[14:16])
    			second = int(altitudeFormattedTime[17:19])
    			
    			altitudeTime = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
    			
    			altitudeValue = float(data[5])
    			csvAltitudeTimes.append(datetime.timestamp(altitudeTime))
    			csvAltitudeValues.append(altitudeValue)
    	print("CSV and .mat same length? " + stationName, len(csvAltitudeTimes) == len(unixTimes))
    	print("CSV Altitude Times vs unixTimes len", len(csvAltitudeTimes), len(unixTimes))
    	altitudeTime = datetime.timestamp(datetime(year=3000, month=1, day=1))
    	csvAltitudeTimes.append(altitudeTime)
    	altitudeIndex = 0
    	altitudeValues = []
    	for unixTime in unixTimes:
    		if(unixTime > csvAltitudeTimes[altitudeIndex + 1]):
    			altitudeIndex += 1
    		altitudeValues.append(csvAltitudeValues[altitudeIndex])
    	windDict[key]["altitudes"] = altitudeValues
    except (HTTPError, FileNotFoundError):
#     	print("oops bad url")
    	badStations.append(badStations.append(stationDict))
    	
# print(windDict)
with open(NOS_WIND_FILE_NAME, "w") as outfile:
    json.dump(windDict, outfile, cls=NumpyEncoder)
    	
#     print(type(data.get("Wind_Speed")))
#     print(type(data.get("Wind_Direction")))
	
# 	T=cat(1,T,(A.time/86400)+toff);
# 	WS=cat(1,WS,(A.Wind_Speed));
# 	WD=cat(1,WD,(A.Wind_Direction));
# 	G=cat(1,G,(A.Wind_Gust));
# 	Tstr=datestr(T);
# 	
# 	STNN=SS(i);
# 	STNa=SSN{i};
# 	
# 	sidn=['STN' str0(i) '.WS']; eval([sidn '=' 'WS']);
# 	sidn=['STN' str0(i) '.WD']; eval([sidn '=' 'WD']);
# 	sidn=['STN' str0(i) '.T']; eval([sidn '=' 'T']);
# 	sidn=['STN' str0(i) '.G']; eval([sidn '=' 'G']);
# 	sidn=['STN' str0(i) '.SN']; eval([sidn '=' 'STNN']);
# 	sidn=['STN' str0(i) '.SName']; eval([sidn '=' 'STNa']);
# 	sidn=['STN' str0(i) '.Tstr']; eval([sidn '=' 'Tstr']);
# 	
# 	aa=aa+1;
# 	STNS(aa)=i;
#     end
# end
# % return
# %%
# figure
# plot(T,WS,'LineWidth',2)
# hold on
# plot(T,G,'LineWidth',2)
# datetick('x','mm/dd-HH','keepticks');     
# legend('Wind Speed','Gust')
# ylabel('Wind Speed (m/s)')
# 
# figure
# plot(T,WD,'LineWidth',2)
# datetick('x','mm/dd-HH','keepticks');     
# legend('Wind Direction')
# ylabel('Wind Direction (Heading)')
