"""
Plots seasonal trends over 1951 to 2011 of SAM and jet properties for various 
reanalyses and CMIP5. 

Outputs:
--------
This script produces plots:

1. Trends in the above variables over 1951-2011.
2. The relationship between SAM and strength trends.
3. The relationship between SAM and trends in the other variables, as well as 
trends in SAM and the climatology of the variables. (e.g. SAM trend vs 
climatological jet position).

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import trend_ts

# set plotting params.
plt.close('all')
plt.ion()
font = {'size'   : 12}
plt.rc('font', **font)

#============================================#
# Define some functions

def get_seasons(df):
    """Extract the 4 seasons and the annual mean from dataframe df, and save 
    them as df.djf, df.mam, df.jja, df.son and df.ann and then return df. Note 
    December is from the previous year.
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

def year_lim(df, ys, ye):
    """ Limits the dataframe df to between years starting in ys and ending in 
    ye inclusive"""
    dfo = df[ ( df.index.year >= ys ) & ( df.index.year <= ye ) ]
    if ( df.index.year.min() > ys ):
         print 'WARNING: data record begins after requested trend start.' 
    elif ( df.index.year.max() < ye ):
         print 'WARNING: data record ends before requested trend end.', 
         df.index.year.max() 
    return dfo
    
def calc_trends(dfp, var, ys , ye ):
    """Calculate linear trend in the dataframe dfp between years (datetime 
    indices) ys and ye inclusive. Saves the trend as dfp.slope and calculates 
    and saves the linear prediction (dfp.yhat) for all input years.
    """
    dfp =  year_lim( dfp.resample('A') , ys, ye )              
    dfp.slope , conf_int , p_value, yhat, intercept =\
                 trend_ts.trend_ts(dfp.index.year, dfp[var])
    dfp['yhat'] = dfp.slope * dfp.index.year + intercept         
    return dfp
                  
def rean_proc(dfr, axtrend=None, tys=None, tye=None, mew=2, ms=15, ls='_'):
    """ Loop over the columns of dfr (corresponding to different reanalyses) and
    2. if axtrend is given then compute the linear trend between years tys and 
    tye (inclusive) and plot the trends on axis axtrends. 
    3. Return the trends.
    
    The data from dfr are colored columwise in the plots using colors provided 
    in the global variable rlc, and similarly are labelled using the names 
    listed in the global variable rean.
    """
    seas = ['mam', 'jja', 'son', 'djf', 'ann'] 
    rean_trends = np.zeros((len(dfr.columns), 5))
    dfr.seasons = get_seasons( dfr ) ; 
    
    # Loop over reanalyses and do some basic dataframe checks and adjustments.
    # We're assuming len(dfr.columns) == len(rean).
    for (i, cn) in enumerate( dfr.columns ):      
        # check that we are not trying to use data that doesn't exist
        if ( dfr[cn].dropna().index.year.min() > tys ):
            print cn, 'WARNING: start >', str(tys)
        elif ( dfr[cn].dropna().index.year.max() < tye ):
            print cn, 'WARNING: end <', str(tye)
           
        # If axtrend was passed, plot the linear trend between tys and tye for 
        # each season and each reanalysis. Season names are listed in the 
        # global  variable seas.
        if (axtrend):
            for (k, nm) in enumerate(seas):
                names = 'dfr.seasons.' + nm
                mt = calc_trends( eval( names ), cn, tys , tye )
                rean_trends[i, k]  =  mt.slope * 10          
                if (nm == 'ann') & ( not np.isnan(rean_trends[i, k])):
                    axtrend.plot(k, rean_trends[i, k], ls,
                                 ms=ms, mew=mew, label=cn)
                else:
                    axtrend.plot(k, rean_trends[i, k], ls,
                                 ms=ms, mew=mew, label='')

            axtrend.set_xticks(np.arange(5 + 1))
            axtrend.plot([-1, 5], [0, 0], 'k--')  
    return rean_trends            
          
def mod_proc(df, axtrend, tys, tye, color='r', ls='_', label='CMIP5'):
    """ Loop over the columns of df calculate trends for each one, plus 
    plot the ensemble trend stats"""
    seas     = ['mam', 'jja', 'son', 'djf', 'ann'] 
    num_models =  len( df.columns )
    mod_trends = np.empty( ( num_models  , 5 ) )
    df.seasons = get_seasons(df)

    for i, cn in enumerate(df.columns):  
        for (k , nm) in enumerate(seas):
            names = 'df.seasons.' + nm
            mt = calc_trends( eval(names), cn, tys, tye )
            mod_trends[i, k] = mt.slope * 10
            
            if i == ( num_models - 1 ):
                mod_trend_mean = np.mean( mod_trends[ : , k ] )
                mod_trend_std =  np.std( mod_trends[ : , k ] )
                c = sp.stats.t.isf(0.025, num_models - 1 )
                #print c, num_models, np.sqrt(num_models)
                mod_95_ci = ( c * mod_trend_std ) / np.sqrt( num_models )
                mod_5thp = np.percentile( mod_trends[ : , k ] , 2.5 )
                mod_95thp = np.percentile( mod_trends[ : , k ] , 97.5 )
                                
                axtrend.plot( [ k , k ] , [ mod_5thp  , mod_95thp ],color, 
                             linewidth=4, alpha=0.25)
                axtrend.plot([k, k], [mod_trend_mean - mod_95_ci, 
                             mod_trend_mean + mod_95_ci ], color, linewidth=4) 
                if nm == 'ann':
                    axtrend.plot(k, np.mean(mod_trends[:, k]), '_' + color, 
                                 ms=15,                         
                                 mew=2, label=label)
                else:
                    axtrend.plot(k, np.mean(mod_trends[:, k]), '_' + color, ms=15, 
                                 mew=2, label='')    
    axtrend.set_xticks(np.arange(5 + 1))
    axtrend.plot([-1, 5], [0, 0], 'k--')                 
    return mod_trends

def relp(xs, ys, corr=False, reg=None, label='CMIP5', color='r', alpha=1, 
         line=True):
    """ plot a scatter of ys vs xs, and then compute the OLS regression line 
    and plot on yhat. If corr=True then compute the pearson r and p-value and 
    print in near the bottom right corner
    """
    svj_slope , conf_int , p_value, svj_yhat, svj_intercept =\
        trend_ts.trend_ts( xs  , ys )
    xvals = np.arange( np.min( xs ) - abs(np.max( xs )*15)  ,\
           abs( np.max( xs )*15) )
    ypred = xvals * svj_slope + svj_intercept
    plt.plot( xs , ys , color + 'o', label=label, alpha=alpha)
    if line==True:
        plt.plot( xvals , ypred , color + '--' )
    
    if corr==True:
        r, p = sp.stats.pearsonr(xs, ys)
        yrange = max(ys) - min(ys)
        xran = max(xs) - min(xs)
        plt.text(max(xs) -0.25*xran, min(ys)-0.2*yrange,
                 "$r$: " + str(np.round(r,2)), color=color)
        plt.text(max(xs) -0.25*xran, min(ys) - 0.4*yrange, 
                 "$p$: " + str(np.round(p,2)), color=color )
        #plt.xlim( [ min(xs) - 0.15*xran, max(xs) +  0.15*xran] )
        #plt.ylim( [ min(ys) - 0.15*yrange, max(ys) +  0.15*yrange] )
        #plt.autoscale(enable=True, axis='both', tight=True)
    
    if reg:
        plt.text(0.15, -0.4+ reg,
                 "$b$: " + str(np.round(svj_slope,1)), color=color)  
    
def reanp( xs , ys, trend=True):
    """ Plot a scatter (using x's) of ys vs xs using colors in the global 
    variable rlc. We're assuming len(xs) == len(ys) == len(rean) == len(rlc), 
    where reana and rlc are global variables. If corr=True compute the OLS 
    regression line and plot on yhat in black. 
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

#============================================#
def plot_seas_trends_1951_2011(datapath):
    """ Plots seasonal trends over 1951 to 2011 of SAM and jet properties
    """
 
    #============================================#
    # Define the years for the trend analysis
    tys = 1951 # start (inclusive)
    tye = 2011 # stop (inclusive)
    #============================================#
    #
    # Define some global variables that we use repeatedly
    #
    # the names of the reanalyses we are using (in column-order of the dataframes)
    rean     = ['R1', 'R2', '20CR', 'ERA', 'CFSR', 'MERRA']
    # corresponding colors to use for plotting each reanalysis
    rlc      = ['k', 'y','g', 'b', 'c', 'm'] 

    rean     = ['20CR']
    rlc      = ['g']  
    ls      = ['_g']  

    # names of the seasons
    seas     = ['mam', 'jja', 'son', 'djf', 'ann']  
    xtics    = [datetime(1870,1,1) + relativedelta(years=20*jj) for jj in range(8) ]

    # Load the data from `datapath` which is (mostly) saved as pandas dataframes 
    #in HDF5, and plot annual mean timeseries.
    
    # load in the reanlaysis data
    h5f = pd.HDFStore(datapath + 'zonmean_sam-jet_analysis_reanalysis.h5', 'r')
    dfr = h5f['zonmean_sam']
    h5f.close()
    dfhadslp = dfr['HadSLP2r']/100.
    dfhadslp = pd.DataFrame(dfhadslp.dropna(), columns=['HadSLP2r'])

    # load in the 20CR ensemble data
    h5f_20CR = pd.HDFStore(datapath + 'zonmean_sam-jet_analysis_20CR_ensemble.h5', 
                           'r')
    df_20cr_ens_sam = h5f_20CR['zonmean_sam']/100.
    df_20cr_ens_locmax = h5f_20CR['locmax']
    df_20cr_ens_maxspd = h5f_20CR['maxspd'] 
    df_20cr_ens_width = h5f_20CR['width'] 
    h5f_20CR.close()

    # load in the CMIP5 model data
    h5f_c5 = pd.HDFStore(datapath + 'zonmean_sam-jet_analysis_cmip5.h5', 'r')
    df_c5_ens_sam = h5f_c5['zonmean_sam']/100.
    df_c5_ens_locmax = h5f_c5['locmax']
    df_c5_ens_maxspd = h5f_c5['maxspd'] 
    df_c5_ens_width = h5f_c5['width'] 
    h5f_c5.close()               
                            
    #========= SAM - press ===============#
    f3 = plt.figure(3)
    plt.figure(3).set_size_inches((8,8), forward=True )
    f3a = plt.subplot(421)
    hadslp_sam_trends = rean_proc(dfhadslp, axtrend=f3a, tys=tys, tye=tye,
                                mew=2, ms=10, ls='.k')   
   
    mod_sam_trends = mod_proc(df_c5_ens_sam, f3a, tys=tys, tye=tye, color='r')
    tcr_sam_trends = mod_proc(df_20cr_ens_sam, f3a, tys=tys, tye=tye, color='g',
                            ls='_g', label='20CR')

    #========= Jet max speed - uspd ===============#
    f3b = plt.subplot(423)
    mod_uspd_trends = mod_proc(df_c5_ens_maxspd, f3b, tys=tys, tye=tye, color='r')
    tcr_uspd_trends = mod_proc(df_20cr_ens_maxspd, f3b, tys=tys, tye=tye, color='g',
                            label='20CR')

    #========= Location - locmax ===============#
    f3c = plt.subplot(425)
    mod_pos_trends = mod_proc(df_c5_ens_locmax, f3c, tys=tys, tye=tye, color='r')
    tcr_pos_trends = mod_proc(df_20cr_ens_locmax, f3c, tys=tys, tye=tye, color='g',
                            label='20CR')

    #========= Width ===============#
    f3d = plt.subplot(427)
    mod_width_trends = mod_proc(df_c5_ens_width, f3d, tys=tys, tye=tye, color='r')
    tcr_width_trends = mod_proc(df_20cr_ens_width, f3d, tys=tys, tye=tye, color='g',
                            label='20CR')

    # ========= Do some figure beautifying and labelled etc ========= #
    panlab = ['a)', 'b)', 'c)', 'd)', 'e)', 'f)' ,'g)', 'h)']

    f3ax = [ f3a, f3b, f3c, f3d]

    yaxlab = ['SAM trend \n(hPa dec$^{-1}$)', 
            'Strength trend \n(ms$^{-1}$ dec$^{-1}$)', 
            'Position trend \n($^{\circ}$ lat. dec$^{-1}$)', 
            'Width trend \n($^{\circ}$ lat. dec$^{-1}$)' 
            ]

    yaxlab1 = ['SAM Index (hPa)' , 
            'Strength (m/s)',
            'Position ($^{\circ}$S)', 
            'Width ($^{\circ}$ lat.)'
            ]

    for i, ax in enumerate(f3ax):
        ylim = ax.get_ylim()
        yrange = max(ylim) - min(ylim)
        ax.text( -0.35, max( ylim ) -0.15*yrange, panlab[i])
        ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(5, prune='upper'))
        ax.set_xlim([-0.5, 5 -0.5])

        if (ax != f3d): # only keep xlabels for the bottom panels
            ax.set_xticklabels([])
            ax.set_xlabel('')
            
        ax.set_ylabel( yaxlab[i] )
    
    f3d.set_xticklabels(  [ s.upper() for s in seas]  )   
    #f3d.yaxis.set_major_locator(mpl.ticker.MaxNLocator(5, prune='upper'))
    plt.figure(3).subplots_adjust(hspace=0.06, wspace=0.05, right=0.8, left=0.2)
    f3a.legend(ncol=3, prop={'size':12},numpoints=1, bbox_to_anchor=(1.075, 1.265),
            handlelength=0.01, handletextpad=0.8, frameon=False )
    f3d.yaxis.set_ticks([-0.4, -0.2, 0, 0.2])

    # save some pdfs
    plt.figure(3).savefig('../plots/seas_trends_1951-2011.pdf',format='pdf'
                        , dpi=300, bbox_inches='tight') 
    
    #for i in range(5):
        #print seas[i]
        #print sp.stats.ttest_ind(mod_sam_trends[:,i], 
                                #tcr_sam_trends[:,i], equal_var=False)
    
    # ------------------------------------------------------------------------------
    #                        Do SAM vs SPEED trend plots
    # ------------------------------------------------------------------------------

    # Setup up some someplots
    f, gs2 = plt.subplots(3,2, sharex=True, sharey=True)
    f.delaxes(gs2[0,1])
    maxis = [-0.1, 0.35, -0.8, 1.6]
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
        relp( mod_uspd_trends[ : , ord ],mod_sam_trends[ : , ord ], reg=0.01,
            label='CMIP5' )
        relp( tcr_uspd_trends[ : , ord ],tcr_sam_trends[ : , ord ], reg=-0.225,
            color='g', label='20CR')

    seas_label = [ ['a) ANN', '' ] , ['b) MAM','c) JJA'] , ['d) SON', 'e) DJF'] ]
    plt.text(maxis[0] -maxis[1],maxis[2]*1.7 , 
             'Strength trend (ms$^{-1}$dec$^{-1}$)')
    gs2[1,0].set_ylabel('SAM trend (hPa dec$^{-1}$)')


    [gs2[m,n].text(-0.075, 1.25, seas_label[m][n] ) for m in range(3) for n in range(2)]
    gs2[0,0].legend(ncol=1, prop={'size':12},numpoints=1, bbox_to_anchor=(1.8,
    1.05),handlelength=0.01, handletextpad=1, borderpad=1, frameon=False )

    plt.savefig('../plots/sam_v_uspd_seas_1951_2011.pdf',format='pdf',dpi=300,
                bbox_inches='tight' )

    #=============================================================================

    # Look at some more relationships between SAM trends and (left) trends in uspd, 
    #pos and width 
    # and (right) between SAM trends and climatological uspd, pos and width.

    # set up subplots.
    f, gs2 = plt.subplots(3,2, sharey=True)
    f.set_size_inches((8,8), forward=True )
    gs2[0,0].set_ylim([-0.5,2])

    # compute climatological uspd, pos and width in the CMIP5 models.
    modsam = year_lim( df_c5_ens_sam , tys , tys ).mean()
    modpos = year_lim( df_c5_ens_locmax , tys , tys ).mean()
    moduspd = year_lim( df_c5_ens_maxspd , tys , tys ).mean()
    modwidth = year_lim( df_c5_ens_width , tys , tys ).mean()

    # compute climatological uspd, pos and width in the 20CR ensemble
    tcrsam = year_lim( df_20cr_ens_sam , tys , tys ).mean()
    tcrpos = year_lim( df_20cr_ens_locmax , tys , tys ).mean()
    tcruspd = year_lim( df_20cr_ens_maxspd , tys , tys ).mean()
    tcrwidth = year_lim( df_20cr_ens_width , tys , tys ).mean()

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
        relp(eval('tcr_' + var + '_trends' + '[:,s]' ) , tcr_sam_trends[:,s] 
            , corr=False, color='g', label='20CR', alpha=1, line=False)    
        gs2[i,0].set_xlabel(yaxlab[i+1].replace('\n',''))
        gs2[i,0].xaxis.set_major_locator( mpl.ticker.MaxNLocator(4, prune='both'))
        plt.sca( gs2[i,1] )
        relp( eval('mod' + var ) , mod_sam_trends[:,s], corr=True )
        relp( eval('tcr' + var ) , tcr_sam_trends[:,s], corr=False, 
            color='g',label='20CR', alpha=1, line=False )
        gs2[i,1].set_xlabel(yaxlab1[i+1].replace('\n',''))
        gs2[i,0].xaxis.set_major_locator( mpl.ticker.MaxNLocator(4, prune='both'))
        gs2[i,1].xaxis.set_major_locator( mpl.ticker.MaxNLocator(6)) 
        
    
    gs2[1,1].xaxis.set_major_locator( mpl.ticker.MaxNLocator(5)) 
    plt.subplots_adjust(hspace=0.5, right=0.7, wspace=0.1)
    gs2[0,0].set_ylabel('SAM trend (hPa dec$^{-1}$)')
    gs2[1,0].set_ylabel('SAM trend (hPa dec$^{-1}$)')
    gs2[2,0].set_ylabel('SAM trend (hPa dec$^{-1}$)')

    gs2[0,0].set_title('Trends')
    gs2[0,1].set_title('Climatology')
    gs2[0,1].legend(ncol=1, prop={'size':12},numpoints=1, bbox_to_anchor=(1.475,
    1.05),handlelength=0.01, handletextpad=1, borderpad=1, frameon=False )

    xl = [(-0.025, 0.2), (5,9.5), (-0.6, 0.05), (-54, -41.5), (-0.2, 0.375), (29, 38)]
    for i, ax in enumerate(gs2.flatten()):
        ax.set_ylim([-0.5, 2])
        ax.set_xlim(xl[i])
        
    for i,var in enumerate(lvars):
        xr = abs(gs2[i,0].axis()[1] - gs2[i,0].axis()[0])*0.05 + gs2[i,0].axis()[0]
        gs2[i,0].text(xr, 1.75, lab1[i])
        xr = abs(gs2[i,1].axis()[1] - gs2[i,1].axis()[0])*0.05 + gs2[i,1].axis()[0]
        gs2[i,1].text(xr, 1.75, lab2[i])    
        
    plt.savefig('../plots/sam_vs_jet_scatter.pdf',format='pdf',dpi=300,
                bbox_inches='tight')

if __name__ == '__main__':
    plot_seas_trends_1951_2011(datapath='../data_retrieval/data/')
    
    