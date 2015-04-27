"""
Plots the timseries of SAM index and jet properties for 20CR, HadSLP2r and CMIP5.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import numpy as np
import scipy as sp
from scipy import stats
import trend_ts
reload(trend_ts)
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from dateutil.parser import parse
import sam_analysis_data as sad

""" Analyze time series in 20CR, CMIP5 and HadSLP2r

Neil Swart, v4, Feb 2015
Neil.Swart@ec.gc.ca

"""

# set font size
plt.close('all')
plt.ion()
font = {'size'   : 12}
plt.rc('font', **font)

#
# Define some global variables that we use repeatedly
#
# the names of the reanalyses we are using (in column-order of the dataframes)
rean     = ['R1', 'R2', '20CR', 'ERA', 'CFSR', 'MERRA']
num_rean = len( rean )
# corresponding colors to use for plotting each reanalysis
rlc      = [ 'k' , 'y', 'g' , 'b' , 'c' , 'm' ] 
rlc      = [ 'g' , 'y', 'g' , 'b' , 'c' , 'm' ]
seas     = ['mam', 'jja', 'son', 'djf', 'ann']  # names of the seasons
lensea   = len( seas )
xtics    = [datetime(1870,1,1) + relativedelta(years=20*jj) for jj in range(8) ] 
# xticks for time-series plot.
#============================================#
# Load the data which is saved in HDF. The data are in pandas dataframes. There 
#is one dataframe for each variable of interest
# (SAM, jet speed = maxpsd, jet position = locmax and jet width. For each 
#variable there is one dataframe for reanalyses and
# one dataframe for the CMIP5 models. With each dataframe the indices (rows) 
#are 
#a datetime index representing the monthly data
# while each column refers to an individual reanalysis or CMIP5 model. The 
#column order of the reanalyses is given in the variable
# rean above. We're not differentiating models by name here.

# This was the old definitions computed in ferret and no longer used.
#press, maxspd, locmax, width, modpress, modmaxspd, modlocmax, modwidth =\
#                      sad.load_sam_df()
#press.columns = rean
#maxspd.columns = rean
#locmax.columns = rean
#width.columns = rean

# load in the Marshall SAM data
dfmarshall = pd.read_csv('/HOME/ncs/data/marshall_sam/marshall_sam.csv', 
		  index_col=0, parse_dates=True)

# load the reanalysis data
h5f = pd.HDFStore('/raid/ra40/data/ncs/cmip5/sam/rean_sam.h5', 'r')
dfr = h5f['zonmean_sam/df']
h5f.close()
dfhadslp = dfr['HadSLP2r']/100.

# load in the 20CR ensemble data
h5f_20CR = pd.HDFStore(
    '/raid/ra40/data/ncs/reanalyses/20CR/20cr_ensemble_sam_analysis.h5',
    'r')
df_20cr_ens_sam = h5f_20CR['sam']/100.
df_20cr_ens_locmax = h5f_20CR['locmax']
df_20cr_ens_maxspd = h5f_20CR['maxspd'] 
df_20cr_ens_width = h5f_20CR['width'] 
h5f_20CR.close()

# load in the next set of model data
h5f_c5 = pd.HDFStore('/raid/ra40/data/ncs/cmip5/sam/c5_zonmean_sam-jet_analysis.h5',
                     'r')
df_c5_ens_sam = h5f_c5['sam']/100.
df_c5_ens_locmax = h5f_c5['locmax']
df_c5_ens_maxspd = h5f_c5['maxspd'] 
df_c5_ens_width = h5f_c5['width'] 
h5f_c5.close()


#============================================#


def modtsplot(df, ax, color='r', label='CMIP5'):
    """ For the columns of df, compute the columnwise-ensemble mean and 95% 
        confidence interval, then plot the envelope and mean.
    """
    # compute the ensemble mean across all columns (models).
    ens_mean = df.mean( axis=1 )
    # compute the 95% CI with n -1 degrees of freedom.
    num_models =  len( df.columns )
    ens_std = df.std(axis=1) 
    c = sp.stats.t.isf(0.025, num_models - 1 )
    ts_95_ci = ( c * ens_std ) / np.sqrt( num_models )
    #ts_95_ci = 2 * ens_std
    
    # reample to annual and plot
    ens_mean = ens_mean.resample('A')
    ts_95_ci = ts_95_ci.resample('A')
    ax.fill_between(ens_mean.index , ( ens_mean - ts_95_ci ) ,  ( ens_mean + 
                    ts_95_ci), color=color, alpha=0.25, linewidth=0)  
    ax.plot(ens_mean.index, ens_mean, color=color,linewidth=1 ,label=label)   
                  
def rean_proc(dfr, axts):
    """ Loop over the columns of dfr (corresponding to different reanalyses) 
        and plot the time-series in axis axts.
    """
    for (i, name) in enumerate( ['20CR'] ):#enumerate( rean ):     
        axts.plot(dfr.resample('A').index, dfr[name].resample('A'), 
                  color=rlc[ i ], linewidth=2, alpha=1, label=name)
        axts.set_axisbelow(True)
              
                          
#========= SAM - press ===============#

# Set up the figures
f1 = plt.figure(1)
plt.figure(1).set_size_inches((8,8), forward=True )

f1a = plt.subplot( 421 )
f1b = plt.subplot( 423 )
f1c = plt.subplot( 425 )
f1d = plt.subplot( 427 )

#rean_proc(press, axts=f1a)    
#modtsplot(modpress, f1a)
modtsplot(df_c5_ens_sam, f1a, color='r', label='CMIP5')
modtsplot(df_20cr_ens_sam, f1a, color='g', label='20CR')

#dfmarshall['sam'].resample('A').plot(ax=f1a, color='0.5', style='-', 
             #linewidth=2, grid=False, label='Marshall', zorder=3)
dfhadslp['sam'].resample('A').plot(ax=f1a, color='k', style='--', 
             linewidth=2, grid=False, label='HadSLP2r')

#rean_proc(maxspd, axts=f1b)
#modtsplot(modmaxspd, f1b)
modtsplot(df_c5_ens_maxspd, f1b, color='r', label='CMIP5')
modtsplot(df_20cr_ens_maxspd, f1b, color='g', label='20CR')

#rean_proc(locmax, axts=f1c)
#modtsplot(modlocmax, f1c)
modtsplot(df_c5_ens_locmax, f1c, color='r', label='CMIP5')
modtsplot(df_20cr_ens_locmax, f1c, color='g', label='20CR')

#rean_proc(width, axts=f1d)
#modtsplot(modwidth, f1d)
modtsplot(df_c5_ens_width, f1d, color='r', label='CMIP5')
modtsplot(df_20cr_ens_width, f1d, color='g', label='20CR')

# FIGURE 1: Time-series
# defines some lists of labels.
f1ax = [ f1a, f1b, f1c, f1d ]
panlab = ['a)', 'b)', 'c)', 'd)', 'e)', 'f)' ,'g)', 'h)']
yaxlab1 = ['SAM Index (hPa)' , 'Umax (m s$^{-1}$)','Position ($^{\circ}$S)', 
	   'Width ($^{\circ}$ lat.)']


# Loop of figure 1 and label plus adjust subplots.
for i, ax in enumerate( f1ax ):
    ax.set_xticks( xtics )
    ax.set_xlim( [datetime(1881,1,1) , datetime(2013,12,31)] )
    ax.autoscale(enable=True, axis='y', tight=True )
    ylim = ax.get_ylim()
    yrange =  max(ylim) - min(ylim)
    ax.text( datetime(1885,1,1), max( ylim ) -0.15*yrange, panlab[i])
    #ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(6) )
    ax.set_ylabel( yaxlab1[i] )

    if (ax != f1d): # only keep xlabels for the bottom panels
        ax.set_xticklabels([])
        ax.set_xlabel('')
    else: 
        plt.setp( ax.xaxis.get_majorticklabels(), rotation=35, ha='right' )
        ax.set_xlabel('Year')

majorFormatter = mpl.ticker.FormatStrFormatter('%d')
f1a.yaxis.set_major_locator(mpl.ticker.MultipleLocator(4))
f1a.yaxis.set_major_formatter(majorFormatter)
f1b.yaxis.set_major_locator(mpl.ticker.MultipleLocator(1))
f1b.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%1.1f'))
f1c.yaxis.set_major_locator(mpl.ticker.MultipleLocator(2))
f1c.yaxis.set_major_formatter(majorFormatter)
f1d.yaxis.set_major_locator(mpl.ticker.MultipleLocator(1))
f1d.yaxis.set_major_formatter(majorFormatter)
      
plt.figure(1).subplots_adjust(hspace=0.05)

f1a.legend(ncol=3, prop={'size':12}, bbox_to_anchor=(1.05, 1.3),
           handlelength=2.2, handletextpad=0.075, columnspacing=1.2,
           frameon=False)

# save some pdfs
plt.figure(1).savefig('sam_pos_str_width_ts_v5.pdf',format='pdf',dpi=300,
                      bbox_inches='tight')
