                    """# Find all unique coordinates across datasets
                    all_coords = set()
                    for ds in ds_list:
                        all_coords.update(ds.coords)
                    # Add missing coordinates to each dataset
                    for i, ds in enumerate(ds_list):
                        missing_coords = all_coords - set(ds.coords)
                        for coord in missing_coords:
                            ds = ds.assign_coords({coord:(coord, [0.0])})
                            ds_list[i] = ds
                    datasets = [self._round_coords(ds) for ds in ds_list]
                    ds = xr.concat(datasets, dim='time')"""
