import xarray as xr
import numpy as np

ds = xr.open_dataset(r'ETOPO_2022_v1_60s_N90W180_bed.nc')
ds_subsampled = ds.isel(lat=slice(None, None, 4), lon=slice(None, None, 4))

ds_subsampled['z'] = ds_subsampled['z'].where(ds_subsampled['z'] <= 10, np.nan)

compression = dict(zlib=True, complevel=5)  # Adjust complevel (1-9) as needed
encoding = {var: compression for var in ds_subsampled.data_vars}

# Save the modified dataset with compression
ds_subsampled.to_netcdf('ETOPO_2022_v1_240s_N90W180_bath.nc', encoding=encoding)

