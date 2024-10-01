from scipy.io import loadmat
import fugropylib
import xarray as xr

adcp = r'..\..\..\08 Data\05 Measured data\Neptune_Sensor_1.mat'
mat = loadmat(adcp, simplify_cells =True)

date = np.vstack((mat['SerYear'].ravel() + 2000, mat['SerMon'].ravel(),
                  mat['SerDay'].ravel(), mat['SerHour'].ravel(),
                  mat['SerMin'].ravel(), mat['SerSec'].ravel())).T
new_date = [dtm.datetime(*x) for x in date]
new_depth = (mat['RDIBinSize'] * mat['SerBins'] + mat['RDIBin1Mid']).ravel() * -1

DS = xr.Dataset(data_vars={
   'Spd': (('date', 'depth'), mat['SerMagmmpersec'] / 1000),
   'Dir': (('date', 'depth'), mat['SerDir10thDeg'] / 10),
   'count1': (('date', 'depth'),mat['SerC1cnt']),
   'count2': (('date', 'depth'),mat['SerC2cnt']),
   'count3': (('date', 'depth'),mat['SerC3cnt']),
   'count4': (('date', 'depth'),mat['SerC4cnt']),
   'echo1': (('date', 'depth'),mat['SerEA1cnt']),
   'echo2': (('date', 'depth'),mat['SerEA2cnt']),
   'echo3': (('date', 'depth'),mat['SerEA3cnt']),
   'echo4': (('date', 'depth'),mat['SerEA4cnt']),    
   'echoA': (('date', 'depth'),mat['SerEAAcnt']),    
   'PG1': (('date', 'depth'),mat['SerPG1']),
   'PG2': (('date', 'depth'),mat['SerPG2']),
   'PG3': (('date', 'depth'),mat['SerPG3']),
   'PG4': (('date', 'depth'),mat['SerPG4']),
   'VSPD': (('date', 'depth'),mat['SerVmmpersec']),
   'ERRVL': (('date', 'depth'),mat['SerErmmpersec'])},
    coords={'date': new_date, 'depth': new_depth})
DS = DS.sortby("date")

time = fugropylib.Aid.dadatetime_2matlab(DS_QCed.date)
out = fugropylib.Mat.fmdm_meta(lat=27.37, lon=-89.92,
                                waterdepth=1425.23,
                                Contract='GC613A Neptune')
out['Current'] = {}
out['Current']['t'] = time
out['Current']['Spd'] = DS_QCed.Spd.values
out['Current']['Dir'] = DS_QCed.Dir.values
out['Current']['depth'] = [int(i) for i in DS_QCed.depth]
fugropylib.Mat.save('ADCP_sensor_1_Qced_FMDM.mat', {'Data':out})
