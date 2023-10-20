. ./MetGetEnv.sh
# This command gets wind
# metget build --domain gfs 0.1 -80.0 30.0 -60.0 50.0 --start '2023-09-14 13:00' --end '2023-09-19 06:00' --variable wind_pressure  --format generic-netcdf --timestep 3600 --strict --compression --output adcirc_gfs_analysis_wind_pressure_2023091413-2023091906 --multiple-forecasts

# This command resulted in just returning ice with no wind
# metget build --domain gfs 0.1 -80.0 30.0 -60.0 50.0 --start '2023-09-14 13:00' --end '2023-09-19 06:00' --variable wind_pressure --variable rain --variable temperature --variable humidity --variable ice  --format generic-netcdf --timestep 3600 --strict --compression --output adcirc_gfs_analysis_wind_pressure_2023091413-2023091906 --multiple-forecasts


# metget build --domain gfs 0.1 -80.0 30.0 -60.0 50.0 --start '2023-09-14 13:00' --end '2023-09-19 06:00' --variable rain --format generic-netcdf --timestep 3600 --strict --compression --output adcirc_gfs_analysis_rain_2023091413-2023091906 --multiple-forecasts

# Get december noreaster 2022 dec 14 - 2022 dec 19
metget build --domain gfs 0.1 -80.0 30.0 -60.0 50.0 --start '2022-12-14 13:00' --end '2022-12-19 06:00' --variable wind_pressure  --format generic-netcdf --timestep 3600 --strict --compression --output adcirc_gfs_analysis_wind_pressure_2022121413-2022121906 --multiple-forecasts
metget build --domain gfs 0.1 -80.0 30.0 -60.0 50.0 --start '2022-12-14 13:00' --end '2022-12-19 06:00' --variable rain --format generic-netcdf --timestep 3600 --strict --compression --output adcirc_gfs_analysis_rain_2022121413-2022121906 --multiple-forecasts

