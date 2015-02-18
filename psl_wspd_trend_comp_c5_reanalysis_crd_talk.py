import cmipdata as cd
import os
os.system( 'rm -rf /tmp/cdo*') # clean out tmp to make space for CDO processing.
import numpy as np
import scipy as sp
import scipy.stats
import matplotlib.pyplot as plt
import matplotlib as mpl
from trend_ts import trend_ts
# set font size
plt.close('all')
plt.ion()
font = {'size'   : 12}
plt.rc('font', **font)

# Define the location of the data
rean_names =['R1', 'R2', '20CR', 'ERA-Int', 'CFSR', 'MERRA']
rean_data_path = '/HOME/ncs/data/reanalyses/'
mod_psl_path  = '/home/ncs/ra40/cmip5/sam/c5_slp/'
mod_uas_path  = '/home/ncs/ra40/cmip5/sam/c5_uas/'

fig, axa = plt.subplots(2,2,sharex=True)

# Define a  set of colors to use in plots
rlc = [ 'k' , 'y', 'g' , 'b' , 'c' , 'm' ] 

def trend_by_lat(x):
    """Takes in the month-latitude numpy array and return decadal trends at each lat"""
    trend = np.zeros( x.shape[1] )
    for j in range( x.shape[1] ):
        trend[j], intercept, r_value, p_value, std_err = sp.stats.linregress( range( x.shape[0] ), x[:,j] )
    trend = trend*120 # convert from /month to /decade
    return trend
#####################################################
#     do the CMIP5 models
######################################################

# PSL
f = open(mod_psl_path+'list_match_uas','r')
filenames = [ line.strip() for line in f ]
filenames = [ mod_psl_path + f for f in filenames ]

# Get the model latitudes. they have already been regridded:
dimensions = cd.get_dimensions( filenames[0], 'psl')
mlat = dimensions['lat']

# Load the zonal-mean model psl data into a matrix with dims: model, time, latitude
kwargs={'start_date':'1979-01-01', 'end_date':'2009-12-31'} #, 'timmean':True}
mat = cd.loadfiles( filenames, 'psl', **kwargs) 

mod_psl_clim = mat.mean(axis=1).squeeze()  # The climatology for each model
ensmean_psl  = mod_psl_clim.mean(axis=0)   # The ens. mean climatology
ensstd_psl   = mod_psl_clim.std(axis=0)    # The std of climatologies
num_models   = mat.shape[0]                # number of models.

c = sp.stats.t.isf(0.025, num_models - 1 ) # the two-tailed 5% critical value from the t-dist
psl_95pci = ( c *  ensstd_psl) / np.sqrt( num_models ) # the 95% confidence interval

axa[0,0].fill_between(mlat, (ensmean_psl- psl_95pci)/1e2,(ensmean_psl+ psl_95pci)/1e2 , color='r', alpha=0.25,edgecolor='none' )
axa[0,0].plot(mlat, ensmean_psl/1e2, color='r', linewidth=3, label='CMIP5' )

# Trends
mod_psl_trend = np.zeros( (num_models, len(mlat)) )
for n in range(num_models):
    mod_psl_trend[n,:] = trend_by_lat( mat[n,:,:].squeeze() )/1e2
    
ensmean_psl_trend = mod_psl_trend.mean(axis=0)
ensstd_psl_trend = mod_psl_trend.std(axis=0)
psl_95pci = ( c *  ensstd_psl_trend) / np.sqrt( num_models ) # the 95% confidence interval

axa[0,1].fill_between(mlat, (ensmean_psl_trend-psl_95pci),(ensmean_psl_trend+ psl_95pci), color='r', alpha=0.25,edgecolor='none')
axa[0,1].plot(mlat, ensmean_psl_trend, color='r', linewidth=3)

#########################################################################################
# u10m
(filenames_uas, modelnames) = cd.listfiles(mod_uas_path + 'zonmean_uas_Amon_*_2013')

# Get the model latitudes. they have already been regridded:
dimensions = cd.get_dimensions( filenames_uas[0], 'uas')
mlat = dimensions['lat']

# Load the zonal-mean model psl data into a matrix with dims: model, time, latitude
kwargs={'start_date':'1979-01-01', 'end_date':'2009-12-31'} #, 'timmean':True}
mat = cd.loadfiles(filenames_uas, 'uas', **kwargs) 

mod_uas_clim = mat.mean(axis=1).squeeze()  # The climatology for each model
ensmean_uas  = mod_uas_clim.mean(axis=0)   # The ens. mean climatology
ensstd_uas   = mod_uas_clim.std(axis=0)    # The std of climatologies
num_models   = mat.shape[0]                # number of models.

c = sp.stats.t.isf(0.025, num_models - 1 ) # the two-tailed 5% critical value from the t-dist
uas_95pci = ( c *  ensstd_uas) / np.sqrt( num_models ) # the 95% confidence interval

axa[1,0].fill_between(mlat, (ensmean_uas-uas_95pci),(ensmean_uas+ uas_95pci), color='r', alpha=0.25,edgecolor='none' )
axa[1,0].plot(mlat, ensmean_uas, color='r', linewidth=3, label='CMIP5' )

# Trends
mod_uas_trend = np.zeros( (num_models, len(mlat)) )
for n in range(num_models):
    mod_uas_trend[n,:] = trend_by_lat( mat[n,:,:].squeeze() )
    
ensmean_uas_trend = mod_uas_trend.mean(axis=0)
ensstd_uas_trend = mod_uas_trend.std(axis=0)
uas_95pci = ( c *  ensstd_uas_trend) / np.sqrt( num_models ) # the 95% confidence interval

axa[1,1].fill_between(mlat, (ensmean_uas_trend-uas_95pci),(ensmean_uas_trend+ uas_95pci), color='r', alpha=0.25,edgecolor='none')
axa[1,1].plot(mlat, ensmean_uas_trend, color='r', linewidth=3)

######################################################
#    do the reanalyses
######################################################

for i, rean in enumerate(rean_names):
    print rean
    
    # Do the SLP
    infile = rean_data_path + rean + '_slp.mon.mean.nc'
    dimensions = cd.get_dimensions( infile, 'slp')
    lat = dimensions['lat']
    slp = cd.loadvar(infile, 'slp', start_date='1979-01-01', end_date='2009-12-31', zonmean=True)  
    axa[0,0].plot(lat, np.mean(slp, axis=0)/1e2, color=rlc[i], linewidth=2, label=rean )
    
    # Compute the trend
    trend = trend_by_lat( slp )
    axa[0,1].plot( lat, trend/1e2, color=rlc[i], linewidth=2 )
    axa[0,1].set_ylim(-1, 0.8)

    
    # Do the UWND
    infile = rean_data_path + rean + '_uwnd.10m.mon.mean.nc'
    u10m = cd.loadvar(infile, 'uwnd', start_date='1979-01-01', end_date='2009-12-31', zonmean=True)  
    dimensions = cd.get_dimensions( infile, 'uwnd')
    lat = dimensions['lat'] 
    axa[1,0].plot(lat, np.mean(u10m, axis=0), color=rlc[i], linewidth=2 )
    axa[1,0].set_ylim(-6, 9)

    
    # Compute the trend
    trend = trend_by_lat( u10m )
    axa[1,1].plot( lat, trend, color=rlc[i], linewidth=2 )
    axa[1,1].set_yticks(np.arange(-0.2,0.4,0.1) )
    axa[1,1].set_ylim(-0.2, 0.3)


axa[0,0].legend(ncol=2, prop={'size':11}, handlelength=1.5, handletextpad=0.1, borderpad=1, bbox_to_anchor=(1.05, 0.52), columnspacing=0.4, frameon=False)

# Put on "zero" lines    
axa[1,1].plot( lat, lat*0, 'k--', linewidth=0.5, zorder=1 )
axa[0,1].plot( lat, lat*0, 'k--', linewidth=0.5, zorder=1 )
axa[1,0].plot( lat, lat*0, 'k--', linewidth=0.5, zorder=1 )

# Put on labels and adjust some plot properties
labels = ['a)', 'b)', 'c)', 'd)']
ylabels =[ r'SLP (hPa)', r'Trend (hPa/dec)', 'U 10m (m s$^{-1}$)', 'Trend (m s$^{-1}$/dec)']    
titles = ['Climatologies', 'Trends']
for k,ax in enumerate( axa.flatten() ):
    ax.minorticks_on()
    ax.tick_params('both', length=6, width=1, which='major')
    ax.tick_params('both', length=3, width=1, which='minor')
    ax.set_xlim([-90, 90])    
    ax.set_ylabel( ylabels[k] )
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(7))
    ymin, ymax = ax.get_ylim()
    yrange = ymax - ymin
    ax.text( -72, ymax - 0.12*yrange, labels[k] )
    if k < 2:
        plt.setp( ax.get_xticklabels(), visible=False)
        ax.set_title(titles[k])
    else:
	ax.set_xlabel('Latitude')
	
    if (k == 1) or (k == 3 ):
       ax.yaxis.set_label_position("right") 
       ax.yaxis.tick_right()
       ax.yaxis.set_ticks_position('both')
    
plt.subplots_adjust(wspace=0.1,hspace=0.1)
plt.savefig('rean_vs_c5_clim_trends_by_lat_crd_talk.pdf',bbox_inches='tight')