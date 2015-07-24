"""
Computes the sam index for various reanalyses and saves them to DataFrames in HDF5.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""

import os
import numpy as np
from netCDF4 import Dataset,num2date,date2num
import pandas as pd
import cdo as cdo; cdo = cdo.Cdo() # recommended import
os.system( 'rm -rf /tmp/cdo*') # clean out tmp to make space for CDO processing.
import cmipdata as cd
from calc_sam import calc_sam

def mk_rean_sam_index(datapath='./'):
    # list in the pre-defined list of files to use. 
    rean = ['R1', 'R2', '20CR', 'ERA-Int', 'CFSR', 'MERRA', 'HadSLP2r']
    rean2 = ['R1', 'R2', '20CR', 'ERA', 'CFSR', 'MERRA', 'HadSLP2r']
    tail = '_slp.mon.mean.nc'
    names = [ 'zonal-mean_remap_' + r + tail for r in rean ]

    df_sam = pd.DataFrame()
 
    for i, name in enumerate(names):
        print name
        # load the data and make dataframes
        ifile = os.path.join(datapath, name)
        dims = cd.get_dimensions(ifile, 'slp', toDatetime=True)
        dims['time'] = [pd.datetime(d.year, d.month, 1) for d in dims['time']]
        sami = calc_sam(ifile, 'slp')
        samdf = pd.DataFrame(sami, index=dims['time']) 
        df_sam = pd.concat([df_sam, samdf], axis=1)
    
    df_sam.columns = rean2
    
    # Store the DataFrame in HDF5
    out_file = os.path.join(datapath, 'zonmean_sam-jet_analysis_reanalysis.h5')
    store = pd.HDFStore(out_file, 'a')
    store['zonmean_sam'] = df_sam
    store.close()    

if __name__ == '__main__':
    mk_rean_sam_index(datapath='../data_retrieval/data/')