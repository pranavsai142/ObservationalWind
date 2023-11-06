#!/usr/bin/env python3
# Contact: Josh Port (joshua_port@uri.edu)
#
# Scales observational wind data to 10m based on directional z0.
# Before running, convert observational data from Design Safe to a cell array and save it as a v7 .mat file.
# In Matlab:
#     load('/home/josh/Documents/renci_downloads/Wind Comparison/Michael_MET_Observed.mat')
#     MichaelWindObs = table2cell(MichaelWindObs);
#     save("MichaelWindObs_Cell.mat","-v7")
#
import datetime
import numpy
import os
import pickle
import scipy.interpolate
import scipy.io
import sys
pp_dir = "/home/josh/Documents/renci_downloads/Scale & Subset/richamp-support"  # UPDATE
sys.path.append(os.path.abspath(pp_dir))
import scale_and_subset  # noqa: E402
import water_z0  # noqa: E402

start = datetime.datetime.now()

hr_file = '/home/josh/Documents/renci_downloads/Wind Comparison/NLCD_z0_RICHAMP_Reg_Grid.nc'  # UPDATE
mat_file = '/home/josh/Downloads/MichaelWindObs_Cell.mat'  # UPDATE
out_file = 'JwpMichaelWindUpscaledDirectional.mat'  # UPDATE
z0_interp_file = '/home/josh/Downloads/z0_interp.pickle'  # UPDATE

# Load roughness file and create static z0 interpolant (for determining land vs. water)
hr_lat, hr_land_rough = scale_and_subset.Roughness.get_lat_and_land_rough(hr_file)
z0_hr = scale_and_subset.Roughness(hr_file, hr_lat, hr_land_rough)
z0_static_interpolant = scipy.interpolate.RectBivariateSpline(z0_hr.lat(), z0_hr.lon(), z0_hr.land_rough(), kx=1, ky=1)

# Load interpolant
with open(z0_interp_file, 'rb') as file:
    z0_directional_interpolant = pickle.load(file)

# Load observational data
michael_data = scipy.io.loadmat(mat_file)

k = 0.40
z_obs = 10
u10_jwp = {}

for i in range(0, len(michael_data['MichaelWindObs'])):
    lon_obs = michael_data['MichaelWindObs'][i, 3][0, 0]
    lat_obs = michael_data['MichaelWindObs'][i, 4][0, 0]
    orig_spd_ms = michael_data['MichaelWindObs'][i, 7]
    met_dir = michael_data['MichaelWindObs'][i, 9]
    station_ht_m = michael_data['MichaelWindObs'][i, 11][0, 0]

    # Sanitize data; met_dir appears to be NaN for some stations instead of 0 degrees; whoever prepped this data must have divided by 0 in their trig functions
    met_dir[numpy.isnan(met_dir)] = 0

    # Get roughness at station location; based on derived u* over open water and directional z0 when under the influence of land
    z0_static = z0_static_interpolant(lat_obs, lon_obs)
    if i not in [0, 1, 10, 16]:  # These stations are outside the interpolant domain
        z0_directional = z0_directional_interpolant((lat_obs, lon_obs, met_dir))
    else:
        z0_directional = numpy.zeros(met_dir.shape) + z0_static  # use static z0 if directional z0 is unavailable
    ust_est = water_z0.retrieve_ust_U10(orig_spd_ms, station_ht_m)
    ust_est[ust_est == 0] = 0.0000000001  # Avoid divide by zero errors
    z0 = z0_static * numpy.exp(-(k * orig_spd_ms) / ust_est)
    for j in range(0, len(orig_spd_ms)):
        if z0_directional[j] > .0031:  # z0 = 0.003 corresponds to water in the NLCD file (FEMA mappings)
            z0[j] = z0_directional[j]

    # Scale wind using equations 9 & 10 here: https://dr.lib.iastate.edu/handle/20.500.12876/1131
    b = 1 / (numpy.log(10) - numpy.log(z0))  # Eq 10
    tenm_spd_ms = orig_spd_ms * (1 + b * numpy.log(station_ht_m / 10))  # Eq 9

    key = 'station_' + str(i + 1)  # Matlab requires this to be alphanumeric and start with a letter
    u10_jwp[key] = tenm_spd_ms

# Save output to a .mat file
scipy.io.savemat(out_file, u10_jwp)
print("Observational wind data scaling complete. Runtime:", str(datetime.datetime.now() - start))
