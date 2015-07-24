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

def save_reanalysis_trends(var, rean, start_date, end_date, datapath):
    """Compute reanalysis trends and save to HDF5
    """
    lr = len(rean)
    slopes = np.zeros((180, 360, lr))
    cdo_str = '-seldate,' + start_date + ',' + end_date + ' -selvar,' + var + ' '
    tail =  '_' + var + '.mon.mean.nc'

     # Loop over the reanalyses
    for i, r in enumerate(rean):    
        ifile = os.path.join(datapath, 'remap_' + r + tail)
        cdo.trend(input=(cdo_str + ifile)
                  , output="int.nc " + r + "_slope.nc")
        slopes[:,:,i] = cd.loadvar(r + '_slope.nc', var)    
        os.system('rm -f int.nc ' + r + '_slope.nc')
        os.system('rm -f int.nc ' + r + '_slope.nc')

    # Store the DataFrame in HDF5
    out_file = os.path.join(datapath, 'reanalysis_trends.h5')
    h5f = h5py.File(out_file, 'a')
    sy = start_date.split('-')[0]
    ey = end_date.split('-')[0]
    ds_path = os.path.join(var, sy + '_' + ey)
    ds_name = os.path.join(ds_path, 'c5_' + var + '_trend_' + sy + '_' + ey)    
    h5f.create_dataset(ds_name, data=slopes)
    h5f.create_dataset(ds_path + 'reanalysis_names', data=rean)
    #h5f[ds_name].dims.create_scale(h5f[ds_path + 'model_names'], 'model_names')
    #f[ds_name].dims[2].attach_scale(h5f[ds_path + 'model_names'])
    h5f.close()

def mk_rean_trends(datapath='./'):
    """Compute reanalysis trends in slp, u10m and uflx over various periods.
    """
    # remove old trends if they exist
    ot = datapath + 'reanalysis_trends.h5'
    if os.path.isfile(ot):
        os.remove(ot)
    # do slp
    rean = ['R1', 'R2', '20CR', 'ERA-Int', 'CFSR', 'MERRA', 'HadSLP2r']
    save_reanalysis_trends('slp', rean=rean, start_date='1979-01-01',
                           end_date='2004-12-31', datapath=datapath)

    save_reanalysis_trends('slp', rean=['20CR', 'HadSLP2r'], 
                           start_date='1951-01-01', end_date='2004-12-31', 
                           datapath=datapath)


    # do u10m
    save_reanalysis_trends('u10m', rean=['20CR'], start_date='1951-01-01',
                           end_date='2011-12-31', datapath=datapath)

    rean = ['R1', 'R2', '20CR', 'ERA-Int', 'CFSR', 'MERRA']
    save_reanalysis_trends('u10m', rean=rean, start_date='1988-01-01',
                           end_date='2011-12-31', datapath=datapath)
    
    # do uflx
    save_reanalysis_trends('uflx', rean=rean, start_date='1988-01-01',
                           end_date='2011-12-31', datapath=datapath)
    
if __name__ == '__main__':
    mk_rean_trends(datapath='../data_retrieval/data/')
