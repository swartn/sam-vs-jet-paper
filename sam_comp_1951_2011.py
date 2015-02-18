import numpy as np
import scipy as sp
from scipy import stats
import trend_ts
reload(trend_ts)
#import smooth
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mticker
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from dateutil.parser import parse
plt.close('all')
plt.ion()

#################################
# Define the years for the trend analysis

tys = 1951 # start (inclusive)
tye = 2011 # stop (inclusive)

#################################

# Create the Pandas dataframes

# Reanalyses
press = pd.read_csv('rean_press_40_65S.txt',names=['date','ind','rno','p40','p65']) # read in
press.date = press.date.apply(lambda d: parse(d) )                           # parse dates

maxspd = pd.read_csv('rean_uspd.txt',names=['date','ind','rno','wspd']) # read in
maxspd.date = maxspd.date.apply(lambda d: parse(d) )  

# Models
modpress = pd.read_csv('/ra40/data/ncs/cmip5/sam/c5_slp/mod_press_40_65S.txt',\
 names=['date','ind','rno','p40','p65']) # read in
modpress.date = modpress.date.apply(lambda d: parse(d) )                           # parse dates
modpress.rno = modpress.rno - 1 # make the model 'labels' start at 1.

modmaxspd = pd.read_csv('/ra40/data/ncs/cmip5/sam/c5_uas/mod_umax.txt',\
 names=['date','ind','rno','wspd']) # read in
modmaxspd.date = modmaxspd.date.apply(lambda d: parse(d) )  
modmaxspd.rno = modmaxspd.rno - 1 # make the model 'labels' start at 1.

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
    ''' limits the dataframe df to between years starting in ys and ending in ye inclusive'''
    dfo = df[ ( df.index.year >= ys ) & ( df.index.year <= ye ) ]
    if ( df.index.year.min() > ys ):
         print 'WARNING: data record begins after requested trend start.' 
    elif ( df.index.year.max() < ye ):
         print 'WARNING: data record ends before requested trend end.', df.index.year.max() 
    return dfo

def plot_sam_ts( dfp , ys , ye , col='k', mlab='' ):
    ''' Plot time-series of the sam index for a dataframe, including a linear trend between years
    ys and ye inclusive'''
    # plot up the monthly data lightly in the background
    #ax = dfp.sam.plot(color='b',linewidth=1,alpha=0.5,label='')
    ax = dfp.resample('A').sam.plot( color=col ,linewidth=3,alpha=1,label=mlab)
    plt.ylabel('SAM Index (hPa)')
    plt.xlabel('Date')
    plt.xlim([dfp.index[0] , dfp.index[-1] ] )
    # plot on the linear trend in red
    dft = sam_trends( dfp , ys, ye)
    #dft.yhat.plot(color='m',linestyle='-' , linewidth = 2, label='')
    plt.xlim([dfp.index[0] , dfp.index[-1] ] )
    return ax

def sam_trends( dfp, ys , ye ):
    '''Calculate linear trend in the sam of datframe dfp between years ys and ye inclusive'''
    dft =  year_lim( dfp.resample('A') , ys, ye )              # resample annually
    dft.sam_slope , conf_int , p_value, yhat, intercept = trend_ts.trend_ts( dft.index.year , dft.sam )
    dft['yhat'] = dft.sam_slope * dft.index.year + intercept           # calc yhat values to return
    #print dft.sam_slope*10
    return dft

def wspd_trends( dfp, ys , ye ):
    '''Calculate linear trend in the sam of datframe dfp between years ys and ye inclusive'''
    dft =  year_lim( dfp.resample('A') , ys, ye )              # resample annually
    dft.wspd_slope , conf_int , p_value, yhat, intercept = trend_ts.trend_ts( dft.index.year , dft.wspd )
    dft['yhat_wspd'] = dft.wspd_slope * dft.index.year + intercept           # calc yhat values to return
    #print dft.wspd_slope*10
    return dft

def plot_wspd_ts( dfp , ys , ye , col='k', mlab='' ):
    ''' Plot time-series of the wspd for a dataframe, including a linear trend between years
    ys and ye inclusive'''
    # plot up the monthly data lightly in the background
    #dfp.wspd.plot(color='b',linewidth=1,alpha=0.5)
    dfp.resample('A').wspd.plot( color = col ,linewidth=3,alpha=1)
    plt.ylabel('Umax (m/s)')
    plt.xlabel('Date')
    plt.xlim([dfp.index[0] , dfp.index[-1] ] )

    # plot on the linear trend in red
    dft = wspd_trends( dfp , ys, ye)
    #dft.yhat_wspd.plot(color='m',linestyle='-',linewidth=2,label=mlab)
    plt.xlim( [ dfp.index[0] , dfp.index[-1] ] )

rean = ['R1', 'R2', '20CR', 'ERA', 'CFSR', 'MERRA']
lrean = [ ['20CR'] ]
rlc = [ 'k' , 'y', 'g' , 'b' , 'c' , 'm' ]
plt.hold(True)

seas = ['mam', 'jja', 'son', 'djf', 'ann']
lensea = len( seas )


num_rean =  press.rno.max()
rean_trends = np.zeros( ( num_rean  , lensea ) )

for (i, name) in enumerate( rean ):
    dfr = press[ press.rno == i + 1 ] 
    dfr.index = dfr.date                                                        
    dfr = dfr.drop(["date"], axis=1)
   
    if ( dfr.index.year.min() > tys ):
        print name, 'is not being used because start >', str(tys)
    elif ( dfr.index.year.max() < tye ):
        print name, 'is not being used because end <', str(tye)
    else:
        print name

        dfr['sam'] = ( dfr.p40 - dfr.p65 ) / 100
        dfr.seasons = get_seasons(dfr)

        xtics = [datetime(1870,1,1) + relativedelta(years=10*jj) for jj in range(16) ]
        # plot the time-series
        plt.figure(1)
        f1upper = plt.subplot(211)
        f1upper.xaxis.grid(color=[0.6,0.6,0.6])
        f1upper.yaxis.grid(color=[0.6,0.6,0.6])
        f1upper.set_axisbelow(True)
        ax = plot_sam_ts( dfr , tys , tye , rlc[i], name )

        
        # Do the monthly trends
        plt.figure(2)
        f2upper = plt.subplot(221)

        for ( k , nm ) in enumerate( seas ):
            names = 'dfr.seasons.' + nm
            mt = sam_trends( eval( names ), tys , tye )
            print i,k
            rean_trends[ i , k ]  =  mt.sam_slope * 10
            plt.plot( k , rean_trends[ i , k ] ,'_', color = rlc[ i ] , ms = 15 , mew = 2 )

        plt.gca().set_xticks( np.arange( lensea + 1 ) )
        #plt.gca().set_xticklabels( [ l.upper() for l in seas ] )
        plt.gca().set_xticklabels( [] )
        plt.ylabel('SAM trend (hPa/dec)')
        plt.axis([-0.5, lensea -0.5 , -0.5, 2.5])
        plt.plot([-1, 5],[0, 0], 'k--')

#---------------------------------------------------------------------------------------------------------
#    Now do the models
#---------------------------------------------------------------------------------------------------------

# plot the annual mean time-series
plt.figure(1)
plt.sca( f1upper )   
em_press = modpress
em_press.date = em_press.date.apply(lambda d: np.datetime64( datetime( d.year, d.month, 1 ) ) )
em_press['sam'] = ( em_press.p40 - em_press.p65 ) / 100
em_press = em_press.pivot(index='date',columns='rno',values='sam')
ens_mean_sam = em_press.mean( axis=1 )
ens_mean_sam.resample('A').plot(color='r',linewidth=3 ,label='CMIP5')

f1upper.legend( loc=2 , ncol=2 )
f1upper.set_xticks( xtics )
f1upper.set_xlim( [datetime(1871,1,1) , datetime(2012,12,31)] )
f1upper.set_xticklabels([])
f1upper.set_xlabel('')

# now do the monthly trends
plt.sca( f2upper )   
num_models =  modpress.rno.max()
mod_trends = np.empty( ( num_models  , lensea ) )

for i in np.arange( num_models ):
    df = modpress[ modpress.rno == i + 1 ]
    #print i+1
    df.index = df.date                                                        
    df = df.drop(["date"], axis=1)
    df['sam'] = ( df.p40 - df.p65 ) / 100
    df.seasons = get_seasons(df)

    
    for ( k , nm ) in enumerate( seas ):
        names = 'df.seasons.' + nm
        mt = sam_trends( eval( names ), tys, tye )
        mod_trends[ i , k ] = mt.sam_slope * 10
        if i == ( modpress.rno.max() - 1 ):
            mod_trend_mean = np.mean( mod_trends[ : , k ] )
            mod_trend_std =  np.std( mod_trends[ : , k ] )
            c = stats.t.isf(0.025, num_models - 1 )
            mod_95_ci = ( c * mod_trend_std ) / np.sqrt( num_models )
            mod_5thp = np.percentile( mod_trends[ : , k ] , 5 )
            mod_95thp = np.percentile( mod_trends[ : , k ] , 95 )
            plt.plot( [ k , k ] , [ mod_5thp  , mod_95thp ],'r', linewidth=4, alpha=0.25 )
            plt.plot( [ k , k ] , [ mod_trend_mean - mod_95_ci , mod_trend_mean + mod_95_ci ]\
              ,'r', linewidth=4 ) 
            plt.plot( k , np.mean( mod_trends[ : , k ] ) ,'_r',ms=15,mew=2 )
    
# ---------------------------------------------------------------------------------------------------
#                         SPEEDS
# ---------------------------------------------------------------------------------------------------

rean_spd_trends = np.zeros( ( num_rean  , lensea ) )

for (i, name) in enumerate( rean ):
    dfr = maxspd[ maxspd.rno == i + 1  ] #
    dfr.index = dfr.date                                                        
    dfr = dfr.drop(["date"], axis=1)
    
    if ( dfr.index.year.min() > tys ):
        print name, 'is not being used because start >', str(tys)
    elif ( dfr.index.year.max() < tye ):
        print name, 'is not being used because end <', str(tye)
    else:
        print name
        dfr.seasons = get_seasons( dfr )
        # Plot the annual mean time-series 
        plt.figure(1)
        f1lower = plt.subplot(212)
        f1lower.xaxis.grid(color=[0.6,0.6,0.6])
        f1lower.yaxis.grid(color=[0.6,0.6,0.6])
        f1lower.set_axisbelow(True)
        plot_wspd_ts( dfr , tys , tye , rlc[i] )
 
        plt.figure(2)
        f2lower = plt.subplot( 223 )
        for ( k, nm ) in enumerate( seas ):
            names = 'dfr.seasons.' + nm
            mt = wspd_trends( eval( names ), tys , tye )
            rean_spd_trends[ i, k ] = mt.wspd_slope * 10
            plt.plot( k , rean_spd_trends[i,k] , '_', color = rlc[i] , ms=15, mew=2 )
        
        #print name, rean_spd_trends[i,:]
        plt.gca().set_xticks( np.arange(6) )
        plt.gca().set_xticklabels( [ l.upper() for l in seas ] )
        plt.ylabel('Umax trend (m/s/dec)')
        plt.axis([-0.5, lensea -0.5 , -0.25, 0.5])
        plt.plot([-1, 6],[0, 0], 'k--')

#---------------------------------------------------------------------------------------------------------
#    Now do the models
#---------------------------------------------------------------------------------------------------------

# plot the annual mean ts
plt.sca( f1lower )   
test1 = modmaxspd
test1.date = test1.date.apply(lambda d: np.datetime64( datetime( d.year, d.month, 1 ) ) )
test = test1.pivot( index = 'date' , columns = 'rno', values = 'wspd' )
ens_mean_umax = test.mean(axis=1)
ens_mean_umax.resample('A').plot( color = 'r' , linewidth=3 )

f1lower.set_xticklabels( [ str(jj.year) for jj in xtics ],rotation=30)
f1lower.set_xticks(xtics)
f1lower.set_xlim( [datetime(1871,1,1) , datetime(2012,12,31) ] )
plt.savefig('sam_jet_ts_1951_2011.pdf',format='pdf',dpi=300,bbox_inches='tight')


# now do the monthly trends
plt.sca( f2lower )   
num_models =  modmaxspd.rno.max()
mod_wspd_trends = np.empty( ( num_models , lensea ) )

for i in np.arange( num_models ):
    #print i
    df = modmaxspd[ modmaxspd.rno == i + 1 ]

    df.index = df.date                                                        
    df = df.drop(["date"], axis=1)
    df.seasons = get_seasons(df)
    
    for (k,nm) in enumerate(seas):
        names = 'df.seasons.' + nm
        mt = wspd_trends( eval( names ), tys, tye )
        mod_wspd_trends[ i , k ] = mt.wspd_slope * 10
        if i == ( num_models - 1 ):
            mod_trend_mean = np.mean( mod_wspd_trends[ : , k ] )
            mod_trend_std =  np.std( mod_wspd_trends[ : , k ] )
            c = stats.t.isf(0.025, num_models - 1 )
            mod_95_ci = ( c * mod_trend_std ) / np.sqrt( num_models )
            mod_5thp = np.percentile( mod_wspd_trends[ : , k ] , 5 )
            mod_95thp = np.percentile( mod_wspd_trends[ : , k ] , 95 )
            plt.plot( [ k , k ] , [ mod_5thp  , mod_95thp ],'r', linewidth=4, alpha=0.25 )
            plt.plot( [ k , k ] , [ mod_trend_mean - mod_95_ci , mod_trend_mean + mod_95_ci ]\
              ,'r', linewidth=4 ) 
            plt.plot( k , np.mean( mod_wspd_trends[ : , k ] ) ,'_r', ms=15 , mew=2 )

plt.savefig('sam_jet_trends_1951_2011.pdf',format='pdf',dpi=300,bbox_inches='tight')

# ---------------------------------------------------------------------------------------------------
#                        Do SAM vs SPEED trend plots
# ---------------------------------------------------------------------------------------------------

rean_trends[ rean_trends == 0.0 ] = np.nan
rean_spd_trends[ rean_spd_trends == 0.0 ] = np.nan

#gs = gridspec.GridSpec(3, 2 )
f, gs2 = plt.subplots(3,2, sharex=True, sharey=True)
f.delaxes(gs2[0,1])
maxis = [-0.75, 2.5, -0.25, 0.5]
plt.axis(maxis)
rat = ( maxis[1] - maxis[0] ) / ( maxis[3] - maxis[2] )
plt.setp(gs2.flat, aspect = rat, adjustable='box-forced')
f.subplots_adjust( hspace=0.15, wspace = -0.6)
gs2[2,1].xaxis.set_major_locator( mticker.MaxNLocator(6, prune='both'))
gs2[2,1].yaxis.set_major_locator( mticker.MaxNLocator(6, prune='both'))


def relp( xs , ys ):
    svj_slope , conf_int , p_value, svj_yhat, svj_intercept =\
        trend_ts.trend_ts( xs  , ys )

    xvals = np.arange( np.min( xs ) - np.max( xs )*5.  ,\
         np.max( xs )*5.  )
    ypred = xvals * svj_slope + svj_intercept
    plt.plot( xs , ys , 'ro')
    plt.plot( xvals , ypred , 'r--' )

def reanp( xs , ys):
    print xs,ys
    [ plt.plot( xs[i] , ys[i] , 'x', color=rlc[ int(i) ],\
       markersize=10,markeredgewidth=3) for i in range( xs.shape[0] ) ]

# Annual
plt.sca( gs2[0,0] )
relp(  mod_trends[ : , 4 ] ,  mod_wspd_trends[ : , 4 ] )
reanp( rean_trends[ : , 4 ] , rean_spd_trends[ : , 4 ] )

# MAM
plt.sca( gs2[1,0] )
relp(  mod_trends[ : , 0 ] ,  mod_wspd_trends[ : , 0 ] )
reanp( rean_trends[ : , 0 ] , rean_spd_trends[ : , 0 ] )
gs2[1,0].set_ylabel('Umax trend (ms$^{-1}$/dec)')

#JJA
plt.sca( gs2[1,1] )
relp(  mod_trends[ : , 1 ] ,  mod_wspd_trends[ : , 1 ] )
reanp( rean_trends[ : , 1 ] , rean_spd_trends[ : , 1 ] )

#SON
plt.sca( gs2[2,0] )
relp(  mod_trends[ : , 2 ] ,  mod_wspd_trends[ : , 2 ] )
reanp( rean_trends[ : , 2 ] , rean_spd_trends[ : , 2 ] )

#DJF
plt.sca( gs2[2,1] )
relp(  mod_trends[ : , 3 ] ,  mod_wspd_trends[ : , 3 ] )
reanp( rean_trends[ : , 3 ] , rean_spd_trends[ : , 3 ] )

seas_label = [ ['ann', '' ] , ['mam','jja'] , ['son', 'djf'] ]
plt.text( maxis[0] -maxis[1],maxis[2]*1.7  , 'SAM trend (hPa/dec)')
[ gs2[m,n].text(-0.4,0.4, seas_label[m][n].upper() ) for m in range(3) for n in range(2)  ]
plt.draw()

plt.savefig('sam_v_jet_1951_2011.pdf',format='pdf',dpi=300,bbox_inches='tight')


print
print 'Rean. vs Mod mean trend:'
print
print 'SAM'
print  rean_trends[ 2 , 4 ] / np.mean( mod_trends[ : , 4 ] )
print
print 'Speed'
print   rean_spd_trends[ 2 , 4 ] / np.mean( mod_wspd_trends[ : , 4 ] )
