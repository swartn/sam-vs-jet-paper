"""
Computes kinematic properties of the jet for the various reanalyses and saves them 
to DataFrames in HDF5.

In this case base on 10 m winds.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import os
import numpy as np
from netCDF4 import Dataset
import pandas as pd
import cmipdata as cd
from calc_shw_jet_properties import jetprop

def mk_rean_jetprop(datapath='./'):
    # list in the pre-defined list of files to use. 
    rean = ['R1', 'R2', '20CR', 'ERA-Int', 'CFSR', 'MERRA']
    rean2 = ['R1', 'R2', '20CR', 'ERA', 'CFSR', 'MERRA']
    tail = '_u10m.mon.mean.nc'
    names = [ 'zonal-mean_remap_' + r + tail for r in rean ]

    # Initialize some jetprop arrays
    df_umax = pd.DataFrame()
    df_uloc = pd.DataFrame()
    df_width = pd.DataFrame()

     # Loop over the reanalyses
    for i, name in enumerate(names):
        # define the input
        ifile = os.path.join(datapath, name)
        print ifile
         
        # Get the dimensions     
        dims = cd.get_dimensions(ifile, 'u10m', toDatetime=True)
        dims['time'] = [pd.datetime(d.year, d.month, 1) for d in dims['time']]
    
        # load the data
        nc = Dataset(ifile)
        u10m = nc.variables['u10m'][:].squeeze()
        lat = dims['lat']
        
        # Compute the properties
        jetmax, latofmax, latn, lats, jetwidth = jetprop(u10m, lat)
        # Assign to pd DataFrames
        df = pd.DataFrame(jetmax, index=dims['time'])
        df_umax = pd.concat([df_umax, df], axis=1)
        df = pd.DataFrame(latofmax, index=dims['time'])
        df_uloc = pd.concat([df_uloc, df], axis=1)
        df = pd.DataFrame(jetwidth, index=dims['time'])
        df_width = pd.concat([df_width, df], axis=1)
        
        # Test plots to make sure props were calculated right
        #ri = 49
        #plt.close()
        #plt.plot( lat, uwnd[ri,:], 'k-o', linewidth=2)
        #plt.plot( lat, lat*0, 'k--')
        #plt.plot( latofmax[ri], jetmax[ri], 'rx', markersize=8, markeredgewidth=1)
        #plt.plot(  [-90, 90], [ jetmax[ri],jetmax[ri]  ], 'r--')
        #plt.plot(  [-90, 90], [ jetmax[ri]*0.5, jetmax[ri]*0.5], 'r--')
        
        ##print latn[ri], lats[ri]
        #plt.plot( [latn[ri], latn[ri]], [-10, 10], 'r--')
        #plt.plot( [lats[ri], lats[ri]], [-10, 10], 'r--')
        #raw_input('go?')
    
    df_umax.columns = rean2
    df_uloc.columns = rean2
    df_width.columns = rean2

    # Store the DataFrame in HDF5
    out_file = os.path.join(datapath, 'zonmean_sam-jet_analysis_reanalysis.h5')  
    store = pd.HDFStore(out_file, 'a')
    store['width'] = df_width
    store['maxspd'] = df_umax
    store['locmax'] = df_uloc
    store.close()
    
if __name__ == '__main__':
    mk_rean_jetprop(datapath='../data_retrieval/data/')