"""
Calculate the kinematic properties of the SH westerly jet for the CMIP5 ensemble 
and saves them in an HDF store containing PD DataFrames.

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
pp = '/raid/ra40/data/ncs/cmip5/sam/c5_uas/'

# list in the pre-defined list of files to use. Should be 30 models.
f = open(pp + 'list')
names = f.read()
names = filter(None, names.split('\n') ) # split and remove empty strings

ri = 10
width = np.zeros((1596, 30))
umax = np.zeros((1596, 30))
uloc = np.zeros((1596, 30))
 
for i, name in enumerate(names):
    # load the data and make dataframes
    dims = cd.get_dimensions(pp + name, 'uas', toDatetime=True)
    nc = Dataset(pp + name)
    uas = nc.variables['uas'][:].squeeze()
    lat = dims['lat']
    jetmax, latofmax, latn, lats, jetwidth = jetprop(uas, lat)
    umax[:,i] = jetmax
    uloc[:,i] = latofmax
    width[:,i] = jetwidth
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

df_umax = pd.DataFrame(umax, index=dims['time'], columns=np.arange(1,31))
df_uloc = pd.DataFrame(uloc, index=dims['time'], columns=np.arange(1,31))
df_width = pd.DataFrame(width, index=dims['time'], columns=np.arange(1,31))
    
# Create a place to put the data
store = pd.HDFStore(
           '/raid/ra40/data/ncs/cmip5/sam/c5_zonmean_sam-jet_analysis.h5', 
           'a')
store['width'] = df_width
store['maxspd'] = df_umax
store['locmax'] = df_uloc
store.close()      