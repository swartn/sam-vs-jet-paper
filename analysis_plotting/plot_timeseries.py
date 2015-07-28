"""
Plots the timseries of SAM index and jet properties for 20CR, HadSLP2r and CMIP5.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import numpy as np
import scipy as sp
from scipy import stats
import trend_ts
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from dateutil.parser import parse

# set font size for plotting
plt.close('all')
plt.ion()
font = {'size' : 12}
plt.rc('font', **font)

#============================================#
# Define some plotting routines first
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
                    ts_95_ci), color=color, alpha=0.35, linewidth=0)  
    ax.plot(ens_mean.index, ens_mean, color=color,linewidth=1 ,label=label)   
                  
#============================================#
# The main routine
#============================================#

def plot_timeseries(datapath):
    # Load the data from `datapath` which is (mostly) saved as pandas dataframes 
    #in HDF5, and plot annual mean timeseries. 

    # load in the Marshall SAM data
    dfmarshall = pd.read_csv(datapath + 'marshall_sam.csv', 
                    index_col=0, parse_dates=True)

    # load the reanalysis data
    h5f = pd.HDFStore(datapath + 'zonmean_sam-jet_analysis_reanalysis.h5', 'r')
    dfr = h5f['zonmean_sam']
    dfhadslp = dfr['HadSLP2r']/100.
    h5f.close()

    # load in the 20CR ensemble data
    h5f_20CR = pd.HDFStore(datapath + 'zonmean_sam-jet_analysis_20CR_ensemble.h5',
                           'r')
    df_20cr_ens_sam = h5f_20CR['zonmean_sam']/100.
    df_20cr_ens_locmax = h5f_20CR['locmax']
    df_20cr_ens_maxspd = h5f_20CR['maxspd'] 
    df_20cr_ens_width = h5f_20CR['width'] 
    h5f_20CR.close()

    # load in the next set of model data
    h5f_c5 = pd.HDFStore(datapath + 'zonmean_sam-jet_analysis_cmip5.h5', 'r')
    df_c5_ens_sam = h5f_c5['zonmean_sam']/100.
    df_c5_ens_locmax = h5f_c5['locmax']
    df_c5_ens_maxspd = h5f_c5['maxspd'] 
    df_c5_ens_width = h5f_c5['width'] 
    h5f_c5.close()            
                            
    # Now do the actual plotting
    
    
    # Set up the figures
    f1 = plt.figure(1)
    f1.set_size_inches((8,8), forward=True )

    f1a = plt.subplot(421)
    f1b = plt.subplot(423)
    f1c = plt.subplot(425)
    f1d = plt.subplot(427)

    # Plot SAM
    modtsplot(df_c5_ens_sam, f1a, color='r', label='CMIP5')
    modtsplot(df_20cr_ens_sam, f1a, color='g', label='20CR')

    # plot marshall data
    #dfmarshall['sam'].resample('A').plot(ax=f1a, color='0.5', style='-', 
                #linewidth=2, grid=False, label='Marshall', zorder=3)
    #dfhadslp['sam'].resample('A').plot(ax=f1a, color='k', style='--', 
    #             linewidth=2, grid=False, label='HadSLP2r')

    hslp = dfhadslp.resample('A')
    l = f1a.plot(hslp.index, hslp, 'k--', linewidth=1, label='HadSLP2r')
    l[0].set_dashes([3,2])

    # Plot jet strength
    modtsplot(df_c5_ens_maxspd, f1b, color='r', label='CMIP5')
    modtsplot(df_20cr_ens_maxspd, f1b, color='g', label='20CR')

    # Plot jet location
    modtsplot(df_c5_ens_locmax, f1c, color='r', label='CMIP5')
    modtsplot(df_20cr_ens_locmax, f1c, color='g', label='20CR')

    # Plot jet width
    modtsplot(df_c5_ens_width, f1d, color='r', label='CMIP5')
    modtsplot(df_20cr_ens_width, f1d, color='g', label='20CR')

    # defines lists of labels
    f1ax = [ f1a, f1b, f1c, f1d ]
    panlab = ['a)', 'b)', 'c)', 'd)', 'e)', 'f)' ,'g)', 'h)']
    yaxlab1 = ['SAM Index (hPa)' , 'Strength (m s$^{-1}$)','Position ($^{\circ}$S)', 
            'Width ($^{\circ}$ lat.)']

    xtics = [datetime(1870,1,1) + relativedelta(years=20*jj) for jj in range(8)] 

    # Loop of figure 1 and label plus adjust subplots.
    for i, ax in enumerate(f1ax):
        ax.set_xticks(xtics)
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

    # Finesse some axis details.
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
    f1.savefig('../plots/timeseries.pdf',format='pdf',dpi=300,
                        bbox_inches='tight')

if __name__ == '__main__':
    plot_timeseries(datapath='../data_retrieval/data/')
    
    