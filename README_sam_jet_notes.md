Title: Analysis Notes: SAM and westerly jet changes
Category: Research
Date: 2015-04-27

## Summary
This document describes the data and software used to prepare a paper entitled
"Comparing trends in the Southern Annular Mode and westerly jet".

## Data
The data used is the sea-level pressure (psl) and 10 m zonal winds (uas) from 30 
CMIP5 models (available from the ESGF). Corresponding data from six reanalyses, 
listed in the paper is also used. In addition the HadSLP2r, CCMP satellite winds 
and station pressure data from Marshall and also used.

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
