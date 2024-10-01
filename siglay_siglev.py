from bokeh.io import output_notebook, show
import xarray as xr
import os
from scipy.io import loadmat
import requests
from netCDF4 import Dataset
import cftime

output_notebook()
aid = requests.get(r'https://raw.githubusercontent.com/myamashita/FUGRO_AID/0.1.1/aid.py').content
exec(aid)

url = "http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3"
ds = xr.open_dataset(url, decode_times=False, drop_variables=['siglay', 'siglev'])
nc = Dataset(url)
siglay = nc['siglay']
siglev = nc['siglev']

lat = 43.716625
lon = -69.323858
ds_point = ds.isel(node=(np.abs(ds.lon-lon)**2+np.abs(ds.lat-lat)**2).argmin(),
                   nele=(np.abs(ds.lonc-lon)**2+np.abs(ds.latc-lat)**2).argmin())
time_fix = cftime.num2date(ds_point.time, units=ds_point.time.units, calendar='gregorian')
ds_point = ds_point.assign_coords(time=time_fix)


surface = ds_point.sel(siglay=0)
surface.to_netcdf("saved_on_disk.nc")
