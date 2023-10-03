import netCDF4 as nc
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
node0 = (float(windDataset.variables["x"][0].data), float(windDataset.variables["y"][0].data))
print("node0", node0)

numberOfNodes = windDataset.variables["x"].shape[0]

print("number of nodes", numberOfNodes)
print("wind at top right of grid")
windX0 = windDataset.variables["windx"][0][0]
windY0 = windDataset.variables["windy"][0]
print("windX0", windX0)
print("windY0", windY0)