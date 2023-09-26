# Queries NOAA NOS buoys and saves the data
# Pranav 9/25/2023
# Fuck matlab

import scipy.io
from urllib.request import urlretrieve
from urllib.error import HTTPError

stationIds = [8413320, 8443970, 8447435, 8449130, 8447930, 8452660, 8510560, 8418150, 8419870, 8454049, 8454000, 8461490, 8411060, 8531680, 8534720, 8452944]
stationNames = ['Bar Harbor', 'Boston', 'Chatham', 'Nantucket', 'Woods Hole', 'Newport', 'Montauk', 'Portland', 'Seavey Island, ME', 'Quonset Point', 'Providence', 'New London', 'Cutler Faris Wharf', 'Sandy Hook', 'Altlantic City', 'Conimicut Light'] 
startDate = "20230912"
endDate = "20230919"
dateStartFormat = "2023-09-12"
    
for x in range(len(stationNames)):
# for x in range(1)
    stationId = str(stationIds[x])
    url='https://opendap.co-ops.nos.noaa.gov/erddap/tabledap/IOOS_Wind.mat?STATION_ID%2Ctime%2CWind_Speed%2CWind_Direction%2CWind_Gust&STATION_ID%3E=%22' + stationId + '%22&BEGIN_DATE%3E=%22' + startDate + '%22&END_DATE%3E=%22' + endDate + '%22&time%3E=' + dateStartFormat + 'T00%3A00%3A00Z'
    matFilename = stationId + ".mat"
    try:
    	urlretrieve(url, matFilename)
    	data = scipy.io.loadmat(matFilename)
    	print(data["IOOS_Wind"]["time"])
    	print(data["IOOS_Wind"]["Wind_Direction"])
    	print(data["IOOS_Wind"]["Wind_Speed"])
    	print(data["IOOS_Wind"]["Wind_Gust"])
    except HTTPError:
    	print("oops bad url" + url)
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