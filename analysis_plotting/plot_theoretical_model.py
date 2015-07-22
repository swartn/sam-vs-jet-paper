"""
A theoretical model of the jet response to SAM changes.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
plt.close('all')
plt.ion()
import scipy as sp
from scipy.special import erf
import brewer2mpl

lat = np.linspace( -70 , -20 , 100 ); # latitudes
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

mf, gs = plt.subplots( 3 , 3)
plt.subplots_adjust(wspace=0.1)
sp_labs = ['a)', 'b)', 'c)', 'd)', 'e)', 'f)']

strength0 = 7 # m/s
position0 = -48 # degrees
width0    =  np.sqrt(32) # degrees latitude
    
def sam_model(strength, position, width):
    """ Generates a gaussian jet with the properties described by strength, position
    and width on the latitude grid given in y. Then it uses the generated zonal windspeed 
    and indefinitely integrates to find the pressure via the inverted geostrophic relationship, 
    and finally calculates the sam index, which is returned"""

    # Generate the grid information 
    y = np.linspace(-70, -20, 100)
    deg2rad = np.pi / 180 # conversion
    f = 2. * 2. * np.pi / ( 3600 * 24 ) * np.sin( deg2rad * y.mean() ) # coriolis: f-plane
    dy_meters = y[1] - y[0]
    dist = ( y / y ) * ( 111120 *dy_meters )  ; # distance between latitudes in meters
    rho = 1.2 #density of air
    
    # Generate the gaussian jet
    u = strength * np.exp( -1*( (y - position)**2 / ( 2*width )**2 ) )
 
    # invert the geostrophic relationship
    dPdy = -1*( u*f*rho )  
    
    # integrate to get pressure
    P = np.cumsum( dPdy * dist )
    
    # compute the SAM index as P40 - P65  
    sam = ( P[np.where( abs(y+40) == min(abs(y+40)) )] - P[np.where( abs(y+65) == min(abs(y+65)) )] )/100.
    return (P+985e2)/100, sam, u, max(u)

def splot( lat, pres, u, sam, param, param0, col='k', cp=0):
    gs[0,cp].plot( lat , pres , '-', color=col ) ; gs[0,cp].axis( [-70, -30, 980, 1015])
    gs[1,cp].plot( lat , u , '-', color=col ) ; gs[1,cp].axis( [-70, -30, 0, 10])
    gs[0,cp].set_xticklabels([])
    gs[0,cp].yaxis.set_major_locator( mticker.MaxNLocator(6, prune='both'))
    xtics=np.arange(-70,-30,10)
    gs[1,cp].set_xticks(xtics )
    gs[0,cp].set_xticks(xtics )

    a = list( gs[1,cp].get_position().bounds )
    a[1] = a[1]*1.01
    gs[1,cp].set_position(a)
    gs[1,cp].set_xlabel('Latitude')

    refpres, refsam, refu, refStrength = sam_model(strength0, position0, width0)
    gs[2,cp].plot( param-param0, sam - refsam,'o', color=col,zorder=5 )
    gs[2,cp].plot( [-10,10] , [0,0] ,'--k', linewidth=0.5, color=[0.5, 0.5, 0.5] ,zorder=1)
    gs[2,cp].plot( [0,0] , [-5,5] ,'--k',linewidth=0.5, color=[0.5, 0.5, 0.5], zorder=2)
    gs[2,cp].set_ylim([-5, 5])    

    
    if cp == 0:
        gs[1,cp].set_title('Strength') 
    elif cp == 1: 
        gs[1,cp].set_title('Position') 
    else:
        gs[1,cp].set_title('Width') 
      
    if cp > 0:
        [ msp.set_yticklabels([]) for msp in gs[:,cp] ]
    else:
        gs[0,0].set_ylabel('Pressure (hPa)')
        gs[1,0].set_ylabel('U (m/s)')
        gs[2,0].set_ylabel('$\Delta$ SAM (hPa)')

col = cmap=brewer2mpl.get_map('RdBu', 'diverging', 8,reverse=True).mpl_colors

# do a trend in Strength
for i,str in enumerate( np.linspace( strength0*0.75, strength0*1.25, 8 ) ):
    pres, sam, u, Strength = sam_model(strength=str, position=position0, width=width0 )
    splot( lat, pres, u, sam, str, strength0,col=col[i], cp=0)

gs[2,0].set_xlabel('$\Delta$ Strength (m/s)')
gs[2,0].set_xlim([-5, 5])
    
# do a trend in position
refpres, refsam, refu, refStrength = sam_model(strength0, position0, width0)
for i,pos in enumerate( np.linspace( position0+4, position0-4, 8 ) ):
    pres, sam, u, Strength = sam_model(strength=strength0, position=pos, width=width0 )
    splot( lat, pres, u, sam, pos, position0,col=col[i], cp=1)
    print pos, sam - refsam
    
gs[2,1].set_xlabel('$\Delta$ pos. ($^{\circ}$ lat.)')
gs[2,1].set_xlim([-5, 5])

# do a trend in width
for i,wid in enumerate( np.linspace( width0*0.75, width0*1.25, 8 ) ):
    pres, sam, u, Strength = sam_model(strength=strength0, position=position0, width=wid )
    splot( lat, pres, u, sam, wid, width0,col=col[i], cp=2)
gs[2,2].set_xlabel('$\Delta$ width ($^{\circ}$ lat.)')
gs[2,2].set_xlim([-5, 5])    

for sp in [0,1,2]:
  plt.delaxes( gs[0,sp] )
  gs[1,sp].text(-67, 8.5, sp_labs[sp])
  gs[2,sp].text(-4.25, 3.5, sp_labs[sp+3])

plt.savefig('../plots/gaussian_jet.pdf',format='pdf',bbox_inches='tight')
