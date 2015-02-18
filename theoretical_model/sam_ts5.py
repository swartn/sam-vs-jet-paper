"""
A theoretical model of the jet response to SAM changes
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
plt.close('all')
plt.ion()
font = {'size'   : 16}
plt.rc('font', **font)
import scipy as sp
from scipy.special import erf
import pandas as pd
from dateutil.parser import parse
import trend_ts

#============================================#
# Define the years for the trend analysis
# Period 2
tys2 = 1951 # start (inclusive)
tye2 = 2011 # stop (inclusive)
#============================================#

def year_lim( df , ys , ye ):
    """ Limits the dataframe df to between years starting in ys and ending in ye inclusive"""
    dfo = df[ ( df.index.year >= ys ) & ( df.index.year <= ye ) ]
    if ( df.index.year.min() > ys ):
         print 'WARNING: data record begins after requested trend start.' 
    elif ( df.index.year.max() < ye ):
         print 'WARNING: data record ends before requested trend end.', df.index.year.max() 
    return dfo

locmax = pd.read_csv('../rean_uloc.txt',names=['date','ind','rno','pos']) # read in
locmax.date = locmax.date.apply(lambda d: parse(d) )  
rean = ['R1', 'R2', 'TCR', 'ERA', 'CFSR', 'MERRA']
locmax = locmax.pivot( index = 'date' , columns = 'rno', values = 'pos' )
locmax.columns = rean

locmax = year_lim(locmax, tys2, tys2)
rean_pos = np.array(  locmax.mean().tolist() )   

modlocmax = pd.read_csv('/ra40/data/ncs/cmip5/sam/c5_uas/mod_uloc.txt',\
 names=['date','ind','rno','pos']) # read in
 
modlocmax.date = modlocmax.date.apply(lambda d: parse(d) )  
modlocmax.rno = modlocmax.rno - 1 # make the model 'labels' start at 1.
modlocmax = modlocmax.pivot( index = 'date' , columns = 'rno', values = 'pos' )

modlocmax = year_lim(modlocmax, tys2, tys2)
mod_pos = np.array(  modlocmax.mean().tolist() )   

lat = np.linspace( -70 , -20 , 200 ); # latitudes
dy = lat[1] - lat[0]
deg2rad = np.pi / 180 # conversion
rho = 1.2 ; # density of air 
lat_p = ( lat[ 0 : -1 ] + lat[ 1 : : ] ) / 2. ; # velocity points
dist = ( lat_p / lat_p ) * ( 111120 *dy )  ; # distance between latitudes in meters
f = 2. * 2. * np.pi / ( 3600 * 24 ) * np.sin( deg2rad * lat_p.mean() ) # coriolis: f-plane
#f = 2. * 2. * np.pi / ( 3600 * 24 ) * np.sin( deg2rad * lat_p ) # coriolis: beta-plane

# find the indices of the SAM locations
l40 = lat[ lat < -40 ];
l65 = lat[ lat < -65 ];
i_65 = np.where( lat == l65[-1] )
i_40 = np.where( lat == l40[-1] )

# Default parameters for the jet
latc0   = -52       # central lat
sig0    = 8         # half width
strth0  = 15.0e2    # range in hPa
strc0   = 1000.0e2  # central press in hPa

def calc( latc=latc0 , sig=sig0, strth=strth0 ):
    """Use the input latitude (latc), width (sig) and strength to
    compute the meriodional pressure using an error function. Then 
    compute the westerlies geostropically from the pressure field.
    """
    # compute the pressure / gradient
    pres = erf( ( lat - latc )  / sig )*strth + strc0
    dP = np.diff( pres ) / dist

    # compute SAM 
    p_40 = pres[ i_40 ]
    p_65 = pres[ i_65 ]
    sam = (p_40 - p_65)/100.0
                
    # compute the geostrophic velocity
    u = ( -1/( f*rho ) )*dP ;
    umax = np.max( u )
    return pres/100, sam, u, umax

def trends( data, year ):
    '''Calculate linear trend in the sam of datframe dfp between years ys and ye inclusive'''
    slope , conf_int , p_value, yhat, intercept = trend_ts.trend_ts( year , data )
    #yhat = sam_slope * year + intercept           # calc yhat values to return
    #print dft.sam_slope*10
    return slope*10 #, yhat

def sam_umax_trend( lat_c0, dsig=dsig, dstr=dstr):
    times = np.arange(60)
    sam = np.zeros( ( len(times),1) ) ; samm = np.zeros( ( len(times),1) ) 
    umax = np.zeros( ( len(times),1) ) ; umaxm = np.zeros( ( len(times),1) ) 
    latc = np.zeros( ( len(times),1) )
    for i,t in enumerate(times):
        latc[i] = lat_c0  + t*dlatc*0.001     # central lat
        dsig = 8                # width
        dstr = 15.0e2   #+ t*dstr*0.002    # range in hPa
        str0 = 1000.0e2           # central press in hPa
        pres, sam[i], u, umax[i] = calc( lat_c = latc[i] , sig = dsig, dpdt = dstr )

    sam_trend = trends( np.squeeze(sam), times )
    pos_trend = trends( np.squeeze(latc), times )
    umax_trend = trends( np.squeeze(umax), times )
    
    return sam_trend, umax_trend    


f1, gs = plt.subplots(3,2, sharey=True)
f1.set_size_inches((8,8), forward=True )

mod_sam_trends = np.zeros( len(modlocmax.columns) )
mod_umax_trends = np.zeros( len(modlocmax.columns) )
for i in range( len(modlocmax.columns) ):
    mod_sam_trends[i], mod_umax_trends[i] = sam_umax_trend( mod_pos[i] ) 

gs[1,1].plot( rean_pos, rean_sam_trends, 'kx')
gs[1,1].plot( mod_pos, mod_sam_trends , 'ro')
gs[1,1].set_ylabel(r'SAM trend (hPa/dec)')
gs[1,1].set_xlabel(r'Initial position')
gs[1,1].yaxis.set_major_locator( mticker.MaxNLocator(6))
gs[1,1].xaxis.set_major_locator( mticker.MaxNLocator(6))
gs[1,1].axis([-56, -44, -0.5, 2])

plt.savefig('sam_v_jet_theory_ts.pdf',format='pdf',bbox_inches='tight')
