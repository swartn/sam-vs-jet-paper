"""
Computes kinematic properties of the jet for the various reanalyses and saves them 
to DataFrames in HDF5.

In this case base on 10 m winds.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""

# Calculate the kinematic properties of the SH westerly jet and save them in an HDF 
# store containing PD DataFrames.
import os
import numpy as np
from netCDF4 import Dataset,num2date,date2num
os.system( 'rm -rf /tmp/cdo*') # clean out tmp to make space for CDO processing.
import pandas as pd
import cmipdata as cd
import cdo as cdo; cdo = cdo.Cdo() # recommended import
import matplotlib.pyplot as plt
plt.ion()
from calc_shw_jet_properties import jetprop

# The data location
pp = '/raid/ra40/data/ncs/reanalyses/uwnd/'

# list in the pre-defined list of files to use. 
rean = ['R1', 'R2', '20CR', 'ERA-Int', 'CFSR', 'MERRA']
rean2 = ['R1', 'R2', '20CR', 'ERA', 'CFSR', 'MERRA']
tail = '_uwnd.10m.mon.mean.nc'
names = [ r + tail for r in rean ]

# Use cdo to get the p at 40S, 65S and compute the SAM.
# First make a zonal mean
#for name in names:
#    cdo.zonmean(input='-selvar,uwnd ' + pp + name, output= pp + 'zonmean_' + name)

df_umax = pd.DataFrame()
df_uloc = pd.DataFrame()
df_width = pd.DataFrame()
ri = 49
for i, name in enumerate(names):
    # load the data and make dataframes
    dims = cd.get_dimensions(pp + 'zonmean_' + name, 'uwnd', toDatetime=True)
    dims['time'] = [pd.datetime(d.year, d.month, 1) for d in dims['time']]
    
    nc = Dataset(pp + 'zonmean_' + name)
    uwnd = nc.variables['uwnd'][:].squeeze()
    lat = dims['lat']
    jetmax, latofmax, latn, lats, jetwidth = jetprop(uwnd, lat)
    df = pd.DataFrame(jetmax, index=dims['time'])
    df_umax = pd.concat([df_umax, df], axis=1)
    df = pd.DataFrame(latofmax, index=dims['time'])
    df_uloc = pd.concat([df_uloc, df], axis=1)
    df = pd.DataFrame(jetwidth, index=dims['time'])
    df_width = pd.concat([df_width, df], axis=1)
    #plt.close()
    #plt.plot( lat, uwnd[ri,:], 'k-o', linewidth=2)
    #plt.plot( lat, lat*0, 'k--')
    #plt.plot( latofmax[ri], jetmax[ri], 'rx', markersize=8, markeredgewidth=1)
    #plt.plot(  [-90, 90], [ jetmax[ri],jetmax[ri]  ], 'r--')
    #plt.plot(  [-90, 90], [ jetmax[ri]*0.5, jetmax[ri]*0.5], 'r--')
    
    ##print latn[ri], lats[ri]
    #plt.plot( [latn[ri], latn[ri]], [-10, 10], 'r--')
    #plt.plot( [lats[ri], lats[ri]], [-10, 10], 'r--')
    #raw_input('go?')
    
df_umax.columns = rean2
df_uloc.columns = rean2
df_width.columns = rean2
   
# Create a place to put the data
store = pd.HDFStore(
           '/raid/ra40/data/ncs/cmip5/sam/reanalysis_zonmean_sam-jet_analysis.h5', 
           'a')
store['width'] = df_width
store['maxspd'] = df_umax
store['locmax'] = df_uloc
store.close()      