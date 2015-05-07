""" Retrieve slp, uwnd and uflx data for MERRA via ftp from pre-defined 
    lists of urls. urls were created with the tool at:

        http://disc.sci.gsfc.nasa.gov/daac-bin/FTPSubset.pl?LOOKUPID_List=MATMNXSLV

    Files arrive in monthly chunks and are concatenated with cdo
   
.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import subprocess
import glob
import os
import mv_to_dest

def get_merra_data(destination='.'):
    varnames = ['slp', 'u10m', 'uflx']
    for var in varnames:   
        subprocess.Popen(['wget', '--content-disposition', '-i', url_file + 
                          var]).wait()
        
        # time-merge the data
        subprocess.Popen(['cdo', 'mergetime', 'MERRA*', 
                         'MERRA_' + var + 'mon.mean.nc']).wait()
        
        # Remove input files
        files = glob.glob('*SUB.nc')
        for f in files:
            os.remove(f)
        
    # move to destination
    files = glob.glob('MERRA*.mon.mean.nc')
    mv_to_dest.mv_to_dest(destination, *files)   
                  
if __name__=='__main__':
    get_merra_data(destination='../data/')

        
  