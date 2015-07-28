"""
Plots maps of trends in u10m over 1951-2011 in 20CR and CMIP5.

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

def plot_trend_maps(datapath):
    # Load the CMIP5 data
    h5f = h5py.File(datapath + 'cmip5_trends.h5','r')
    uas_slope_c5 = h5f['uas/1951_2011/c5_uas_trend_1951_2011'][:]*120
    names2 = h5f['uas/1951_2011/model_names'][:]
    h5f.close()

    # load the data for 20CR
    # Load the data for 20CR
    h5f = h5py.File(datapath + 'reanalysis_trends.h5','r')
    slopes = h5f['u10m/1951_2011/rean_u10m_trend_1951_2011'][:]*120
    rean = h5f['u10m/1951_2011/reanalysis_names'][:]
    h5f.close()
                    
    uas_slope_20cr = slopes[:,:,0]

    dims = {'lat' : np.arange(-89.5,89.6,1),
            'lon' : np.arange(0,360,1)
            }

    fig, axa = plt.subplots(3,2, sharex=True, figsize=(7,7))
    fig.subplots_adjust(top=0.5, hspace=0.1, wspace=0.05)

    vmin = -0.5
    vmax = 0.5
    ncols = 11
    cmap_anom = brewer2mpl.get_map('RdBu', 'diverging', ncols,
                                reverse=True).mpl_colormap
    cmap_anom = discrete_cmap(ncols, cmap_anom)

    m =\
    Basemap(llcrnrlon=0,llcrnrlat=-90,urcrnrlon=360,urcrnrlat=0,projection='mill')

    lons, lats = np.meshgrid(dims['lon'], dims['lat'])
    x, y = m(lons, lats)
    xpt, ypt = m(20,-86)

    cot = m.pcolor(x, y, uas_slope_20cr,vmin=vmin, vmax=vmax, cmap=cmap_anom, 
                ax=axa[0,0], rasterized=True)
    axa[0,0].text(xpt, ypt, '20CR')
    com = m.pcolor(x, y, uas_slope_c5.mean(axis=0),vmin=vmin, vmax=vmax, 
                cmap=cmap_anom, ax=axa[1,0], rasterized=True)
    axa[1,0].text(xpt, ypt, 'CMIP5 mean')
    anom = uas_slope_c5.mean(axis=0)- uas_slope_20cr
    cob = m.pcolor(x, y, anom, vmin=vmin, 
                vmax=vmax, cmap=cmap_anom, ax=axa[1,1], rasterized=True)
    rmse = np.array(np.sqrt( np.mean(anom[0:89,:]**2) ))
    axa[1,1].text(xpt, ypt, str(np.round(rmse,2)))

    # Do stippling
    c5_25_precentile = np.percentile(uas_slope_c5,2.5, axis=0)
    c5_975_precentile = np.percentile(uas_slope_c5,97.5, axis=0)
    ds = 4 # downsample for stippling
    mask = ( (uas_slope_20cr[::ds,::ds]>c5_975_precentile[::ds,::ds]) | 
                    (uas_slope_20cr[::ds,::ds]<c5_25_precentile[::ds,::ds])
        )
    x2 = x[::ds,::ds]
    y2 = y[::ds,::ds]
    m.plot(x2[mask], y2[mask], '.k', alpha=0.75, 
        markersize=0.2, ax=axa[1,1], zorder=2)

    m.drawmeridians(np.arange(0,360,90),labels=[0,0,0,1], linewidth=0,yoffset=0e6
                    , ax=axa[1,0])
    m.drawmeridians(np.arange(0,360,90),labels=[0,0,0,1], linewidth=0,yoffset=0e6
                    , ax=axa[1,1])

    for i, ax in enumerate(axa.flatten()):      
        ax.autoscale(enable=True, axis='both', tight=True)
        m.drawcoastlines(linewidth=1.25, ax=ax)
        m.fillcontinents(color='0.8',ax=ax, zorder=3)
        for k, spine in ax.spines.items():
            spine.set_zorder(4)    
        if i%2 ==0:
            m.drawparallels(np.arange(-80,81,20),labels=[1,0,0,0], linewidth=0
                            , ax=ax)
            
    for ax in [ axa[0,1], axa[2,1], axa[2,0] ]:
        fig.delaxes(ax)
        
    box = axa[0,0].get_position()
    tl = fig.add_axes([box.x0*1.1 + box.width * 1., box.y0, 0.02, box.height])
    bounds = np.linspace(vmin, vmax, ncols)
    plt.colorbar(cot, cax=tl, label='m s$^{-1}$\n decade$^{-1}$',
                spacing='proportional', boundaries=bounds)

    axa[0,0].set_title('u10m trends 1951-2011')
    plt.savefig('../plots/uas_trend_maps_1951-2011.pdf'
                ,bbox_inches='tight', dpi=300)
 
if __name__ == '__main__':
    plot_trend_maps(datapath='../data_retrieval/data/')