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

dims = {'lat' : np.arange(-89.5,89.6,1),
        'lon' : np.arange(0,360,1)
        }


# load the data for all 20CR ense members
ifile_20CR_slopes_all ='/raid/ra40/data/ncs/reanalyses/20CR/slp/\
remap_prmsl_slope_195101-201112.nc'
nc = Dataset(ifile_20CR_slopes_all)
psl_slopes_all_20cr = nc.variables['prmsl'][:].squeeze()*120 
dims20cr = cd.get_dimensions(ifile_20CR_slopes_all, 'prmsl')
           
ifile_20CR_slopes_all_u10m = '/home/ncs/ra40/reanalyses/20CR/winds_10m/u_10m/\
remap_u10m_slope_195101-201112.nc'
nc = Dataset(ifile_20CR_slopes_all_u10m)
u10m_slopes_all_20cr = nc.variables['u10m'][:].squeeze()*120            
dims20cr2 = cd.get_dimensions(ifile_20CR_slopes_all_u10m, 'u10m')
           
###############################################################################
# oLook at the uncertainty in the trends
###############################################################################

fig, (axt, axm, axb) = plt.subplots(3,1, sharex=True, figsize=(7,7))
fig.subplots_adjust(right=0.8, top=0.8, hspace=0.2)

# For SLP
vmin = -100
vmax = 100
ncols = 11

# For u10m
vmin2 = -0.5
vmax2 = 0.5

cmap_anom = brewer2mpl.get_map('RdBu', 'diverging', ncols,
                               reverse=True).mpl_colormap
cmap_anom = discrete_cmap(ncols, cmap_anom)

m =\
Basemap(llcrnrlon=0,llcrnrlat=-90,urcrnrlon=360,urcrnrlat=0,projection='mill',
        suppress_ticks=True)

lons, lats = np.meshgrid(dims20cr['lon'], dims20cr['lat'])
lons2, lats2 = np.meshgrid(dims20cr2['lon'], dims20cr2['lat'])

x, y = m(lons, lats)
x2, y2 = m(lons2, lats2)

cot = m.pcolor(x, y, psl_slopes_all_20cr.mean(axis=0),vmin=vmin, vmax=vmax, 
               cmap=cmap_anom, ax=axt, rasterized=True, zorder=0)
CS = m.contour(x, y, psl_slopes_all_20cr.std(axis=0)*2,np.arange(0,20,2),
                ax=axt, colors='k', zorder=0)
plt.clabel(CS, CS.levels, inline=True, fmt='%d', fontsize=10, zorder=1)

com = m.pcolor(x2, y2, u10m_slopes_all_20cr.mean(axis=0),vmin=vmin2, vmax=vmax2, 
               cmap=cmap_anom, ax=axm, rasterized=True, zorder=0)
CS2 = m.contour(x2, y2, u10m_slopes_all_20cr.std(axis=0)*2,np.arange(0,0.1,0.01),
               ax=axm, colors='k', zorder=0)
plt.clabel(CS2, CS2.levels, inline=True, fmt='%1.2f', fontsize=10, zorder=1)

xtp = np.arange(0,360,60)
m.drawmeridians(xtp,labels=[0,0,0,1], linewidth=0,yoffset=-1e6
               , ax=axm)
xt, yt = m(np.arange(0,360,60), np.repeat(-90,6))
axm.set_xticks(xt)

for ax in fig.axes:
    ax.autoscale(enable=True, axis='both', tight=True)
    m.drawcoastlines(linewidth=1.25, ax=ax)
    m.fillcontinents(color='0.8',ax=ax, zorder=4)
    m.drawparallels(np.arange(-80,81,20),labels=[1,0,0,0], linewidth=0, ax=ax)
    for k, spine in ax.spines.items():
        spine.set_zorder(10)


box = axt.get_position()
tl = fig.add_axes([box.x0*1.1 + box.width * 1., box.y0, 0.02, box.height])
bounds = np.linspace(vmin, vmax, ncols)
plt.colorbar(cot, cax=tl, label='Pa decade$^{-1}$',spacing='proportional',
             boundaries=bounds)
    
box = axm.get_position()
tl = fig.add_axes([box.x0*1.1 + box.width * 1., box.y0, 0.02, box.height]) 
bounds = np.linspace(vmin2, vmax2, ncols)
plt.colorbar(com, cax=tl, label='m s$^{-1}$ decade$^{-1}$',
            spacing='proportional', boundaries=bounds) 
#fig.delaxes(axm)
fig.delaxes(axb)
plt.savefig('psl_maps_20CR_trends-uncertainty_1951-2011.pdf',bbox_inches=
'tight', dpi=300)




