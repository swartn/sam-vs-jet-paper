""" Compute trends in the uas fields of the CMIP5 models and save them in a
np array within an HDF5 structure.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import cmipdata as cd
import os
import numpy as np
import scipy as sp
import h5py

os.chdir('/raid/ra40/data/ncs/tmp_proc/')

# If necessary do the remapping from the original files
#model_list = ['ACCESS1-0', 'ACCESS1-3', 'BNU-ESM', 'CMCC-CMS', 'CMCC-CM',
              #'CNRM-CM5', 'CSIRO-Mk3-6-0', 'CanESM2', 
              #'GISS-E2-H-CC', 'GISS-E2-H', 'GISS-E2-R-CC', 'GISS-E2-R',
              #'HadCM3', 'HadGEM2-AO', 'HadGEM2-CC', 'HadGEM2-ES', 
              #'IPSL-CM5A-LR', 'IPSL-CM5A-MR', 'IPSL-CM5B-LR', 'MIROC-ESM-CHEM',
              #'MIROC-ESM', 'MIROC5', 'MPI-ESM-LR','MPI-ESM-MR','MRI-CGCM3',
              #'NorESM1-ME', 'NorESM1-M', 'bcc-csm1-1-m', 'bcc-csm1-1','inmcm4'
              #]

#path ='/raid/ra40/data/ncs/cmip5/sam/c5_uas2/'
#filepattern = 'uas_Amon_*r1i1p1*'

#os.system('ln -s ' + path + filepattern + ' .')
#ens = cd.mkensemble(filepattern)

## keep only the models in the list above
#for model, experiment, realization, variable, files in ens.iterate():
    #if model.name not in model_list:
        #ens.del_model(model)

# remap
#ens_remap = cd.remap(ens, remap='r360x180',delete=True)
#------------------------------------------------------------------------------

# Else just continue from the already remapped files
ens_remap = cd.mkensemble('remap_uas*', prefix='remap_')

# Do trends over 1951 to 2011
# compute trends and load into np structure
ens1 = cd.trends(ens_remap, start_date='1951-01-01', 
                end_date='2011-12-31', delete=False)

# keep only the slope files
for model, experiment, realization, variable, files in ens1.iterate():
    for file in files:
        if 'intercept' in file:
            variable.del_filename(file)

# load the slope files into a np array

slopes = cd.loadfiles(ens1, 'uas')

# save np structure, with a list of models in HDF5
h5f = h5py.File('/raid/ra40/data/ncs/cmip5/sam/cmip5_trends.h5', 'a')
h5f.create_dataset('uas/1951_2011/c5_uas_trend_1951_2011', data=slopes)
model_names = [ model.name for model in ens_remap.models]
h5f.create_dataset('uas/1951_2011/model_names', data=model_names)
h5f.close()


##read it back in
#h5f = h5py.File('/raid/ra40/data/ncs/cmip5/sam/cmip5_trends.h5','r')
#slopes2 = h5f['uas/1951_2011/c5_uas_trend_1951_2011'][:]
#names2 = h5f['uas/1951_2011/model_names'][:]
#h5f.close()

# clean up
os.system('rm -f slope*')
os.system('rm -f intercept*')

    

