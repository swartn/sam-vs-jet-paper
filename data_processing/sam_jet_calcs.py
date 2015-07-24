"""
Calculate the SAM index from a netCDF file containing sea-level pressure.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import numpy as np
import pandas as pd
import cdo as cdo; cdo = cdo.Cdo() # recommended import
import os
os.system( 'rm -rf /tmp/cdo*') # clean out tmp to make space for CDO processing.
import cmipdata as cd
from netCDF4 import Dataset

def calc_sam(psl_file, varname, start_date='1871-01-01', end_date='2013-12-31'):
    """
    Compute the SAM index as the pressure difference between 40 and 65S
    
    Parameters:
    -----------
        psl_file : str
            The name of the **zonal meaned** SLP netcdf file to compute the SAM
            from. Can be a full path.
        varname : str
            The name of the Sea Level Pressure variable in psl_file.
    
    Returns:
    -------
        sam : array
            The calculated SAM index
    """
    
    # Extract the pressure at 40 and 65S
    (head, tail) = os.path.split(psl_file)
    ofile_40s = os.path.join(head, 'p40s_' + tail)
    ofile_60s = os.path.join(head, 'p65s_' + tail)
    ofile_sam = os.path.join(head, 'SAM_' + tail)
    
    cdo.remapnn('lon=0/lat=-40.0', input=psl_file, output=ofile_40s)
    cdo.remapnn('lon=0/lat=-65.0', input=psl_file, output=ofile_60s)

    # Compute the SAM index
    cdo.sub(input=ofile_40s + ' ' + ofile_60s, output=ofile_sam, 
            options='-f nc -b 64')

    # load the data and make dataframes
    sam = cd.loadvar(ofile_sam, varname, start_date=start_date,
                     end_date=end_date)
    
    # cleanup
    for f in [ofile_40s, ofile_60s, ofile_sam]:
        os.remove(f)
        
    return sam

def calc_marshall_sam(psl_file, varname, start_date='1871-01-01', end_date='2013-12-31'):
    """
    Compute the SAM index as the pressure difference between 40 and 65S only
    using data from the 12 Marshall (2003) locations.
    
    Parameters:
    -----------
        psl_file : str
            The name of the **zonal meaned** SLP netcdf file to compute the SAM
            from. Can be a full path.
        varname : str
            The name of the Sea Level Pressure variable in psl_file.
    
    Returns:
    -------
        dft : pandas DataFrame
            The calculated SAM index, presure at 40 and 65S.
    """

    # Marshall locations
    mlat40s = np.array([46.9, 37.8, 42.9, 43.5, 39.6, 40.4])*-1
    mlon40s = np.array([37.9, 77.5, 147.3, 172.6, -73.1, -9.9])   
    mlat65s = np.array([70.8, 67.6, 66.6, 66.3, 66.7, 65.2])*-1
    mlon65s = np.array([11.8, 62.9, 93.0, 110.5, 140.0, -64.3])
    
    # load the data 
    dims = cd.get_dimensions(psl_file, varname, toDatetime=True)
    p40 = np.zeros((len(dims['time']), 6))
    p65 = np.zeros((len(dims['time']), 6))   
    ncvar = Dataset(psl_file).variables[varname]
    
    for k in range(6):
    # loop over the six stations at each lat and get data at each one.
        var = cdo.remapnn('lon=' + str( mlon40s[k] ) + '/lat='\
			   + str( mlat40s[k] )
			   , input=('-selvar,' + varname + ' ' + psl_file)
			   , returnMaArray=varname).squeeze()
        p40[:,k] = scale(ncvar, var)
	    
	var2 = cdo.remapnn('lon=' + str( mlon65s[k] ) + '/lat='\
			   + str( mlat65s[k] )
			   , input=('-selvar,' + varname + ' ' + psl_file)
			   , returnMaArray=varname).squeeze()
	p65[:,k] = scale(ncvar, var2)
    
    # Now create the mean pressure at 40S and 65S and return
    s40s = pd.Series(p40.mean(axis=1), index=dims['time'])
    s65s = pd.Series(p65.mean(axis=1), index=dims['time'])
    return s40s, s65s
    
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

def scale(ncvar, var):
    """Apply any scaling and offsetting needed to a netCDF variable ncvar
    """
    try:
        var_offset = ncvar.add_offset
    except:
        var_offset = 0
    try:
        var_scale = ncvar.scale_factor
    except:
        var_scale = 1   

    var = var*var_scale + var_offset
    #return var
    return np.squeeze(var)
    
def plot_stn_locs(lats, lons):
    """ Plots lat, lon positions on a basemap
    """
    from mpl_toolkits.basemap import Basemap, addcyclic
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    plt.ion()
    plt.close('all')
    font = {'size'   : 12}
    plt.rc('font', **font)

    m = Basemap(projection='ortho', lon_0=0,lat_0=-90,)
    m.drawcoastlines(linewidth=1.25)
    m.fillcontinents(color='0.8')
    m.drawparallels(np.arange(-80,81,20),labels=[1,0,0,0])
    m.drawmeridians(np.arange(0,360,30),labels=[1,1,1,1])
    x, y = m(lons, lats)
    m.plot(x,y, 'or', markersize=8)
