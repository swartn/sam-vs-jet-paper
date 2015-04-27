""" Compute the SAM index in various reanalyses.

The SAM index is computed at the difference in zonal mean pressure between 40 and 
65S.

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
    p40 = np.zeros(len(dims['time']))
    p65 = np.zeros(len(dims['time']))   
    tmin = dims['time'].min()
    ds = pd.datetime(tmin.year, tmin.month, 1)
    dates = pd.date_range(ds, periods=(len(dims['time']))
                          , freq='MS')
    ncvar = Dataset(path + r + '_slp.mon.mean.nc').variables['slp']

    var = cdo.remapnn('lon=0/lat=-40'\
		       , input=('-zonmean -selvar,slp ' + path + r 
                       + '_slp.mon.mean.nc')
		       , returnMaArray='slp').squeeze()
    p40 = scale(ncvar, var)
	
    var2 = cdo.remapnn('lon=0/lat=-65'
                       , input=('-zonmean -selvar,slp ' 
                       + path + r + '_slp.mon.mean.nc')
		       , returnMaArray='slp').squeeze()
    p65 = scale(ncvar, var2)

    # Now create the mean pressure at 40S and 65S and add to dataframe
    s40s = pd.Series(p40, index=dates)
    s65s = pd.Series(p65, index=dates)
    df40s = pd.concat([df40s, s40s], axis=1)
    df65s = pd.concat([df65s, s65s], axis=1)
   
# assign column names to the dataframes and calculate SAM
df40s.columns = rean
df65s.columns = rean
dfsam = df40s - df65s
dft = pd.concat([df40s, df65s, dfsam], keys=['p40s', 'p65s', 'sam'])
#dft.to_csv('/raid/ra40/data/ncs/cmip5/sam/rean_marshall_sam')
h5f = pd.HDFStore('/raid/ra40/data/ncs/cmip5/sam/rean_sam.h5', 'a')
h5f['zonmean_sam/df'] = dft
h5f.close() 

