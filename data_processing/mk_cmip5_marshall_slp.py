"""
 Subsample various CMIP5 models at the Marshall station locations and save 
output to pd DataFrames in HDF5.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import os
import numpy as np
import pandas as pd
import cmipdata as cd
import sam_jet_calcs as sjc

def mk_cmip5_marshall_slp(datapath='./'):
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
    names = [ 'remap_psl_Amon_' + m + tail for m in model_list ]
    cnames = [ n.replace('-', '_') for n in model_list ]
    
    # initalize empty dataframes
    df40s = pd.DataFrame()
    df65s = pd.DataFrame()
    dfsam = pd.DataFrame()
     
    for i, name in enumerate(names):
        ifile = os.path.join(datapath, name)
        # load the data and make dataframes
        s40s, s65s = sjc.calc_marshall_sam(ifile, 'psl', 
                           start_date='1951-01-01', end_date='2011-12-31')
        
        df40s = pd.concat([df40s, s40s], axis=1)
        df65s = pd.concat([df65s, s65s], axis=1)
       
    # assign column names to the dataframes and calculate SAM
    df40s.columns = cnames
    df65s.columns = cnames
    dfsam = df40s - df65s
    dft = pd.concat([df40s, df65s, dfsam], keys=['p40s', 'p65s', 'sam'])

    # Store the DataFrame in HDF5
    out_file = os.path.join(datapath, 'zonmean_sam-jet_analysis_cmip5.h5')
    h5f = pd.HDFStore(out_file, 'a')
    h5f['marshall_sam/sam'] = dft
    h5f.close() 
           
if __name__ == '__main__':
    mk_cmip5_marshall_slp(datapath='../data_retrieval/data/')