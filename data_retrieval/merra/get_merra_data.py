""" Retrieve slp, uwnd and uflx data for MERRA via ftp from pre-defined 
    lists of urls. urls were created with the tool at:

        http://disc.sci.gsfc.nasa.gov/daac-bin/FTPSubset.pl?LOOKUPID_List=MATMNXSLV

    Files arrive in monthly chunks and are concatenated with cdo
   
.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import subprocess

def fetch_join_merra(url_file, varname):
    subprocess.Popen(['wget', '--content-disposition', '-i', url_file]).wait()
    
    subprocess.Popen(['cdo', 'mergetime', 'MERRA*', 
                      'MERRA_' + varname + 'mon.mean.nc']).wait()
    subprocess.Popen(['rm', '-f', '*SUB.nc']).wait() # clean up

                  
if __name__=='__main__':
    varnames = ['slp', 'u10m', 'uflx']
    for v in varnames:
        fetch_join_merra('wget_merra_' + v, v)

        
  