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
    files = glob.glob('*.mon.mean.nc')
    # Add in CCMp and HadSLP2r files
    file.extend(['CCMP_198701-201112.nc', 'HadSLP2r_lowvar.mon.mean.nc'])

    for f in files:
        cdo.remapdis('r360x180', input=f, output='remap_' + f)
        cdo.zonmean(input='remap_' + f, output='zonmean_remap_' + f)
        #os.remove(f)

    # move back
    os.chdir(cwd)

if __name__ == '__main__':
    preprocess_observations(destination='./data/')

