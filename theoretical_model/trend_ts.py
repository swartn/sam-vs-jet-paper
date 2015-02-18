def trend_ts( t , y ):
    """
    slope , conf_int , p_value, yhat = trend_ts( t , y )
    Calculate the linear trend in a timeseries y at times t and returns 
    the slope, confidence interval, conf_int, which includes accounting 
    for autocorrelation following Santer et al. (2000), and the 
    predictions of the linear model, yhat, at times t.
    """
    import numpy as np
    import scipy as sp
    from scipy import stats

    slope, intercept, r_value, p_value, std_err = stats.linregress( t , y )

    yhat = intercept + slope * t 
    residuals = y - yhat

    nt = len( residuals )
    r_corr , ptrash = stats.pearsonr( residuals[ 0 : -1] , residuals[ 1 : : ] ) 
    r_corr = 0 if r_corr < 0. else  r_corr
    #print 'r:', r_corr
    Neff = nt * ( 1 - r_corr ) / ( 1 + r_corr ) ; 
    se = np.sqrt( sum( residuals * residuals ) / ( Neff - 2 ) );    
    sb = se / np.sqrt( sum( ( t - np.mean( t ) )**2 ) );  
    # tb = b(1) / sb ;
    tcrit = stats.t.isf(0.025, nt - 2 ) 
    c = tcrit * sb ;

    # print "slope , c, p_value:" , slope , c , p_value
    # print "Is trend significant?" , abs(slope) - c > 0 
    return slope, c, p_value, yhat, intercept
