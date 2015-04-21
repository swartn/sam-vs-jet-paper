import os
import numpy as np
from netCDF4 import Dataset,num2date,date2num
os.system( 'rm -rf /tmp/cdo*') # clean out tmp to make space for CDO processing.
import pandas as pd
import cmipdata as cd
import cdo as cdo; cdo = cdo.Cdo() # recommended import
import matplotlib.pyplot as plt
plt.ion()

# The data location
pp = '/raid/ra40/data/ncs/reanalyses/20CR/u_sig995/monthly/'
#os.chdir(pp)

# The 20CR file with ensemble members stacked in the k-dimension
fn = pp + 'u9950_1871-2012.mon.mean.nc'
zmfn = pp + 'zonmean_' + 'u9950_1871-2012.mon.mean.nc'

# Use cdo to get the p at 40S, 65S and compute the SAM.
# First make a zonal mean
#cdo.zonmean(input=fn, output=zmfn)

# load the data and make dataframes
dims = cd.get_dimensions(zmfn, 'u9950', toDatetime=True)
nc = Dataset(zmfn)
u_20cr = nc.variables['u9950'][:].squeeze()
lat = dims['lat']

def jetprop(uas, lat):
    region = (lat>-70) & (lat<-20)
    rlat = lat[region]
    ruas = uas[: ,region]
    jetmax = ruas.max(axis=1)

    jetmax2 = np.zeros( len(jetmax) )
    latofmax = np.zeros( len(jetmax) )
    jetwidth = np.zeros( len(jetmax) )
    latn = np.zeros( len(jetmax) ) ; lats = np.zeros( len(jetmax) )
    yy = np.linspace(-70,-20,201)

    for t in range(len(jetmax)):
        u2 = np.interp(yy, rlat,ruas[t, :]) 
        jetmax2[t] = u2.max()
        indofmax = u2 == jetmax2[t]
        lom = yy[ indofmax ]
        latofmax[t] = lom[0] if lom.shape !=() else lom

        lat_of_gt_halfmax = yy[u2 >= 0.]
        latn[t] = lat_of_gt_halfmax.max()
        lats[t] = lat_of_gt_halfmax.min()
        jetwidth = latn - lats
        plt.plot(rlat, ruas[t, :])
        #plt.plot(yy, u2, 'r--')
        #raw_input('go?')
    return  jetmax2, latofmax, latn, lats, jetwidth    

ri = 10
width = np.zeros((len(dims['time']), 56))
umax = np.zeros((len(dims['time']), 56))
uloc = np.zeros((len(dims['time']), 56))
 
for i in np.arange(56):
    uas = np.squeeze(u_20cr[:,i,:])
    jetmax, latofmax, latn, lats, jetwidth = jetprop(uas, lat)
    umax[:,i] = jetmax
    uloc[:,i] = latofmax
    width[:,i] = jetwidth
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

df_umax = pd.DataFrame(umax, index=dims['time'], columns=np.arange(1,57))
df_uloc = pd.DataFrame(uloc, index=dims['time'], columns=np.arange(1,57))
df_width = pd.DataFrame(width, index=dims['time'], columns=np.arange(1,57))
    
## Create a place to put the data
store = pd.HDFStore(
           '/raid/ra40/data/ncs/reanalyses/20CR/20cr_ensemble_sam_analysis.h5', 
           'a')
store['width'] = df_width
store['maxspd'] = df_umax
store['locmax'] = df_uloc
store.close()      