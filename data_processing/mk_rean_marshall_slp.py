"""
 Subsample various reanalyses at the Marshall station locations and save 
output to pd DataFrames in HDF5.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""

import os
import numpy as np
from netCDF4 import Dataset,num2date,date2num
import pandas as pd
import cdo as cdo; cdo = cdo.Cdo() # recommended import
os.system( 'rm -rf /tmp/cdo*') # clean out tmp to make space for CDO processing.
import cmipdata as cd
import sam_jet_calcs as sjc

def mk_rean_sam_index(datapath='./'):
    # list in the pre-defined list of files to use. 
    rean = ['R1', 'R2', '20CR', 'ERA-Int', 'CFSR', 'MERRA', 'HadSLP2r']
    rean2 = ['R1', 'R2', '20CR', 'ERA', 'CFSR', 'MERRA', 'HadSLP2r']
    tail = '_slp.mon.mean.nc'
    names = [ 'zonal-mean_remap_' + r + tail for r in rean ]

    df_sam = pd.DataFrame()
    # initalize empty dataframes
    df40s = pd.DataFrame()
    df65s = pd.DataFrame()
    dfsam = pd.DataFrame()
 
    for i, name in enumerate(names):
        print name
        ifile = os.path.join(datapath, name)
        s40s, s65s = sjc.calc_marshall_sam(ifile, 'slp', 
                           start_date='1951-01-01', end_date='2011-12-31')
        
        df40s = pd.concat([df40s, s40s], axis=1)
        df65s = pd.concat([df65s, s65s], axis=1)
       
    # assign column names to the dataframes and calculate SAM
    df40s.columns = rean2
    df65s.columns = rean2
    dfsam = df40s - df65s
    dft = pd.concat([df40s, df65s, dfsam], keys=['p40s', 'p65s', 'sam'])

    # Store the DataFrame in HDF5
    out_file = os.path.join(datapath, 'zonmean_sam-jet_analysis_reanalysis.h5')    
    h5f = pd.HDFStore(out_file, 'a')
    h5f['marshall_sam/sam'] = dft
    h5f.close() 

if __name__ == '__main__':
    mk_rean_sam_index(datapath='../data_retrieval/data/')