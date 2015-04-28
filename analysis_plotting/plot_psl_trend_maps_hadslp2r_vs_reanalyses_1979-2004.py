"""
Plots maps of SLP trends over 1979 to 2004 in HadSLP2r, various reanalyses and 
CMIP5.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import cdo as cdo; cdo = cdo.Cdo() # recommended import
import cmipdata as cd
import h5py
import os
os.system('rm -f /tmp/cdo*')
import numpy as np
import scipy as sp
from mpl_toolkits.basemap import Basemap, addcyclic
import matplotlib.pyplot as plt
import matplotlib as mpl
import brewer2mpl
from discrete_cmap import discrete_cmap
from netCDF4 import Dataset,num2date,date2num
plt.ion()
plt.close('all')
font = {'size'   : 10}
plt.rc('font', **font)


# Load the CMIP5 data
h5f = h5py.File('/raid/ra40/data/ncs/cmip5/sam/cmip5_trends.h5','r')
psl_slope_c5 = h5f['psl/1979_2004/c5_psl_trend_1979_2004'][:]*120
h5f.close()

# load in the reanlaysis data
rean = ['R1', 'R2', '20CR', 'ERA-Int', 'CFSR', 'MERRA']
rlc = [ 'k' , 'y', 'g' , 'b' , 'c' , 'm' ] 
h5f = h5py.File('/raid/ra40/data/ncs/cmip5/sam/reanalysis_trends.h5','r')
slopes = h5f['psl/1979_2004/rean_psl_trend_1979_2004'][:]*120
h5f.close()

# HadSLP data is now with reanlyses.
psl_slope_hadslp = slopes[:,:,6]

dims = {'lat' : np.arange(-89.5,89.6,1),
	'lon' : np.arange(0,360,1)
        }

fig, axa = plt.subplots(8,2, sharex=True, sharey=True, figsize=(7,7), 
                        squeeze=True)
fig.subplots_adjust(right=0.63, hspace=0.1, wspace=0.05)

vmin = -180
vmax = 180
ncols = 11
cmap_anom = brewer2mpl.get_map('RdBu', 'diverging', ncols,
                               reverse=True).mpl_colormap
cmap_anom = discrete_cmap(ncols, cmap_anom)

m =\
Basemap(llcrnrlon=0,llcrnrlat=-90,urcrnrlon=360,urcrnrlat=0,projection='mill')

lons, lats = np.meshgrid(dims['lon'], dims['lat'])
x, y = m(lons, lats)
xpt, ypt = m(20,-88)

cot = m.pcolor(x, y, psl_slope_hadslp,vmin=vmin, vmax=vmax, cmap=cmap_anom, 
               ax=axa[0,0], rasterized=True)
axa[0,0].text(xpt, ypt, 'HadSLP2r')

# put on reanalyses    
for i, r in enumerate(rean):
    m.pcolor(x, y, slopes[:,:,i],vmin=vmin, vmax=vmax, cmap=cmap_anom, 
             ax=axa[i+1, 0], rasterized=True)
    anom = slopes[:,:,i] - psl_slope_hadslp
    #anom = np.ma.masked_outside(anom,-1.0, 1.0)
    m.pcolor(x, y, anom,vmin=vmin, vmax=vmax, 
             cmap=cmap_anom, ax=axa[i+1, 1], rasterized=True) 
    rmse = np.sqrt( np.mean(anom[0:89,:]**2) )
    axa[i+1,0].text(xpt, ypt, r.upper())
    axa[i+1,1].text(xpt, ypt, str(np.round(rmse,2)))
    
# put on cmip5    
m.pcolor(x, y, psl_slope_c5.mean(axis=0),vmin=vmin, vmax=vmax, cmap=cmap_anom, 
         ax=axa[7, 0], rasterized=True)
anom =  psl_slope_c5.mean(axis=0) - psl_slope_hadslp
#anom = np.ma.masked_outside(anom,-1.0, 1.0)
m.pcolor(x, y, anom,vmin=vmin, vmax=vmax, 
         cmap=cmap_anom, ax=axa[7, 1], rasterized=True)
c5_25_precentile = np.percentile(psl_slope_c5,2.5, axis=0)
c5_975_precentile = np.percentile(psl_slope_c5,97.5, axis=0)
ds = 4 # downsample for stippling
mask = ( (psl_slope_hadslp[::ds,::ds]>c5_975_precentile[::ds,::ds]) | 
                  (psl_slope_hadslp[::ds,::ds]<c5_25_precentile[::ds,::ds])
       )
x2 = x[::ds,::ds]
y2 = y[::ds,::ds]
m.plot(x2[mask], y2[mask], '.k', alpha=0.75, 
       markersize=0.2, ax=axa[7,1], zorder=1)

rmse = np.sqrt( np.mean(anom[0:89,:]**2) )
axa[7,0].text(xpt, ypt, 'CMIP5 mean')
axa[7,1].text(xpt, ypt, str(np.round(rmse,2)))

for i, ax in enumerate(axa.flatten()):    
    ax.autoscale(enable=True, axis='both', tight=True)
    m.drawcoastlines(linewidth=1.25, ax=ax)
    m.fillcontinents(color='0.8',ax=ax, zorder=2)
    if i%2 ==0:
        m.drawparallels(np.arange(-80,81,20),labels=[1,0,0,0], linewidth=0, 
                        ax=ax)
	
m.drawmeridians(np.arange(0,360,90),labels=[0,0,0,1], 
                linewidth=0,yoffset=0.5e6, ax=axa[7,0])
m.drawmeridians(np.arange(0,360,90),labels=[0,0,0,1], 
                linewidth=0,yoffset=0.5e6, ax=axa[7,1])

box = axa[0,0].get_position()
tl = fig.add_axes([box.x0*1.1 + box.width * 1., box.y0, 0.02, box.height])
bounds = np.linspace(vmin, vmax, ncols)
plt.colorbar(cot, cax=tl, label='Pa\n decade$^{-1}$',
             spacing='proportional', boundaries=bounds)

fig.delaxes(axa[0,1])
axa[0,0].set_title('SLP trends 1979-2004')
plt.savefig('../plots/psl_trend_maps_hadlsp2r_vs_rean_c5_1979-2004.pdf'
            , bbox_inches='tight', dpi=300)
