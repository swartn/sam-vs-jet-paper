"""
Computes the same index for the CMIP5 ensemble and saves them to DataFrames in HDF5.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import os
import numpy as np
import pandas as pd
import cmipdata as cd
from sam_jet_calcs import calc_sam

def mk_cmip5_sam_index(datapath='./'):
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
    names = [ 'zonal-mean_remap_psl_Amon_' + m + tail for m in model_list ]
    cnames = [ n.replace('-', '_') for n in model_list ]
    
    sam = np.zeros((1584, 30))
     
    for i, name in enumerate(names):
        ifile = os.path.join(datapath, name)
        # load the data and make dataframes
        sam[:,i] = calc_sam(ifile, 'psl', start_date='1881-01-01',
                            end_date='2013-12-31')

    # Get the time axis
    dims = cd.get_dimensions(ifile, 'psl', toDatetime=True)
    t = dims['time']
    a = ( t <= pd.datetime(2013,12,31) ) & ( t >= pd.datetime(1881,1,1) )
    dims['time'] = t[a]
    
    df_sam = pd.DataFrame(sam, index=dims['time'], columns=cnames)
        
    # Store the DataFrame in HDF5
    out_file = os.path.join(datapath, 'zonmean_sam-jet_analysis_cmip5.h5')
    store = pd.HDFStore(out_file, 'a')
    store['sam'] = df_sam
    store.close()
    
if __name__ == '__main__':
    mk_cmip5_sam_index(datapath='../data_retrieval/data/')