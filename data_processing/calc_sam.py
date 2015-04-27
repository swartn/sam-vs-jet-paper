"""
Calculate the SAM index from a netCDF file containing sea-level pressure.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import cdo as cdo; cdo = cdo.Cdo() # recommended import
import os
os.system( 'rm -rf /tmp/cdo*') # clean out tmp to make space for CDO processing.
import cmipdata as cd

def calc_sam(psl_file, varname, pp='', start_date='1871-01-01',
                     end_date='2013-12-31'):
    """
    Compute the SAM index as the pressure difference between 40 and 65S
    
    Parameters:
    -----------
        psl_file : str
            The name of the SLP netcdf file to compute the SAM from.
        varname : str
            The name of the Sea Level Pressure variable in psl_file.
        pp : str
            An option path to prepend to psl_file.
    
    Returns:
    -------
        sam : array
            Teh calculated SAM index
    """
    
    # Extract the pressure at 40 and 65S
    cdo.remapnn('lon=0/lat=-40.0', input=pp + psl_file, output='p40s_' + psl_file)
    cdo.remapnn('lon=0/lat=-65.0', input=pp + psl_file, output='p65s_' + psl_file)

    # Compute the SAM index
    cdo.sub(input='p40s_' + psl_file + ' ' + 'p65s_' + psl_file + ' ', 
            output='SAM_' + psl_file, options='-f nc -b 64')

    # load the data and make dataframes
    sam = cd.loadvar('SAM_' + psl_file, varname, start_date=start_date,
                     end_date=end_date)
    
    # cleanup
    os.system('rm -f p*' + psl_file + ' ' + psl_file + ' ' + 'SAM_' + psl_file)
    return sam
