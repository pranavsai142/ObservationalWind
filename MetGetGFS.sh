. ./MetGetEnv.sh

metget build --domain gfs 0.1 -80.0 30.0 -60.0 50.0 --start '2023-09-14 13:00' --end '2023-09-19 06:00' --variable wind_pressure --format generic-netcdf --timestep 3600 --strict --compression --output adcirc_gfs_analysis_wind_pressure_2023091413-2023091906 --multiple-forecasts