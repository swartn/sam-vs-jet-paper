""" Compute trends in a 2-d field.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import cmipdata as cd
import os
import glob
import numpy as np
import scipy as sp
import h5py

def save_cmip5_trends(ens, var, start_date, end_date, datapath='./'):
    """Compute trends and save as np array in HDF5.
    """
    # Compute the trends using cmipdata/cdo
    ens1 = cd.trends(ens, start_date=start_date, 
                    end_date=end_date, delete=False)
    
    # keep only the slope files, delete the intercept files
    for model, experiment, realization, variable, files in ens1.iterate():
        for file in files:
            if 'intercept' in file:
                variable.del_filename(file)
    
    # load the slope files into a np array
    slopes = cd.loadfiles(ens1, var)
    
    # Store the DataFrame in HDF5
    out_file = os.path.join(datapath, 'cmip5_trends.h5')
    h5f = h5py.File(out_file, 'a')
    sy = start_date.split('-')[0]
    ey = end_date.split('-')[0]
    ds_path = os.path.join(var, sy + '_' + ey)
    ds_name = os.path.join(ds_path, 'c5_' + var + '_trend_' + sy + '_' + ey)    
    h5f.create_dataset(ds_name, data=slopes)
    model_names = [ model.name for model in ens1.models]
    h5f.create_dataset(ds_path + 'model_names', data=model_names)
    #h5f[ds_name].dims.create_scale(h5f[ds_path + 'model_names'], 'model_names')
    #f[ds_name].dims[2].attach_scale(h5f[ds_path + 'model_names'])
    h5f.close()
        
    # clean up
    trash_files = glob.glob('slope*.nc')
    trash_files.extend(glob.glob('intercept*.nc'))
    for f in trash_files:
        os.remove(f)
    
def mk_cmip5_trends(datapath='./'):
    """Compute trends for uas, uflx and slp over various periods.
    """
    # list of models being used
    model_list = ['ACCESS1-0', 'ACCESS1-3', 'BNU-ESM', 'CMCC-CMS', 'CMCC-CM',
                  'CNRM-CM5', 'CSIRO-Mk3-6-0', 'CanESM2', 
                  'GISS-E2-H-CC', 'GISS-E2-H', 'GISS-E2-R-CC', 'GISS-E2-R',
                  'HadCM3', 'HadGEM2-AO', 'HadGEM2-CC', 'HadGEM2-ES', 
                  'IPSL-CM5A-LR', 'IPSL-CM5A-MR', 'IPSL-CM5B-LR', 'MIROC-ESM-CHEM',
                  'MIROC-ESM', 'MIROC5', 'MPI-ESM-LR','MPI-ESM-MR','MRI-CGCM3',
                  'NorESM1-ME', 'NorESM1-M', 'bcc-csm1-1-m', 'bcc-csm1-1','inmcm4'
                  ]
    
    # Where to find the data
    prefix = os.path.join(datapath, 'remap_')
    
    # Do psl
    # make an ensemble object and the calculate the trends for req. dates
    filepattern = prefix + 'psl' + *r1i1p1*.nc
    ens = cd.mkensemble(filepattern, prefix=prefix)
    save_cmip5_trends(ens, 'psl', '1951-01-01', '2004-12-31', datapath=datapath)
    save_cmip5_trends(ens, 'psl', '1979-01-01', '2004-12-31', datapath=datapath)

    # Do uas
    # make an ensemble object and the calculate the trends for req. dates
    filepattern = prefix + 'uas' + *r1i1p1*.nc
    ens = cd.mkensemble(filepattern, prefix=prefix)
    save_cmip5_trends(ens, 'uas', '1951-01-01', '2011-12-31', datapath=datapath)
    save_cmip5_trends(ens, 'uas', '1988-01-01', '2011-12-31', datapath=datapath)

    # Do tauu
    # make an ensemble object and the calculate the trends for req. dates
    filepattern = prefix + 'tauu' + *r1i1p1*.nc
    ens = cd.mkensemble(filepattern, prefix=prefix)
    save_cmip5_trends(ens, 'tauu', '1988-01-01', '2011-12-31', datapath=datapath)

if __name__ == '__main__':
    mk_cmip5_trends(datapath='../data_retrieval/data/')
    
