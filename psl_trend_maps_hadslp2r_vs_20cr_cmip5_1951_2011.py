# look at various sources of uncertainty
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
pth = '/raid/ra40/data/ncs/cmip5/psl/'
plt.rc('font', size=10)

h5f = h5py.File('/raid/ra40/data/ncs/cmip5/sam/cmip5_trends.h5','r')
psl_slope_c5 = h5f['psl/1951_2011/c5_psl_trend_1951_2011'][:]*120
names2 = h5f['psl/1951_2011/model_names'][:]
h5f.close()

# Load the data for 20CR
h5f = h5py.File('/raid/ra40/data/ncs/cmip5/sam/reanalysis_trends.h5','r')
slopes = h5f['psl/1951_2011/rean_psl_trend_1951_2011'][:]*120
rean = h5f['psl/1951_2011/reanalysis_names'][:]
h5f.close()

psl_slope_20cr = slopes[:,:,0]

# HadSLP data is now with reanlyses.
psl_slope_hadslp = slopes[:,:,1]

dims = {'lat' : np.arange(-89.5,89.6,1),
	'lon' : np.arange(0,360,1)
        }

fig, axa = plt.subplots(3,2, sharex=True, figsize=(7,7))
fig.subplots_adjust(top=0.5, hspace=0.1, wspace=0.05)

vmin = -90
vmax = 90
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

m.pcolor(x, y, psl_slope_20cr,vmin=vmin, vmax=vmax, cmap=cmap_anom, 
               ax=axa[1,0], rasterized=True)
anom = psl_slope_20cr - psl_slope_hadslp
m.pcolor(x, y, anom,vmin=vmin, vmax=vmax
	 , cmap=cmap_anom, ax=axa[1,1], rasterized=True)

rmse = np.sqrt( np.mean(anom[0:89,:]**2) )
axa[1,0].text(xpt, ypt, '20CR')
axa[1,1].text(xpt, ypt, str(np.round(rmse,2)))

m.pcolor(x, y, psl_slope_c5.mean(axis=0),vmin=vmin, vmax=vmax, cmap=cmap_anom
	 , ax=axa[2,0], rasterized=True)
anom = psl_slope_c5.mean(axis=0)- psl_slope_hadslp
m.pcolor(x, y, anom, vmin=vmin,  vmax=vmax, cmap=cmap_anom, ax=axa[2,1]
	 , rasterized=True)
rmse = np.sqrt( np.mean(anom[0:89,:]**2) )
axa[2,0].text(xpt, ypt, 'CMIP5 mean')
axa[2,1].text(xpt, ypt, str(np.round(rmse,2)))

c5_25_precentile = np.percentile(psl_slope_c5,2.5, axis=0)
c5_975_precentile = np.percentile(psl_slope_c5,97.5, axis=0)
mask = ( (psl_slope_hadslp>c5_975_precentile) | 
                  (psl_slope_hadslp<c5_25_precentile)
       )
m.plot(x[mask][::2], y[mask][::2], '.k', alpha=0.2, 
       markersize=0.1, ax=axa[2,1], zorder=1)

m.drawmeridians(np.arange(0,360,90),labels=[0,0,0,1], linewidth=0,yoffset=-0e6
                , ax=axa[2,1])
m.drawmeridians(np.arange(0,360,90),labels=[0,0,0,1], linewidth=0,yoffset=-0e6
                , ax=axa[2,0])

for i, ax in enumerate(axa.flatten()):    
    ax.autoscale(enable=True, axis='both', tight=True)
    m.drawcoastlines(linewidth=1.25, ax=ax)
    m.fillcontinents(color='0.8',ax=ax, zorder=2)
    if i%2 ==0:
        m.drawparallels(np.arange(-80,81,20),labels=[1,0,0,0], linewidth=0, 
                        ax=ax)

box = axa[0,0].get_position()
tl = fig.add_axes([box.x0*1.1 + box.width * 1., box.y0, 0.02, box.height])
bounds = np.linspace(vmin, vmax, ncols)
plt.colorbar(cot, cax=tl, label='Pa decade$^{-1}$',spacing='proportional',
             boundaries=bounds)

fig.delaxes(axa[0,1])
plt.savefig('psl_maps_HadSLP2r_vs_20CR_vs_C5_1951-2011.pdf',bbox_inches='tight',
            dpi=300)