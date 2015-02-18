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

plt.close('all')
plt.ion()
font = {'size'   : 12}
plt.rc('font', **font)

#============================================#
# Define the years for the trend analysis

tys = 1979 # start (inclusive)
tye = 2009 # stop (inclusive)

tys2 = 1951 # start (inclusive)
tye2 = 2009 # stop (inclusive)
#============================================#

press, maxspd, locmax, width, modpress, modmaxspd, modlocmax, modwidth = sad.load_sam_df()

# Define some functions
def get_seasons(df):
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
    """limits the dataframe df to between years starting in ys and ending in ye inclusive"""
    dfo = df[ ( df.index.year >= ys ) & ( df.index.year <= ye ) ]
    if ( df.index.year.min() > ys ):
         print 'WARNING: data record begins after requested trend start.' 
    elif ( df.index.year.max() < ye ):
         print 'WARNING: data record ends before requested trend end.', df.index.year.max() 
    return dfo

def modtsplot(df, ax):
    """ For the columns of df, compute the ensemble mean and 95% CI, plot the envelope and mean"""
    # compute the ensemble mean 
    ens_mean = df.mean( axis=1 )

    # compute the 95% CI 
    num_models =  len( df.columns )
    ens_std = df.std( axis=1) 
    c = sp.stats.t.isf(0.025, num_models - 1 )
    ts_95_ci = ( c * ens_std ) / np.sqrt( num_models )

    # reample to annual and plot
    ens_mean = ens_mean.resample('A')
    ts_95_ci = ts_95_ci.resample('A')
    ax.fill_between( ens_mean.index , ( ens_mean - ts_95_ci ) ,  ( ens_mean + ts_95_ci),
    color='r', alpha=0.25)  
    ax.plot(ens_mean.index, ens_mean, color='r',linewidth=3 ,label='CMIP5')    
     
def calc_trends( dfp, var, ys , ye ):
    '''Calculate linear trend in the sam of datframe dfp between years ys and ye inclusive'''
    dfp =  year_lim( dfp.resample('A') , ys, ye )              # resample annually
    dfp.slope , conf_int , p_value, yhat, intercept = trend_ts.trend_ts( dfp.index.year , dfp[var] )
    dfp['yhat'] = dfp.slope * dfp.index.year + intercept           # calc yhat values to return
    #print dft.sam_slope*10
    return dfp
                  
def rean_proc(dfr, axts='', axtrend='', tys=0, tye=0):
    """ Loop over the reanalysis and do 1. time-series and 2. trends"""

    rean_trends = np.zeros( ( num_rean  , lensea ) )
    dfr.seasons = get_seasons( dfr ) ; # do the seasonal decomposition
    
    # Loop over reanalyses and do some basic dataframe checks and adjustments
    for (i, name) in enumerate( rean ):      
        # check that we are not trying to use data that doesn't exist
        if ( dfr[i+1].dropna().index.year.min() > tys ):
            print name, 'WARNING: start >', str(tys)
        elif ( dfr[i+1].dropna().index.year.max() < tye ):
            print name, 'WARNING: end <', str(tye)

        # If axts was passed, plot the time-series of var    
        if ( axts ):  
            axts.plot( dfr.resample('A').index, dfr[i+1].resample('A'), color=rlc[ i ], linewidth=2, alpha=1, label=name)
            axts.xaxis.grid(color=[0.6,0.6,0.6])
            axts.yaxis.grid(color=[0.6,0.6,0.6])
            axts.set_axisbelow(True)
            
        # If axtrend was passed, plot the trends in var    
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
        
xtics = [datetime(1870,1,1) + relativedelta(years=20*jj) for jj in range(8) ]
rean = ['R1', 'R2', '20CR', 'ERA', 'CFSR', 'MERRA']
lrean = [ ['20CR'] ]
rlc = [ 'k' , 'y', 'g' , 'b' , 'c' , 'm' ]

seas = ['mam', 'jja', 'son', 'djf', 'ann']
lensea = len( seas )

num_rean =  len(press.columns)
rean_trends = np.zeros( ( num_rean  , lensea ) )


#========= SAM ===============#

# ---- First reanalyses-------

# plot the time-series
# Set up the two figures
f1 = plt.figure(1)
plt.figure(1).set_size_inches((8,8), forward=True )
f1a = plt.subplot( 421 )
rean_proc(press, axts=f1a, tys=tys, tye=tye)

f2 = plt.figure(2)
plt.figure(2).set_size_inches((8,8), forward=True )
# Do the monthly trends
f2a = plt.subplot(421)
rean_proc(press, axtrend=f2a, tys=tys2, tye=tye2)   

f2e = plt.subplot(422, sharey=f2a)
rean_proc(press, axtrend=f2e, tys=tys, tye=tye)   
     
#---------------------------------------------------------------
#    Now do the models   

#-------------------------------------------------------------

# plot the annual mean time-series

modtsplot(modpress, f1a)
f1a.set_ylim( [18 , 42] )
f1a.legend( ncol=1, prop={'size':12}, bbox_to_anchor=(1.4, 1.05), handlelength=1.25, handletextpad=0.075 )

# now do the monthly trends
mod_proc(modpress, f2a, tys=tys, tye=tye2)
mod_proc(modpress, f2e, tys=tys, tye=tye)


# ------------------------------------------------------------
#                         SPEEDS
# ------------------------------------------------------------

# ---- First reanalyses-------

# plot the time-series
plt.figure(1)
f1b = plt.subplot( 423 )
rean_proc(maxspd, axts=f1b, tys=tys, tye=tye)

plt.figure(2)
f2b = plt.subplot(423)
rean_proc(maxspd, axtrend=f2b, tys=tys2, tye=tye2)   

f2f = plt.subplot(424, sharey=f2b)
rean_proc(maxspd, axtrend=f2f, tys=tys, tye=tye)       
#---------------------------------------------------------------
#    Now do the models   

#-------------------------------------------------------------

# plot the annual mean time-series
modtsplot(modmaxspd, f1b)
f1b.set_ylim( [5 , 10] )

# now do the monthly trends
mod_proc(modmaxspd, f2b, tys=tys2, tye=tye2)
mod_proc(modmaxspd, f2f, tys=tys, tye=tye)

# ------------------------------------------------------------
#                         Location
# ------------------------------------------------------------

# ---- First reanalyses-------

# plot the time-series
plt.figure(1)
f1c = plt.subplot( 425 )
rean_proc(locmax, axts=f1c, tys=tys, tye=tye)

plt.figure(2)
f2c = plt.subplot(425)
rean_proc(locmax, axtrend=f2c, tys=tys2, tye=tye2)   

f2g = plt.subplot(426, sharey=f2c)
rean_proc(locmax, axtrend=f2g, tys=tys, tye=tye)   
     
#---------------------------------------------------------------
#    Now do the models   

#-------------------------------------------------------------

# plot the annual mean time-series
modtsplot(modlocmax, f1c)

# now do the monthly trends
mod_proc(modlocmax, f2c, tys=tys2, tye=tye2)
mod_proc(modlocmax, f2g, tys=tys, tye=tye)

# ------------------------------------------------------------
#                         Width
# ------------------------------------------------------------

# ---- First reanalyses-------

# plot the time-series
plt.figure(1)
f1d = plt.subplot( 427 )
rean_proc(width, axts=f1d, tys=tys, tye=tye)

plt.figure(2)
f2d = plt.subplot(427)
rean_proc(width, axtrend=f2d, tys=tys2, tye=tye2)   

f2h = plt.subplot(428, sharey=f2d)
rean_proc(width, axtrend=f2h, tys=tys, tye=tye)      
#---------------------------------------------------------------
#    Now do the models   

#-------------------------------------------------------------

# plot the annual mean time-series
modtsplot(modwidth, f1d)
# now do the monthly trends
mod_proc(modwidth, f2d, tys=tys2, tye=tye2)
f2d.set_xticklabels(  [ s.upper() for s in seas]  )
mod_proc(modwidth, f2h, tys=tys, tye=tye)
f2h.set_xticklabels(  [ s.upper() for s in seas]  )

# Do some figure beautifying and labelled etc
f1ax = [ f1a, f1b, f1c, f1d ]
panlab = ['a)', 'b)', 'c)', 'd)', 'e)', 'f)' ,'g)', 'h)']
yaxlab = ['SAM Index (hPa)' , 'Umax (m/s)','Position ($^{\circ}$S)', 'Width ($^{\circ}$ lat.)']

for i, ax in enumerate( f1ax ):
    ax.set_xticks( xtics )
    ax.set_xlim( [datetime(1880,1,1) , datetime(2013,12,31)] )
    ax.autoscale(enable=True, axis='y', tight=True )
    ylim = ax.get_ylim()
    yrange =  max(ylim) - min(ylim)
    ax.text( datetime(1885,1,1), max( ylim ) -0.15*yrange, panlab[i])
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(6) )
    ax.set_ylabel( yaxlab[i] )

    if (ax != f1d): 
        ax.set_xticklabels([])
        ax.set_xlabel('')
    else: 
        plt.setp( ax.xaxis.get_majorticklabels(), rotation=35, ha='right' )
        ax.set_xlabel('Year')
        
plt.figure(1).subplots_adjust(hspace=0.05)
 
f2ax = [ f2a, f2b, f2c, f2d, f2e, f2f, f2g, f2h]
yaxlab = ['SAM trend \n(hPa/dec)', 'Umax trend \n(ms$^{-1}$/dec)', 'Position trend \n($^{\circ}$ lat./dec)', 'Width trend \n($^{\circ}$ lat./dec)' ]
for i, ax in enumerate( f2ax ):
    ylim = ax.get_ylim()
    yrange =  max(ylim) - min(ylim)
    ax.text( -0.35, max( ylim ) -0.15*yrange, panlab[i])
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(5) )
    ax.set_xlim([-0.5, lensea -0.5])

    if (ax != f2d) & (ax != f2h): 
        ax.set_xticklabels([])
        ax.set_xlabel('')
        
    if i <= 3:
        ax.set_ylabel( yaxlab[i] )
    else:
        plt.setp( ax.get_yticklabels(), visible=False)
        ax.set_ylabel('')     
    

plt.figure(2).subplots_adjust(hspace=0.05, wspace=0.05, right=0.7)
f2e.legend( ncol=1, prop={'size':12}, bbox_to_anchor=(1.6, 1.05), handlelength=0.01, handletextpad=1, borderpad=1 )
f2a.set_title(  str(tys2) + '-' + str(tye2)  )
f2e.set_title(str(tys) + '-' + str(tye) )

plt.figure(1).savefig('sam_pos_str_width_ts_v3.pdf',format='pdf',dpi=300,bbox_inches='tight')
plt.figure(2).savefig('sam_pos_str_width_trends_v3.pdf',format='pdf',dpi=300,bbox_inches='tight')

print "--------- EOF ------------ "