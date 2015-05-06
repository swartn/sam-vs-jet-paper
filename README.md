# Comparing changes in the Southern Annular Mode and surface westerly jet

This repository contains the code used for analyses in the paper

Swart, N.C., J.C. Fyfe, N. Gillet and G.J. Marshall (2015), Comparing changes in the 
Southern Annular Mode and surface westerly jet, J. Climate.

While the source code is provided, we do not provide code to automatically download 
all the required data, however, all of the data is publicly available. 

## Data
The data used is the sea-level pressure (psl), 10 m zonal winds (uas), and zonal 
wind-stress (tauu) fields from from 30 CMIP5 models (see paper methods for a list 
of models). It is publicly available from the [ESGF](http://pcmdi9.llnl.gov).

Corresponding data from six reanalyses, listed in Table 1 the paper (with source 
urls) is also used. Reanalysis data were modified to have the same units and 
variable names. Specifically, the sea-level pressure variable was named ``slp`` 
throughout, and specified in units of Pa. The zonal 10m wind variable was renamed 
to ``uwnd`` throughout and specified in units of ``m/s``. The zonal windstress 
fields were renamed to ``uflx`` throughout, and specified in units of ``Pa``.  
In addition the HadSLP2r, CCMP satellite winds and station pressure data from 
Marshall and also used (see paper).

ERA-Int:
Getting the data requires credentials in a $HOME/.ecmwfapirc file. See
https://software.ecmwf.int/wiki/display/WEBAPI/Accessing+ECMWF+data+servers+in+batch

## Scripts and code
The rough organization of the project is that scripts used to preprocess data are 
in the directory `data_processing/`. This contains things like joining the original 
CMIP5 time-series, subsampling the data and computing the SAM index or jet 
properties. The prefix `calc_` is a module that contains a general routine, for 
example, calculating the SAM index. The files with a `mk_` prefix are associated 
with processing a particular set of data, for example, 20CR. The `mk` scripts will, 
in some instances, call the `calc_` routines.

Scripts used to do the final analysis and plotting are in 
`analysis_plotting/`, where the prefix `plot_` means that the script produces a 
plot used in publication, and `discover_` means that the script is used to do some 
basic exploration of the data. All modules have docstrings that explain their basic 
function.   

All code is written in python 2.7x (older versions of the project also used bash 
and Ferret, but those have all be replaced with python). There are, in general, 
multiple dependencies, including but no limited to:

  - climate data operators (cdo) and their python bindings.
  - pandas_tools (Neil)
  
A more complete list is given below. The Anaconda distribution of python was used:

    Python 2.7.9 |Anaconda 2.2.0 (64-bit)| (default, Mar  9 2015, 16:20:48)

## Notes

## Appendices
Dependencies were:

anaconda                  2.2.0                np19py27_0  
cdo                       1.2.5                     <pip>
cmipdata (/HOME/ncs/pyPackages/cmipdata) 0.0.1.dev0                <pip>
h5py                      2.4.0                np19py27_0  
hdf5                      1.8.14                        0  
ipython                   3.0.0                    py27_0  
ipython-notebook          3.0.0                    py27_1  
ipython-qtconsole         3.0.0                    py27_0  
netcdf4                   1.1.6                np19py27_0  
numpy                     1.9.2                    py27_0  
numpydoc                  0.6.dev0                  <pip>
pandas                    0.15.2               np19py27_1  
python                    2.7.9                         2  
scipy                     0.15.1               np19py27_0  
setuptools                14.3                     py27_0  

## License
This ``sam-vs-jet-paper`` software is Copyright (C) 2015  Neil Swart. It is 
licensed under the [GNU General Public License 
version 2](http://www.gnu.org/licenses/gpl-2.0.txt) -see below and LICENSE.txt.

To create a suitable virtual env in anaconda I did:

    conda create -n sam-jet-env python=2.7.9 pandas=0.15.2 numpy=1.9.2 
    netcdf4=1.1.6 ipython=3.0.0 h5py=2.4.0 pip scipy=0.15.1 matplotlib=1.4.3

    
    pip install cdo==1.2.5 
    
    pip install
    https://software.ecmwf.int/wiki/download/attachments/23694554/ecmwf-api-client-
    python.tgz
    
    pip install esgf-pyclient==0.1.2
    