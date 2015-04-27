""" Subsample various reanalyses at the Marshall station locations and save 
output to pd DataFrames in HDF5.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import cmipdata as cd
import os
import numpy as np
import scipy as sp
import pandas as pd
from netCDF4 import Dataset
import h5py
import cdo as cdo; cdo = cdo.Cdo() # recommended import
os.system('rm -f /tmp/cdo*')
os.chdir('/raid/ra40/data/ncs/tmp_proc/')
from mpl_toolkits.basemap import Basemap, addcyclic
import matplotlib.pyplot as plt
import matplotlib as mpl
plt.ion()
plt.close('all')
font = {'size'   : 12}
plt.rc('font', **font)

path = '/raid/ra40/data/ncs/reanalyses/slp/'
rean = ['R1', 'R2', '20CR', 'ERA-Int', 'CFSR', 'MERRA', 'HadSLP2r']

# Marshall locations
mlat40s = np.array([46.9, 37.8, 42.9, 43.5, 39.6, 40.4])*-1
mlon40s = np.array([37.9, 77.5, 147.3, 172.6, -73.1, -9.9])

mlat65s = np.array([70.8, 67.6, 66.6, 66.3, 66.7, 65.2])*-1
mlon65s = np.array([11.8, 62.9, 93.0, 110.5, 140.0, -64.3])

# initalize empty dataframes
df40s = pd.DataFrame()
df65s = pd.DataFrame()
dfsam = pd.DataFrame()

def scale(ncvar, var):
    # Apply any scaling and offsetting needed:
    try:
        var_offset = ncvar.add_offset
    except:
        var_offset = 0
    try:
        var_scale = ncvar.scale_factor
    except:
        var_scale = 1   

    var = var*var_scale + var_offset
    #return var
    return np.squeeze( var ) 

for i, r in enumerate(rean):   
    # Get the dimensions and initialize arrays
    dims = cd.get_dimensions(path + r + '_slp.mon.mean.nc', 'slp'
			     , toDatetime=True)
    p40 = np.zeros((len(dims['time']), 6))
    p65 = np.zeros((len(dims['time']), 6))   
    tmin = dims['time'].min()
    ds = pd.datetime(tmin.year, tmin.month, 1)
    dates = pd.date_range(ds, periods=(len(dims['time']))
                          , freq='MS')
    ncvar = Dataset(path + r + '_slp.mon.mean.nc').variables['slp']

    for k in range(6):
	# loop over the six stations at each lat and get data at each one.
	var = cdo.remapnn('lon=' + str( mlon40s[k] ) + '/lat='\
	               + str( mlat40s[k] )
		       , input=('-selvar,slp ' + path + r + '_slp.mon.mean.nc')
		       , returnMaArray='slp').squeeze()
	p40[:,k] = scale(ncvar, var)
	
	var2 = cdo.remapnn('lon=' + str( mlon65s[k] ) + '/lat='\
	               + str( mlat65s[k] )
		       , input=('-selvar,slp ' + path + r + '_slp.mon.mean.nc')
		       , returnMaArray='slp').squeeze()
	p65[:,k] = scale(ncvar, var2)

    # Now create the mean pressure at 40S and 65S and add to dataframe
    s40s = pd.Series(p40.mean(axis=1), index=dates)
    s65s = pd.Series(p65.mean(axis=1), index=dates)
    df40s = pd.concat([df40s, s40s], axis=1)
    df65s = pd.concat([df65s, s65s], axis=1)
   
# assign column names to the dataframes and calculate SAM
df40s.columns = rean
df65s.columns = rean
dfsam = df40s - df65s
dft = pd.concat([df40s, df65s, dfsam], keys=['p40s', 'p65s', 'sam'])
#dft.to_csv('/raid/ra40/data/ncs/cmip5/sam/rean_marshall_sam')
h5f = pd.HDFStore('/raid/ra40/data/ncs/cmip5/sam/rean_sam.h5', 'a')
h5f['sam/df'] = dft
h5f.close() 

# setup a plot of the station positions.
def plot_stn_locs(lats, lons):
    m = Basemap(projection='ortho', lon_0=0,lat_0=-90,)
    m.drawcoastlines(linewidth=1.25)
    m.fillcontinents(color='0.8')
    m.drawparallels(np.arange(-80,81,20),labels=[1,0,0,0])
    m.drawmeridians(np.arange(0,360,30),labels=[1,1,1,1])
    x, y = m(lons, lats)
    m.plot(x,y, 'or', markersize=8)

if False:    
    lons = np.append(mlon40s, mlon65s)
    lats = np.append(mlat40s, mlat65s)
    plot_stn_locs(lats, lons)   
    