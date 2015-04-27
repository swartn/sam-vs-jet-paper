""" Subsample the CMIP5 models at Marshall station locations and save output to pd 
DataFrames in HDF5.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import cmipdata as cd
import os
import numpy as np
import scipy as sp
import pandas as pd
import h5py
from netCDF4 import Dataset
import cdo as cdo; cdo = cdo.Cdo() # recommended import
os.system('rm -f /tmp/cdo*')
os.chdir('/raid/ra40/data/ncs/tmp_proc/')

model_list = ['ACCESS1-0', 'ACCESS1-3', 'BNU-ESM', 'CMCC-CMS', 'CMCC-CM',
              'CNRM-CM5', 'CSIRO-Mk3-6-0', 'CanESM2', 
              'GISS-E2-H-CC', 'GISS-E2-H', 'GISS-E2-R-CC', 'GISS-E2-R',
              'HadCM3', 'HadGEM2-AO', 'HadGEM2-CC', 'HadGEM2-ES', 
              'IPSL-CM5A-LR', 'IPSL-CM5A-MR', 'IPSL-CM5B-LR', 'MIROC-ESM-CHEM',
              'MIROC-ESM', 'MIROC5', 'MPI-ESM-LR','MPI-ESM-MR','MRI-CGCM3',
              'NorESM1-ME', 'NorESM1-M', 'bcc-csm1-1-m', 'bcc-csm1-1','inmcm4'
              ]

path ='/ra40/data/ncs/cmip5/psl/'
filepattern = 'remap_psl_Amon_*r1i1p1*'

os.system('ln -s ' + path + filepattern + ' .')
ens = cd.mkensemble(filepattern, prefix='remap_')

# keep only the models in the list above
for model, experiment, realization, variable, files in ens.iterate():
    if model.name not in model_list:
        ens.del_model(model)

print ens.sinfo()
# remap
#ens_remap = cd.remap(ens, remap='r360x180',delete=True)
model_names = [m.name for m in ens.models] 

for n in model_list:
    if n not in model_names:
	print "not all 30 required models are present" 

# Marshall locations
mlat40s = np.array([46.9, 37.8, 42.9, 43.5, 39.6, 40.4])*-1
mlon40s = np.array([37.9, 77.5, 147.3, 172.6, -73.1, -9.9])

mlat65s = np.array([70.8, 67.6, 66.6, 66.3, 66.7, 65.2])*-1
mlon65s = np.array([11.8, 62.9, 93.0, 110.5, 140.0, -64.3])

# initalize empty dataframes
df40s = pd.DataFrame()
df65s = pd.DataFrame()
dfsam = pd.DataFrame()

def scale(ncvar, var):
    # Apply any scaling and offsetting needed:
    try:
        var_offset = ncvar.add_offset
    except:
        var_offset = 0
    try:
        var_scale = ncvar.scale_factor
    except:
        var_scale = 1   

    var = var*var_scale + var_offset
    #return var
    return np.squeeze( var ) 

for model, experiment, realization, variable, files in ens.iterate():    
    # Get the dimensions and initialize arrays
    p40 = np.zeros((732, 6))
    p65 = np.zeros((732, 6))   
    dates = pd.date_range('1951-01-01', '2011-12-31'  , freq='MS')
    #ncvar = Dataset(files[0]).variables['psl']

    for k in range(6):
	# loop over the six stations at each lat and get data at each one.
	var = cdo.remapnn('lon=' + str( mlon40s[k] ) + '/lat='\
	               + str( mlat40s[k] )
		       , input=('-selvar,psl -seldate,1951-01-01,2011-12-31 ' 
		       + files[0]), returnMaArray='psl').squeeze()
	p40[:,k] = var.squeeze() #scale(ncvar, var)
	
	var2 = cdo.remapnn('lon=' + str( mlon65s[k] ) + '/lat='\
	               + str( mlat65s[k] )
		       , input=('-selvar,psl -seldate,1951-01-01,2011-12-31 ' 
		       + files[0]), returnMaArray='psl').squeeze()
	p65[:,k] = var2.squeeze() #scale(ncvar, var2)

    # Now create the mean pressure at 40S and 65S and add to dataframe
    s40s = pd.Series(p40.mean(axis=1), index=dates)
    s65s = pd.Series(p65.mean(axis=1), index=dates)
    df40s = pd.concat([df40s, s40s], axis=1)
    df65s = pd.concat([df65s, s65s], axis=1)
   
# assign column names to the dataframes and calculate SAM
df40s.columns = model_names
df65s.columns = model_names
dfsam = df40s - df65s
dft = pd.concat([df40s, df65s, dfsam], keys=['p40s', 'p65s', 'sam'])
#dft.to_csv('/raid/ra40/data/ncs/cmip5/sam/rean_marshall_sam')
h5f = pd.HDFStore('/raid/ra40/data/ncs/cmip5/sam/c5_sam.h5', 'a')
h5f['sam/df'] = dft
h5f.close() 

  
    