""" Retrieve slp, uwnd and uflx data for R1, R2 and 20CR from
the  NOAA ESRL website.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>

"""
import urllib
import subprocess


def fetch_data(url, ofile):  
        urllib.urlretrieve(url, ofile)

                  
if __name__=='__main__':
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
    
    for (path, ofile) in data_path_ofile:
        print 'Saving: ' + baseurl + path + '\nas: ' + ofile +'\n\n'
        fetch_data(baseurl + path, ofile)
        
  