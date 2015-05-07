#!/usr/bin/python

""" Retrieve and time-merge the slp and uwnd data for the Twentieth Century 
Reanalysis (20CR) ensemble from the nersc portal.

Requires cdo

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import urllib
import subprocess
import os
import glob
import mv_to_dest

def get_20cr_data(destination='.'):
    # 20CR ensemble data is held in yearly files at the url below:
    baseurl = 'http://portal.nersc.gov/pydap/20C_Reanalysis_ensemble'
    slp_path = '/analysis.derived/prmsl/' 
    u10m_path = '/first_guess.derived/u10m/'

    # Fetch data over 1871 to 2012
    for y in xrange(1871, 2013):
        slp_filename = 'prmsl_{year}.mnmean.nc'.format(year=y)
        u10m_filename = 'u10m_{year}.mnmean.nc'.format(year=y)
        urllib.urlretrieve (baseurl + slp_path + slp_filename, slp_filename)
        urllib.urlretrieve (baseurl + u10m_path + u10m_filename, u10m_filename)

    #time-merge the files into one
    prmsl_files = glob.glob('prmsl_*.mnmean.nc')
    subprocess.Popen(['cdo', '-mergetime', ' '.join(prmsl_files),
                      'prmsl_1871-2012.mon.mean.nc']).wait()

    u10m_files = glob.glob('u10m_*.mnmean.nc')
    subprocess.Popen(['cdo', '-mergetime', ' '.join(u10m_files),
                      'u10m_1871-2012.mon.mean.nc'])  

    # Rename variables and files
    subprocess.Popen(['cdo', 'chname,prmsl,slp', 
                      'prmsl_1871-2012.mon.mean.nc',
                      '20CR_slp.mon.mean.nc']).wait()
    os.remove('prmsl_1871-2012.mon.mean.nc')

    os.rename('u10m_1871-2012.mon.mean.nc', '20CR_u10m.mon.mean.nc')

    # move to destination
    files = glob.glob('20CR*.mon.mean.nc')
    mv_to_dest.mv_to_dest(destination, *files)  
    
    # delete old files
    files = glob.glob('*.mnmean.nc')
    for f in files:
        os.remove(f)
                  
if __name__=='__main__':
    get_20cr_data(destination='./data/')   
                  