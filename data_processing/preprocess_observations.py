"""
Does remapping of the reanalyses and observations onto a 1x1 grid and computes 
zonal means.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import os
import glob
import cdo; cdo = cdo.Cdo()

def preprocess_observations(destination='./'):
    # where we are starting from
    cwd = os.getcwd()
    # move to where the data is
    os.chdir(destination)
    # Get the reanalysis monthly mean files
    rean = ['R1', 'R2', '20CR', 'ERA-Int', 'CFSR', 'MERRA']
    var = ['slp', 'u10m', 'uflx']
    files = []
    for r in rean:
        for v in var:
            files.extend([r + '_' + v + '.mon.mean.nc'])

    files = [f for f in files if not f.startswith('remap') and not 
            f.startswith('zonal-mean')]
    # Add in CCMp and HadSLP2r files
    
    files.extend(['CCMP_198701-201112.nc', 'HadSLP2r_slp.mon.mean.nc'])
    files.extend(['20CR_ens_slp.mon.mean.nc', '20CR_ens_u10m.mon.mean.nc'])

    for f in files:
        print f
        if not os.path.isfile('remap_' + f):
            cdo.remapdis('r360x180', input=f, output='remap_' + f)
        if not os.path.isfile('zonal-mean_remap_' + f):        
            cdo.zonmean(input='remap_' + f, output='zonal-mean_remap_' + f)
        #os.remove(f)

    # move back
    os.chdir(cwd)

if __name__ == '__main__':
    preprocess_observations(destination='../data_retrieval/data/')

