import cmipdata as cd
import h5py
import numpy as np
import scipy as sp
import pandas as pd
import pandas_tools as pt
from smooth import smooth
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import matplotlib as mpl
import brewer2mpl
plt.ion()
plt.close('all')
font = {'size'   : 12}
plt.rc('font', **font)

# Load the CMIP5 data
h5f = h5py.File('/raid/ra40/data/ncs/cmip5/sam/cmip5_trends.h5','r')
psl_slope_c5 = h5f['psl/1979_2004/c5_psl_trend_1979_2004'][:]*120
uas_slope_c5_88 = h5f['uas/1988_2011/c5_uas_trend_1988_2011'][:]*120
uflx_slope_c5_88 = h5f['tauu/1988_2011/c5_tauu_trend_1988_2011'][:]*120*100
h5f.close()

# load in the reanlaysis data
rean = ['R1', 'R2', '20CR', 'ERA-Int', 'CFSR', 'MERRA']
rlc = [ 'k' , 'y', 'g' , 'b' , 'c' , 'm' ] 
h5f = h5py.File('/raid/ra40/data/ncs/cmip5/sam/reanalysis_trends.h5','r')
psl_slope_rean = h5f['psl/1979_2004/rean_psl_trend_1979_2004'][:]*120
uas_slope_rean_88 = h5f['uas/1988_2011/rean_uas_trend_1988_2011'][:]*120
uflx_slope_rean_88 = h5f['uflx/1988_2011/rean_uflx_trend_1988_2011'][:]*120*100
h5f.close()

# The HadSLPr2 data is in the rean hdf
psl_slope_hadslp = psl_slope_rean[:,:,6]

# load in the CCMP data
ifile_ccmp = '/raid/ra40/data/ncs/ccmp/ccmp_slope_199801-201112.nc'
slope_ccmp = cd.loadvar(ifile_ccmp, 'uwnd')*120.
slope_ccmp = np.ma.masked_outside(slope_ccmp, -1,1)
uflx_slope_ccmp = cd.loadvar(ifile_ccmp, 'upstr')*120.
uflx_slope_ccmp = np.ma.masked_outside(uflx_slope_ccmp, -15,15)
uflx_slope_ccmp = uflx_slope_ccmp*1.2*1.4e-3*100

# load in the Marshall SAM data
df = pd.read_csv('/HOME/ncs/data/marshall_sam/marshall_sam.csv', 
		  index_col=0, parse_dates=True)

df = pt.time_lim(df, pd.datetime(1979,1,1), pd.datetime(2004,12,31))
dft = pt.ols(df, units='decades')

dims = {'lat' : np.arange(-89.5,89.6,1),
	'lon' : np.arange(0,360,1)
        }

fig, (axt, axm, axb) = plt.subplots(3,1, sharex=True, figsize=(7,7))
fig.subplots_adjust(right=0.5, hspace=0.05)

axt.plot(dims['lat'], psl_slope_c5.mean(axis=(0,2)), 'r-', linewidth=3
	 , label='CMIP5')
axt.plot(dims['lat'], psl_slope_hadslp.mean(axis=(1)), 'k--', linewidth=3
	 , label='HadSLP2r')

axt.plot(dims['lat'], slope_ccmp.mean(axis=1)*np.nan, 'k-.'
	 , linewidth=3, label='CCMP')

axm.plot(dims['lat'], uas_slope_c5_88.mean(axis=(0,2)), 'r-', linewidth=3)
axm.plot(dims['lat'], slope_ccmp.mean(axis=1), 'k-.', linewidth=3)

axb.plot(dims['lat'], uflx_slope_ccmp.mean(axis=1), 'k-.', linewidth=3)
axb.plot(dims['lat'], uflx_slope_c5_88.mean(axis=(0,2)), 'r-', linewidth=3)

for i,r in enumerate(rean):
    axt.plot(dims['lat'], psl_slope_rean[:,:,i].mean(axis=1), linestyle='-'
	     , color=rlc[i], linewidth=2, label=r)
    axm.plot(dims['lat'], uas_slope_rean_88[:,:,i].mean(axis=1), linestyle='-'
	     , color=rlc[i], linewidth=2) 
    axb.plot(dims['lat'], uflx_slope_rean_88[:,:,i].mean(axis=1), linestyle='-'
	     , color=rlc[i], linewidth=2)   
 
# put on the trends in marshall
axt.plot(-40, dft.slp40.slope*100.0, 'kx', markersize=15, markeredgewidth=2)
axt.plot(-65, dft.slp65.slope*100.0, 'kx', markersize=15, markeredgewidth=2
	 , label='Marshall')

axt.legend(bbox_to_anchor=(1.6,1), frameon=False, numpoints=1, fontsize=12)
axb.set_xlabel('Latitude')
ylabs = ['Pa decade$^{-1}$', 
	 'm s$^{-1}$ decade$^{-1}$',
	 r'Pa decade$^{-1}\times 10^{-2}$'
	]
for i, ax in enumerate((axt, axm, axb)):
    ax.set_xlim([-80, -20])
    ax.plot([-90, 0], [0, 0], 'k-')
    ax.set_ylabel(ylabs[i])

axt.set_ylim([-135, 85])
axm.set_ylim([-0.325, 0.325])
axb.set_ylim([-1.5, 1.7])
	
plt.savefig('psl_uas_zonmean_trend_comp_all_1979c1988-2011.pdf'
            , bbox_inches = 'tight', dpi=300)    
  
    