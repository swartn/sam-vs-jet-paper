import cdo as cdo; cdo = cdo.Cdo() # recommended import
import os
import numpy as np
from netCDF4 import Dataset,num2date,date2num
os.system( 'rm -rf /tmp/cdo*') # clean out tmp to make space for CDO processing.
import pandas as pd
import cmipdata as cd

# Go to the data location
pp = '/raid/ra40/data/ncs/reanalyses/20CR/slp/'
os.chdir(pp)

# The 20CR file with ensemble members stacked in the k-dimension
fn = 'prmsl_1871-2012.mon.mean.nc'
zmfn = 'zonmean_' + fn
# Use cdo to get the p at 40S, 65S and compute the SAM.
# First make a zonal mean
cdo.zonmean(input=fn, output=zmfn)

# Extract the pressure at 40 and 65S
cdo.remapnn('lon=0/lat=-40.0', input=zmfn, output='p40s_' + fn)
cdo.remapnn('lon=0/lat=-65.0', input=zmfn, output='p65s_' + fn)

# Compute the SAM index
cdo.sub(input='p40s_' + fn + ' ' + 'p65s_' + fn + ' ', output='SAM_' + fn
         , options =  '-f nc')

# load the data and make dataframes
dims = cd.get_dimensions('SAM_' + fn, 'prmsl', toDatetime=True)
sam_20cr = cd.loadvar('SAM_' + fn, 'prmsl')
p40s_20cr = cd.loadvar('p40s_' + fn, 'prmsl')
p65s_20cr = cd.loadvar('p65s_' + fn, 'prmsl')

df_sam = pd.DataFrame(sam_20cr, index=dims['time'])
#df_p40s = pd.DataFrame(p40s_20cr, index=dims['time'])
#df_p65s = pd.DataFrame(p65s_20cr, index=dims['time'])

# Create a place to put the data
store = pd.HDFStore(
           '/raid/ra40/data/ncs/reanalyses/20CR/20cr_ensemble_sam_analysis.h5', 'a')
store['sam'] = df_sam
#store['p40s'] = df_p40s
#store['p65s'] = df_p65s
store.close()

# cleanup
os.system('rm -f p*' + fn + ' ' + zmfn + ' ' + 'SAM_' + fn)

