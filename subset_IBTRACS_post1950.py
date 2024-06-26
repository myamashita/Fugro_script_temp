import xarray as xr
import numpy as np
import pandas as pd

# Load the dataset
ds = xr.open_dataset(r'IBTrACS.ALL.v04r00.nc')
ds = ds.isel(storm=ds.season >= 1950) 
compression = dict(zlib=True, complevel=5)  # Adjust complevel (1-9) as needed
encoding = {var: compression for var in ds.data_vars}
ds.to_netcdf('IBTrACS_post1950_v04r00.nc', encoding=encoding)
