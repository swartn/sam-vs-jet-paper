"""
Plots maps of SLP trends over 1951 to 2004 in HadSLP2r, 20CR and CMIP5.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import h5py
import cmipdata as cd
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
plt.rc('font', size=10)

datapath = '../data_retrieval/data/'

# Load in the CMIP5 data
h5f = h5py.File(datapath + 'cmip5_trends.h5','r')
psl_slope_c5 = h5f['psl/1951_2004/c5_psl_trend_1951_2004'][:]*120
names2 = h5f['psl/1951_2004/model_names'][:]
h5f.close()

# Load the data for 20CR
h5f = h5py.File(datapath + 'reanalysis_trends.h5','r')
slopes = h5f['slp/1951_2004/rean_slp_trend_1951_2004'][:]*120
rean = h5f['slp/1951_2004/reanalysis_names'][:]
h5f.close()

psl_slope_20cr = slopes[:,:,0]

# HadSLP data is now with reanlyses.
psl_slope_hadslp = slopes[:,:,1]

dims = {'lat' : np.arange(-89.5,89.6,1),
	'lon' : np.arange(0,360,1)
        }

#The locations of the Marshall Stations to plot over
# Marshall locations
marshlat = np.array([46.9, 37.8, 42.9, 43.5, 39.6, 40.4, 70.8, 67.6, 66.6, 66.3, 66.7, 
                 65.2])*-1
marshlon = np.array([37.9, 77.5, 147.3, 172.6, 360-73.1, 360-9.9, 11.8, 62.9, 93.0, 
                     110.5, 140.0, 360-64.3])

fig, axa = plt.subplots(3,2, sharex=True, figsize=(7,7))
fig.subplots_adjust(top=0.5, hspace=0.1, wspace=0.05)

vmin = -120
vmax = 120
ncols = 11
cmap_anom = brewer2mpl.get_map('RdBu', 'diverging', ncols,
                               reverse=True).mpl_colormap
cmap_anom = discrete_cmap(ncols, cmap_anom)

m =\
Basemap(llcrnrlon=0,llcrnrlat=-90,urcrnrlon=360,urcrnrlat=0,projection='mill'
	, fix_aspect=True)

lons, lats = np.meshgrid(dims['lon'], dims['lat'])
x, y = m(lons, lats)
xpt, ypt = m(20,-86)

cot = m.pcolor(x, y, psl_slope_hadslp,vmin=vmin, vmax=vmax, cmap=cmap_anom, 
               ax=axa[0,0], rasterized=True)
axa[0,0].text(xpt, ypt, 'HadSLP2r')
xm, ym = m(marshlon, marshlat)
m.plot(xm, ym, 'ok', zorder=5, ax=axa[0,0])

m.pcolor(x, y, psl_slope_20cr,vmin=vmin, vmax=vmax, cmap=cmap_anom, 
               ax=axa[1,0], rasterized=True )
anom = psl_slope_20cr - psl_slope_hadslp
m.pcolor(x, y, anom,vmin=vmin, vmax=vmax
	 , cmap=cmap_anom,ax=axa[1,1], rasterized=True)

rmse = np.sqrt( np.mean(anom[0:89,:]**2) )
axa[1,0].text(xpt, ypt, '20CR')
axa[1,1].text(xpt, ypt, str(np.round(rmse,2)))

m.pcolor(x, y, psl_slope_c5.mean(axis=0),vmin=vmin, vmax=vmax, cmap=cmap_anom
	 , ax=axa[2,0], rasterized=True)
anom = psl_slope_c5.mean(axis=0)- psl_slope_hadslp
m.pcolor(x, y, anom, vmin=vmin,  vmax=vmax, cmap=cmap_anom, ax=axa[2,1]
	 , rasterized=True, zorder=1)
rmse = np.sqrt( np.mean(anom[0:89,:]**2) )
axa[2,0].text(xpt, ypt, 'CMIP5 mean')
axa[2,1].text(xpt, ypt, str(np.round(rmse,2)))

c5_25_precentile = np.percentile(psl_slope_c5,2.5, axis=0)
c5_975_precentile = np.percentile(psl_slope_c5,97.5, axis=0)

ds = 4 # downsample for stippling
mask = ( (psl_slope_hadslp[::ds,::ds]>c5_975_precentile[::ds,::ds]) | 
                  (psl_slope_hadslp[::ds,::ds]<c5_25_precentile[::ds,::ds])
       )
x2 = x[::ds,::ds]
y2 = y[::ds,::ds]
m.plot(x2[mask], y2[mask], '.k', alpha=0.75, 
       markersize=0.2, ax=axa[2,1], zorder=2)

m.drawmeridians(np.arange(0,360,90),labels=[0,0,0,1], linewidth=0,yoffset=-0e6
                , ax=axa[2,1])
m.drawmeridians(np.arange(0,360,90),labels=[0,0,0,1], linewidth=0,yoffset=-0e6
                , ax=axa[2,0])

for i, ax in enumerate(axa.flatten()):    
    ax.autoscale(enable=True, axis='both', tight=True)
    m.drawcoastlines(linewidth=1.25, ax=ax)
    m.fillcontinents(color='0.8',ax=ax, zorder=3)
    for k, spine in ax.spines.items():
        spine.set_zorder(4)
    if i%2 ==0:
        m.drawparallels(np.arange(-80,81,20),labels=[1,0,0,0], linewidth=0, 
                        ax=ax)

box = axa[0,0].get_position()
tl = fig.add_axes([box.x0*1.1 + box.width * 1., box.y0, 0.02, box.height])
bounds = np.linspace(vmin, vmax, ncols)
plt.colorbar(cot, cax=tl, label='Pa decade$^{-1}$',spacing='proportional',
             boundaries=bounds)

fig.delaxes(axa[0,1])
axa[0,0].set_title('SLP trends 1951-2004')
plt.savefig('../plots/slp_trend_maps_1951-2004.pdf',
            bbox_inches='tight', dpi=300)