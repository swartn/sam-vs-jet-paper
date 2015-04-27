"""
Computes the same index for the 20CR ensemble and saves them to DataFrames in HDF5.

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

# Go to the data location
pp = '/raid/ra40/data/ncs/reanalyses/20CR/slp/'

# The 20CR file with ensemble members stacked in the k-dimension
fn = 'prmsl_1871-2012.mon.mean.nc'
zmfn = 'zonmean_' + fn
# Use cdo to get the p at 40S, 65S and compute the SAM.
# First make a zonal mean
#cdo.zonmean(input=pp+fn, output=pp+zmfn)

# load the data and make dataframes
dims = cd.get_dimensions(pp+zmfn, 'prmsl', toDatetime=True)
sam_20cr = calc_sam(zmfn, 'prmsl', pp, start_date='1871-01-01',
                     end_date='2013-12-31')

df_sam = pd.DataFrame(sam_20cr, index=dims['time'])

# Create a place to put the data
store = pd.HDFStore(
           '/raid/ra40/data/ncs/reanalyses/20CR/20cr_ensemble_sam_analysis.h5', 'a')
store['sam'] = df_sam
store.close()

# cleanup
os.system('rm -f p*' + fn + ' ' + zmfn + ' ' + 'SAM_' + fn)

