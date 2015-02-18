import numpy as np
import scipy as sp
import trend_ts
reload(trend_ts)
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from dateutil.parser import parse
import sam_analysis_data as sad

""" Analyze changes in the Southern Annular Mode and SH westerly jet strength, position and width
in the CMIP5 models and in six reanalyses.

MODIFIED FOR THE OCEAN CARBON WORKSHOP PRESENTATION

This script produces 4 plots:

1. Time-series of SAM and jet strength, position, and width in the models and reananlyses.
2. Trends in the above variables over two-different periods (1951-2011 and 1979-2009).
3. The relationship between SAM and strength trends.
4. The relationship between SAM and trends in the other variables, as well as trends in
SAM and the climatology of the variables. (e.g. SAM trend vs climatological jet position).

Neil Swart, v4, 15/16/2014
Neil.Swart@ec.gc.ca

"""

# set font size
plt.close('all')
plt.ion()
font = {'size'   : 14}
plt.rc('font', **font)

#============================================#
# Define the years for the trend analysis

# Period 1
tys = 1979 # start (inclusive)
tye = 2009 # stop (inclusive)

# Period 2
tys2 = 1951 # start (inclusive)
tye2 = 2011 # stop (inclusive)
#============================================#
#
# Define some global variables that we use repeatedly
#
# the names of the reanalyses we are using (in column-order of the dataframes)
rean     = ['R1', 'R2', '20CR', 'ERA', 'CFSR', 'MERRA']
num_rean = len( rean )
rlc      = [ 'k' , 'y', 'g' , 'b' , 'c' , 'm' ] # corresponding colors to use for plotting each reanalysis
seas     = ['mam', 'jja', 'son', 'djf', 'ann']  # names of the seasons
lensea   = len( seas )
xtics    = [datetime(1870,1,1) + relativedelta(years=20*jj) for jj in range(8) ] # xticks for time-series plot.
#============================================#
# Load the data which is saved in HDF. The data are in pandas dataframes. There is one dataframe for each variable of interest
# (SAM, jet speed = maxpsd, jet position = locmax and jet width. For each variable there is one dataframe for reanalyses and
# one dataframe for the CMIP5 models. With each dataframe the indices (rows) are a datetime index representing the monthly data
# while each column refers to an individual reanalysis or CMIP5 model. The column order of the reanalyses is given in the variable
# rean above. We're not differentiating models by name here.
press, maxspd, locmax, width, modpress, modmaxspd, modlocmax, modwidth = sad.load_sam_df()
#============================================#
# Define some functions
def get_seasons(df):
    """Extract the 4 seasons and the annual mean from dataframe df, and save them as df.djf, df.mam,
    df.jja, df.son and df.ann and then return df. Note December is from the previous year.
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
    """ Limits the dataframe df to between years starting in ys and ending in ye inclusive"""
    dfo = df[ ( df.index.year >= ys ) & ( df.index.year <= ye ) ]
    if ( df.index.year.min() > ys ):
         print 'WARNING: data record begins after requested trend start.' 
    elif ( df.index.year.max() < ye ):
         print 'WARNING: data record ends before requested trend end.', df.index.year.max() 
    return dfo

def modtsplot(df, ax):
    """ For the columns of df, compute the columnwise-ensemble mean and 95% confidence interval, 
    then plot the envelope and mean.
    """
    # compute the ensemble mean across all columns (models).
    ens_mean = df.mean( axis=1 )
    # compute the 95% CI with n -1 degrees of freedom.
    num_models =  len( df.columns )
    ens_std = df.std(axis=1) 
    c = sp.stats.t.isf(0.025, num_models - 1 )
    ts_95_ci = ( c * ens_std ) / np.sqrt( num_models )

    # reample to annual and plot
    ens_mean = ens_mean.resample('A')
    ts_95_ci = ts_95_ci.resample('A')
    ax.fill_between( ens_mean.index , ( ens_mean - ts_95_ci ) ,  ( ens_mean + ts_95_ci),
    color='r', alpha=0.25)  
    ax.plot(ens_mean.index, ens_mean, color='r',linewidth=3 ,label='CMIP5')    
     
def calc_trends( dfp, var, ys , ye ):
    """Calculate linear trend in the dataframe dfp between years (datetime indices) ys and ye inclusive.
    Saves the trend as dfp.slope and calculates and saves the linear prediction (dfp.yhat) for all 
    input years.
    """
    dfp =  year_lim( dfp.resample('A') , ys, ye )              # resample annually
    dfp.slope , conf_int , p_value, yhat, intercept = trend_ts.trend_ts( dfp.index.year , dfp[var] )
    dfp['yhat'] = dfp.slope * dfp.index.year + intercept           # calc yhat values to return
    #print dft.sam_slope*10
    return dfp
                  
def rean_proc(dfr, axts='', axtrend='', tys=0, tye=0):
    """ Loop over the columns of dfr (corresponding to different reanalyses) and:
    1. plot the time-series in axis axts, if axts is given. 
    2. if axtrend is given then compute the linear trend between years tys and 
    tye (inclusive) and plot the trends on axis axtrends. 
    3. Return the trends.
    
    The data from dfr are colored columwise in the plots using colors provided 
    in the global variable rlc, and similarly are labelled using the names listed
    in the global variable rean.
    """

    rean_trends = np.zeros( ( num_rean  , lensea ) )
    dfr.seasons = get_seasons( dfr ) ; # do the seasonal decomposition
    
    # Loop over reanalyses and do some basic dataframe checks and adjustments.
    # We're assuming len(dfr.columns) == len(rean).
    for (i, name) in enumerate( rean ):      
        # check that we are not trying to use data that doesn't exist
        if ( dfr[i+1].dropna().index.year.min() > tys ):
            print name, 'WARNING: start >', str(tys)
        elif ( dfr[i+1].dropna().index.year.max() < tye ):
            print name, 'WARNING: end <', str(tye)

        # If axts was passed, plot the time-series for each column of dfr    
        if ( axts ):  
            axts.plot( dfr.resample('A').index, dfr[i+1].resample('A'), color=rlc[ i ], linewidth=2, alpha=1, label=name)
            axts.xaxis.grid(color=[0.6,0.6,0.6])
            axts.yaxis.grid(color=[0.6,0.6,0.6])
            axts.set_axisbelow(True)
            
        # If axtrend was passed, plot the linear trend between tys and tye for each season and each reanalysis.
        # Season names are listed in the global variable seas.
        if ( axtrend ):
	    for ( k , nm ) in enumerate( seas ):
                names = 'dfr.seasons.' + nm
                mt = calc_trends( eval( names ), i+1, tys , tye )
                rean_trends[ i , k ]  =  mt.slope * 10
                if nm == 'ann':
                    axtrend.plot( k , rean_trends[ i , k ] ,'_', color = rlc[ i ] , ms = 15 , mew = 2, label=rean[i])
                else:
                    axtrend.plot( k , rean_trends[ i , k ] ,'_', color = rlc[ i ] , ms = 15 , mew = 2, label='')

            axtrend.set_xticks( np.arange( lensea + 1 ) )
            axtrend.plot([-1, 5],[0, 0], 'k--')  
    return rean_trends            
	  
def mod_proc(df, axtrend, tys, tye ):
    """ Loop over the columns of df calculate trends for each one, plus plot the ensemble trend stats"""
    num_models =  len( df.columns )
    mod_trends = np.empty( ( num_models  , lensea ) )
    df.seasons = get_seasons(df)

    for i in np.arange( num_models ):  
        for ( k , nm ) in enumerate( seas ):
            names = 'df.seasons.' + nm
            mt = calc_trends( eval( names ), i+1, tys, tye )
            mod_trends[ i , k ] = mt.slope * 10
            
            if i == ( num_models - 1 ):
                mod_trend_mean = np.mean( mod_trends[ : , k ] )
                mod_trend_std =  np.std( mod_trends[ : , k ] )
                c = sp.stats.t.isf(0.025, num_models - 1 )
                mod_95_ci = ( c * mod_trend_std ) / np.sqrt( num_models )
                mod_5thp = np.percentile( mod_trends[ : , k ] , 5 )
                mod_95thp = np.percentile( mod_trends[ : , k ] , 95 )
                axtrend.plot( [ k , k ] , [ mod_5thp  , mod_95thp ],'r', linewidth=4, alpha=0.25 )
                axtrend.plot( [ k , k ] , [ mod_trend_mean - mod_95_ci , mod_trend_mean + mod_95_ci ]\
                  ,'r', linewidth=4 ) 
                if nm == 'ann':
                    axtrend.plot( k , np.mean( mod_trends[ : , k ] ) ,'_r',ms=15,mew=2, label='CMIP5')
                else:
                    axtrend.plot( k , np.mean( mod_trends[ : , k ] ) ,'_r',ms=15,mew=2, label='')    
    return mod_trends                    
                          
#========= SAM - press ===============#

# Set up the figures
f1 = plt.figure(1)
f1.set_size_inches((8,8), forward=True )
f1b = f1.add_subplot(323)
f1c = f1.add_subplot(325)
f1.subplots_adjust(hspace=0.05,right=1.25)

# Set up figure 2
f2 = plt.figure(2)
f2.set_size_inches((8,8), forward=True )
f2b = f2.add_subplot(323)
f2c = f2.add_subplot(325)
f2.subplots_adjust(left=0.2,right=1.4)


#========= Jet max speed - uspd ===============#

# ---- First reanalyses ----
# plot the time-series
trash = rean_proc(maxspd, axts=f1c, tys=tys, tye=tye)

# now do the monthly trends
trash = rean_proc(maxspd, axtrend=f2c, tys=tys, tye=tye)   

 
# ---- Now do the models ----    
# plot the annual mean time-series
modtsplot(modmaxspd, f1c)
f1c.set_ylim( [5 , 10] )

# now do the monthly trends
trash = mod_proc(modmaxspd, f2c, tys=tys, tye=tye)

#========= Location - locmax ===============#

# ---- First reanalyses-------

# plot the time-series
trash = rean_proc(locmax, axts=f1b, tys=tys, tye=tye)

# now do the monthly trends
trash = rean_proc(locmax, axtrend=f2b, tys=tys, tye=tye)   

    
# ---- Now do the models ----    
# plot the annual mean time-series
modtsplot(modlocmax, f1b)

f1b.legend( ncol=1, prop={'size':12}, bbox_to_anchor=(1.25, 1.05),
handlelength=1.25, handletextpad=0.075, frameon=False )

# now do the monthly trends
trash = mod_proc(modlocmax, f2b, tys=tys, tye=tye)

# ========= Do some figure beautifying and labelled etc ========= #

# FIGURE 1: Time-series
# defines some lists of labels.
f1ax = [ f1b, f1c]
yaxlab1 = ['Position ($^{\circ}$S)',
           'Umax (m/s)']

# Loop of figure 1 and label plus adjust subplots.
for i, ax in enumerate( f1ax ):
    ax.set_xticks( xtics )
    ax.set_xlim( [datetime(1880,1,1) , datetime(2013,12,31)] )
    ax.autoscale(enable=True, axis='y', tight=True )
    ylim = ax.get_ylim()
    yrange =  max(ylim) - min(ylim)
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(6) )
    ax.set_ylabel( yaxlab1[i] )

    if (ax != f1c): # only keep xlabels for the bottom panels
        ax.set_xticklabels([])
        ax.set_xlabel('')
    else: 
        plt.setp( ax.xaxis.get_majorticklabels(), rotation=35, ha='right' )
        ax.set_xlabel('Year')
        
# FIGURE 2: Trends
# defines some lists of labels.
f2ax = [ f2b, f2c]
yaxlab = ['Position trend \n($^{\circ}$ lat./dec)'
          , 'Umax trend \n(ms$^{-1}$/dec)']

f2c.set_xticklabels(  [ s.upper() for s in seas]  )

# Loop of figure 2 and label plus adjust subplots.
for i, ax in enumerate( f2ax ):
    ylim = ax.get_ylim()
    yrange =  max(ylim) - min(ylim)
    #ax.text( -0.35, max( ylim ) -0.15*yrange, panlab[i])
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(5) )
    ax.set_xlim([-0.5, lensea -0.5])

    if (ax != f2c): # only keep xlabels for the bottom panels
        ax.set_xticklabels([])
        ax.set_xlabel('')
        
    if i < 3: # only keep ylabels for the left panels
        ax.set_ylabel( yaxlab[i] )
    else:
        plt.setp( ax.get_yticklabels(), visible=False)
        ax.set_ylabel('')     
    
plt.figure(2).subplots_adjust(hspace=0.06, wspace=0.05, right=0.7)
f2b.legend( ncol=1, prop={'size':12}, bbox_to_anchor=(1.35, 1.05),
handlelength=0.01, numpoints=1, handletextpad=1, borderpad=1, frameon=False )
f2.subplots_adjust(left=0.2,right=1.1)

# save some pdfs
plt.figure(1).savefig('sam_pos_str_width_ts_v4_ocw.pdf',format='pdf',dpi=300,
bbox_inches='tight')
plt.figure(2).savefig('sam_pos_str_width_trends_v4_ocw.pdf',format='pdf',dpi=
300,bbox_inches='tight')

