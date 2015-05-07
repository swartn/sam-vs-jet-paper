Data retrieval and processing
=============================

Introduction
-------------

This series of programs retrieves the data required for the analysis in the paper
>Comparing trends in the Southern Annular Mode and surface westerly jet

`run.py` can be used to run all the sub-modules and retrieve all the data. The 
individual download scripts described below can also be run to get just a 
particular set of data. 

After downloading the original data the scripts in some instances time-merge the 
data, change variable names/units. The processed data is moved to the `./data/` 
dir by default, but the destination can be specified.

NOTE:

Some of the data servers require authentication credentials, that you will need to 
have. Specifically for the CMIP5, CFSR, CCMP and ERA-Interim data - see below.

Authentication requirements
---------------------------

- CMIP5 data downloaded from the ESGF need credentials, and a valid certificate see 
  the [ESGF site](http://pcmdi9.llnl.gov/esgf-web-fe/) for details.

- Data downloaded using the ECMWF API (i.e. ERA-Interim), require registration and
  and an authentication file at ` $HOME/.ecmwfapirc`. See 
  (https://software.ecmwf.int/wiki/display/WEBAPI/Access+ECMWF+Public+Datasets)

- Data downloaded from the [CISL Research Data Archive](http://rda.ucar.edu/)
  require login credentials. These login credentials must be put into the wget
  scripts for the CFSR and CCMP data, or they will fail (see below).
  
Data specifics and scripts
--------------------------

### CMIP5 data
script : get_cmip5_data.py
authentication : ESGF credentials required (will be requested by wget scripts).
notes : The script provided attempts to download the psl, uas and tauu data for
        ensemble member 1 of the 30 CMIP5 models used in the paper. Unfortunately,
        because the ESGF nodes and data are dynamic, and the way 
        searching/downloading is handled it's hard to ensure that the data for all 
        30 models is downloaded everytime. Alternative strategies are to manually
        download the data from the [ESGF
        website](http://pcmdi9.llnl.gov/esgf-web-fe/), or from other sources. If you
        have the data available locally, you could just use the processing section 
        of the script. Processing mostly involves time-merging the files across the 
        historical and RCP4.5 experiments.
        
        
        