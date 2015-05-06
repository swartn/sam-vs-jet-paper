""" Build a download script for ESGF data.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>

"""
from pyesgf.search import SearchConnection
import re
import subprocess

def get_cmip5(experiment, variable, time_frequency, models, ensembles):  
    conn = SearchConnection('http://pcmdi9.llnl.gov/esg-search', distrib=True)
    ctx = conn.new_context(project='CMIP5', experiment=experiment, 
                           time_frequency=time_frequency, variable=variable, 
                           model=models, ensemble=ensembles)

    a = ctx.get_download_script()
    
    # write the download script out
    with open('getc5.sh','w') as f:
        f.write(a)
        
    # run the download script
    subprocess.Popen(['chmod', 'u+x', 'getc5.sh']).wait()
    subprocess.Popen(['./getc5.sh']).wait()  
    
    # delete any empty files.
    subprocess.Popen(['find', './*.nc', '-type', 'f', '-size', '0', 
                      '-delete']).wait() 
    
if __name__=='__main__':
    
    model_list = ['ACCESS1-0', 'ACCESS1-3', 'BNU-ESM', 'CMCC-CMS', 'CMCC-CM',
              'CNRM-CM5', 'CSIRO-Mk3-6-0', 'CanESM2', 
              'GISS-E2-H-CC', 'GISS-E2-H', 'GISS-E2-R-CC', 'GISS-E2-R',
              'HadCM3', 'HadGEM2-AO', 'HadGEM2-CC', 'HadGEM2-ES', 
              'IPSL-CM5A-LR', 'IPSL-CM5A-MR', 'IPSL-CM5B-LR', 'MIROC-ESM-CHEM',
              'MIROC-ESM', 'MIROC5', 'MPI-ESM-LR','MPI-ESM-MR','MRI-CGCM3',
              'NorESM1-ME', 'NorESM1-M', 'bcc-csm1-1-m', 'bcc-csm1-1','inmcm4'
              ]    
    
    data_to_get = {'experiment' : ['historical', 'rcp45'], 
                   'time_frequency' :'mon', 
                   'models' : model_list, 
                   'ensembles' : 'r1i1p1'
                  }
    
    get_cmip5(variable='uas', **data_to_get)
    get_cmip5(variable='psl', **data_to_get)
    get_cmip5(variable='tauu', **data_to_get)
    
    