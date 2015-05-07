""" Retrieve CFSR slp, u10m and uflx data from the NCAR RDA website and join it 
    together.
    
    NOTE: You must have credentials for http://rda.ucar.edu/ and enter them
          into the wget files.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>

"""
import subprocess
import glob
import os
import mv_to_dest

def get_cfsr_data(destination='.'):

    # Define the wget files:
    wget_ouput_files = {'get_cfsr_psl_test.csh' : 'pgblnl.gdas.PRMSL.MSL.grb2' , 
                  'get_cfsr_u10m_test.csh' : 'pgbl01.gdas.WND.10m.grb2.subset',
                  'get_cfsr_uflx_test.csh' : 'pgbl01.gdas.U_FLX.SFC.grb2'
                 } 

    for wget, output in wget_ouput_files.iteritems(): 
        # make sure permissions are set on the wget
        subprocess.Popen(['chmod', 'u+x', wget])

        # download the data, which is specified in the defined wget script.
        subprocess.Popen(['./' + wget]).wait()

        # convert from grib2 to netcdf using cdo
        subprocess.Popen(['cdo', '-f', 'nc', 'copy', output, output + '.nc']).wait()
       
        # remove grib2 version
        os.remove(output) 
        
        # Change variables to my standard names / units
        if wget == 'get_cfsr_psl_test.csh':
            subprocess.Popen(['cdo', 'chname,prmsl,slp', 
                              output + '.nc',  'CFSR_slp.mon.mean.nc']).wait()
            os.remove(output + '.nc')

        if wget == 'get_cfsr_u10m_test.csh':
            subprocess.Popen(['cdo', 'chname,10u,u10m','-selvar,10u', 
                              output + '.nc',  'CFSR_u10m.mon.mean.nc']).wait()
            os.remove(output + '.nc')

        if wget == 'get_cfsr_uflx_test.csh':
            os.rename(output + '.nc', 'CFSR_uflx.mon.mean.nc')
            
    # move to destination
    files = glob.glob('CFSR*.mon.mean.nc')
    mv_to_dest.mv_to_dest(destination, *files)    
          
if __name__=='__main__':
    get_cfsr_data(destination='../data/')
