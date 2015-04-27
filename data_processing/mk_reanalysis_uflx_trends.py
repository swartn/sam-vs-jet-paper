""" Compute trends in the uflx fields of various reanalyses and save them in a
np array within an HDF5 structure.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import cmipdata as cd
import os
import numpy as np
import scipy as sp
import h5py
import cdo as cdo; cdo = cdo.Cdo() # recommended import
os.system('rm -f /tmp/cdo*')
os.chdir('/raid/ra40/data/ncs/tmp_proc/')


d1 = '1988-01-01'
d2 = '2011-12-31'

cdo_str = '-remapdis,r360x180 -seldate,' + d1 + ',' + d2 + ' -selvar,uflx '

path = '/raid/ra40/data/ncs/reanalyses/uflx/'
rean = ['R1', 'R2', '20CR', 'ERA-Int', 'CFSR', 'MERRA']

slopes = np.zeros((180,360,6))

for i, r in enumerate(rean):    
    ifile = path + r + '_uflx.omask.sfc.mon.mean.nc'
    cdo.trend(input=(cdo_str + ifile)
              , output="int.nc " + r + "_slope.nc")
    slopes[:,:,i] = cd.loadvar(r + '_slope.nc', 'uflx')    
    os.system('rm -f int.nc ' + r + '_slope.nc')
    os.system('rm -f int.nc ' + r + '_slope.nc')

# save np structure, with a list of models in HDF5
h5f = h5py.File('/raid/ra40/data/ncs/cmip5/sam/reanalysis_trends.h5', 'a')
h5f.create_dataset('uflx/1988_2011/rean_uflx_trend_1988_2011', data=slopes)
h5f.create_dataset('uflx/1988_2011/reanalysis_names', data=rean)
h5f.close()