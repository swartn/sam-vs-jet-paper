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
dy = lat[1] - lat[0]
deg2rad = np.pi / 180 # conversion
rho = 1.2 ; # density of air 
lat_p = ( lat[ 0 : -1 ] + lat[ 1 : : ] ) / 2. ; # velocity points
dist = ( lat_p / lat_p ) * 111120 *dy ; # distance between latitudes in meters
f = 2. * 2. * np.pi / ( 3600 * 24 ) * np.sin( deg2rad * lat_p.mean() ) # coriolis

# find the indices of the SAM locations
l40 = lat[ lat < -40 ];
l65 = lat[ lat < -65 ];
i_65 = np.where( lat == l65[-1] )
i_40 = np.where( lat == l40[-1] )

mf, gs = plt.subplots( 3 , 3 )

dlatc = -52     # central lat
dsig = 8      # width
dstr = 13.0e2   # rane in hPa
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

def splot( lat, pres, u, sam, umax, col='k', cp=0):
    gs[1,cp].plot( lat_p , u , '-', color=col ) ; gs[1,cp].axis( [-70, -30, 0, 20])
    xtics = np.arange(-70,-30,10)
    gs[1,cp].set_xticks(xtics )

    a = list( gs[1,cp].get_position().bounds )
    a[1] = a[1]*1.01
    gs[1,cp].set_position(a)
    gs[1,cp].set_xlabel('Latitude ($^{\circ}$S)')
    gs[1,cp].set_xticklabels( [xtic*-1 for xtic in xtics] )

    refpres, refsam, refu, refumax = calc()
    gs[2,cp].plot( [-6,6] , [0,0] ,'--', linewidth=0.5, color=[0.5, 0.5, 0.5], zorder=1 )
    gs[2,cp].plot( [0,0] , [-5,5] ,'--', linewidth=0.5, color=[0.5, 0.5, 0.5], zorder=2 )
    gs[2,cp].plot(umax -refumax, sam - refsam ,'o', color=col,zorder=5 )
    gs[2,cp].set_xticks( np.arange(-8,9,4) )
    gs[2,cp].axis([-6, 6, -6, 6])
    gs[2,cp].set_xlabel('$\Delta$ Umax (m/s)')
    
    if cp == 0:
        gs[1,cp].set_title('Strength') 
    elif cp == 1: 
        gs[1,cp].set_title('Position') 
    else:
        gs[1,cp].set_title('Width') 
      
    if cp > 0:
        [ msp.set_yticklabels([]) for msp in gs[:,cp] ]
    else:
        #gs[0,0].set_ylabel('Pressure (hPa)')
        gs[1,0].set_ylabel('U (m/s)')
        #gs[2,0].set_ylabel('$\Delta$ Umax (m/s)')
        gs[2,0].set_ylabel('$\Delta$ SAM (hPa)')


# do a trend in strength
pres, sam, u, umax = calc()
splot( lat, pres, u, sam, umax )

for str in np.linspace( dstr*0.8, dstr*1.2, 5 ):
    pres, sam, u, umax = calc( dpdt=str )
    splot( lat, pres, u, sam, umax,col='k', cp=0)

# do a trend in position
pres, sam, u, umax = calc()
#splot( lat, pres, u, sam, umax, col='k',cp=1)

for c in np.linspace( dlatc -2 , dlatc + 8 , 5 ):
    pres, sam, u, umax = calc( lat_c = c )
    splot( lat, pres, u, sam, umax,col='k', cp=1 )

# do a trend in width
pres, sam, u, umax = calc()
splot( lat, pres, u, sam, umax, col='k' ,cp=2)

for w in np.linspace( dsig*0.8, dsig*1.2, 5 ):
    pres, sam, u, umax = calc( sig = w )
    splot( lat, pres, u, sam, umax,col='k' , cp=2 )
   
for sp in [0,1,2]:
  plt.delaxes( gs[0,sp] )
  
plt.subplots_adjust(hspace=0.45, wspace=0.1, right=0.7)

x = np.arange(-8,8)

 
plt.savefig('sam_v_jet_theory.pdf',format='pdf',bbox_inches='tight')
