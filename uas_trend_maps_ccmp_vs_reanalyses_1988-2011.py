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

d1 = '1988-01-01'
d2 = '2011-12-31'

cdo_str = '-remapdis,r360x180 -seldate,' + d1 + ',' + d2 + ' -selvar,uwnd '

path = '/raid/ra40/data/ncs/reanalyses/uwnd/'
rean = ['R1', 'R2', '20CR', 'ERA-Int', 'CFSR', 'MERRA']

# if true go and compute the slopes
if False:
    os.chdir(path)
    for r in rean:
	ifile = path + r + '_uwnd.10m.mon.mean.nc'
        cdo.trend(input=(cdo_str + ifile)
                  , output="int.nc " + r + "_slope.nc")
	
# Load the CMIP5 data
h5f = h5py.File('/raid/ra40/data/ncs/cmip5/sam/cmip5_trends.h5','r')
uas_slope_c5 = h5f['uas/1988_2011/c5_uas_trend_1988_2011'][:]*120
#names2 = h5f['uas/1988_2011/model_names'][:]
h5f.close()

# load in the data
slopes = np.zeros((180,360,6))
for i, r in enumerate(rean):
    slopes[:,:,i] = cd.loadvar(path + r.lower() + '_slope.nc', 'uwnd')*120.0

dims = cd.get_dimensions(path + 'r1_slope.nc', 'uwnd')

ifile_ccmp = '/raid/ra40/data/ncs/ccmp/ccmp_slope_199801-201112.nc'
slope_ccmp = cd.loadvar(ifile_ccmp, 'uwnd')*120.

fig, axa = plt.subplots(8,2, sharex=True, sharey=True, figsize=(7,7), 
                        squeeze=True)
fig.subplots_adjust(right=0.65, hspace=0.1, wspace=0.05)

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
xpt, ypt = m(20,-88)

cot = m.pcolor(x, y, slope_ccmp,vmin=vmin, vmax=vmax, cmap=cmap_anom, 
               ax=axa[0,0] )
axa[0,0].text(xpt, ypt, 'CCMP')

# put on reanalyses    
for i, r in enumerate(rean):
    m.pcolor(x, y, slopes[:,:,i],vmin=vmin, vmax=vmax, cmap=cmap_anom, 
             ax=axa[i+1, 0] )
    anom = slopes[:,:,i] - slope_ccmp
    anom = np.ma.masked_outside(anom,-1.0, 1.0)
    m.pcolor(x, y, anom,vmin=vmin, vmax=vmax, 
             cmap=cmap_anom, ax=axa[i+1, 1] ) 
    rmse = np.sqrt( np.mean(anom[0:89,:]**2) )
    axa[i+1,0].text(xpt, ypt, r.upper())
    axa[i+1,1].text(xpt, ypt, str(np.round(rmse,2)))
  
    
for i, ax in enumerate(axa.flatten()):    
    ax.autoscale(enable=True, axis='both', tight=True)
    m.drawcoastlines(linewidth=1.25, ax=ax)
    m.fillcontinents(color='0.8',ax=ax)
    if i%2 ==0:
        m.drawparallels(np.arange(-80,81,20),labels=[1,0,0,0], linewidth=0, 
                        ax=ax)
# put on cmip5    
m.pcolor(x, y, uas_slope_c5.mean(axis=0),vmin=vmin, vmax=vmax, cmap=cmap_anom, 
         ax=axa[7, 0] )
anom =  uas_slope_c5.mean(axis=0) - slope_ccmp
anom = np.ma.masked_outside(anom,-1.0, 1.0)
m.pcolor(x, y, anom,vmin=vmin, vmax=vmax, 
         cmap=cmap_anom, ax=axa[7, 1] )
rmse = np.sqrt( np.mean(anom[0:89,:]**2) )
axa[7,0].text(xpt, ypt, 'CMIP5 mean')
axa[7,1].text(xpt, ypt, str(np.round(rmse,2)))
	
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
plt.savefig('u10m_trends_ccmp_vs_reanlayses_1988-2011.eps',bbox_inches='tight'
	    , dpi=300)
os.system('eps2pdf u10m_trends_ccmp_vs_reanlayses_1988-2011.eps')
os.system('rm -f u10m_trends_ccmp_vs_reanlayses_1988-2011.eps') 