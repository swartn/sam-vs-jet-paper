import cdo as cdo; cdo = cdo.Cdo() # recommended import
import os
import numpy as np
from netCDF4 import Dataset,num2date,date2num
os.system( 'rm -rf /tmp/cdo*') # clean out tmp to make space for CDO processing.
import pandas as pd
import cmipdata as cd

# Go to the data location
pp = '/raid/ra40/data/ncs/cmip5/sam/c5_slp/'

# list in the pre-defined list of files to use. Should be 30 models.
f = open(pp + 'list_match_uas')
names = f.read()
names = filter(None, names.split('\n') ) # split and remove empty strings

def calc_sam(psl_file):
    # Extract the pressure at 40 and 65S
    cdo.remapnn('lon=0/lat=-40.0', input=pp + psl_file, output='p40s_' + psl_file)
    cdo.remapnn('lon=0/lat=-65.0', input=pp + psl_file, output='p65s_' + psl_file)

    # Compute the SAM index
    cdo.sub(input='p40s_' + psl_file + ' ' + 'p65s_' + psl_file + ' ', 
            output='SAM_' + psl_file, options =  '-f nc')

    # load the data and make dataframes
    sam = cd.loadvar('SAM_' + psl_file, 'psl', start_date='1881-01-01',
                     end_date='2013-12-31')
    
    # cleanup
    os.system('rm -f p*' + psl_file + ' ' + psl_file + ' ' + 'SAM_' + psl_file)
    return sam, dims

sam = np.zeros((1596, 30))
dims = cd.get_dimensions(pp + names[0], 'psl', toDatetime=True)
t = dims['time']
a = ( t <= pd.datetime(2013,12,31) ) & ( t >= pd.datetime(1881,1,1) )
dims['time'] = t[a]
 
for i, name in enumerate(names):
    # load the data and make dataframes
    sam[:,i], dims = calc_sam(name)

df_sam = pd.DataFrame(sam, index=dims['time'], columns=np.arange(1,31))
    
## Create a place to put the data
store = pd.HDFStore(
           '/raid/ra40/data/ncs/cmip5/sam/c5_zonmean_sam-jet_analysis.h5', 
           'a')
store['sam'] = df_sam
store.close()    