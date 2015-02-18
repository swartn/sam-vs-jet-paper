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

locmax = pd.read_csv('../rean_uloc.txt',names=['date','ind','rno','pos']) # read in
locmax.date = locmax.date.apply(lambda d: parse(d) )  
rean = ['R1', 'R2', 'TCR', 'ERA', 'CFSR', 'MERRA']
locmax = locmax.pivot( index = 'date' , columns = 'rno', values = 'pos' )
locmax.columns = rean

rean_pos = np.zeros( len(rean) )
for (i, name) in enumerate( rean ):
    rean_pos[i] = locmax[name].dropna().mean()
    

modlocmax = pd.read_csv('/ra40/data/ncs/cmip5/sam/c5_uas/mod_uloc.txt',\
 names=['date','ind','rno','pos']) # read in
 
modlocmax.date = modlocmax.date.apply(lambda d: parse(d) )  
modlocmax.rno = modlocmax.rno - 1 # make the model 'labels' start at 1.
modlocmax = modlocmax.pivot( index = 'date' , columns = 'rno', values = 'pos' )

mod_pos = np.zeros( len( modlocmax.columns) )
for i,name in enumerate(modlocmax.columns):
    mod_pos[i] = modlocmax[name].dropna().mean()

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

#mf, gs = plt.subplots( 3 , 2 )
gs =[]
gs.append( plt.axes([0.2, 0.55, 0.4, 0.35]) )
gs.append( plt.axes([0.2, 0.1, 0.4, 0.35]) )

dlatc = -52     # central lat
dsig = 8      # width
dstr = 15.0e2   # range in hPa
str0 = 1000.0e2  # central press in hPa

def calc( lat_c = dlatc , sig = dsig, dpdt = dstr ):  
    # compute the pressure / gradient
    pres = erf( ( lat - lat_c )  / sig )*dpdt + str0
    dP = np.diff( pres ) / dist

    # compute SAM 
    p_40 = pres[ i_40 ]
    p_65 = pres[ i_65 ]
    sam = ( p_40 - p_65 ) /100
                
    # compute the geostrophic velocity
    u = ( -1 / ( f * rho ) ) * dP ;
    umax = np.max( u )
    return pres/100, sam, u, umax

def trends( data, year ):
    '''Calculate linear trend in the sam of datframe dfp between years ys and ye inclusive'''
    slope , conf_int , p_value, yhat = trend_ts.trend_ts( year , data )
    #yhat = sam_slope * year + intercept           # calc yhat values to return
    #print dft.sam_slope*10
    return slope*10 #, yhat

def gen_sam_umax( lat_c0, times, dsig=dsig, dstr=dstr,dlatc=dlatc ):
    sam = np.zeros( ( len(times),1) ) ; samm = np.zeros( ( len(times),1) ) 
    umax = np.zeros( ( len(times),1) ) ; umaxm = np.zeros( ( len(times),1) ) 
    
    for i,t in enumerate(times):
        dlatc = lat_c0  + t*dlatc*0.001     # central lat
        dsig = 8                # width
        dstr = 15.0e2 + t*dstr*0.002    # range in hPa
        str0 = 1000.0e2           # central press in hPa
        pres, sam[i], u, umax[i] = calc( lat_c = dlatc , sig = dsig, dpdt = dstr )  
    return times, sam, umax, pres, u    
    
def sam_umax_trend(lat_c0, dsig = dsig, dstr = dstr ):
    # do trends in strength and position and plot
    times = np.arange(30)
    times, sam, umax, pres, u = gen_sam_umax(lat_c0, times, dsig = dsig, dstr = dstr )
    sam_trend = trends( np.squeeze(sam), times )
    umax_trend = trends( np.squeeze(umax), times )
    return sam_trend, umax_trend

# Get initial values and plot    
times, sam, umax, pres, u0 = gen_sam_umax(lat_c0=locmax.mean().mean(), times=[0], dsig = dsig, dstr = dstr )
gs[0].plot( lat_p, u0 , 'b')
times, sam, umax, pres, u0 = gen_sam_umax(lat_c0=locmax.mean().mean(), times=[29], dsig = dsig, dstr = dstr )
gs[0].plot( lat_p, u0 , 'b--')

xtics=np.arange(-70,-30,10)
gs[0].set_xticks(xtics )
gs[0].set_xlabel('Latitude')

rean_sam_trends = np.zeros( len(rean) )
rean_umax_trends = np.zeros( len(rean) )
for i in range( len(rean) ):
    rean_sam_trends[i], rean_umax_trends[i] = sam_umax_trend( rean_pos[i] ) 

mod_sam_trends = np.zeros( len(modlocmax.columns) )
mod_umax_trends = np.zeros( len(modlocmax.columns) )
for i in range( len(modlocmax.columns) ):
    mod_sam_trends[i], mod_umax_trends[i] = sam_umax_trend( mod_pos[i] ) 

gs[1].plot( rean_sam_trends , rean_umax_trends, 'kx')
gs[1].plot( mod_sam_trends , mod_umax_trends, 'ro')
gs[1].set_xlabel(r'SAM trend (hPa/dec)')
gs[1].set_ylabel(r'Umax trend (ms$^{-1}$/dec)')
gs[1].yaxis.set_major_locator( mticker.MaxNLocator(6))
gs[1].xaxis.set_major_locator( mticker.MaxNLocator(6))
gs[1].set_ylim([0.15, 0.21] )

#plt.savefig('sam_v_jet_theory_ts.pdf',format='pdf',bbox_inches='tight')
