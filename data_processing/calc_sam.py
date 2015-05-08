"""
Calculate the SAM index from a netCDF file containing sea-level pressure.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import cdo as cdo; cdo = cdo.Cdo() # recommended import
import os
os.system( 'rm -rf /tmp/cdo*') # clean out tmp to make space for CDO processing.
import cmipdata as cd

def calc_sam(psl_file, varname, start_date='1871-01-01', end_date='2013-12-31'):
    """
    Compute the SAM index as the pressure difference between 40 and 65S
    
    Parameters:
    -----------
        psl_file : str
            The name of the SLP netcdf file to compute the SAM from. Can be a full
            path.
        varname : str
            The name of the Sea Level Pressure variable in psl_file.
    
    Returns:
    -------
        sam : array
            The calculated SAM index
    """
    
    # Extract the pressure at 40 and 65S
    (head, tail) = os.path.split(path)
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
