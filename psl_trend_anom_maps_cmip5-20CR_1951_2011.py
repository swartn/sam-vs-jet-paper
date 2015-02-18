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

# load the data for cmip5 mean slope
ifile_c5_slope = 'ensmean_remap_psl_slope_195101-201112.nc'
#psl_slope_c5 = cd.loadvar(pth + ifile_c5_slope, 'psl') *120 # convert to yrs
dims = cd.get_dimensions(pth + ifile_c5_slope, 'psl')

#h5f = h5py.File('/raid/ra40/data/ncs/cmip5_trends.h5','r')
h5f = h5py.File('/raid/ra40/data/ncs/cmip5/sam/cmip5_trends.h5','r')
psl_slope_c5 = h5f['psl/1951_2011/c5_psl_trend_1951_2011'][:]*120
names2 = h5f['psl/1951_2011/model_names'][:]
h5f.close()

# load the data for 20CR
ifile_20CR_slope ='/raid/ra40/data/ncs/reanalyses/20CR/\
20CR_slp_slope_195101-201112.nc'
psl_slope_20cr = cd.loadvar(ifile_20CR_slope, 'slp')*120 # convert to yrs

# load the data for all 20CR ense members
ifile_20CR_slopes_all ='/raid/ra40/data/ncs/reanalyses/20CR/slp/\
prmsl_slope_195101-201112.nc'
nc = Dataset(ifile_20CR_slopes_all)
psl_slopes_all_20cr = nc.variables['prmsl'][:].squeeze()*120 
dims20cr = cd.get_dimensions(ifile_20CR_slopes_all, 'prmsl')

fig, (axt, axm, axb) = plt.subplots(3,1, sharex=True, figsize=(7,7))
fig.subplots_adjust(right=0.8, top=0.8, hspace=0.2)

vmin = -90
vmax = 90
ncols = 11
cmap_anom = brewer2mpl.get_map('RdBu', 'diverging', ncols,
                               reverse=True).mpl_colormap
cmap_anom = discrete_cmap(ncols, cmap_anom)

m =\
Basemap(llcrnrlon=0,llcrnrlat=-90,urcrnrlon=360,urcrnrlat=0,projection='mill')

lons, lats = np.meshgrid(dims['lon'], dims['lat'])
x, y = m(lons, lats)
xpt, ypt = m(20,-86)

cot = m.pcolor(x, y, psl_slope_20cr,vmin=vmin, vmax=vmax, cmap=cmap_anom, 
               ax=axt )
com = m.pcolor(x, y, psl_slope_c5.mean(axis=0),vmin=vmin, vmax=vmax, 
               cmap=cmap_anom, ax=axm )
cob = m.pcolor(x, y, psl_slope_c5.mean(axis=0)- psl_slope_20cr, vmin=vmin, 
               vmax=vmax, cmap=cmap_anom, ax=axb)
c5_25_precentile = np.percentile(psl_slope_c5,2.5, axis=0)
c5_975_precentile = np.percentile(psl_slope_c5,97.5, axis=0)
mask = ( (psl_slope_20cr>c5_975_precentile) | 
                  (psl_slope_20cr<c5_25_precentile)
       )
m.plot(x[mask], y[mask], '.k', alpha=0.5, markersize=0.75, ax=axb)
m.drawmeridians(np.arange(0,360,60),labels=[0,0,0,1], linewidth=0,yoffset=-1e6
                , ax=axb)

for ax in fig.axes:
    ax.autoscale(enable=True, axis='both', tight=True)
    m.drawcoastlines(linewidth=1.25, ax=ax)
    #m.fillcontinents(color='0.8',ax=ax)
    m.drawparallels(np.arange(-80,81,20),labels=[1,0,0,0], linewidth=0, ax=ax)
    
axt.set_title('20CR SLP trend')
axm.set_title('CMIP5 mean SLP trend')
axb.set_title('CMIP5 - 20CR')

box = axt.get_position()
tl = fig.add_axes([box.x0*1.1 + box.width * 1., box.y0, 0.02, box.height])
bounds = np.linspace(vmin, vmax, ncols)
plt.colorbar(cot, cax=tl, label='Pa decade$^{-1}$',spacing='proportional',
             boundaries=bounds)

plt.savefig('psl_maps_20CR_vs_C5_1951-2011.pdf',bbox_inches='tight', dpi=300)
             
###############################################################################
# oLook at the uncertainty in the trends
###############################################################################

fig, (axt, axm, axb) = plt.subplots(3,1, sharex=True, figsize=(7,7))
fig.subplots_adjust(right=0.8, top=0.8, hspace=0.2)

vmin = -100
vmax = 100
ncols = 11
cmap_anom = brewer2mpl.get_map('RdBu', 'diverging', ncols,
                               reverse=True).mpl_colormap
cmap_anom = discrete_cmap(ncols, cmap_anom)

vmin2 = 0
vmax2 = 40
ncols2 = 9
cmap = cmap=brewer2mpl.get_map('YlOrRd', 'sequential', ncols2).mpl_colormap
cmap = discrete_cmap(ncols2, cmap)


m =\
Basemap(llcrnrlon=0,llcrnrlat=-90,urcrnrlon=360,urcrnrlat=0,projection='mill')

lons, lats = np.meshgrid(dims20cr['lon'], dims20cr['lat'])
x, y = m(lons, lats)

cot = m.pcolor(x, y, psl_slopes_all_20cr.mean(axis=0),vmin=vmin, vmax=vmax, 
               cmap=cmap_anom, ax=axt )
com = m.pcolor(x, y, psl_slopes_all_20cr.std(axis=0)*2,vmin=vmin2, vmax=vmax2, 
               cmap=cmap, ax=axm )
#cob = m.pcolor(x, y, psl_slope_c5 - psl_slope_20cr, vmin=vmin, vmax=vmax, 
#               cmap=cmap_anom, ax=axb)

m.drawmeridians(np.arange(0,360,60),labels=[0,0,0,1], linewidth=0,yoffset=-1e6
                , ax=axb)

for ax in fig.axes:
    ax.autoscale(enable=True, axis='both', tight=True)
    m.drawcoastlines(linewidth=1.25, ax=ax)
    #m.fillcontinents(color='0.8',ax=ax)
    m.drawparallels(np.arange(-80,81,20),labels=[1,0,0,0], linewidth=0, ax=ax)
    
axt.set_title('20CR SLP trend mean')
axm.set_title('20CR SLP trend std')

box = axt.get_position()
tl = fig.add_axes([box.x0*1.1 + box.width * 1., box.y0, 0.02, box.height])
bounds = np.linspace(vmin, vmax, ncols)
plt.colorbar(cot, cax=tl, label='Pa decade$^{-1}$',spacing='proportional',
             boundaries=bounds)
                                              
box = axm.get_position()
tl = fig.add_axes([box.x0*1.1 + box.width * 1., box.y0, 0.02, box.height]) 
bounds = np.linspace(vmin2, vmax2, ncols2)
plt.colorbar(com, cax=tl, label='Pa decade$^{-1}$',
            spacing='proportional', boundaries=bounds) 
#fig.delaxes(axm)
fig.delaxes(axb)
plt.savefig('psl_maps_20CR_trends-uncertainty_1951-2011.pdf',bbox_inches=
'tight', dpi=300)

#plt.savefig('dd.png',bbox_inches='tight')

## Test to see if the trend looks right
#kwargs={'start_date':'1951-01-01', 
	#'end_date':'2011-12-31',
	#'remap':'r360x180'
       #}

#ifile_20CR_intercept ='/raid/ra40/data/ncs/reanalyses/20CR/\
#20CR_slp_intercept_195101-201112.nc'
#psl_intercept_20cr = cd.loadvar(ifile_20CR_intercept, 'slp')

#ifile_20cr_psl = '/raid/ra40/data/ncs/reanalyses/20CR/\
#20CR_slp.mon.mean.nc'
#psl_20cr = cd.loadvar(ifile_20cr_psl, 'slp', **kwargs)

#ifile_20cr_psl_spread = '/raid/ra40/data/ncs/reanalyses/20CR/\
#20CR_slp_spread.mon.mean.nc'
#psl_spread_20cr = cd.loadvar(ifile_20cr_psl_spread, 'prmsl', **kwargs)

#plt.figure()
#plt.plot(psl_20cr[:,15,50],'ok') 
#x = np.arange( psl_20cr.shape[0])
#y = x*psl_slope_20cr[15,50]/120 + psl_intercept_20cr[15,50]
#plt.plot(x,y,'r-')

##plt.plot(psl_20cr[:,15,50] + psl_spread_20cr[:,15,50],'or') 
##plt.plot(psl_20cr[:,15,50] - psl_spread_20cr[:,15,50],'ob') 

#psl_mean = psl_20cr.mean(axis=0)
#psl_std = psl_spread_20cr.mean(axis=0)

#fig, (axt, axm, axb) = plt.subplots(3,1, sharex=True, figsize=(14,14))
#fig.subplots_adjust(right=0.5, top=0.5, hspace=0.2)

#vmin = psl_mean.min()
#vmax = psl_mean.max()
#ncols = 9
#cmap = cmap=brewer2mpl.get_map('YlOrRd', 'sequential', ncols).mpl_colormap
#cmap = discrete_cmap(ncols, cmap)


#m =\
#Basemap(llcrnrlon=0,llcrnrlat=-90,urcrnrlon=360,urcrnrlat=0,projection='mill')

#lons, lats = np.meshgrid(dims['lon'], dims['lat'])
#x, y = m(lons, lats)

#cot = m.pcolor(x, y, psl_mean,vmin=vmin, vmax=vmax, cmap=cmap, 
               #ax=axt )
#com = m.pcolor(x, y, psl_std,vmin=vmin, vmax=vmax, cmap=cmap
	      #, ax=axm )
##cob = m.pcolor(x, y, psl_slope_c5 - psl_slope_20cr, vmin=vmin, vmax=vmax, 
               ##cmap=cmap_anom, ax=axb)

#m.drawmeridians(np.arange(0,360,60),labels=[0,0,0,1], linewidth=0,yoffset=-1e6
                #, ax=axb)

#for ax in fig.axes:
    #ax.autoscale(enable=True, axis='both', tight=True)
    #m.drawcoastlines(linewidth=1.25, ax=ax)
    ##m.fillcontinents(color='0.8',ax=ax)
    #m.drawparallels(np.arange(-80,81,20),labels=[1,0,0,0], linewidth=0, ax=ax)
    
#axt.set_title('20CR SLP mean')
#axm.set_title('20CR SLP std')
#axb.set_title('CMIP5 - 20CR')

#box = axt.get_position()
#tl = fig.add_axes([box.x0*1.1 + box.width * 1., box.y0, 0.02, box.height])
#bounds = np.linspace(vmin, vmax, ncols)
#plt.colorbar(cot, cax=tl, label='Pa decade$^{-1}$',spacing='proportional',
             #boundaries=bounds)
             





