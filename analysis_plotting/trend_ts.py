"""Some functions for calculating linear least squared trends from numpy arrays,
   with various options for confidence intervals.

   neil.swart@ec.gc.ca, 13/10/2014
"""
import numpy as np
import scipy as sp
from scipy import stats

def trend_ts(t, y, sigma=0.05, autocorr=False):
    """ 
    Calculate a linear trend and confidence interval.    

    The linear trend in timeseries y at times t is computed with a 95%
    confidence interval, which includes accounting for autocorrelation following
    Santer et al. (2000) if autocorr=True.
    
    Parameters
    ----------
    
    t : array like
        The times
        
    y : array like
        The data 
        
    sigma : float
          Used to compute the 1 - sigma confidence interval. A sigma of 0.05
          would be for a 95% confidence interval. 
        
    autocorr : boolean
        If True, autocorrelation (AR1) is taken into account when calculating
        confidence intervals and p-values (Following Santer et al. [2000]).
    
    Returns
    -------
    slope : float
          The slope of the trend line
          
    c : float
          The 95% confidence interval
    
    p_value : float
          The p-value for the slope coefficient (test of the null hypothesis
          that slope is different from zero).
   
    yhat : array
          The predictions of the linear model at times t.
    
    """
    slope, intercept, r_value, p_value, std_err = stats.linregress( t , y )

    yhat = intercept + slope * t
    residuals = y - yhat

    nt = len( residuals )

    # adjust for lag-1  autocorrelation?
    if autocorr == True:
        r_corr , ptrash = stats.pearsonr( residuals[ 0 : -1] , residuals[ 1 : : ] )
        r_corr = 0 if r_corr <= 0. else r_corr # only keep +ve autocorr's
    else:
        r_corr = 0

    #print 'r:', r_corr
    Neff = float( nt * ( 1 - r_corr ) / ( 1 + r_corr ) ) ;
    se = np.sqrt( sum( residuals * residuals ) / ( Neff - 2 ) );
    sb = se / np.sqrt( sum( ( t - np.mean( t ) )**2 ) );
    tb = slope / sb ;
    tcrit = stats.t.isf(sigma/2.0, nt - 2 )
    c = tcrit * sb ;
    p_value = stats.t.sf(np.abs(tb), nt-2)*2

    # print "slope , c, p_value:" , slope , c , p_value
    # print "Is trend significant?" , abs(slope) - c > 0 
    return slope, c, p_value, yhat, intercept