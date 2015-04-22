import cdo as cdo; cdo = cdo.Cdo() # recommended import
import os
import numpy as np
from netCDF4 import Dataset,num2date,date2num
os.system( 'rm -rf /tmp/cdo*') # clean out tmp to make space for CDO processing.
import pandas as pd
import cmipdata as cd

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

def calc_sam(slp_file):
    # Extract the pressure at 40 and 65S
    cdo.remapnn('lon=0/lat=-40.0', input= '-selvar,slp ' + pp + slp_file, 
                output='p40s_' + slp_file)
    cdo.remapnn('lon=0/lat=-65.0', input='-selvar,slp ' + pp + slp_file, 
                output='p65s_' + slp_file)

    # Compute the SAM index
    cdo.sub(input='p40s_' + slp_file + ' '  
            + 'p65s_' + slp_file + ' ', output='SAM_' + slp_file, options ='-b F64')

    # load the data and make dataframes
    sam = cd.loadvar('SAM_' + slp_file, 'slp')
    
    # cleanup
    os.system('rm -f p*' + slp_file + ' ' + slp_file + ' ' + 'SAM_' + slp_file)
    return sam

df_sam = pd.DataFrame()
 
for i, name in enumerate(names):
    print name
    # load the data and make dataframes
    dims = cd.get_dimensions(pp + 'zonmean_' + name, 'slp', toDatetime=True)
    dims['time'] = [pd.datetime(d.year, d.month, 1) for d in dims['time']]
    sami = calc_sam('zonmean_' + name)
    samdf = pd.DataFrame(sami, index=dims['time']) 
    df_sam = pd.concat([df_sam, samdf], axis=1)
    
df_sam.columns = rean2
    
## Create a place to put the data
store = pd.HDFStore(
           '/raid/ra40/data/ncs/cmip5/sam/reanalysis_zonmean_sam-jet_analysis.h5', 
           'a')
store['sam'] = df_sam
store.close()    