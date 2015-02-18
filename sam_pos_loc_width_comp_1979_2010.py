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

plt.close('all')
plt.ion()
font = {'size'   : 14}
plt.rc('font', **font)

#============================================#
# Define the years for the trend analysis

tys = 1979 # start (inclusive)
tye = 2009 # stop (inclusive)
#============================================#


# Create the Pandas dataframes
print "readfiles"
# Reanalyses
press = pd.read_csv('rean_press_40_65S.txt',names=['date','ind','rno','p40','p65']) # read in
press.date = press.date.apply(lambda d: parse(d) )                           # parse dates

maxspd = pd.read_csv('rean_uspd.txt',names=['date','ind','rno','wspd']) # read in
maxspd.date = maxspd.date.apply(lambda d: parse(d) )  

locmax = pd.read_csv('rean_uloc.txt',names=['date','ind','rno','pos']) # read in
locmax.date = locmax.date.apply(lambda d: parse(d) )  

width = pd.read_csv('rean_uwidth.txt',names=['date','ind','rno','width']) # read in
width.date = width.date.apply(lambda d: parse(d) )  

# Models
modpress = pd.read_csv('/ra40/data/ncs/cmip5/sam/c5_slp/mod_press_40_65S.txt',\
 names=['date','ind','rno','p40','p65']) # read in
modpress.date = modpress.date.apply(lambda d: parse(d) )                           # parse dates
modpress.rno = modpress.rno - 1 # make the model 'labels' start at 1.

modmaxspd = pd.read_csv('/ra40/data/ncs/cmip5/sam/c5_uas/mod_umax.txt',\
 names=['date','ind','rno','wspd']) # read in
modmaxspd.date = modmaxspd.date.apply(lambda d: parse(d) )  
modmaxspd.rno = modmaxspd.rno - 1 # make the model 'labels' start at 1.

modlocmax = pd.read_csv('/ra40/data/ncs/cmip5/sam/c5_uas/mod_uloc.txt',\
 names=['date','ind','rno','pos']) # read in
modlocmax.date = modlocmax.date.apply(lambda d: parse(d) )  
modlocmax.rno = modlocmax.rno - 1 # make the model 'labels' start at 1.

modwidth = pd.read_csv('/ra40/data/ncs/cmip5/sam/c5_uas/mod_uwidth.txt',\
 names=['date','ind','rno','width']) # read in
modwidth.date = modwidth.date.apply(lambda d: parse(d) )  
modwidth.rno = modwidth.rno - 1 # make the model 'labels' start at 1.

print "finished reading files"


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

def loc_trends( dfp, ys , ye ):
    '''Calculate linear trend in the sam of datframe dfp between years ys and ye inclusive'''
    dft =  year_lim( dfp.resample('A') , ys, ye )              # resample annually
    dft.loc_slope , conf_int , p_value, yhat, intercept = trend_ts.trend_ts( dft.index.year , dft.pos )
    dft['yhat_loc'] = dft.loc_slope * dft.index.year + intercept           # calc yhat values to return
    #print dft.wspd_slope*10
    return dft 
    
def width_trends( dfp, ys , ye ):
    '''Calculate linear trend in the sam of datframe dfp between years ys and ye inclusive'''
    dft =  year_lim( dfp.resample('A') , ys, ye )              # resample annually
    dft.width_slope , conf_int , p_value, yhat, intercept = trend_ts.trend_ts( dft.index.year , dft.width )
    dft['yhat_width'] = dft.width_slope * dft.index.year + intercept           # calc yhat values to return
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

def plot_loc_ts( dfp , ys , ye , col='k', mlab='' ):
    ''' Plot time-series of the location for a dataframe, including a linear trend between years
    ys and ye inclusive'''
    # plot up the monthly data lightly in the background
    #dfp.wspd.plot(color='b',linewidth=1,alpha=0.5)
    dfp.resample('A').pos.plot( color = col ,linewidth=3,alpha=1)
    plt.ylabel('Position ($^{\circ}$S)')
    plt.xlabel('Date')
    plt.xlim([dfp.index[0] , dfp.index[-1] ] )

    # plot on the linear trend in red
    dft = loc_trends( dfp , ys, ye)
    #dft.yhat_wspd.plot(color='m',linestyle='-',linewidth=2,label=mlab)
    plt.xlim( [ dfp.index[0] , dfp.index[-1] ] )
    
def plot_width_ts( dfp , ys , ye , col='k', mlab='' ):
    ''' Plot time-series of the location for a dataframe, including a linear trend between years
    ys and ye inclusive'''
    # plot up the monthly data lightly in the background
    #dfp.wspd.plot(color='b',linewidth=1,alpha=0.5)
    dfp.resample('A').width.plot( color = col ,linewidth=3,alpha=1)
    plt.ylabel('Width ($^{\circ}$ lat.)')
    plt.xlabel('Date')
    plt.xlim([dfp.index[0] , dfp.index[-1] ] )

    # plot on the linear trend in red
    dft = width_trends( dfp , ys, ye)
    #dft.yhat_wspd.plot(color='m',linestyle='-',linewidth=2,label=mlab)
    plt.xlim( [ dfp.index[0] , dfp.index[-1] ] )    
    

xtics = [datetime(1870,1,1) + relativedelta(years=10*jj) for jj in range(16) ]
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
        dfr.seasons = get_seasons( dfr ) ;

       # plot the time-series
        plt.figure(num=1,dpi=300)
        plt.figure(1).set_size_inches((10,10), forward=True )
        f1a = plt.subplot( 411 )
        f1a.xaxis.grid(color=[0.6,0.6,0.6])
        f1a.yaxis.grid(color=[0.6,0.6,0.6])
        f1a.set_axisbelow(True)
        ax = plot_sam_ts( dfr , tys , tye , rlc[i], name )

        # Do the monthly trends
        plt.figure(2)
        plt.figure(2).set_size_inches((10,10), forward=True )
        f2a = plt.subplot(421)

        for ( k , nm ) in enumerate( seas ):
            names = 'dfr.seasons.' + nm
            mt = sam_trends( eval( names ), tys , tye )
            print i,k
            rean_trends[ i , k ]  =  mt.sam_slope * 10
            if nm == 'ann':
                plt.plot( k , rean_trends[ i , k ] ,'_', color = rlc[ i ] , ms = 15 , mew = 2, label=rean[i])
            else:
                plt.plot( k , rean_trends[ i , k ] ,'_', color = rlc[ i ] , ms = 15 , mew = 2, label='')

        plt.gca().set_xticks( np.arange( lensea + 1 ) )
        #plt.gca().set_xticklabels( [ l.upper() for l in seas ] )
        plt.gca().set_xticklabels( [] )
        plt.ylabel('SAM trend \n(hPa/dec)')
        plt.axis([-0.5, lensea -0.5 , -0.75, 2])
        plt.plot([-1, 5],[0, 0], 'k--')
        

#---------------------------------------------------------------------------------------------------------
#    Now do the models    plt.ytics([ np.arange(46,55,1))

#---------------------------------------------------------------------------------------------------------

# plot the annual mean time-series
plt.figure(1)
plt.sca( f1a )   
em_press = modpress
em_press.date = em_press.date.apply(lambda d: np.datetime64( datetime( d.year, d.month, 1 ) ) )
em_press['sam'] = ( em_press.p40 - em_press.p65 ) / 100
em_press = em_press.pivot(index='date',columns='rno',values='sam')
ens_mean_sam = em_press.mean( axis=1 )
ens_mean_sam.resample('A').plot(color='r',linewidth=3 ,label='CMIP5')

num_models =  modpress.rno.max()

ens_std_sam = em_press.std( axis=1) 
c = sp.stats.t.isf(0.025, num_models - 1 )
sam_ts_95_ci = ( c * ens_std_sam ) / np.sqrt( num_models )
ens_mean_sam = ens_mean_sam.resample('A')
sam_ts_95_ci = sam_ts_95_ci.resample('A')
plt.fill_between( ens_mean_sam.index , ( ens_mean_sam - sam_ts_95_ci ) ,  ( ens_mean_sam + sam_ts_95_ci),
color='r', alpha=0.25)

f1a.set_xticks( xtics )
f1a.set_xlim( [datetime(1871,1,1) , datetime(2012,12,31)] )
f1a.set_ylim( [18 , 42] )

f1a.legend( loc=2 , ncol=3, prop={'size':12},bbox_to_anchor=(0.1, 1), handlelength=1.25)
f1a.set_xticklabels([])
f1a.set_xlabel('')
f1a.text( datetime(1873,01,01), 39, 'a)')

# now do the monthly trends
plt.sca( f2a )   
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
            c = sp.stats.t.isf(0.025, num_models - 1 )
            mod_95_ci = ( c * mod_trend_std ) / np.sqrt( num_models )
            mod_5thp = np.percentile( mod_trends[ : , k ] , 5 )
            mod_95thp = np.percentile( mod_trends[ : , k ] , 95 )
            plt.plot( [ k , k ] , [ mod_5thp  , mod_95thp ],'r', linewidth=4, alpha=0.25 )
            plt.plot( [ k , k ] , [ mod_trend_mean - mod_95_ci , mod_trend_mean + mod_95_ci ]\
              ,'r', linewidth=4 ) 
            if nm == 'ann':
                plt.plot( k , np.mean( mod_trends[ : , k ] ) ,'_r',ms=15,mew=2, label='CMIP5')
            else:
                plt.plot( k , np.mean( mod_trends[ : , k ] ) ,'_r',ms=15,mew=2, label='')

f2a.legend( ncol=1, prop={'size':12}, bbox_to_anchor=(1.5, 1), handlelength=1)
f2a.text(-0.25,1.65,'a)')

print
print '--------------------------------------'
print 'Speeds:'
print '--------------------------------------'
print

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
 
        dfr.seasons = get_seasons( dfr )
        # Plot the annual mean time-series 
        plt.figure(1)
        f1b = plt.subplot(412)
        f1b.xaxis.grid(color=[0.6,0.6,0.6])
        f1b.yaxis.grid(color=[0.6,0.6,0.6])
        f1b.set_axisbelow(True)
        plot_wspd_ts( dfr , tys , tye , rlc[i] )
 
        plt.figure(2)
        f2b = plt.subplot( 423 )
        for ( k, nm ) in enumerate( seas ):
            names = 'dfr.seasons.' + nm
            mt = wspd_trends( eval( names ), tys , tye )
            rean_spd_trends[ i, k ] = mt.wspd_slope * 10
            plt.plot( k , rean_spd_trends[i,k] , '_', color = rlc[i] , ms=15, mew=2 )

        plt.gca().set_xticks( np.arange(6) )
        plt.gca().set_xticklabels( [ ] )
        plt.ylabel('Umax trend \n (m/s/dec)')
        plt.axis([-0.5, lensea -0.5 , -0.25, 0.5])
        plt.plot([-1, 6],[0, 0], 'k--')

#---------------------------------------------------------------------------------------------
#    Now do the models
#---------------------------------------------------------------------------------------------

# plot the annual mean ts
plt.sca( f1b )   
test1 = modmaxspd
test1.date = test1.date.apply(lambda d: np.datetime64( datetime( d.year, d.month, 1 ) ) )
test = test1.pivot( index = 'date' , columns = 'rno', values = 'wspd' )
ens_mean_umax = test.mean(axis=1)
ens_mean_umax.resample('A').plot( color = 'r' , linewidth=3 )

ens_std_umax = test.std( axis=1) 
c = sp.stats.t.isf(0.025, num_models - 1 )
umax_ts_95_ci = ( c * ens_std_umax ) / np.sqrt( num_models )
ens_mean_umax = ens_mean_umax.resample('A')
umax_ts_95_ci = umax_ts_95_ci.resample('A')
plt.fill_between( ens_mean_umax.index , ( ens_mean_umax - umax_ts_95_ci ) ,  ( ens_mean_umax + umax_ts_95_ci),
color='r', alpha=0.25)


f1b.set_xticklabels( [ str(jj.year) for jj in xtics ],rotation=30)
f1b.set_xticks(xtics)
f1b.set_xlim( [datetime(1871,1,1) , datetime(2012,12,31) ] )

f1b.set_xticklabels([])
f1b.set_xlabel('')
f1b.text( datetime(1873,01,01), 8.85, 'b)')


# now do the monthly trends
plt.sca( f2b )   
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
            c = sp.stats.t.isf(0.025, num_models - 1 )
            mod_95_ci = ( c * mod_trend_std ) / np.sqrt( num_models )
            mod_5thp = np.percentile( mod_wspd_trends[ : , k ] , 5 )
            mod_95thp = np.percentile( mod_wspd_trends[ : , k ] , 95 )
            plt.plot( [ k , k ] , [ mod_5thp  , mod_95thp ],'r', linewidth=4, alpha=0.25 )
            plt.plot( [ k , k ] , [ mod_trend_mean - mod_95_ci , mod_trend_mean + mod_95_ci ]\
              ,'r', linewidth=4 ) 
            plt.plot( k , np.mean( mod_wspd_trends[ : , k ] ) ,'_r', ms=15 , mew=2 )

f2b.text( -0.25,0.4,'b)')

#plt.savefig('sam_jet_trends_1979_2010.pdf',format='pdf',dpi=300,bbox_inches='tight')

print
print '--------------------------------------'
print 'Location:'
print '--------------------------------------'
print

# ---------------------------------------------------------------------------------------------------
#                         Location
# ---------------------------------------------------------------------------------------------------

rean_loc_trends = np.zeros( ( num_rean  , lensea ) )

for (i, name) in enumerate( rean ):
    dfr = locmax[ locmax.rno == i + 1  ] #
    dfr.index = dfr.date                                                        
    dfr = dfr.drop(["date"], axis=1)
    
    if ( dfr.index.year.min() > tys ):
        print name, 'is not being used because start >', str(tys)
    elif ( dfr.index.year.max() < tye ):
        print name, 'is not being used because end <', str(tye)
    else:
 
        dfr.seasons = get_seasons( dfr )
        # Plot the annual mean time-series 
        plt.figure(1)
        f1c = plt.subplot(413)
        f1c.xaxis.grid(color=[0.6,0.6,0.6])
        f1c.yaxis.grid(color=[0.6,0.6,0.6])
        f1c.set_axisbelow(True)
        plot_loc_ts( dfr , tys , tye , rlc[i] )
 
        plt.figure(2)
        f2c = plt.subplot( 425 )
        for ( k, nm ) in enumerate( seas ):
            names = 'dfr.seasons.' + nm
            mt = loc_trends( eval( names ), tys , tye )
            rean_loc_trends[ i, k ] = mt.loc_slope * 10
            plt.plot( k , rean_loc_trends[i,k] , '_', color = rlc[i] , ms=15, mew=2 )

        plt.gca().set_xticks( np.arange(6) )
        plt.gca().set_xticklabels( [ ] )
        plt.ylabel('Position trend \n ($^{\circ}$/dec)')
        plt.axis([-0.5, lensea -0.5 , -1, 1])
        plt.plot([-1, 6],[0, 0], 'k--')

#---------------------------------------------------------------------------------------------
#    Now do the models
#---------------------------------------------------------------------------------------------

# plot the annual mean ts
plt.sca( f1c )   
test1 = modlocmax
test1.date = test1.date.apply(lambda d: np.datetime64( datetime( d.year, d.month, 1 ) ) )
test = test1.pivot( index = 'date' , columns = 'rno', values = 'pos' )
ens_mean_uloc = test.mean(axis=1)
ens_mean_uloc.resample('A').plot( color = 'r' , linewidth=3 )

ens_std_loc = test.std( axis=1) 
c = sp.stats.t.isf(0.025, num_models - 1 )
loc_ts_95_ci = ( c * ens_std_loc ) / np.sqrt( num_models )
ens_mean_loc = ens_mean_uloc.resample('A')
loc_ts_95_ci = loc_ts_95_ci.resample('A')
plt.fill_between( ens_mean_loc.index , ( ens_mean_loc - loc_ts_95_ci ) ,  ( ens_mean_loc + loc_ts_95_ci),
color='r', alpha=0.25)

f1c.set_xticks(xtics)
f1c.set_xlim( [datetime(1871,1,1) , datetime(2012,12,31) ] )
f1c.set_xticklabels([])
f1c.set_xlabel('')

plt.figure(1).subplots_adjust(hspace=0.1)
f1c.yaxis.set_major_locator( mpl.ticker.MaxNLocator(7,prune='upper') )
f1b.yaxis.set_major_locator( mpl.ticker.MaxNLocator(7,prune='upper') )

f1c.text( datetime(1873,01,01), -47.25, 'c)')
f1c.set_yticks( np.arange(-54,-46,2) )

#plt.savefig('sam_pos_str_ts_1979_2010.pdf',format='pdf',dpi=300,bbox_inches='tight')


# now do the monthly trends
plt.sca( f2c )   
num_models =  modlocmax.rno.max()
mod_loc_trends = np.empty( ( num_models , lensea ) )

for i in np.arange( num_models ):
    #print i
    df = modlocmax[ modlocmax.rno == i + 1 ]

    df.index = df.date                                                        
    df = df.drop(["date"], axis=1)
    df.seasons = get_seasons(df)
    
    for (k,nm) in enumerate(seas):
        names = 'df.seasons.' + nm
        mt = loc_trends( eval( names ), tys, tye )
        mod_loc_trends[ i , k ] = mt.loc_slope * 10
        if i == ( num_models - 1 ):
            mod_trend_mean = np.mean( mod_loc_trends[ : , k ] )
            mod_trend_std =  np.std( mod_loc_trends[ : , k ] )
            c = sp.stats.t.isf(0.025, num_models - 1 )
            mod_95_ci = ( c * mod_trend_std ) / np.sqrt( num_models )
            mod_5thp = np.percentile( mod_loc_trends[ : , k ] , 5 )
            mod_95thp = np.percentile( mod_loc_trends[ : , k ] , 95 )
            plt.plot( [ k , k ] , [ mod_5thp  , mod_95thp ],'r', linewidth=4, alpha=0.25 )
            plt.plot( [ k , k ] , [ mod_trend_mean - mod_95_ci , mod_trend_mean + mod_95_ci ]\
              ,'r', linewidth=4 ) 
            plt.plot( k , np.mean( mod_loc_trends[ : , k ] ) ,'_r', ms=15 , mew=2 )


f2b.yaxis.set_major_locator( mpl.ticker.MaxNLocator(6,prune='both') )
f2c.yaxis.set_major_locator( mpl.ticker.MaxNLocator(6,prune='upper') )
plt.figure(2).subplots_adjust(hspace=0.1)
plt.figure(2).subplots_adjust(left=0.2)
plt.figure(2).subplots_adjust(right=0.9)

f2c.text( -0.25,0.75,'c)')

#plt.savefig('sam_pos_str_trends_1979_2010.pdf',format='pdf',dpi=300,bbox_inches='tight')

print
print '--------------------------------------'
print 'Width:'
print '--------------------------------------'
print
# ---------------------------------------------------------------------------------------------------
#                         Width
# ---------------------------------------------------------------------------------------------------

rean_width_trends = np.zeros( ( num_rean  , lensea ) )

for (i, name) in enumerate( rean ):
    dfr = width[ width.rno == i + 1  ] #
    dfr.index = dfr.date                                                        
    dfr = dfr.drop(["date"], axis=1)
    
    if ( dfr.index.year.min() > tys ):
        print name, 'is not being used because start >', str(tys)
    elif ( dfr.index.year.max() < tye ):
        print name, 'is not being used because end <', str(tye)
    else:
 
        dfr.seasons = get_seasons( dfr )
        # Plot the annual mean time-series 
        plt.figure(1)
        f1d = plt.subplot(414)
        f1d.xaxis.grid(color=[0.6,0.6,0.6])
        f1d.yaxis.grid(color=[0.6,0.6,0.6])
        f1d.set_axisbelow(True)
        plot_width_ts( dfr , tys , tye , rlc[i] )
 
        plt.figure(2)
        f2d = plt.subplot( 427 )
        for ( k, nm ) in enumerate( seas ):
            names = 'dfr.seasons.' + nm
            mt = width_trends( eval( names ), tys , tye )
            rean_width_trends[ i, k ] = mt.width_slope * 10
            plt.plot( k , rean_width_trends[i,k] , '_', color = rlc[i] , ms=15, mew=2 )

        plt.gca().set_xticks( np.arange(6) )
        plt.gca().set_xticklabels( [ l.upper() for l in seas ] )
        plt.ylabel('Width trend \n ($^{\circ}$/dec)')
        plt.axis([-0.5, lensea -0.5 , -0.3, 0.3])
        plt.plot([-1, 6],[0, 0], 'k--')

#---------------------------------------------------------------------------------------------
#    Now do the models
#---------------------------------------------------------------------------------------------

# plot the annual mean ts
plt.sca( f1d )   
test1 = modwidth
test1.date = test1.date.apply(lambda d: np.datetime64( datetime( d.year, d.month, 1 ) ) )
test = test1.pivot( index = 'date' , columns = 'rno', values = 'width' )
ens_mean_uwidth = test.mean(axis=1)
ens_mean_uwidth.resample('A').plot( color = 'r' , linewidth=3 )

ens_std_width = test.std( axis=1) 
c = sp.stats.t.isf(0.025, num_models - 1 )
width_ts_95_ci = ( c * ens_std_width ) / np.sqrt( num_models )
ens_mean_width = ens_mean_uwidth.resample('A')
width_ts_95_ci = width_ts_95_ci.resample('A')
plt.fill_between( ens_mean_width.index , ( ens_mean_width - width_ts_95_ci ) ,  ( ens_mean_width + width_ts_95_ci),
color='r', alpha=0.25)

f1d.set_xticklabels( [ str(jj.year) for jj in xtics ],rotation=30)
f1d.set_xticks(xtics)
f1d.set_xlim( [datetime(1871,1,1) , datetime(2012,12,31) ] )

plt.figure(1).subplots_adjust(hspace=0.1)
f1d.yaxis.set_major_locator( mpl.ticker.MaxNLocator(7,prune='upper') )
f1b.yaxis.set_major_locator( mpl.ticker.MaxNLocator(7,prune='upper') )

f1d.text( datetime(1873,01,01), 35.25, 'd)')

plt.savefig('sam_pos_str_width_ts_1979_2010.pdf',format='pdf',dpi=300,bbox_inches='tight')

# now do the monthly trends
plt.sca( f2d )   
num_models =  modwidth.rno.max()
mod_width_trends = np.empty( ( num_models , lensea ) )

for i in np.arange( num_models ):
    #print i
    df = modwidth[ modwidth.rno == i + 1 ]

    df.index = df.date                                                        
    df = df.drop(["date"], axis=1)
    df.seasons = get_seasons(df)
    
    for (k,nm) in enumerate(seas):
        names = 'df.seasons.' + nm
        mt = width_trends( eval( names ), tys, tye )
        mod_width_trends[ i , k ] = mt.width_slope * 10
        if i == ( num_models - 1 ):
            mod_trend_mean = np.mean( mod_width_trends[ : , k ] )
            mod_trend_std =  np.std( mod_width_trends[ : , k ] )
            c = sp.stats.t.isf(0.025, num_models - 1 )
            mod_95_ci = ( c * mod_trend_std ) / np.sqrt( num_models )
            mod_5thp = np.percentile( mod_width_trends[ : , k ] , 5 )
            mod_95thp = np.percentile( mod_width_trends[ : , k ] , 95 )
            plt.plot( [ k , k ] , [ mod_5thp  , mod_95thp ],'r', linewidth=4, alpha=0.25 )
            plt.plot( [ k , k ] , [ mod_trend_mean - mod_95_ci , mod_trend_mean + mod_95_ci ]\
              ,'r', linewidth=4 ) 
            plt.plot( k , np.mean( mod_width_trends[ : , k ] ) ,'_r', ms=15 , mew=2 )


f2b.yaxis.set_major_locator( mpl.ticker.MaxNLocator(6,prune='both') )
f2d.yaxis.set_major_locator( mpl.ticker.MaxNLocator(6,prune='upper') )
plt.figure(2).subplots_adjust(hspace=0.1)
plt.figure(2).subplots_adjust(left=0.2)
plt.figure(2).subplots_adjust(right=0.9)

f2d.text( -0.25,0.2,'d)')

plt.savefig('sam_pos_str_width_trends_1979_2010.pdf',format='pdf',dpi=300,bbox_inches='tight')

print "--------- EOF ------------ "
