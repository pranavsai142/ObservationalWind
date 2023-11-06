. ./MetGetEnv.sh
# This command gets wind for Lee
# metget build --domain gfs 0.1 -80.0 30.0 -60.0 50.0 --start '2023-09-14 13:00' --end '2023-09-19 06:00' --variable wind_pressure  --format generic-netcdf --timestep 3600 --strict --compression --output adcirc_gfs_analysis_wind_pressure_2023091413-2023091906 --multiple-forecasts

# This command gets rain for Lee
# metget build --domain gfs 0.1 -80.0 30.0 -60.0 50.0 --start '2023-09-14 13:00' --end '2023-09-19 06:00' --variable rain --format generic-netcdf --timestep 3600 --strict --compression --output adcirc_gfs_analysis_rain_2023091413-2023091906 --multiple-forecasts

# Getting lee NHC best track
# floodwater metget build --domain nhc-2023-al-13-036 0.1 -100.0 5.0 -60.0 47.0 --start '2023-08-27 06:00' --end '2023-09-14 06:00' --timestep 3600 --strict --compression --format raw --output adcirc_nhc_analysis_wind_pressure_2023082706-2023091406

# Get december noreaster 2022 dec 14 - 2022 dec 19
# metget build --domain gfs 0.1 -80.0 30.0 -60.0 50.0 --start '2022-12-20 00:00' --end '2022-12-24 00:00' --variable wind_pressure  --format generic-netcdf --timestep 3600 --strict --compression --output adcirc_gfs_analysis_wind_pressure_2022122000-2022122400 --multiple-forecasts
# metget build --domain gfs 0.1 -80.0 30.0 -60.0 50.0 --start '2022-12-20 00:00' --end '2022-12-24 00:00' --variable rain --format generic-netcdf --timestep 3600 --strict --compression --output adcirc_gfs_analysis_rain_2022122000-2022122400 --multiple-forecasts

# Wind For OTIS near Acapulco
metget build --domain gfs 0.1 -99.9 16.3 -98.9 17.3 --start '2023-10-22 22:00' --end '2023-10-29 21:00' --variable wind_pressure  --format generic-netcdf --timestep 3600 --strict --compression --output adcirc_gfs_analysis_wind_pressure_2023102222-2023102921 --multiple-forecasts
