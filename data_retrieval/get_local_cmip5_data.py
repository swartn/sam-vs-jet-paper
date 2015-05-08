"""
Create required CMIP5 fields from data on local disks
=====================================================

The follow steps are needed.
1. soft link in the data from local disk
2. Join all time-slices (within and across experiments)
3. remap to a 1-degree grid
4. Compute the zonal means
5. Move to destination

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""

import cmipdata as cd
import subprocess
import os
import glob
import mv_to_dest

def process_local_cmip5_data(var):
    """time-merge, remap and zonal mean CMIP5 data
    """
    # 2. Join the time-slices
    # First build a cmipdata ensemble object
    filepattern = var + '*.nc' 
    ens = cd.mkensemble(filepattern)
    # Join the time-slices 
    ens = cd.cat_experiments(ens, var, 'historical', 'rcp45')    

    # remap to a 1x1 grid
    ens = cd.remap(ens,remap='r360x180', delete=True)

    # Compute zonal means
    ens = cd.zonmean(ens, delete=False)

def get_local_cmip5_data(destination='./'):
    """ link in, and preprocess CMIP5 data then copy to destination.
    """
    # These are the 30 model we used in the paper:
    model_list = ['ACCESS1-0', 'ACCESS1-3', 'BNU-ESM', 'CMCC-CMS', 'CMCC-CM',
                  'CNRM-CM5', 'CSIRO-Mk3-6-0', 'CanESM2', 
                  'GISS-E2-H-CC', 'GISS-E2-H', 'GISS-E2-R-CC', 'GISS-E2-R',
                  'HadCM3', 'HadGEM2-AO', 'HadGEM2-CC', 'HadGEM2-ES', 
                  'IPSL-CM5A-LR', 'IPSL-CM5A-MR', 'IPSL-CM5B-LR', 'MIROC-ESM-CHEM',
                  'MIROC-ESM', 'MIROC5', 'MPI-ESM-LR','MPI-ESM-MR','MRI-CGCM3',
                  'NorESM1-ME', 'NorESM1-M', 'bcc-csm1-1-m', 'bcc-csm1-1','inmcm4'
                  ]
    
    variables = ['uas', 'psl', 'tauu']
    
    for var in variables:
        # Soft-link in the CMIP5 data from elsewhere on disk
        for model in model_list:
            base_path = '/raid/rd40/data/CMIP5/'
            hist_path = os.path.join(base_path, 'historical', var, model, 'r1i1p1', 
                                     var + '*')
            rcp45_path = os.path.join(base_path, 'rcp45', var, model, 'r1i1p1', 
                                      var + '*')
            os.system('ln -s ' + hist_path + ' .' )
            os.system('ln -s ' + rcp45_path + ' .' )
        
        #Do the processing
        process_local_cmip5_data(var)
        
        #Move files to destination
        files = glob.glob('*' + var + '*.nc')
        mv_to_dest.mv_to_dest(destination, *files)
   
if __name__ == '__main__':   
    get_local_cmip5_data(destination='./data/')




