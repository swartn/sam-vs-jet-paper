""" Retrieve slp, uwnd and uflx data for MERRA via ftp from pre-defined 
    lists of urls. urls were created with the tool at:

        http://disc.sci.gsfc.nasa.gov/daac-bin/FTPSubset.pl?LOOKUPID_List=MATMNXSLV

    Files arrive in monthly chunks and are concatenated with cdo
   
.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import subprocess
import glob
import os
import cdo; cdo = cdo.Cdo()
import mv_to_dest

def get_merra_data(destination='.', src_path='./'):
    varnames = ['slp', 'u10m', 'uflx']
    for var in varnames:   
        wget_file = os.path.join(src_path, 'wget_merra_' + var)
        subprocess.Popen(['wget', '--content-disposition', '-i', wget_file]).wait()
        
        # time-merge the data
        subprocess.Popen(['cdo', 'mergetime', 'MERRA*', 
                         'MERRA_' + var + '.mon.mean.nc']).wait()
        
        # Remove input files
        files = glob.glob('*SUB.nc')
        for f in files:
            os.remove(f)
    
    # Change some variable names
    cdo.chname('taux,uflx', input='MERRA_uflx.mon.mean.nc', output='tmp1.nc')
    os.rename('tmp1.nc',  'MERRA_uflx.mon.mean.nc')
       
    # move to destination
    files = glob.glob('MERRA*.mon.mean.nc')
    mv_to_dest.mv_to_dest(destination, *files)   
                  
if __name__=='__main__':
    get_merra_data(destination='../data/')

        
  