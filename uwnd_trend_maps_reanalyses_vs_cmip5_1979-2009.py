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
uas_slope_c5 = h5f['uas/1979_2009/c5_uas_trend_1979_2009'][:]*120
#names2 = h5f['uas/1988_2011/model_names'][:]
h5f.close()

rean = ['R1', 'R2', '20CR', 'ERA-Int', 'CFSR', 'MERRA']
rlc = [ 'k' , 'y', 'g' , 'b' , 'c' , 'm' ] 
h5f = h5py.File('/raid/ra40/data/ncs/cmip5/sam/reanalysis_trends.h5','r')
slopes = h5f['uas/1979_2009/rean_uas_trend_1979_2009'][:]*120
h5f.close()

ifile_ccmp = '/raid/ra40/data/ncs/ccmp/ccmp_slope_199801-201112.nc'
dims = cd.get_dimensions(ifile_ccmp, 'uwnd')

fig, axa = plt.subplots(7,1, sharex=True, sharey=True, figsize=(7,7), 
                        squeeze=True)
fig.subplots_adjust(right=0.62, hspace=0.1, wspace=0.1)

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
xpt, ypt = m(20,-86)

# put on cmip5    
cot = m.pcolor(x, y, uas_slope_c5.mean(axis=0),vmin=vmin, vmax=vmax, 
               cmap=cmap_anom, ax=axa[0], rasterized=True)
axa[0].text(xpt, ypt, 'CMIP5 mean')
# put on reanalyses    
for i, r in enumerate(rean):
    m.pcolor(x, y, slopes[:,:,i],vmin=vmin, vmax=vmax, cmap=cmap_anom, 
             ax=axa[i+1], rasterized=True)
    axa[i+1].text(xpt, ypt, r.upper())
  
    
for i, ax in enumerate(axa.flatten()):    
    ax.autoscale(enable=True, axis='both', tight=True)
    m.drawcoastlines(linewidth=1.25, ax=ax)
    m.fillcontinents(color='0.8',ax=ax)
    m.drawparallels(np.arange(-80,81,20),labels=[1,0,0,0], linewidth=0, 
                    ax=ax)
	
m.drawmeridians(np.arange(0,360,90),labels=[0,0,0,1], 
                linewidth=0, yoffset=0.5e6, ax=axa[6])

box = axa[0].get_position()
tl = fig.add_axes([box.x0*1.1 + box.width * 1., box.y0, 0.02, box.height])
bounds = np.linspace(vmin, vmax, ncols)
plt.colorbar(cot, cax=tl, label='m s$^{-1}$\ndecade$^{-1}$',
             spacing='proportional', boundaries=bounds)

plt.savefig('u10m_trends_cmip5_vs_reanlayses_1979-2009_maps.pdf'
             ,bbox_inches='tight', dpi=300)

plt.figure()
plt.plot(dims['lat'], uas_slope_c5.mean(axis=(0,2)),color='r', linewidth=2)

for i, r in enumerate(rean):
    plt.plot(dims['lat'], slopes[:,:,i].mean(axis=1),color=rlc[i])

plt.plot(dims['lat'], dims['lat']*0,'k-')
plt.autoscale(enable=True, axis='both', tight=True)
plt.ylim([-0.2, 0.3])
