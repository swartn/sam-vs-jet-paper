""" Retrieve slp, uwnd and uflx data for R1, R2 and 20CR from
the  NOAA ESRL website.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>

"""
import urllib
import subprocess
import glob
import os
import cdo; cdo = cdo.Cdo()
os.system('rm -f /tmp/cdo*')
import mv_to_dest

def get_r1_r2_20cr_esrl_data(destination='.'):        
    # some details of the base urls / paths to data
    baseurl = 'ftp://ftp.cdc.noaa.gov/Datasets/'
    r1p = 'ncep.reanalysis.derived/'  # R1 path
    r2p = 'ncep.reanalysis2.derived/' # R2 path
    tcp = '20thC_ReanV2/Monthlies/'  # 20CR
    
    # list of tuples specifying data paths/filenames and outfilename 
    data_path_ofile = [
         (r1p + 'surface/slp.mon.mean.nc', 'R1_slp.mon.mean.nc'),
         (r1p + 'surface_gauss/uwnd.10m.mon.mean.nc', 'R1_u10m.mon.mean.nc'),
         (r1p + 'surface_gauss/uflx.sfc.mon.mean.nc', 'R1_uflx.mon.mean.nc'),
         (r2p + 'surface/mslp.mon.mean.nc', 'R2_slp.mon.mean.nc'),
         (r2p + 'gaussian_grid/uwnd.10m.mon.mean.nc', 'R2_u10m.mon.mean.nc'),
         (r2p + 'gaussian_grid/uflx.sfc.mon.mean.nc', 'R2_uflx.mon.mean.nc'),
         (tcp + 'monolevel/prmsl.mon.mean.nc', '20CR_slp.mon.mean.nc'),
         (tcp + 'gaussian/monolevel/uwnd.10m.mon.mean.nc', '20CR_u10m.mon.mean.nc'),
         (tcp + 'gaussian/monolevel/uflx.mon.mean.nc', '20CR_uflx.mon.mean.nc')
                      ] 
    # Download the data
    for (path, ofile) in data_path_ofile:
        print 'Saving: ' + baseurl + path + '\nas: ' + ofile +'\n\n'
        urllib.urlretrieve(baseurl + path, ofile)
        
    # Change some variable names
    for r in ['R1', 'R2', '20CR']:
        cdo.chname('uwnd,u10m', input=r + '_u10m.mon.mean.nc', 
                   output='tmp.nc')
        os.rename('tmp.nc', r + '_u10m.mon.mean.nc')
    
    cdo.chname('mslp,slp', input='R2_slp.mon.mean.nc', output='tmp1.nc')
    os.rename('tmp1.nc',  'R2_slp.mon.mean.nc')
    cdo.chname('prmsl,slp', input='20CR_slp.mon.mean.nc', 
               output='tmp2.nc')
    os.rename('tmp2.nc',  '20CR_slp.mon.mean.nc')    
    
    # make sure 20CR grids are not generic 
    cdo.selvar('uflx', input='20CR_uflx.mon.mean.nc', output='tmp3.nc')
    os.rename('tmp3.nc',  '20CR_uflx.mon.mean.nc')    
    cdo.selvar('u10m', input='20CR_u10m.mon.mean.nc', output='tmp4.nc')
    os.rename('tmp4.nc',  '20CR_u10m.mon.mean.nc')  
    cdo.selvar('slp', input='20CR_slp.mon.mean.nc', output='tmp5.nc')
    os.rename('tmp5.nc',  '20CR_slp.mon.mean.nc')      

    # move to destination
    files = glob.glob('*.mon.mean.nc')
    mv_to_dest.mv_to_dest(destination, *files)        
                  
if __name__=='__main__':
    get_r1_r2_20cr_esrl_data(destination='./data/')
    
        
  