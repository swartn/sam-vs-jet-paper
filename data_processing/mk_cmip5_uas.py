"""
Create cmip5 timeseries
===========================

The follow steps are needed.
2. Join all time-slices (within and across experiments)
3. remap to a 1-degree grid
4. Compute the zonal means

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""

import cmipdata as cd
import subprocess
import os

def process_local_cmip5_data(var):
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


if __name__ == '__main__':   
    variables = ['uas', 'psl', 'tauu']
    for var in variables:
        # Soft-link in the CMIP5 data from elsewhere on disk
        base_path = '/raid/rd40/data/CMIP5/'
        hist_path = os.path.join(base_path, 'historical', var, '*', 'r1i1p1', var)
        rcp45_path = os.path.join(base_path, 'rcp45', var, '*', 'r1i1p1', var)
        os.system('ln -s ' + hist_path + ' .' )
        os.system('ln -s ' + rcp45_path + ' .' )
        
        # Do the processing
        process_local_cmip5_data(var)





