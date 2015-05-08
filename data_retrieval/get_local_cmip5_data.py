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
    # 2. Join the time-slices
    # First build a cmipdata ensemble object
    filepattern = var + '*.nc' 
    ens = cd.mkensemble(filepattern)
    # Join the time-slices 
    ens = cd.cat_experiments(ens, var, 'historical', 'rcp45')    

    # remap to a 1x1 grid
    ens_remap = cd.remap(ens,remap='r360x180', delete=True)

    # Compute zonal means
    ens_zonmean = cd.zonmean(ens_remap, delete=False)
    return ens_remap, ens_zonmean

def get_local_cmip5_data():
    variables = ['uas', 'psl', 'tauu']
    for var in variables:
        # Soft-link in the CMIP5 data from elsewhere on disk
        base_path = '/raid/rd40/data/CMIP5/'
        hist_path = os.path.join(base_path, 'historical', var, '*', 'r1i1p1', var)
        rcp45_path = os.path.join(base_path, 'rcp45', var, '*', 'r1i1p1', var)
        os.system('ln -s ' + hist_path + ' .' )
        os.system('ln -s ' + rcp45_path + ' .' )
        
        # Do the processing
        ens_remap, ens_zonmean = process_local_cmip5_data(var)
        
        # Move files to destination
        files = glob.glob('*' + var + '*.nc')
        for f in files:
            mv_to_dest.mv_to_dest(f)
   
if __name__ == '__main__':   
    get_local_cmip5_data(destination='./data/')




