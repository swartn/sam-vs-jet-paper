"""
Computes the sam index for various reanalyses and saves them to DataFrames in HDF5.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""

import cdo as cdo; cdo = cdo.Cdo() # recommended import
import os
import numpy as np
from netCDF4 import Dataset,num2date,date2num
os.system( 'rm -rf /tmp/cdo*') # clean out tmp to make space for CDO processing.
import pandas as pd
import cmipdata as cd
from calc_sam import calc_sam

# The data location
pp = '/raid/ra40/data/ncs/reanalyses/slp/'

# list in the pre-defined list of files to use. 
rean = ['R1', 'R2', '20CR', 'ERA-Int', 'CFSR', 'MERRA']
rean2 = ['R1', 'R2', '20CR', 'ERA', 'CFSR', 'MERRA']
tail = '_slp.mon.mean.nc'
names = [ r + tail for r in rean ]

# Use cdo to get the p at 40S, 65S and compute the SAM.
# First make a zonal mean
#for name in names:
#    cdo.zonmean(input='-selvar,slp ' + pp + name, output= pp + 'zonmean_' + name)

df_sam = pd.DataFrame()
 
for i, name in enumerate(names):
    print name
    # load the data and make dataframes
    dims = cd.get_dimensions(pp + 'zonmean_' + name, 'slp', toDatetime=True)
    dims['time'] = [pd.datetime(d.year, d.month, 1) for d in dims['time']]
    sami = calc_sam('zonmean_' + name, 'slp', pp)
    samdf = pd.DataFrame(sami, index=dims['time']) 
    df_sam = pd.concat([df_sam, samdf], axis=1)
    
df_sam.columns = rean2
    
## Create a place to put the data
store = pd.HDFStore(
           '/raid/ra40/data/ncs/cmip5/sam/reanalysis_zonmean_sam-jet_analysis.h5', 
           'a')
store['sam'] = df_sam
store.close()    