import numpy as np
import matplotlib.pyplot as plt
plt.close('all')
plt.ion()
font = {'size'   : 16}
plt.rc('font', **font)
import matplotlib as mpl
import trend_ts

#f1 = plt.figure(1)

def trends( data, year ):
    '''Calculate linear trend in the sam of datframe dfp between years ys and ye inclusive'''
    slope , conf_int , p_value, yhat, intercept = trend_ts.trend_ts( year , data )
    return slope*10 #, yhat

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
    #f1.gca().plot(position, sam, 'ro')
    return sam

def gen_timeseries(strength=7, position=-48, width=30, strength_trend=0, position_trend=0, width_trend=0):
    """ Generate a 60-year time-series of jet properties and sam, starting from the properties
    strength, position and width, and changing annually according to strenght_trend, position_trend
    and width_trend. At the end, the sam trend is calculated and returned.
    """
    years = np.arange(60)
    sam = np.zeros( ( len(years),1) ) 

    for t in years:
	# apply the linear trends, divde by 10 to move from /decade to /year
	strength = strength + strength_trend/10.
        position = position + position_trend/10.
        width = width + t*width_trend
        #f1.gca().plot(t, position,'ro')

        # get the sam index for the specified jet properties
        sam[t] = sam_model(strength, position, np.sqrt(width) )    

    sam_trend = trends( np.squeeze(sam), years )
    
    return sam_trend     

# setup some figures:
f2, gs = plt.subplots(3,2, sharey=True)
f2.set_size_inches((8,8), forward=True )

###############################################################3
#      First the varying trends
###############################################################3
# Test a range of strength trends
strength_trends = np.linspace(0, 0.4, 30)
for strength_trend in strength_trends:
    sam_trend = gen_timeseries( strength_trend=strength_trend )
    gs[0,0].plot( strength_trend, sam_trend, 'ro')

# Test a range of position trends
position_trends = np.linspace(-1, 0, 30)
initial_position = np.linspace(-44, -54, 30)

for i, position_trend in enumerate(position_trends):
    sam_trend = gen_timeseries( position=initial_position[i], position_trend=position_trend )
    gs[1,0].plot( position_trend, sam_trend, 'ro')
    
# Test a range of width trends
width_trends = np.linspace(-0.4, 0.6, 30)
for width_trend in width_trends:
    sam_trend = gen_timeseries( width_trend=width_trend )
    gs[2,0].plot( width_trend, sam_trend, 'ro')   

###############################################################3
#      Now the varying climatologies
###############################################################3

# Test a range of initial strengths and a uniform strengthening
strength_trend = 0.2 # m/s per decade
initial_strength = np.linspace(5, 10, 30)
for strength in initial_strength:
    sam_trend = gen_timeseries( strength=strength, strength_trend=strength_trend )
    gs[0,1].plot( strength, sam_trend, 'ro')
    
# Test a range of initial positions and a uniform poleward shift
position_trend = -0.5 # degrees per decade
initial_position = np.linspace(-54, -44, 30)
for position in initial_position:
    sam_trend = gen_timeseries( position=position, position_trend=position_trend )
    gs[1,1].plot( position, sam_trend, 'ro')
	 
# Test a range of initial widths and a uniform widening
width_trend = 0.2 # degrees per decade
initial_width = np.linspace(30, 33, 30)
for width in initial_width:
    sam_trend = gen_timeseries( width=width, width_trend=width_trend )
    gs[2,1].plot( width, sam_trend, 'ro')    

# adjust the plots    
gs[0,0].set_ylim([-0.25,1])     
for ax in gs.flatten():
    ax.yaxis.set_major_locator( mpl.ticker.MaxNLocator(6))
    ax.xaxis.set_major_locator( mpl.ticker.MaxNLocator(6))
    