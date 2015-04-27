"""
Computes the same index for the CMIP5 ensemble and saves them to DataFrames in HDF5.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import numpy as np
import pandas as pd
import cmipdata as cd
from calc_sam import calc_sam

# Go to the data location
pp = '/raid/ra40/data/ncs/cmip5/sam/c5_slp/'

# list in the pre-defined list of files to use. Should be 30 models.
f = open(pp + 'list_match_uas')
names = f.read()
names = filter(None, names.split('\n') ) # split and remove empty strings

sam = np.zeros((1596, 30))
dims = cd.get_dimensions(pp + names[0], 'psl', toDatetime=True)
t = dims['time']
a = ( t <= pd.datetime(2013,12,31) ) & ( t >= pd.datetime(1881,1,1) )
dims['time'] = t[a]
 
for i, name in enumerate(names):
    # load the data and make dataframes
    sam[:,i] = calc_sam(name, 'psl', pp, start_date='1881-01-01',
                        end_date='2013-12-31')

df_sam = pd.DataFrame(sam, index=dims['time'], columns=np.arange(1,31))
    
# Create a place to put the data
store = pd.HDFStore(
           '/raid/ra40/data/ncs/cmip5/sam/c5_zonmean_sam-jet_analysis.h5', 
           'a')
store['sam'] = df_sam
store.close()    