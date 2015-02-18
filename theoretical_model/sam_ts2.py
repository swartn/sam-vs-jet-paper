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

#import trend_ts

lat = np.linspace( -70 , -20 , 200 ); # latitudes
dy = lat[1] - lat[0]
deg2rad = np.pi / 180 # conversion
rho = 1.2 ; # density of air 
lat_p = ( lat[ 0 : -1 ] + lat[ 1 : : ] ) / 2. ; # velocity points
dist = ( lat_p / lat_p ) * ( 111120 *dy )  ; # distance between latitudes in meters
f = 2. * 2. * np.pi / ( 3600 * 24 ) * np.sin( deg2rad * lat_p.mean() ) # coriolis

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
"""
def trends( data, year ):
    '''Calculate linear trend in the sam of datframe dfp between years ys and ye inclusive'''
    slope , conf_int , p_value, yhat, intercept = trend_ts.trend_ts( year , data )
    yhat = sam_slope * year + intercept           # calc yhat values to return
    #print dft.sam_slope*10
    return slope #, yhat
"""
   

# Get initial values and plot    
pres0, sam0, u0, umax0 = calc( lat_c = dlatc , sig = dsig, dpdt = dstr ) 
gs[0].plot( lat_p, u0 , 'b')
presm0, samm0, um0, umaxm0 = calc( lat_c = dlatc + 2 , sig = dsig, dpdt = dstr ) 
gs[0].plot( lat_p, um0 , 'r')

xtics=np.arange(-70,-30,10)
gs[0].set_xticks(xtics )
gs[0].set_xlabel('Latitude')


# do trends in strength and position and plot
times = np.arange(10)
sam = np.zeros( ( len(times),1) ) ; samm = np.zeros( ( len(times),1) ) 
umax = np.zeros( ( len(times),1) ) ; umaxm = np.zeros( ( len(times),1) ) 


for t in times:
    dlatc = -52  + t*dlatc*0.01     # central lat
    dsig = 8                # width
    dstr = 15.0e2 + t*dstr*0.01    # range in hPa
    str0 = 1000.0e2           # central press in hPa
    pres, sam[t], u, umax[t] = calc( lat_c = dlatc , sig = dsig, dpdt = dstr )  
    presm, samm[t], um, umaxm[t] = calc( lat_c = dlatc + 2 , sig = dsig, dpdt = dstr )
    
# plot the final state
gs[0].plot( lat_p, u , 'b--')
gs[0].plot( lat_p, um , 'r--')
xtics=np.arange(-70,-30,10)
gs[0].set_xticks(xtics )
gs[0].set_xlim([-70, -30])
gs[0].set_xlabel(r'Latitude ($^{\circ}$S)')
gs[0].set_ylabel(r'U (m/s)')

samp = sam - sam.mean()
umaxp = umax - umax.mean()
gs[1].plot( [ samp[0], samp[-1] ],[ umaxp[0], umaxp[-1] ] , 'k', linewidth=3)
sammp = samm - samm.mean()
umaxmp = umaxm - umaxm.mean()
gs[1].plot( [ sammp[0], sammp[-1] ],[ umaxmp[0], umaxmp[-1] ] , 'r--', linewidth=3)

gs[1].set_xlabel(r'$\Delta$ SAM (hPa/dec)')
gs[1].set_ylabel(r'$\Delta$ U (ms$^{-1}$/dec)')
gs[1].yaxis.set_major_locator( mticker.MaxNLocator(6))
gs[1].xaxis.set_major_locator( mticker.MaxNLocator(6))

#plt.savefig('sam_v_jet_theory_ts.pdf',format='pdf',bbox_inches='tight')
