"""
Plots maps of trends in u10m over 1988-2011 in CCMP, various reanalyes and CMIP5.

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

datapath = '../data_retrieval/data/'

# Load the CMIP5 data
h5f = h5py.File(datapath + 'cmip5_trends.h5','r')
uas_slope_c5 = h5f['uas/1988_2011/c5_uas_trend_1988_2011'][:]*120
#names2 = h5f['uas/1988_2011/model_names'][:]
h5f.close()

# load in the reanalysis data
h5f = h5py.File(datapath + 'reanalysis_trends.h5','r')
slopes = h5f['u10m/1988_2011/rean_u10m_trend_1988_2011'][:]*120
rean = h5f['u10m/1988_2011/reanalysis_names'][:]
h5f.close()

# load in the CCMP data
ifile_ccmp = datapath + 'slope_remap_CCMP_198701-201112.nc' #despite name, starts 88
slope_ccmp = cd.loadvar(ifile_ccmp, 'uwnd')
slope_ccmp = slope_ccmp*120.
slope_ccmp = np.ma.masked_outside(slope_ccmp, -1,1)

dims = {'lat' : np.arange(-89.5,90.1,1),
	'lon' : np.arange(0,361,1)
        }

fig, axa = plt.subplots(8,2, sharex=True, sharey=True, figsize=(7,7), 
                        squeeze=True)
fig.subplots_adjust(right=0.63, hspace=0.1, wspace=0.05)

vmin = -1
vmax = 1
ncols = 11
cmap_anom = brewer2mpl.get_map('RdBu', 'diverging', ncols,
                               reverse=True).mpl_colormap
cmap_anom = discrete_cmap(ncols, cmap_anom)

m =\
Basemap(llcrnrlon=0,llcrnrlat=-90,urcrnrlon=360,urcrnrlat=0,projection='mill')

lons, lats = np.meshgrid(dims['lon'], dims['lat'])
x, y = m(lons, lats)
xpt, ypt = m(20,-88.5)

cot = m.pcolor(x, y, slope_ccmp,vmin=vmin, vmax=vmax, cmap=cmap_anom, 
               ax=axa[0,0], rasterized=True)
axa[0,0].text(xpt, ypt, 'CCMP')

# put on reanalyses    
for i, r in enumerate(rean):
    m.pcolor(x, y, slopes[:,:,i],vmin=vmin, vmax=vmax, cmap=cmap_anom, 
             ax=axa[i+1, 0], rasterized=True)
    anom = slopes[:,:,i] - slope_ccmp
    anom = np.ma.masked_outside(anom,-1.0, 1.0)
    m.pcolor(x, y, anom,vmin=vmin, vmax=vmax, 
             cmap=cmap_anom, ax=axa[i+1, 1], rasterized=True) 
    rmse = np.sqrt( np.mean(anom[0:89,:]**2) )
    axa[i+1,0].text(xpt, ypt, r.upper())
    axa[i+1,1].text(xpt, ypt, str(np.round(rmse,2)))
 
# put on cmip5    
m.pcolor(x, y, uas_slope_c5.mean(axis=0),vmin=vmin, vmax=vmax, cmap=cmap_anom, 
         ax=axa[7, 0], rasterized=True)
anom =  uas_slope_c5.mean(axis=0) - slope_ccmp
anom = np.ma.masked_outside(anom,-1.0, 1.0)
m.pcolor(x, y, anom,vmin=vmin, vmax=vmax, 
         cmap=cmap_anom, ax=axa[7, 1], rasterized=True)
rmse = np.sqrt( np.mean(anom[0:89,:]**2) )

c5_25_precentile = np.percentile(uas_slope_c5,2.5, axis=0)
c5_975_precentile = np.percentile(uas_slope_c5,97.5, axis=0)
ds = 4 # downsample for stippling
mask = ( (slope_ccmp[::ds,::ds]>c5_975_precentile[::ds,::ds]) | 
                  (slope_ccmp[::ds,::ds]<c5_25_precentile[::ds,::ds]))

x2 = x[::ds,::ds]
y2 = y[::ds,::ds]
m.plot(x2[mask], y2[mask], '.k', alpha=0.75, 
       markersize=0.2, ax=axa[7,1], zorder=1)

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
plt.colorbar(cot, cax=tl, label='m s$^{-1}$\ndecade$^{-1}$',
             spacing='proportional', boundaries=bounds)

fig.delaxes(axa[0,1])
axa[0,0].set_title('u10m trends 1988-2011')
plt.savefig('../plots/uas_trend_maps_1988-2011.pdf',
            bbox_inches='tight', dpi=300)