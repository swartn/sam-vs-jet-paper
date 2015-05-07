""" Retrieve HadSLP2 from NOAA ESRL and HadSLP2r- reduced variance from the 
Met office website, and do some processing to join them.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>

"""
import urllib
import subprocess    
import os
from netCDF4 import Dataset
import numpy as np
import mv_to_dest

def get_hadslp2r_data(destination='.'):
    # HadSLP2r url at NOAA ESRL
    url_2 = 'ftp://ftp.cdc.noaa.gov/Datasets.other/hadslp2/slp.mnmean.real.nc'

    # HadSLP2r_lowvar url at metoffice
    url_2r_lowvar = ('http://www.metoffice.gov.uk/hadobs/hadslp2/data/' + 
                     'HadSLP2r_lowvar_200501-201212.nc')

    # download the source data
    urllib.urlretrieve(url_2, 'HadSLP2r.mon.mean.nc')
    urllib.urlretrieve(url_2r_lowvar, 'HadSLP2r_lowvar_200501-201212.nc')    

    # Cut the HaSLP2r data from ESRL to be from 1850 to 2005
    subprocess.Popen(['cdo', 'seldate,1850-01-01,2004-12-31', 
                      'HadSLP2r.mon.mean.nc', 
                      'HadSLP2r_185001-200412.mon.mean.nc']).wait()

    # make a dummy file covering 200501-201212 into which we will place the lowvar
    # version of the data from the metoffice. This is necessary because the
    # metoffice nc file grid is rotated, and that is also non CF compliant.
    subprocess.Popen(['cdo', 'seldate,2005-01-01,2012-12-31', 
                      'HadSLP2r.mon.mean.nc', 
                      'HadSLP2r_200501-201212.mon.mean.nc']).wait()

    # Read in the HadSLP2r_lowvar data from the metoffice, and rotate it to have
    # the same orientation as the HadSLP2r data from ESRL above.
    nc = Dataset('HadSLP2r_lowvar_200501-201212.nc', 'r')
    slp = nc.variables['Press'][:]
    nc.close()

    # Reshape the data
    slp = np.reshape(slp, (96,37,72))

    # Open the dummy file and write in the reshaped lowvar data.
    ncout = Dataset('HadSLP2r_200501-201212.mon.mean.nc', 'r+', format='NETCDF3' )
    varout = ncout.variables['slp']
    varout[:] = slp
    ncout.close()

    # Now join the original HadSLP2r (1850-2004) with the lowvar data (2005-2012)
    subprocess.Popen(['cdo', 'mergetime', 
                      'HadSLP2r_185001-200412.mon.mean.nc', 
                      'HadSLP2r_200501-201212.mon.mean.nc',
                      'HadSLP2r_lowvar.mon.mean.nc']).wait()

    # move to destination
    mv_to_dest.mv_to_dest(destination, 'HadSLP2r_lowvar.mon.mean.nc')   

    # cleanup
    infiles = ['HadSLP2r_185001-200412.mon.mean.nc', 
               'HadSLP2r_200501-201212.mon.mean.nc',
               'HadSLP2r_lowvar_200501-201212.nc',
               'HadSLP2r.mon.mean.nc'
              ]
    for f in infiles:
      os.remove(f)
    
if __name__=='__main__':
    get_hadslp2r_data(destination='./data/')
