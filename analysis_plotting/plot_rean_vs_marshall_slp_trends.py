"""
Plots seasonal trends of SLP at 40 and 60S and the SAM index, all computed at the
Marshall station locations, and for various reanalyses and CMIP5.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import cmipdata as cd
import trend_ts
from datetime import datetime
from dateutil.relativedelta import relativedelta
import h5py
import numpy as np
import scipy as sp
import pandas as pd
import pandas_tools as pt
import matplotlib.pyplot as plt
import matplotlib as mpl
import brewer2mpl
plt.ion()
plt.close('all')
font = {'size'   : 12}
plt.rc('font', **font)

def modtsplot(df, ax):
    """ For the columns of df, compute the columnwise-ensemble mean and 95% 
confidence interval, 
    then plot the envelope and mean.
    """
    # compute the ensemble mean across all columns (models).
    df = df.dropna()
    ens_mean = df.mean(axis=1)
    # compute the 95% CI with n -1 degrees of freedom.
    num_models =  len( df.columns )
    ens_std = df.std(axis=1) 
    c = sp.stats.t.isf(0.025, num_models - 1 )
    ts_95_ci = ( c * ens_std ) / np.sqrt( num_models )

    # reample to annual and plot
    #ens_mean = ens_mean.resample('A')
    #ts_95_ci = ts_95_ci.resample('A')
    ax.fill_between( ens_mean.index, (ens_mean - ts_95_ci ),  
		    ( ens_mean + ts_95_ci), color='r', alpha=0.25,
		    linewidth=0)  
    #ens_mean.plot(ax=ax, color='r',linewidth=3 ,label='CMIP5',legend=False, 
                  #grid=False)
    ax.plot(ens_mean.index, ens_mean, color='r',linewidth=1 ,label='CMIP5')  

datapath = '../data_retrieval/data/'

# load in the Marshall SAM data
df = pd.read_csv(datapath + 'marshall_sam.csv', index_col=0, parse_dates=True)

# load the reanalysis data
rean = ['R1', 'R2', '20CR', 'ERA-Int', 'CFSR', 'MERRA', 'HadSLP2r']
rlc = [ 'k' , 'y', 'g' , 'b' , 'c' , 'm', 'k']
ls = ['-k', '-y', '-g', '-b', '-c', '-m', '--k']
h5f = pd.HDFStore(datapath + 'zonmean_sam-jet_analysis_reanalysis.h5', 'r')
dfr = h5f['marshall_sam/sam']
h5f.close()


# load in the cmip5 data
h5fc5 = pd.HDFStore(datapath + 'zonmean_sam-jet_analysis_cmip5.h5', 'r')
dfc5 = h5fc5['marshall_sam/sam'] 
h5fc5.close() 

d1 = pd.datetime(1957,1,1)
d2 = pd.datetime(2011,12,31)

          
 # Define some functions
def get_seasons(df):
    """Extract the 4 seasons and the annual mean from dataframe df, and save 
    them as df.djf, df.mam,
    df.jja, df.son and df.ann and then return df. Note December is from the 
    previous year.
    """
    df.mam = df[ ( df.index.month >= 3 ) & ( df.index.month <= 5 )]
    df.jja = df[ ( df.index.month >= 6 ) & ( df.index.month <= 8 )]
    df.son = df[ ( df.index.month >= 9 ) & ( df.index.month <= 11 )]
    dfsh = df.shift(12)
    df.djf = pd.concat( [ dfsh[dfsh.index.month==12 ] ,\
         df[ ( df.index.month >= 1 ) & ( df.index.month <= 2 )] ],axis=0)
    df.djf = df.djf.sort()
    df.ann = df.resample('A')
    df.mon = df
    return df

def year_lim( df , ys , ye ):
    """ Limits the dataframe df to between years starting in ys and ending in ye 
    inclusive"""
    dfo = df[ ( df.index.year >= ys ) & ( df.index.year <= ye ) ]
    return dfo

def calc_trends( dfp, var, ys , ye ):
    """Calculate linear trend in the dataframe dfp between years (datetime 
    indices) ys and ye inclusive. Saves the trend as dfp.slope and calculates 
    and saves the linear prediction (dfp.yhat) for all input years.
    """
    #dfp = dfp.dropna()
    dfp =  year_lim( dfp.resample('A') , ys, ye )              
    dfp.slope , dfp.conf_int , p_value, yhat, intercept =\
              trend_ts.trend_ts(dfp.index.year , dfp[var])
    dfp['yhat'] = dfp.slope * dfp.index.year + intercept          
    return dfp      
          
          
def rean_proc(dfr, axtrend=None, tys=0, tye=0, ms=15, mew=2):
    """ Loop over the columns of dfr (corresponding to different reanalyses) 
    and:
    1. if axtrend is given then compute the linear trend between years tys and 
    tye (inclusive) and plot the trends on axis axtrends. 
    2. Return the trends.
    
    The data from dfr are colored columwise in the plots using colors provided 
    in the global variable rlc, and similarly are labelled using the names 
    listed in the global variable rean.
    """

    rean_trends = np.zeros( ( num_rean  , lensea ) )
    rean_ci = np.zeros( ( num_rean  , lensea ) )  
    dfr.seasons = get_seasons( dfr ) ; # do the seasonal decomposition
    
    # Loop over reanalyses and do some basic dataframe checks and adjustments.
    # We're assuming len(dfr.columns) == len(rean).
    for (i, name) in enumerate( rean ):               
        # If axtrend was passed, plot the linear trend between tys and tye for 
        # each season and each reanalysis.
        # Season names are listed in the global variable seas.
        if ( axtrend ):
            for (k, nm) in enumerate(seas):
                names = 'dfr.seasons.' + nm
                mt = calc_trends( eval(names), name, tys, tye)
                rean_trends[i, k]  =  mt.slope * 10
                rean_ci[i, k]  =  mt.conf_int * 10            
                if (nm == 'ann') & (not np.isnan(rean_trends[i, k])):
                    axtrend.plot(k, rean_trends[i, k], ls[i],          
                                 ms=ms, mew=mew, label=reanl[i])
                else:
                    axtrend.plot(k, rean_trends[i, k], ls[i], 
                                 ms=ms, mew=mew, label='')

            axtrend.set_xticks( np.arange( lensea + 1 ) )
            axtrend.plot([-1, 5],[0, 0], 'k--')  
    return rean_trends, rean_ci            
          
def mod_proc(df, axtrend, tys, tye ):
    """ Loop over the columns of df calculate trends for each one, plus plot the 
    ensemble trend stats"""
    num_models =  len( df.columns )
    mod_trends = np.empty( ( num_models  , lensea ) )
    df.seasons = get_seasons(df)

    for i, mname in enumerate( df.columns ):  
        for (k, nm) in enumerate(seas):
            names = 'df.seasons.' + nm
            mt = calc_trends( eval(names), mname, tys, tye )
            mod_trends[i, k] = mt.slope * 10
            
            if i == ( num_models - 1 ):
                mod_trend_mean = np.mean( mod_trends[ : , k ] )
                mod_trend_std =  np.std( mod_trends[ : , k ] )
                c = sp.stats.t.isf(0.025, num_models - 1 )
                mod_95_ci = ( c * mod_trend_std ) / np.sqrt( num_models )
                mod_5thp = np.percentile( mod_trends[ : , k ] , 5 )
                mod_95thp = np.percentile( mod_trends[ : , k ] , 95 )
                axtrend.plot([k, k], [mod_5thp, mod_95thp], 'r',
                             linewidth=4, alpha=0.25)
                axtrend.plot([k, k], [mod_trend_mean - mod_95_ci,
                             mod_trend_mean + mod_95_ci ],          
                             'r', linewidth=4) 
                if nm == 'ann':
                    axtrend.plot(k , np.mean(mod_trends[:, k]), 
                                 '_r', ms=15, mew=2, label='CMIP5')
                else:
                    axtrend.plot(k, np.mean(mod_trends[:, k]), 
                                 '_r', ms=15, mew=2, label='')    
    return mod_trends                              

df40s = pd.concat([dfr.ix['p40s']/100., df.slp40], axis=1)
df40s.columns=[u'R1', u'R2', u'TCR', u'ERA', u'CFSR', 
               u'MERRA', u'HadSLP2r', u'Marshall']
df65s = pd.concat([dfr.ix['p65s']/100., df.slp65], axis=1)
df65s.columns=[u'R1', u'R2', u'TCR', u'ERA', u'CFSR', 
               u'MERRA', u'HadSLP2r', u'Marshall']
dfsam = pd.concat([dfr.ix['sam']/100., df.sam], axis=1)
dfsam.columns=[u'R1', u'R2', u'TCR', u'ERA', u'CFSR', 
               u'MERRA', u'HadSLP2r', u'Marshall']

# setup some global variables          
num_rean = len( rean )
seas     = ['mam', 'jja', 'son', 'djf', 'ann']  
lensea   = len( seas )          
tys1 = [1958, 1979]
tye1 = [2011, 2009]

# make the plots          
fig, axa = plt.subplots(3,2, sharex=True, figsize=(7,7), sharey=True)
fig.subplots_adjust(hspace=0.05, wspace=0.05, right=0.8, left=0.2)

for c in [0,1]:
    tys = tys1[c]
    tye = tye1[c]
    rean = ['R1', 'R2', 'TCR', 'ERA', 'CFSR', 'MERRA']
    reanl = ['R1', 'R2', '20CR', 'ERA-Int', 'CFSR', 'MERRA']
    obs = ['HadSLP2r', 'Marshall']
    ls = ['_k', '_y', '_g', '_b', '_c', '_m', '.k', 'kx']
    rean_p40_trends, rean_p40_ci  = rean_proc(df40s.drop(obs,1), 
                  axtrend=axa[0, c], tys=tys, tye=tye) 
    mod_sam_trends = mod_proc(dfc5.ix['p40s']/100., axa[0, c], tys=tys, tye=tye)

    rean_p65_trends, rean_p65_ci = rean_proc(df65s.drop(obs,1), 
                  axtrend=axa[1, c], tys=tys, tye=tye) 
    mod_sam_trends = mod_proc(dfc5.ix['p65s']/100., axa[1, c], tys=tys, 
                  tye=tye)          
    rean_sam_trends, rean_sam_ci = rean_proc(dfsam.drop(obs,1), 
                  axtrend=axa[2, c], tys=tys, tye=tye) 
    mod_sam_trends = mod_proc(dfc5.ix['sam']/100., axa[2, c], tys=tys, tye=tye) 
        
   
    obs = ['R1', 'R2', 'TCR', 'ERA', 'CFSR', 'MERRA']   
    rean = ['HadSLP2r', 'Marshall']
    reanl = ['HadSLP2r', 'Marshall']
    ls = ['.k', 'kx']   
    obs_p40_trends, obs_p40_ci  = rean_proc(df40s.drop(obs,1), 
                  axtrend=axa[0, c], tys=tys, tye=tye, ms=10, mew=2) 
    obs_p65_trends, obs_p65_ci = rean_proc(df65s.drop(obs,1), 
                  axtrend=axa[1, c], tys=tys, tye=tye, ms=10, mew=2) 
    obs_sam_trends, obs_sam_ci = rean_proc(dfsam.drop(obs,1), 
                  axtrend=axa[2, c], tys=tys, tye=tye, ms=10, mew=2) 
    if c==0:
        print obs_sam_trends[1,:]

   
yaxlab = ['P at 40$^{\circ}$S \n(hPa dec$^{-1}$)', '',
          'P at 65$^{\circ}$S \n(hPa dec$^{-1}$)','',
          'SAM \n(hPa dec$^{-1}$)', ''
         ]

panlab = ['a)', 'b)', 'c)', 'd)', 'e)', 'f)' ,'g)', 'h)']
          
# Loop of figure 2 and label plus adjust subplots.
for i, ax in enumerate( fig.axes ):
    ax.set_ylim([-2.5, 2.5])
    ylim = ax.get_ylim()
    yrange =  max(ylim) - min(ylim)
    ax.text( -0.35, max( ylim ) -0.125*yrange, panlab[i])
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(5) )
    ax.set_xlim([-0.5, lensea -0.5])

    if (ax != axa[2,0]) &  (ax != axa[2,1]): 
        ax.set_xticklabels([])
        ax.set_xlabel('')
    if i%2==0:    
        ax.set_ylabel( yaxlab[i] )          
          
axa[0,0].set_xticklabels(  [ s.upper() for s in seas]  )
axa[0,1].set_xticklabels(  [ s.upper() for s in seas]  )

axa[0,1].legend(ncol=1, prop={'size':12},numpoints=1, 
                bbox_to_anchor=(1.65, 1.05), handlelength=0.01,
                handletextpad=1, borderpad=1, frameon=False) 

axa[0,0].set_title(str(tys1[0]) + '-' + str(tye1[0]) )
axa[0,1].set_title(str(tys1[1]) + '-' + str(tye1[1]) )

plt.savefig('../plots/marshall_trends.pdf',format='pdf',dpi=300,
                       bbox_inches='tight')