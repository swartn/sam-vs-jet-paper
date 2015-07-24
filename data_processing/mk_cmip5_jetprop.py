"""
Calculate the kinematic properties of the SH westerly jet for the CMIP5 ensemble 
and saves them in an HDF store containing PD DataFrames.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import os
import numpy as np
from netCDF4 import Dataset
import pandas as pd
import cmipdata as cd
from calc_shw_jet_properties import jetprop

def mk_cmip5_jetprop(datapath='./'):
    # List of models to get data for
    model_list = ['ACCESS1-0', 'ACCESS1-3', 'BNU-ESM', 'CMCC-CMS', 'CMCC-CM',
              'CNRM-CM5', 'CSIRO-Mk3-6-0', 'CanESM2', 
              'GISS-E2-H-CC', 'GISS-E2-H', 'GISS-E2-R-CC', 'GISS-E2-R',
              'HadCM3', 'HadGEM2-AO', 'HadGEM2-CC', 'HadGEM2-ES', 
              'IPSL-CM5A-LR', 'IPSL-CM5A-MR', 'IPSL-CM5B-LR', 'MIROC-ESM-CHEM',
              'MIROC-ESM', 'MIROC5', 'MPI-ESM-LR','MPI-ESM-MR','MRI-CGCM3',
              'NorESM1-ME', 'NorESM1-M', 'bcc-csm1-1-m', 'bcc-csm1-1','inmcm4'
              ]    
    
    tail = '_historical-rcp45_r1i1p1_188101-201212.nc'
    names = [ 'zonal-mean_remap_uas_Amon_' + m + tail for m in model_list ]
    
    # Initialize some arrays
    width = np.zeros((1584, 30))
    umax = np.zeros((1584, 30))
    uloc = np.zeros((1584, 30))
     
    for i, name in enumerate(names):
        # define and load the file dimensions and uas data
        ifile = os.path.join(datapath, name)
        print ifile
        dims = cd.get_dimensions(ifile, 'uas', toDatetime=True)
        nc = Dataset(ifile)
        uas = nc.variables['uas'][:].squeeze()
        lat = dims['lat']
        # compute jet props
        jetmax, latofmax, latn, lats, jetwidth = jetprop(uas, lat)
        umax[:,i] = jetmax
        uloc[:,i] = latofmax
        width[:,i] = jetwidth
    
    # Assign to pd DataFrames
    df_umax = pd.DataFrame(umax, index=dims['time'], columns=np.arange(1,31))
    df_uloc = pd.DataFrame(uloc, index=dims['time'], columns=np.arange(1,31))
    df_width = pd.DataFrame(width, index=dims['time'], columns=np.arange(1,31))

    # Store the DataFrame in HDF5
    out_file = os.path.join(datapath, 'zonmean_sam-jet_analysis_cmip5.h5')
    store = pd.HDFStore(out_file, 'a')
    store['width'] = df_width
    store['maxspd'] = df_umax
    store['locmax'] = df_uloc
    store.close()
 
if __name__ == '__main__':
    mk_cmip5_jetprop(datapath='../data_retrieval/data/')