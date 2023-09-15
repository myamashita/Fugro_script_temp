import os
def list_empty_files(directory):
    # List all files in the given directory
    files_in_directory = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # Filter out only the empty files
    empty_files = [f for f in files_in_directory if os.path.getsize(os.path.join(directory, f)) == 0]

    return empty_files

directory_path = "./1999"  # change to your target directory
latitude_N = -20.8968
latitude_S = -22.8968
longitude_W = -41.5489
longitude_E = -39.5489
empty_files = list_empty_files(directory_path)
for f in empty_files[::-1]:
    print(f)
    url = f'http://ncss.hycom.org/thredds/ncss/grid/GLBv0.08/expt_53.X/data/{f[:4]}?var=water_u&var=water_v&north={latitude_N}&west={longitude_W}&east={longitude_E}&south={latitude_S}&disableProjSubset=on&horizStride=1&time_start={f[:4]}-{f[4:6]}-{f[6:8]}T00%3A00%3A00Z&time_end={f[:4]}-{f[4:6]}-{f[6:8]}T21%3A00%3A00Z&timeStride=1&vertCoord=&accept=netcdf'
    wget = f'wget "{url}" -O {f[:4]}/{f[:8]}.nc'
    os.system(wget)
