""" Download psl, uas and tauu fields for 30 CMIP5 models.

    
    NOTE: ESGF openid credentials are required. See
    
        http://pcmdi9.llnl.gov/esgf-web-fe/

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
from pyesgf.search import SearchConnection
import re
import subprocess
import os
import glob
import cmipdata as cd
import mv_to_dest

def fetch_cmip5(experiment, variable, time_frequency, models, ensembles):
    """ Download CMIP5 data for a specified set of facets
    
    Uses pyesgf module to query the ESGF nodes RESTful API, and generate a
    wget script which is then executed.
    
    Input parameters defining facets can be strings or lists of strings.
    """
    conn = SearchConnection('http://pcmdi9.llnl.gov/esg-search', distrib=True)
    ctx = conn.new_context(project='CMIP5', experiment=experiment, 
                           time_frequency=time_frequency, variable=variable, 
                           model=models, ensemble=ensembles, latest=True,
                           replica=True, download_emptypath='unknown')

    a = ctx.get_download_script()
    
    # write the download script out
    with open('getc5.sh','w') as f:
        f.write(a)
        
    # run the download script
    subprocess.Popen(['chmod', 'u+x', 'getc5.sh']).wait()
    subprocess.Popen(['./getc5.sh']).wait()  
    
    # delete any empty files.
    os.system('find ./*.nc -type f -size 0 -delete') 

def get_cmip5_data(destination='.'):
    """
    Fetches CMIP5 data for uas, psl and tauu variables and 30 defined models.
    """
    # List of models to get data for
    model_list = ['ACCESS1-0', 'ACCESS1-3', 'BNU-ESM', 'CMCC-CMS', 'CMCC-CM',
              'CNRM-CM5', 'CSIRO-Mk3-6-0', 'CanESM2', 
              'GISS-E2-H-CC', 'GISS-E2-H', 'GISS-E2-R-CC', 'GISS-E2-R',
              'HadCM3', 'HadGEM2-AO', 'HadGEM2-CC', 'HadGEM2-ES', 
              'IPSL-CM5A-LR', 'IPSL-CM5A-MR', 'IPSL-CM5B-LR', 'MIROC-ESM-CHEM',
              'MIROC-ESM', 'MIROC5', 'MPI-ESM-LR','MPI-ESM-MR','MRI-CGCM3',
              'NorESM1-ME', 'NorESM1-M', 'bcc-csm1-1-m', 'bcc-csm1-1','inmcm4'
              ]    
    
    # Specify general data properties (monthly, ensemble 1, hist/rcp45 experiments)
    data_to_get = {'experiment' : ['historical', 'rcp45'], 
                   'time_frequency' :'mon', 
                   'models' : model_list, 
                   'ensembles' : 'r1i1p1'
                  }
    
    # fetch original data for uas, psl and tauu and time-merge it
    variables = ['uas', 'psl', 'tauu']
    for var in variables:
        fetch_cmip5(variable=var, **data_to_get)
    
        # time-merge the data across the historical and rcp45 experiments
        filepattern = var + '_Amon*.nc'
        ens = cd.mkensemble(filepattern)
        ens = cd.cat_experiments(ens, 'uas', 'historical', 'rcp45') 
        
        for model, experiment, realization, variable, files in ens.iterate():
            for f in files:
                mv_to_dest(f, destination)
              
if __name__=='__main__':
     get_cmip5_data(destination='./data/')
    