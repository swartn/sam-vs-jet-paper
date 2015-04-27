""" Compute trends in the slp fields of various reanalyses and save them in a
np array within an HDF5 structure.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import cmipdata as cd
import os
import numpy as np
import scipy as sp
import h5py
import cdo as cdo; cdo = cdo.Cdo() # recommended import
import time
os.system('rm -f /tmp/cdo*')
now = time.strftime("%Y%m%d%H%M")
os.mkdir('/raid/ra40/data/ncs/tmp_proc/d' + now)
os.chdir('/raid/ra40/data/ncs/tmp_proc/d' + now)

d1 = '1979-01-01'
d2 = '2011-12-31'

cdo_str = '-remapdis,r360x180 -seldate,' + d1 + ',' + d2 + ' -selvar,slp '

path = '/raid/ra40/data/ncs/reanalyses/slp/'
#rean = ['R1', 'R2', '20CR', 'ERA-Int', 'CFSR', 'MERRA']
#rean = ['R1', 'R2', '20CR', 'ERA-Int', 'CFSR', 'MERRA', 'HadSLP2r']
rean = ['20CR', 'HadSLP2r']

slopes = np.zeros((180,360,7))

for i, r in enumerate(rean):    
    ifile = path + r + '_slp.mon.mean.nc'
    cdo.trend(input=(cdo_str + ifile)
              , output="int.nc " + r + "_slope.nc")
    slopes[:,:,i] = cd.loadvar(r + '_slope.nc', 'slp')    
    os.system('rm -f int.nc ' + r + '_slope.nc')
    
# save np structure, with a list of models in HDF5
h5f = h5py.File('/raid/ra40/data/ncs/cmip5/sam/reanalysis_trends.h5', 'a')
del h5f['psl/1979_2011/rean_psl_trend_1979_2011']
del h5f['psl/1979_2011/reanalysis_names']
h5f.create_dataset('psl/1979_2011/rean_psl_trend_1979_2011', data=slopes)
h5f.create_dataset('psl/1979_2011/reanalysis_names', data=rean)
h5f.close()
os.chdir('/home/ncs/sam_data_processing')
os.system('rm -rf /raid/ra40/data/ncs/tmp_proc/d' + now)
