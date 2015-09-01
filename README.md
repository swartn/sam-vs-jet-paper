# Comparing changes in the Southern Annular Mode and surface westerly jet

[![DOI](https://zenodo.org/badge/16109/swartn/sam-vs-jet-paper.svg)](https://zenodo.org/badge/latestdoi/16109/swartn/sam-vs-jet-paper)

This repository contains the python  code used for the paper

Swart, N.C., J.C. Fyfe, N. Gillet and G.J. Marshall (2015), Comparing changes
in the Southern Annular Mode and surface westerly jet, J. Climate.

This code will perform all the processing, analysis, and plotting to produce the 
final figures appearing in the paper. 

## Project organization
The project is organized in directories as follows:

  - [`data_retrieval`](data_retrieval/) contains scripts for downloading the 
     original (mostly netCDF) data. The `data`directory is the location where 
     all raw and processed data is stored.
  
  - [`data_processing`](data_processing/) contains scripts for performing basic 
    preprocessing of the data, and some analysis to produce derivative datasets 
    (mostly stored in HDF5).
     
  - [`analysis_and_plotting`](analysis_and_plotting/) contains the scripts that 
    produce the 14 figures in the paper.
     
  - [`plots`](plots/) contains the output plots in PDF format.
  
  - [`paper`](paper/) contains the LaTeX source for the final paper.
  
The first three directories each contain their own README with further information.
They also contain a script (e.g. `run_plotting.py`), that will automatically 
execute all the relevant code. All modules have docstrings that explain their basic 
function.  

## How to repeat the analysis

To reproduce the figures you need to:

1. Download the raw input data (`run_retrieval.py`)
2. Complete all processing steps (`run_processing.py`)
3. Complete all plotting steps (`run_plotting.py`)

Over 30GB of raw input data are required for the project. All the data is public
and freely available online. However, the data downloading 
step is the most complicated and the most likely to be problematic. I cannot ensure 
that the data download scripts will work given the dynamic nature 
of the online data repositories, and the authentication credentials 
some of the sites require. Users can also download the data manually 
(referring to the comprehensive list provided 
[here](data_retrieval/data/input_data_list.csv)), 
or may request the input data from the authors. 

The `run.py` script will 
automatically execute everything in steps 2 and 3, as long as all the 
[required input data](data_retrieval/data/input_data_list.csv) is provided and the 
environment is setup correctly (see below).

## Software and dependencies
I wrote and tested the code using the Anaconda python distribution on Linux machines
running Ubuntu 14.04.2 LTS. The specific Anaconda distribution used was:

    Python 2.7.9 |Anaconda 2.2.0 (64-bit)| (default, Mar  9 2015, 16:20:48) 

Additional software requirements include climate data
operators [cdo](https://code.zmaw.de/projects/cdo) and their python bindings, my 
[`cmipdata`](https://github.com/swartn/cmipdata) python package 
(tested with commit 07d17b2f4a), and some downloading utilities.

To create a suitable virtual env in anaconda I did:

    conda create -n sam-jet-env python=2.7.9 pandas=0.15.2 numpy=1.9.2 \
    netcdf4=1.1.6 ipython=3.0.0 h5py=2.4.0 pip scipy=0.15.1 matplotlib=1.4.3 \
    basemap=1.0.7 statsmodels=0.6.1 pytables=3.1.1 h5py=2.4.0 netCDF4 
   
    pip install cdo==1.2.5 
    
    pip install git+https://github.com/swartn/cmipdata.git
    

    pip install https://software.ecmwf.int/wiki/download/attachments/47287906/\
    ecmwf-api-client-python.tgz

    pip install esgf-pyclient==0.1.2
    
To give an overall idea, most of the basic data processing (like regridding to a 
common grid, zonal means, subsamping, computing trend maps etc) are done with cdo. 
Some analysis, like computing trends from timeseries, and computing the jet 
properties, are done in python (using numpy, scipy, statsmodels and pandas). All
plotting is done with matplotlib. Note that [this bugfix](https://github.com/jenshnielsen/matplotlib/commit/d5dafdbb48e984e52218640888ae7fa8feb36032)
must be applied to matplotlib.

## License
This ``sam-vs-jet-paper`` software is Copyright (C) 2015  Neil Swart. It is 
licensed under the [GNU General Public License 
version 2](http://www.gnu.org/licenses/gpl-2.0.txt) -see below and the LICENSE file.

## Disclaimer
This was a mult-author paper, but all the software is the responsibility of me, Neil 
Swart. I invested a lot of effort to get this code to the point of basically being
reusable, and have tried to ensure that everything is correct. However there are
no guarantees whatsoever (see License), and inevitably some problems will be 
found. If you find one, please let me know. The code was not designed to be 
particularly beautiful or efficient. Everything was originally written as scripts in 
scientific exploration mode, and in the beginning I was quite new to python. There 
are places where things could be more efficient, more pythonic, and there are some 
limited sections of code that are repeated, but here it is nonetheless.
