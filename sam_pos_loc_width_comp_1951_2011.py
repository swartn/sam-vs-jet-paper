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

This script produces 4 plots:

1. Time-series of SAM and jet strength, position, and width in the models and reananlyses.
2. Trends in the above variables over two-different periods (1951-2011 and 1979-2009).
3. The relationship between SAM and strength trends.
4. The relationship between SAM and trends in the other variables, as well as trends in
SAM and the climatology of the variables. (e.g. SAM trend vs climatological jet position).

# v5 separates the plot of trends over the two different periods.

Neil Swart, v4, 15/16/2014
Neil.Swart@ec.gc.ca

"""

# set font size
plt.close('all')
plt.ion()
font = {'size'   : 12}
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
press, maxspd, locmax, width, modpress, modmaxspd, modlocmax, modwidth =\
                      sad.load_sam_df()

# load in the Marshall SAM data
dfmarshall = pd.read_csv('/HOME/ncs/data/marshall_sam/marshall_sam.csv', 
		  index_col=0, parse_dates=True)

# load the reanalysis data
# load in the reanlaysis data
h5f = pd.HDFStore('/raid/ra40/data/ncs/cmip5/sam/rean_sam.h5', 'a')
dfr = h5f['zonmean_sam/df']
h5f.close()
dfhadslp = dfr['HadSLP2r']/100.
dfhadslp = pd.DataFrame(dfhadslp.ix['sam'].dropna(), columns=['HadSLP2r'])

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
    color='r', alpha=0.25, linewidth=0)  
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
    for (i, cn) in enumerate( dfr.columns ):      
        # check that we are not trying to use data that doesn't exist
        if ( dfr[cn].dropna().index.year.min() > tys ):
            print rean[i], 'WARNING: start >', str(tys)
        elif ( dfr[cn].dropna().index.year.max() < tye ):
            print rean[i], 'WARNING: end <', str(tye)

        # If axts was passed, plot the time-series for each column of dfr    
        if ( axts ):  
            axts.plot( dfr.resample('A').index, dfr[cn].resample('A'), 
		      color=rlc[ i ], linewidth=2, alpha=1, label=rean[i])
            #axts.xaxis.grid(color=[0.6,0.6,0.6])
            #axts.yaxis.grid(color=[0.6,0.6,0.6])
            axts.set_axisbelow(True)
            
        # If axtrend was passed, plot the linear trend between tys and tye for each season and each reanalysis.
        # Season names are listed in the global variable seas.
        if ( axtrend ):
	    for ( k , nm ) in enumerate( seas ):
                names = 'dfr.seasons.' + nm
                mt = calc_trends( eval( names ), cn, tys , tye )
                rean_trends[i, k]  =  mt.slope * 10
                #############################33
                # Set R1 trends to NAN so we dont see it
                rean_trends[0, :] = np.nan
                #################################                
                if (nm == 'ann') & ( not np.isnan(rean_trends[i, k])):
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
plt.figure(1).set_size_inches((8,8), forward=True )
f1a = plt.subplot( 421 )

# ---- First reanalyses ----
# plot the time-series
rean_proc(press, axts=f1a, tys=tys, tye=tye)

# Set up figure 2
f2 = plt.figure(2)
plt.figure(2).set_size_inches((8,8), forward=True )

# Do the monthly trends
f2a = plt.subplot(421)
trash = rean_proc(press, axtrend=f2a, tys=tys, tye=tye)   

# Set up figure 3*
f3 = plt.figure(3)
plt.figure(3).set_size_inches((8,8), forward=True )

# Do the monthly trends for period 2
plt.figure(3)
f3a = plt.subplot(421)
sam_trends = rean_proc(press, axtrend=f3a, tys=tys2, tye=tye2)   
rean=['HadSLP2r']
rlc = ['k']
num_rean = 1 
hadslp_sam_trends = rean_proc(dfhadslp, axtrend=f3a, tys=tys2, tye=tye2)   
rean     = ['R1', 'R2', '20CR', 'ERA', 'CFSR', 'MERRA']
num_rean = len( rean )
rlc      = [ 'k' , 'y', 'g' , 'b' , 'c' , 'm' ]    
 
# ---- Now do the models ----    
# plot the annual mean time-series
modtsplot(modpress, f1a)
f1a.set_ylim( [18 , 42] )
dfmarshall['sam'].resample('A').plot(ax=f1a, color='0.5', style='-', 
             linewidth=2, grid=False, label='Marshall', zorder=1)
#dfhadslp['sam'].resample('A').plot(ax=f1a, color='g', style='--', 
             #linewidth=3, grid=False, label='HadSLP2r')

f1a.legend( ncol=1, prop={'size':12}, bbox_to_anchor=(1.45, 1.05),
            handlelength=2, handletextpad=0.075, frameon=False )

# now do the monthly trends
trash = mod_proc(modpress, f2a, tys=tys, tye=tye)
mod_sam_trends = mod_proc(modpress, f3a, tys=tys2, tye=tye2)

#========= Jet max speed - uspd ===============#

# ---- First reanalyses ----
# plot the time-series
plt.figure(1)
f1b = plt.subplot( 423 )
trash = rean_proc(maxspd, axts=f1b, tys=tys, tye=tye)

# now do the monthly trends
plt.figure(2)
f2b = plt.subplot(423)
trash = rean_proc(maxspd, axtrend=f2b, tys=tys, tye=tye)   

plt.figure(3)
f3b = plt.subplot(423)
uspd_trends = rean_proc(maxspd, axtrend=f3b, tys=tys2, tye=tye2)       
# ---- Now do the models ----    
# plot the annual mean time-series
modtsplot(modmaxspd, f1b)
f1b.set_ylim( [5 , 10] )

# now do the monthly trends
trash = mod_proc(modmaxspd, f2b, tys=tys, tye=tye)
mod_uspd_trends = mod_proc(modmaxspd, f3b, tys=tys2, tye=tye2)

#========= Location - locmax ===============#

# ---- First reanalyses-------

# plot the time-series
plt.figure(1)
f1c = plt.subplot( 425 )
trash = rean_proc(locmax, axts=f1c, tys=tys, tye=tye)

# now do the monthly trends
plt.figure(2)
f2c = plt.subplot(425)
trash = rean_proc(locmax, axtrend=f2c, tys=tys, tye=tye)   

plt.figure(3)
f3c = plt.subplot(425)
pos_trends = rean_proc(locmax, axtrend=f3c, tys=tys2, tye=tye2)   
     
# ---- Now do the models ----    
# plot the annual mean time-series
modtsplot(modlocmax, f1c)

# now do the monthly trends
trash = mod_proc(modlocmax, f2c, tys=tys, tye=tye)
mod_pos_trends = mod_proc(modlocmax, f3c, tys=tys2, tye=tye2)


#========= Width ===============#

# ---- First reanalyses-------

# plot the time-series
plt.figure(1)
f1d = plt.subplot( 427 )
trash = rean_proc(width, axts=f1d, tys=tys, tye=tye)

# now do the monthly trends
plt.figure(2)
f2d = plt.subplot(427)
trash = rean_proc(width, axtrend=f2d, tys=tys, tye=tye)   

plt.figure(3)
f3d = plt.subplot(427)
width_trends = rean_proc(width, axtrend=f3d, tys=tys2, tye=tye2)      

# ---- Now do the models ----    
# plot the annual mean time-series
modtsplot(modwidth, f1d)
# now do the monthly trends
trash = mod_proc(modwidth, f2d, tys=tys, tye=tye)
mod_width_trends = mod_proc(modwidth, f3d, tys=tys2, tye=tye2)

f2d.set_xticklabels(  [ s.upper() for s in seas]  )
f3d.set_xticklabels(  [ s.upper() for s in seas]  )

# ========= Do some figure beautifying and labelled etc ========= #

# FIGURE 1: Time-series
# defines some lists of labels.
f1ax = [ f1a, f1b, f1c, f1d ]
panlab = ['a)', 'b)', 'c)', 'd)', 'e)', 'f)' ,'g)', 'h)']
yaxlab1 = ['SAM Index (hPa)' , 'Umax (m/s)','Position ($^{\circ}$S)', 'Width ($^{\circ}$ lat.)']

# Loop of figure 1 and label plus adjust subplots.
for i, ax in enumerate( f1ax ):
    ax.set_xticks( xtics )
    ax.set_xlim( [datetime(1880,1,1) , datetime(2013,12,31)] )
    ax.autoscale(enable=True, axis='y', tight=True )
    ylim = ax.get_ylim()
    yrange =  max(ylim) - min(ylim)
    ax.text( datetime(1885,1,1), max( ylim ) -0.15*yrange, panlab[i])
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(6) )
    ax.set_ylabel( yaxlab1[i] )

    if (ax != f1d): # only keep xlabels for the bottom panels
        ax.set_xticklabels([])
        ax.set_xlabel('')
    else: 
        plt.setp( ax.xaxis.get_majorticklabels(), rotation=35, ha='right' )
        ax.set_xlabel('Year')
        
plt.figure(1).subplots_adjust(hspace=0.05)

# FIGURE 2: Trends
# defines some lists of labels.
f2ax = [ f2a, f2b, f2c, f2d]
f3ax = [ f3a, f3b, f3c, f3d]

yaxlab = ['SAM trend \n(hPa/dec)', 
          'Umax trend \n(ms$^{-1}$/dec)', 
          'Position trend \n($^{\circ}$ lat./dec)', 
          'Width trend \n($^{\circ}$ lat./dec)' ]
          
# Loop of figure 2 and label plus adjust subplots.
for i, ax in enumerate( f2ax ):
    ylim = ax.get_ylim()
    yrange =  max(ylim) - min(ylim)
    ax.text( -0.35, max( ylim ) -0.15*yrange, panlab[i])
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(5) )
    ax.set_xlim([-0.5, lensea -0.5])

    if (ax != f2d): # only keep xlabels for the bottom panels
        ax.set_xticklabels([])
        ax.set_xlabel('')
        
    ax.set_ylabel( yaxlab[i] )
  
    
plt.figure(2).subplots_adjust(hspace=0.06, wspace=0.05, right=0.7)
f2a.legend(ncol=1, prop={'size':12},numpoints=1, bbox_to_anchor=(1.5, 1.05),
           handlelength=0.01, handletextpad=1, borderpad=1, frameon=False )

# Title trend panels with the start and end year of the trends
f2a.set_title(  str(tys) + '-' + str(tye)  )

# Loop of figure 2 and label plus adjust subplots.
for i, ax in enumerate( f3ax ):
    ylim = ax.get_ylim()
    yrange =  max(ylim) - min(ylim)
    ax.text( -0.35, max( ylim ) -0.15*yrange, panlab[i])
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(5) )
    ax.set_xlim([-0.5, lensea -0.5])

    if (ax != f3d): # only keep xlabels for the bottom panels
        ax.set_xticklabels([])
        ax.set_xlabel('')
        
    ax.set_ylabel( yaxlab[i] )
  
    
plt.figure(3).subplots_adjust(hspace=0.06, wspace=0.05, right=0.7)
f3a.legend(ncol=1, prop={'size':12},numpoints=1, bbox_to_anchor=(1.5, 1.05),
           handlelength=0.01, handletextpad=1, borderpad=1, frameon=False )

f3a.set_title(str(tys2) + '-' + str(tye2) )

# save some pdfs
plt.figure(1).savefig('sam_pos_str_width_ts_v5.pdf',format='pdf',dpi=300,
                      bbox_inches='tight')
plt.figure(2).savefig('sam_pos_str_width_trends_v5.pdf',format='pdf',dpi=300,
                       bbox_inches='tight')
plt.figure(3).savefig('sam_pos_str_width_trends_v5-2.pdf',format='pdf',dpi=300,
                       bbox_inches='tight')
                       
# ---------------------------------------------------------------------------------------------------
#                        Do SAM vs SPEED trend plots
# ---------------------------------------------------------------------------------------------------

def relp( xs , ys, corr=False ):
    """ plot a scatter of ys vs xs, and then compute the OLS regression line and plot on yhat. 
    If corr=True then compute the pearson r and p-value and print in near the bottom right corner
    """
    svj_slope , conf_int , p_value, svj_yhat, svj_intercept =\
        trend_ts.trend_ts( xs  , ys )
    xvals = np.arange( np.min( xs ) - abs(np.max( xs )*15)  ,\
           abs( np.max( xs )*15) )
    ypred = xvals * svj_slope + svj_intercept
    plt.plot( xs , ys , 'ro', label='CMIP5')
    plt.plot( xvals , ypred , 'r--' )
    
    if corr==True:
        r, p = sp.stats.pearsonr(xs, ys)
        yrange = max(ys) - min(ys)
        xran = max(xs) - min(xs)
        plt.text(max(xs) -0.25*xran, min(ys)-0.2*yrange,
		 "$r$: " + str(np.round(r,2)), color='r')
        plt.text(max(xs) -0.25*xran, min(ys) - 0.4*yrange, 
		 "$p$: " + str(np.round(p,2)), color='r' )
        plt.xlim( [ min(xs) - 0.15*xran, max(xs) +  0.15*xran] )
        #plt.ylim( [ min(ys) - 0.15*yrange, max(ys) +  0.15*yrange] )
    
def reanp( xs , ys, trend=True):
    """ Plot a scatter (using x's) of ys vs xs using colors in the global variable rlc.
    We're assuming len(xs) == len(ys) == len(rean) == len(rlc), where reana and rlc 
    are global variables. If corr=True compute the OLS regression line and plot on yhat in black. 
    """
    for  i in range(xs.shape[0]):
       if( not np.isnan(ys[i]) ):
           plt.plot(xs[i], ys[i], 'x', color=rlc[int(i)],
                    markersize=10,markeredgewidth=3, label=rean[i]) 

    if trend == True:
        svj_slope , conf_int , p_value, svj_yhat, svj_intercept =\
            trend_ts.trend_ts( xs  , ys )
        xvals = np.arange( np.min( xs ) - np.max( xs )*15  ,\
            np.max( xs )*15  )
        ypred = xvals * svj_slope + svj_intercept
        plt.plot( xvals , ypred , 'k--' )
        
# ---------------------------------------------------------------------------------------------------

# Setup up some someplots
f, gs2 = plt.subplots(3,2, sharex=True, sharey=True)
f.delaxes(gs2[0,1])
maxis = [-0.25, 0.5, -2, 4]
plt.axis(maxis)
rat = ( maxis[1] - maxis[0] ) / ( maxis[3] - maxis[2] )
plt.setp(gs2.flat, aspect = rat, adjustable='box-forced')
f.subplots_adjust( hspace=0.15, wspace = -0.65)
gs2[2,1].xaxis.set_major_locator( mpl.ticker.MaxNLocator(4, prune='both'))
gs2[2,1].yaxis.set_major_locator( mpl.ticker.MaxNLocator(6,prune='upper'))    

order = [4, 0, 1, 2, 3]   # order of the seasons in seas we want to use.
axorder = [0, 2, 3, 4, 5] # order of the axis positions we want to use.

# list over all seasons in seas and plot a scatter of uspd vs sam trends for 
#models and reanalysis.
for i,ord in enumerate(order):
    plt.sca( gs2.flatten()[ axorder[i] ] )
    relp( mod_uspd_trends[ : , ord ],mod_sam_trends[ : , ord ] )
    reanp( uspd_trends[ : , ord ], sam_trends[ : , ord ] )

seas_label = [ ['a) ANN', '' ] , ['b) MAM','c) JJA'] , ['d) SON', 'e) DJF'] ]
plt.text( maxis[0] -maxis[1],maxis[2]*1.7  , 'Umax trend (ms$^{-1}$/dec)')
gs2[1,0].set_ylabel('SAM trend (hPa/dec)')

[ gs2[m,n].text(-0.2, 3, seas_label[m][n] ) for m in range(3) for n in range(2)  ]

plt.savefig('sam_v_jet_1979_2010_v5.pdf',format='pdf',dpi=300,
            bbox_inches='tight' )

print
print 'Rean. vs Mod mean trend:'
print
print 'SAM'
print  np.mean( sam_trends[ 0:3 , 4 ] ) / np.mean( mod_sam_trends[ : , 4 ] )
print
print 'Speed'
print   np.mean( uspd_trends[ 0:3 , 4 ] ) / np.mean( mod_uspd_trends[ : , 4 ] )


########################################################################################################

# Look at some more relationships between SAM trends and (left) trends in uspd, pos and width 
# and (right) between SAM trends and climatological uspd, pos and width.

# set up subplots.
f, gs2 = plt.subplots(3,2, sharey=True)
f.set_size_inches((8,8), forward=True )
gs2[0,0].set_ylim([-0.5,2])

# compute climatological uspd, pos and width in the reanalyses.
rsam = year_lim( press , tys2 , tys2 ).mean()
rpos = year_lim( locmax , tys2 , tys2 ).mean()
ruspd = year_lim( maxspd , tys2 , tys2 ).mean()
rwidth = year_lim( width , tys2 , tys2 ).mean()

# compute climatological uspd, pos and width in the CMIP5 models.
modsam = year_lim( modpress , tys2 , tys2 ).mean()
modpos = year_lim( modlocmax , tys2 , tys2 ).mean()
moduspd = year_lim( modmaxspd , tys2 , tys2 ).mean()
modwidth = year_lim( modwidth , tys2 , tys2 ).mean()

lvars =['uspd','pos', 'width' ]
s=3 # choose a season to look at. 3 = djf.
lab1 = ['a)', 'c)', 'e)']
lab2 = ['b)', 'd)', 'f)']

# loop over lvars and plot the scatter of var trend vs SAM trend (left) and 
# var_climatology vs SAM trend (right)
for i,var in enumerate(lvars):
    plt.sca( gs2[i,0] )
    relp(eval('mod_' + var + '_trends' + '[:,s]' ) , mod_sam_trends[:,s] 
         , corr=True)
    reanp( eval(var + '_trends[:,s]'), sam_trends[:,s] ,trend=False)
    gs2[i,0].set_xlabel(yaxlab[i+1].replace('\n',''))
    gs2[i,0].xaxis.set_major_locator( mpl.ticker.MaxNLocator(4, prune='both'))
    plt.sca( gs2[i,1] )
    relp( eval('mod' + var ) , mod_sam_trends[:,s], corr=True )
    gs2[i,1].set_xlabel(yaxlab1[i+1].replace('\n',''))
    reanp( np.array(eval('r' + var)), sam_trends[:,s].T ,trend=False)
    gs2[i,0].xaxis.set_major_locator( mpl.ticker.MaxNLocator(4, prune='both'))
    gs2[i,1].xaxis.set_major_locator( mpl.ticker.MaxNLocator(6)) 
    
    xr = abs(gs2[i,0].axis()[1] - gs2[i,0].axis()[0])*0.05 + gs2[i,0].axis()[0]
    gs2[i,0].text(xr, 1.75, lab1[i])
    xr = abs(gs2[i,1].axis()[1] - gs2[i,1].axis()[0])*0.05 + gs2[i,1].axis()[0]
    gs2[i,1].text(xr, 1.75, lab2[i])    
    
gs2[1,1].xaxis.set_major_locator( mpl.ticker.MaxNLocator(5)) 
plt.subplots_adjust( hspace=0.3, right=0.7, wspace=0.1)
gs2[1,0].set_ylabel('SAM trend (hPa/dec)')
gs2[0,0].set_title('Trends')
gs2[0,1].set_title('Climatology')
gs2[0,1].legend(ncol=1, prop={'size':12},numpoints=1, bbox_to_anchor=(1.55,
1.05),handlelength=0.01, handletextpad=1, borderpad=1, frameon=False )

plt.savefig('sam_trends_v_jet_scatter_1951-2011.pdf',format='pdf',dpi=300,
            bbox_inches='tight')

print "correlation between ",tys2, " jet position and sam trend in CMIP5"
print sp.stats.pearsonr(modpos, mod_sam_trends[:,3])
print "correlation between ", tys2 ," jet strength and sam trend in CMIP5"
print sp.stats.pearsonr(moduspd, mod_sam_trends[:,3])    

