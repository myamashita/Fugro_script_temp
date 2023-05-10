import pandas as pd
import os

# Reanalysis GLB subset netcdf (just 1 day per request) EXPT 53.X: 01-01-1994 to 31-12-2015 3H
latitude_N = 28.6755
latitude_S = 26.6755
longitude_W = -91.8021
longitude_E = -89.8021

timerange = pd.date_range("1994-01-01", "1994-12-31", freq='1D')
for i in timerange:
    url = f'http://ncss.hycom.org/thredds/ncss/grid/GLBv0.08/expt_53.X/data/{i:%Y}?var=water_u&var=water_v&north={latitude_N}&west={longitude_W}&east={longitude_E}&south={latitude_S}&disableProjSubset=on&horizStride=1&time_start={i:%Y}-{i:%m}-{i:%d}T00%3A00%3A00Z&time_end={i:%Y}-{i:%m}-{i:%d}T21%3A00%3A00Z&timeStride=1&vertCoord=&accept=netcdf'
    wget = f'wget "{url}" -O {i:%Y%m%d}.nc'
    os.system(wget)
