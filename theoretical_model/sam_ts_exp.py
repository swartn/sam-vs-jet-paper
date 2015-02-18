import numpy as np
import matplotlib.pyplot as plt
plt.close('all')
plt.ion()
font = {'size'   : 16}
plt.rc('font', **font)
import matplotlib as mpl
import trend_ts
import brewer2mpl

#fig,axa = plt.subplots(2,1)

def trends( data, year ):
    '''Calculate linear trend in the sam of datframe dfp between years ys and ye inclusive'''
    slope , conf_int , p_value, yhat, intercept = trend_ts.trend_ts( year , data )
    return slope*10 #, yhat

def sam_model(strength, position, width,col):
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
    #axa[0].plot(y, P, color=col, linewidth=2)
    #axa[1].plot(y, u, color=col, linewidth=2)
    return sam

def gen_timeseries(strength=7, position=-48, width=30, strength_trend=0, position_trend=0, width_trend=0):
    """ Generate a 60-year time-series of jet properties and sam, starting from the properties
    strength, position and width, and changing annually according to strenght_trend, position_trend
    and width_trend. At the end, the sam trend is calculated and returned.
    """
    years = np.arange(50)
    sam = np.zeros( ( len(years),1) ) 
    col = cmap=brewer2mpl.get_map('RdBu', 'diverging', 10).mpl_colors
    for t in years:
	# apply the linear trends, divde by 10 to move from /decade to /year
	strength = strength + strength_trend/10.
        position = position + position_trend/10.
        width = width +  width_trend/10.
        #f1.gca().plot(t, position,'ro')

        # get the sam index for the specified jet properties
        sam[t] = sam_model(strength, position, np.sqrt(width*0.7),col[0] )    
        #print width, sam[t]

    sam_trend = trends( np.squeeze(sam), years )
    
    return sam_trend     

# setup some figures:
#f2, gs = plt.subplots(3,2, sharey=True)
#f2.set_size_inches((8,8), forward=True )

###############################################################3
#      First the varying trends
###############################################################3

# Define the climatologies and the trends for 30 pretend models

# position of the CMIP5 jets over 1950-1960
modpos = np.array([-50.88888889, -51.12037037, -47.7037037 , -46.26851852,
       -48.2037037 , -50.43518519, -47.48148148, -49.26851852,
       -50.37962963, -49.40740741, -49.80555556, -48.4537037 ,
       -49.21296296, -51.10185185, -49.10185185, -50.5       ,
       -43.53703704, -45.7962963 , -44.73148148, -46.01851852,
       -45.91666667, -45.5       , -48.67592593, -47.98148148,
       -52.71296296, -52.38888889, -52.37037037, -51.48148148,
       -49.00925926, -50.01851852])

for ipa in modpos:
    sam_trend = gen_timeseries(position=ipa, position_trend=-0.3)
    plt.plot(ipa, sam_trend, 'ro')
    
plt.xlabel('Initial position ($^{\circ}$S)')
plt.ylabel('SAM trend (hPa/dec.)')
    
    