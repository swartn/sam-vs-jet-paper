"""
Computes kinematic properties of the jet for the 20CR ensemble and saves them to 
DataFrames in HDF5.

In this case the computation is based of sigma-9950 level winds.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import os
import numpy as np
from netCDF4 import Dataset,num2date,date2num
import pandas as pd
import cmipdata as cd
import matplotlib.pyplot as plt
from calc_shw_jet_properties import jetprop
plt.ion()

# The data location
pp = '/raid/ra40/data/ncs/reanalyses/20CR/u_sig995/monthly/'
#os.chdir(pp)

# The 20CR file with ensemble members stacked in the k-dimension
fn = pp + 'u9950_1871-2012.mon.mean.nc'
zmfn = pp + 'zonmean_' + 'u9950_1871-2012.mon.mean.nc'

# Use cdo to get the p at 40S, 65S and compute the SAM.
# First make a zonal mean
#cdo.zonmean(input=fn, output=zmfn)

# load the data and make dataframes
dims = cd.get_dimensions(zmfn, 'u9950', toDatetime=True)
nc = Dataset(zmfn)
u_20cr = nc.variables['u9950'][:].squeeze()
lat = dims['lat']


ri = 10
width = np.zeros((len(dims['time']), 56))
umax = np.zeros((len(dims['time']), 56))
uloc = np.zeros((len(dims['time']), 56))
 
for i in np.arange(56):
    # step through the 56 ensemble members and compute statistic for each one.
    uas = np.squeeze(u_20cr[:,i,:])
    jetmax, latofmax, latn, lats, jetwidth = jetprop(uas, lat)
    umax[:,i] = jetmax
    uloc[:,i] = latofmax
    width[:,i] = jetwidth
    ## Plot the jet at a selected time-index, and put on the properties computed.
    #plt.close()
    #plt.plot( lat, uas[ri,:], 'k-o', linewidth=2)
    #plt.plot( lat, lat*0, 'k--')
    #plt.plot( latofmax[ri], jetmax[ri], 'rx', markersize=8, markeredgewidth=1)
    #plt.plot(  [-90, 90], [ jetmax[ri],jetmax[ri]  ], 'r--')
    #plt.plot(  [-90, 90], [ jetmax[ri]*0.5, jetmax[ri]*0.5], 'r--')
    
    #print latn[ri], lats[ri]
    #plt.plot( [latn[ri], latn[ri]], [-10, 10], 'r--')
    #plt.plot( [lats[ri], lats[ri]], [-10, 10], 'r--')
    #raw_input('go?')

# Put the data into Pandas DataFrames.
df_umax = pd.DataFrame(umax, index=dims['time'], columns=np.arange(1,57))
df_uloc = pd.DataFrame(uloc, index=dims['time'], columns=np.arange(1,57))
df_width = pd.DataFrame(width, index=dims['time'], columns=np.arange(1,57))
    
# Create a place to put the data in HDF5.
store = pd.HDFStore(
           '/raid/ra40/data/ncs/reanalyses/20CR/20cr_ensemble_sam_analysis.h5', 
           'a')
store['width'] = df_width
store['maxspd'] = df_umax
store['locmax'] = df_uloc
store.close()      