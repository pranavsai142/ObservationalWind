import scipy.io
from urllib.request import urlretrieve
from urllib.error import HTTPError
from datetime import datetime, timedelta
import json
from Encoders import NumpyEncoder

data = scipy.io.loadmat("Dec2022_MET.mat")
print(data["STN13"])
print(data["STN13"][0][0][0])
print(len(data["STN13"][0][0][2]))
data = scipy.io.loadmat("8411060.mat")
unixTimes = data["IOOS_Wind"]["time"][0][0].flatten()
windDirections = data["IOOS_Wind"]["Wind_Direction"][0][0].flatten()
windSpeeds = data["IOOS_Wind"]["Wind_Speed"][0][0].flatten()
windGusts = data["IOOS_Wind"]["Wind_Gust"][0][0].flatten()
print(len(windSpeeds))
print(unixTimes)