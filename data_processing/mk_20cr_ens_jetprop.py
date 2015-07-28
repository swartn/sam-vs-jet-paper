"""
Computes kinematic properties of the jet for the 20CR ensemble and saves them to 
DataFrames in HDF5.

In this case base on 10 m winds.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import numpy as np
import os
from netCDF4 import Dataset
import pandas as pd
import cmipdata as cd
from sam_jet_calcs import jetprop

def mk_20cr_ens_jetprop(datapath='../data_retrieval/data/'):
    """Calculated the kinematic properties of the jet for the 20CR ensemble
    """
    #The pre-computed zonal mean u10m file
    zmfn = os.path.join(datapath, 'zonal-mean_remap_20CR_ens_u10m.mon.mean.nc')

    # load the data and make dataframes
    dims = cd.get_dimensions(zmfn, 'u10m', toDatetime=True)
    nc = Dataset(zmfn)
    u_20cr = nc.variables['u10m'][:].squeeze()
    lat = dims['lat']

    # initialize some empty arrays for the jet props.
    width = np.zeros((len(dims['time']), 56))
    umax = np.zeros((len(dims['time']), 56))
    uloc = np.zeros((len(dims['time']), 56))
 
    # Calculate properties for each ensemble member
    for i in np.arange(56):
        uas = np.squeeze(u_20cr[:,i,:])
        jetmax, latofmax, latn, lats, jetwidth = jetprop(uas, lat)
        umax[:,i] = jetmax
        uloc[:,i] = latofmax
        width[:,i] = jetwidth

        # make a plot at a random time index ri, to see that the defs are working.
        #ri = 10
        #plt.close()
        #plt.plot( lat, uas[ri,:], 'k-o', linewidth=2)
        #plt.plot( lat, lat*0, 'k--')
        #plt.plot( latofmax[ri], jetmax[ri], 'rx', markersize=8, markeredgewidth=1)
        #plt.plot(  [-90, 90], [ jetmax[ri],jetmax[ri]  ], 'r--')
        #plt.plot(  [-90, 90], [ jetmax[ri]*0.5, jetmax[ri]*0.5], 'r--')
    
        #print latn[ri], lats[ri]
        #plt.plot( [latn[ri], latn[ri]], [-10, 10], 'r--')
        #plt.plot( [lats[ri], lats[ri]], [-10, 10], 'r--')
        #raw_input('go?')

    # Create Pandas DataFrames from the arrays
    df_umax = pd.DataFrame(umax, index=dims['time'], columns=np.arange(1,57))
    df_uloc = pd.DataFrame(uloc, index=dims['time'], columns=np.arange(1,57))
    df_width = pd.DataFrame(width, index=dims['time'], columns=np.arange(1,57))
    
    # Store the DataFrame in HDF5
    out_file = os.path.join(datapath, 'zonmean_sam-jet_analysis_20CR_ensemble.h5')
    store = pd.HDFStore(out_file, 'a')
    store['width'] = df_width
    store['maxspd'] = df_umax
    store['locmax'] = df_uloc
    store.close()      

if __name__ == '__main__':
    mk_20cr_ens_jetprop(datapath='../data_retrieval/data/')
    