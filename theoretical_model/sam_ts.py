"""
A theoretical model of the jet response to SAM changes
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
plt.close('all')
plt.ion()
import scipy as sp
from scipy.special import erf

lat = np.linspace( -70 , -20 , 200 ); # latitudes
deg2rad = np.pi / 180 # conversion
rho = 1.2 ; # density of air 
lat_p = ( lat[ 0 : -1 ] + lat[ 1 : : ] ) / 2. ; # velocity points
dist = ( lat_p / lat_p ) * 111120 ; # distance between latitudes in meters
f = 2. * 2. * np.pi / ( 3600 * 24 ) * np.sin( deg2rad * lat_p ) # coriolis

# find the indices of the SAM locations
l40 = lat[ lat < -40 ];
l65 = lat[ lat < -65 ];
i_65 = np.where( lat == l65[-1] )
i_40 = np.where( lat == l40[-1] )

mf, gs = plt.subplots( 3 , 2 )

dlatc = -52     # central lat
dsig = 6.5      # width
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


# Get initial values and plot    
pres0, sam0, u0, umax0 = calc( lat_c = dlatc , sig = dsig, dpdt = dstr ) 
gs[0,0].plot( lat_p, u0 , 'b')
presm0, samm0, um0, umaxm0 = calc( lat_c = dlatc + 2 , sig = dsig, dpdt = dstr ) 
gs[0,0].plot( lat_p, um0 , 'r')

xtics=np.arange(-70,-30,10)
gs[0,0].set_xticks(xtics )
gs[0,0].set_xlabel('Latitude')
     
# do trends in strength and position and plot
for t in np.arange(100):
    dlatc = -52  + t*dlatc*0.0002     # central lat
    dsig = 6.5                # width
    dstr = 15.0e2 + t*dstr*0.0002    # range in hPa
    str0 = 1000.0e2           # central press in hPa
    pres, sam, u, umax = calc( lat_c = dlatc , sig = dsig, dpdt = dstr )
    gs[1,0].plot( t, sam - sam0 , 'bo')
    gs[2,0].plot( t, umax - umax0 , 'bo')
    
    presm, samm, um, umaxm = calc( lat_c = dlatc + 2 , sig = dsig, dpdt = dstr )
    gs[1,0].plot( t, samm - samm0 , 'ro')
    gs[2,0].plot( t, umaxm - umaxm0 , 'ro')
    
# plot the final state
gs[0,0].plot( lat_p, u , 'b--')
gs[0,0].plot( lat_p, um , 'r--')
gs[1,0].set_xticklabels([])

gs[0,1].plot( [0, sam - sam0],[0, umax - umax0], 'b')
gs[0,1].plot( [0, samm -samm0],[0, umaxm -umaxm0], 'r')


#plt.savefig('sam_v_jet_theory_ts.pdf',format='pdf',bbox_inches='tight')
