"""
Does remapping to 1x1 grid and computes zonal means for the CMIP5 
model fields.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import os
import glob
import cmipdata as cd

def preprocess_models(datapath='./'):
    # where we are starting from
    cwd = os.getcwd()
    # move to where the data is
    os.chdir(datapath)

    # time-merge, remap and zonal mean the model data
    variables = ['uas', 'psl', 'tauu']
    for var in variables:
        # time-merge the data across the historical and rcp45 experiments
        filepattern = var + '_Amon*.nc'
        ens = cd.mkensemble(filepattern)
       
        # remap to a 1x1 grid
        ens_remap = cd.remap(ens,remap='r360x180', delete=True)

        # Compute zonal means
        ens_zonmean = cd.zonmean(ens_remap, delete=False)

    # move back
    os.chdir(cwd)

if __name__ == '__main__':
    preprocess_models(datapath='../data_retrieval/data/')

