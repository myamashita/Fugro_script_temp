import pandas as pd
import os

# Reanalysis GoM subset netcdf (just 1 day per request) EXPT 50.1: 01-01-1993 to 31-12-2012 3H
latitude_N = 28.6755
latitude_S = 26.6755
longitude_W = -91.8021
longitude_E = -89.8021

timerange = pd.date_range("1993-01-01", "1993-12-31", freq='1D')
for i in timerange:
    url = f'http://ncss.hycom.org/thredds/ncss/GOMu0.04/expt_50.1/data/netcdf/1993?var=water_u&var=water_v&north={latitude_N}&west={longitude_W}&east={longitude_E}&south={latitude_S}&disableProjSubset=on&horizStride=1&time_start=1993-{i:%m}-{i:%d}T00%3A00%3A00Z&time_end=1993-{i:%m}-{i:%d}T21%3A00%3A00Z&timeStride=1&vertCoord=&accept=netcdf'
    wget = f'wget "{url}" -O {i:%Y%m%d}.nc'
    os.system(wget)
