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

# to 2011
# HadSLP data is now with reanlyses.
h5f = h5py.File('/raid/ra40/data/ncs/cmip5/sam/reanalysis_trends.h5','r')
slopes = h5f['psl/1951_2011/rean_psl_trend_1951_2011'][:]*120
rean = h5f['psl/1951_2011/reanalysis_names'][:]
h5f.close()
psl_slope_hadslp_2011 = slopes[:,:,1]

# to 2004
# HadSLP data is now with reanlyses.
h5f = h5py.File('/raid/ra40/data/ncs/cmip5/sam/reanalysis_trends.h5','r')
slopes = h5f['psl/1951_2004/rean_psl_trend_1951_2004'][:]*120
rean = h5f['psl/1951_2004/reanalysis_names'][:]
h5f.close()
psl_slope_hadslp_2004 = slopes[:,:,1]

dims = {'lat' : np.arange(-89.5,89.6,1),
	'lon' : np.arange(0,360,1)
        }

fig, axa = plt.subplots(3,2, sharex=True, figsize=(7,7))
fig.subplots_adjust(top=0.5, hspace=0.1, wspace=0.05)

vmin = -80
vmax = 80
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

cot = m.pcolor(x, y, psl_slope_hadslp_2004,vmin=vmin, vmax=vmax, 
               cmap=cmap_anom, ax=axa[0,0] )
cot.set_rasterized('True')
axa[0,0].text(xpt, ypt, 'HadSLP2r 2004')

com = m.pcolor(x, y, psl_slope_hadslp_2011,vmin=vmin, vmax=vmax, 
               cmap=cmap_anom, ax=axa[1,0] )
com.set_rasterized('True')
anom = psl_slope_hadslp_2011 - psl_slope_hadslp_2004
com = m.pcolor(x, y, anom,vmin=vmin, vmax=vmax
	 , cmap=cmap_anom,ax=axa[1,1] )

com.set_rasterized('True')
rmse = np.sqrt( np.mean(anom[0:89,:]**2) )
axa[1,0].text(xpt, ypt, 'HaSLP2r 2011')
axa[1,1].text(xpt, ypt, str(np.round(rmse,2)))

m.drawmeridians(np.arange(0,360,90),labels=[0,0,0,1], linewidth=0,yoffset=-0e6
                , ax=axa[1,1])
m.drawmeridians(np.arange(0,360,90),labels=[0,0,0,1], linewidth=0,yoffset=-0e6
                , ax=axa[1,0])

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
fig.delaxes(axa[2,0])
fig.delaxes(axa[2,1])

plt.savefig('psl_maps_HadSLP2r_1951_to_2004_vs_2011_ending.pdf'
    ,bbox_inches='tight' , dpi=300)
#os.system('eps2pdf psl_maps_HadSLP2r_1951_to_2004_vs_2011_ending.eps')
#os.system('rm -f psl_maps_HadSLP2r_1951_to_2004_vs_2011_ending.eps')