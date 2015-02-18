import numpy as np
import matplotlib.pyplot as plt
plt.close('all')
plt.ion()

def gauss(strength=1, position=0, width=1, y=np.linspace(-2,2,100)):
    g = strength * np.exp( -1*( (y - position)**2 / ( width*1.4 ) ) )
    return y, g
    
def press( y, u):
    """ Takes in the zonal windspeed,u, at positions,y, and indefinitely 
    integrates to find the pressure via the geostrophic relationship"""

    # Get Coriolis and grid spacing
    deg2rad = np.pi / 180 # conversion
    f = 2. * 2. * np.pi / ( 3600 * 24 ) * np.sin( deg2rad * y.mean() ) # coriolis: f-plane
    dy_meters = y[1] - y[0]
    dist = ( y / y ) * ( 111120 *dy_meters )  ; # distance between latitudes in meters
    rho = 1.2 #density of air
    
    # invert the geostrophic relationship
    dPdy = -1*( u*f*rho )  
    
    # integrate to get pressure
    P = np.cumsum( dPdy * dist )
    return P
    
if __name__ == "__main__":
    y, g = gauss(strength=7, position=-52, width=30, y=np.linspace(-80,-20,100))
    P = press( y, g)
    f, axa = plt.subplots(2,1)
    axa[0].plot(y, P/100)
    axa[1].plot(y, g)
