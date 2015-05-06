#!/usr/bin/python

""" Retrieve and time-merge the slp and uwnd data for the Twentieth Century 
Reanalysis (20CR) ensemble from the nersc portal.

Requires cdo

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import urllib
import subprocess
import numpy

def fetch_data():
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
    subprocess.Popen(['cdo', 'mergetime', 'prmsl_*.mnmean.nc',
                  'prmsl_1871-2012.mon.mean.nc'])

    subprocess.Popen(['cdo', 'mergetime', 'u10m_*.mnmean.nc',
                  'u10m_1871-2012.mon.mean.nc'])  
                  
if __name__=='__main__':
    import timeit
    print '20CR download time:'
    print(timeit.timeit("fetch_data()", setup="from __main__ import fetch_data",
          number=1) )
    
                  