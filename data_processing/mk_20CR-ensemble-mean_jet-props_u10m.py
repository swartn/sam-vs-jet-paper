"""
Computes kinematic properties of the jet for the 20CR ensemble mean and saves them 
to DataFrames in HDF5.

This is for the ensemble mean 20CR computed from the individual members and using 
10 m winds.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""

import numpy as np
from netCDF4 import Dataset
import pandas as pd
import cmipdata as cd
import matplotlib.pyplot as plt
plt.ion()
from calc_shw_jet_properties import jetprop

# The data location
pp = '/raid/ra40/data/ncs/reanalyses/20CR/winds_10m/u_10m/'
#os.chdir(pp)

# The 20CR file with ensemble members stacked in the k-dimension
fn = pp + 'ensmean_u10m_1871-2012.mon.mean.nc'
zmfn = pp + 'zonmean_' + 'ensmean_u10m_1871-2012.mon.mean.nc'

# First make a zonal mean
#cdo.zonmean(input=fn, output=zmfn)

# load the data and make dataframes
dims = cd.get_dimensions(zmfn, 'u10m', toDatetime=True)
nc = Dataset(zmfn)
u_20cr = nc.variables['u10m'][:].squeeze()
lat = dims['lat']

ri = 10
width = np.zeros((len(dims['time'])))
umax = np.zeros((len(dims['time'])))
uloc = np.zeros((len(dims['time'])))
 
for i in np.arange(1):
    uas = np.squeeze(u_20cr[:,:])
    jetmax, latofmax, latn, lats, jetwidth = jetprop(uas, lat)
    umax = jetmax
    uloc = latofmax
    width = jetwidth
    plt.close()
    plt.plot( lat, uas[ri,:], 'k-o', linewidth=2)
    plt.plot( lat, lat*0, 'k--')
    plt.plot( latofmax[ri], jetmax[ri], 'rx', markersize=8, markeredgewidth=1)
    plt.plot(  [-90, 90], [ jetmax[ri],jetmax[ri]  ], 'r--')
    plt.plot(  [-90, 90], [ jetmax[ri]*0.5, jetmax[ri]*0.5], 'r--')
    
    print latn[ri], lats[ri]
    plt.plot( [latn[ri], latn[ri]], [-10, 10], 'r--')
    plt.plot( [lats[ri], lats[ri]], [-10, 10], 'r--')
    raw_input('go?')

df_umax = pd.DataFrame(umax, index=dims['time'], columns=[1])
df_uloc = pd.DataFrame(uloc, index=dims['time'], columns=[1])
df_width = pd.DataFrame(width, index=dims['time'], columns=[1])
    
## Create a place to put the data
store = pd.HDFStore(
           '/raid/ra40/data/ncs/reanalyses/20CR/20cr_ensemble_sam_analysis.h5', 
           'a')
store['ensmean/width'] = df_width
store['ensmean/maxspd'] = df_umax
store['ensmean/locmax'] = df_uloc
store.close()      