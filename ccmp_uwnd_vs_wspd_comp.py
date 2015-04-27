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

# load in the CCMP data
ifile_ccmp = '/raid/ra40/data/ncs/ccmp/ccmp_slope_199801-201112.nc'
slope_ccmp_uwnd = cd.loadvar(ifile_ccmp, 'uwnd')*120.
slope_ccmp_wspd = cd.loadvar(ifile_ccmp, 'wspd')*120.

slope_ccmp_uwnd = np.ma.masked_outside(slope_ccmp_uwnd, -2,2)
slope_ccmp_wspd = np.ma.masked_outside(slope_ccmp_wspd, -2,2)


dims = {'lat' : np.arange(-89.5,90.1,1),
	'lon' : np.arange(0,361,1)
        }

fig, axa = plt.subplots(2,1, sharex=True, sharey=True, figsize=(7,7), 
                        squeeze=True)
fig.subplots_adjust(right=0.825, top=0.65, hspace=0.1, wspace=0.05)

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

cot = m.pcolor(x, y, slope_ccmp_uwnd,vmin=vmin, vmax=vmax, cmap=cmap_anom, 
               ax=axa[0], rasterized=True)
axa[0].text(xpt, ypt, 'uwnd')

cob = m.pcolor(x, y, slope_ccmp_wspd,vmin=vmin, vmax=vmax, cmap=cmap_anom, 
               ax=axa[1], rasterized=True)
axa[1].text(xpt, ypt, 'wspd')

for i, ax in enumerate(axa.flatten()):    
    ax.autoscale(enable=True, axis='both', tight=True)
    m.drawcoastlines(linewidth=1.25, ax=ax)
    m.fillcontinents(color='0.8',ax=ax, zorder=2)
    if i%2 ==0:
        m.drawparallels(np.arange(-80,81,20),labels=[1,0,0,0], linewidth=0, 
                        ax=ax)
	
m.drawmeridians(np.arange(0,360,90),labels=[0,0,0,1], 
                linewidth=0,yoffset=0.5e6, ax=axa[1])

box = axa[0].get_position()
tl = fig.add_axes([box.x0*1.1 + box.width * 1., box.y0, 0.02, box.height])
bounds = np.linspace(vmin, vmax, ncols)
plt.colorbar(cot, cax=tl, label='m s$^{-1}$\ndecade$^{-1}$',
             spacing='proportional', boundaries=bounds)

axa[0].set_title('CCMP trends 1988-2011')
#plt.savefig('ccmp_uwnd_vs_wspd_trend_maps.pdf',bbox_inches='tight'
	    #, dpi=300)
	   
print "SO uwnd trend: ", slope_ccmp_uwnd[0:55,:].mean()
print "SO wspd trend: ", slope_ccmp_wspd[0:55,:].mean()
