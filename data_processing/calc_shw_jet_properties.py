"""
Calculate the kinematic properties of the SH westerly surface jet from zonal wind 
data.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import numpy as np

def jetprop(uas, lat):
    """ Computes and returns the kinematic properties of the jet.   
    
    Parameters:
    -----------
        uas : array
            A 2-d array, which gives the timeseries of zonal mean zonal wind. The
            time must be in the zeroth dimension, and lat in dimension 1.
        lat : array
            The latitudes associated with the 0th dimension on uas.
            
    Returns:
    --------
    jetmax : array
        The timeseries of the jet strength (largest values btwn 20 and 70S).
    latofmax : array 
        Timeseries of the position, in degrees, of the jet maximum
    latn : array
        Timeseries of the northern edge of the jet.
    lats : array
        Timeseries of the southern edge of the jet.
    jetwidth :  array  
        Timeseries of the jet width, which is latn - lats.
        
    """
    # select the sub-region between 20 and 70S.
    region = (lat>-70) & (lat<-20)
    rlat = lat[region]
    ruas = uas[: ,region]
    
    # if latitude goes in the "wrong" direction the reverse it.
    if rlat[10] < rlat[1]:
        rlat = rlat[::-1]
        ruas = ruas[:, ::-1] 
    
    n = uas.shape[0]

    # Initialize some arrays.
    jetmax = np.zeros(n)    # Speed of the jet at it's maximum btwn 20 and 70S
    latofmax = np.zeros(n)  # Position of jetmax in degrees S.
    jetwidth = np.zeros(n)  # Range of latitude btwn 20-70S where uas > 0.
    latn = np.zeros(n)      # northern edge of where uas > 0.
    lats = np.zeros(n)      # southern edge of where uas > 0.
    
    # Define a 0.25 degree grid on which to compute the properties.
    yy = np.linspace(-70,-20,201)

    for t in range(n):
        # Loop over all timesteps and compute the properties of the jet.
        # First intepolate uas to the new 0.25 degree grid.
        u2 = np.interp(yy, rlat,ruas[t, :]) 
        jetmax[t] = u2.max()
        indofmax = u2 == jetmax[t]
        lom = yy[ indofmax ]
        # choose the first if more than one latitude of max (sometimes 2).
        latofmax[t] = lom[0] if lom.shape !=() else lom 

        lats_of_westerlies = yy[u2 >= 0.]
        latn[t] = lats_of_westerlies.max()
        lats[t] = lats_of_westerlies.min()
        jetwidth = latn - lats

    return  jetmax, latofmax, latn, lats, jetwidth    