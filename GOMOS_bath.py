import xarray as xr
import pandas as pd

df = pd.read_csv('GOMOS2014_7km.csv')
ds = df.set_index(['Latitude', 'Longitude']).to_xarray()
compression = dict(zlib=True, complevel=5)  # Adjust complevel (1-9) as needed
encoding = {var: compression for var in ds.data_vars}
ds.to_netcdf('GOMOS7km.nc', encoding=encoding)
