import numpy as np
import matplotlib.pyplot as plt
plt.close('all')
plt.ion()
font = {'size'   : 16}
plt.rc('font', **font)
import matplotlib as mpl
import trend_ts

f1 = plt.figure(1)

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
    print sam
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
        width = width +  width_trend/10.
        #f1.gca().plot(t, position,'ro')

        # get the sam index for the specified jet properties
        sam[t] = sam_model(strength, position, np.sqrt(width*0.7) )    

    sam_trend = trends( np.squeeze(sam), years )
    
    return sam_trend     

# setup some figures:
f2, gs = plt.subplots(3,2, sharey=True)
f2.set_size_inches((8,8), forward=True )

###############################################################3
#      First the varying trends
###############################################################3

# Define the climatologies and the trends for 30 pretend models
initial_strength = np.linspace(5, 10, 30)
strength_trends = np.linspace(0.1, 0, 30)

initial_position = np.linspace(-43, -53, 30)
position_trends = np.linspace(-0.4, 0, 30)

initial_width = np.linspace(30, 35, 30)
width_trends = np.linspace(-0.04, 0.2, 30)

# Test a range of strength trends
mod_sam_trends = []
for i in range(30):
    sam_trend = gen_timeseries( strength=initial_strength[i], position=initial_position[i] 
    , width=initial_width[i], strength_trend=strength_trends[i], position_trend=position_trends[i], width_trend=width_trends[i] )
    gs[0,0].plot( strength_trends[i], sam_trend, 'ro')
    gs[0,1].plot( initial_strength[i], sam_trend, 'ro')
    gs[1,0].plot( position_trends[i], sam_trend, 'ro')
    gs[1,1].plot( initial_position[i], sam_trend, 'ro')
    gs[2,0].plot( width_trends[i], sam_trend, 'ro') 
    gs[2,1].plot( initial_width[i], sam_trend, 'ro')   
    mod_sam_trends.append( sam_trend)

mod_sam_trends = np.array( mod_sam_trends )  
strength_20CR       =  6.7 #initial_strength.mean()
position_20CR       =  -53 #initial_position.mean()
width_20CR          =  32.5 #initial_width.mean() 
strength_trend_20CR =  0.25# strength_trends.mean()
position_trend_20CR =  0# position_trends.mean() 
width_trend_20CR    = -0.15

sam_trend_20CR = gen_timeseries(strength=strength_20CR, position=position_20CR, width=width_20CR, strength_trend=strength_trend_20CR, position_trend=position_trend_20CR, width_trend=width_trend_20CR)    

# adjust the plots    
gs[0,0].set_ylim([-0.5,1])     
for ax in gs.flatten():
    ax.yaxis.set_major_locator( mpl.ticker.MaxNLocator(6))
    ax.xaxis.set_major_locator( mpl.ticker.MaxNLocator(6))


ft, axa = plt.subplots(1,2)

def mod_trend_plot(mod_trends, axtrend, k=1):
    mod_5thp = np.percentile( mod_trends, 5 )
    mod_95thp = np.percentile( mod_trends, 95 )
    axtrend.plot( [ k , k ] , [ mod_5thp  , mod_95thp ],'r', linewidth=4, alpha=0.25 )
    axtrend.plot( k , np.mean( mod_trends) ,'_r',ms=15,mew=2, label='CMIP5')

    
mod_trend_plot( mod_sam_trends, axa[0]) 
axa[0].plot( 1, sam_trend_20CR, 'gx')

mod_trend_plot( strength_trends, axa[1]) 
axa[1].plot( 1, strength_trend_20CR, 'gx')


    
    
    