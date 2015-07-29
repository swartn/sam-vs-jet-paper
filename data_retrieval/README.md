Data retrieval and processing
=============================

Introduction
-------------

This series of programs retrieves the data required for the analysis. The full list
of required input data is [here](data/input_data_list.csv).

`run_retrieval.py` can be used to try and run all the sub-modules. The 
individual download scripts described below can also be run to get just a 
particular set of data. 

After downloading the original data the scripts in some instances time-merge the 
data, change variable names/units. The processed data is moved to the `./data/` 
directory by default, but the destination can be specified.

NOTE:

1) Some of the data servers require authentication credentials, that you will need to 
have. Specifically for the CMIP5, CFSR, CCMP and ERA-Interim data - see below.

Also note that these scripts generally worked when I tried them in May 2015, but 
since webpages are dynamic, I can't help it if data moves or the scripts no longer 
work. Indeed, there are no guarantees whatsoever, see the [License](../License) file.

2) uflx fields must be land masked to exactly reproduce the result in the paper. 
   This is done in the scripts here for R1, R2 and 20CR, but will have to be
   done manually for the other 3 reanalyses.

Authentication requirements
---------------------------

- CMIP5 data downloaded from the ESGF need credentials, and a valid certificate see 
  the [ESGF site](http://pcmdi9.llnl.gov/esgf-web-fe/) for details. When running 
  the script will ask for your openid and password. Scripts:
    - `get_cmip5_data.py`

- Data downloaded using the ECMWF API (i.e. ERA-Interim), require registration and
  and an authentication file needs to be placed at ` $HOME/.ecmwfapirc`. See 
 [ECMWF public datasets page]
(https://software.ecmwf.int/wiki/display/WEBAPI/Access+ECMWF+Public+
Datasets ). Scripts:
    - `get_era_int_data.py`


- Data downloaded from the [CISL Research Data Archive](http://rda.ucar.edu/)
  require login credentials. These login credentials must be manually written into 
  the wget scripts (`.csh files`) for the CFSR and CCMP data, or they will fail. 
  Scripts:
    - ccmp/`get_ccmp_data.py`
    - ccmp/`wget_ccmp.sh`
    - cfsr/`get_cfsr_data.py`
    - cfsr/`get_cfsr_*.csh`

Data specifics and Notes
-------------------------

### CMIP5 data
script : `get_cmip5_data.py`

authentication : ESGF credentials required (will be requested by wget scripts).

notes : The script provided attempts to download the psl, uas and tauu data for
        ensemble member 1 of the 30 CMIP5 models used in the paper. Unfortunately,
        because the ESGF nodes and data are dynamic, and the way 
        searching/downloading is handled it's hard to ensure that the data for all 
        30 models is downloaded every time. During testing, I struggled to get more 
        than about 11 models this way, even though many more are available. 
        Alternative strategies are to manually download the data from the [ESGF
        website](http://pcmdi9.llnl.gov/esgf-web-fe/), or from other sources and 
        then just do the processing on the local files (see below), which is what
        I ultimately did.
        
script : `get_local_cmip5_data.py`

authentication : None

notes : This script is used to process the CMIP5 data if it is already available on 
        local disk. It is an example, and the paths are specific to my machine. You 
        will need to change where data is linked in from.       
        
### R1, R2 and 20CR ensemble mean
script : `get_r1_r2_20cr_esrl_data.py`

authentication : None

notes : This works well since no authentication is needed. 
        
### 20CR individual ensemble member files
script : `get_20cr_data.py`

authentication : None

notes : This works well since no authentication is needed. Files are downloaded on 
a per year basis, then time merged afterwards.

### HadSLP2r_lowvar
script : `get_hadslp2r_data.py`

authentication : None

notes : This works well since no authentication is needed. The process of getting 
        the HadSLP2r data from the ESRL website, and then getting the 
        HadSLP2r_lowvar data (covering 2005-2012) from the MetOffice site, and 
        merging the two together is a bit messy. This is mostly because the 
        metoffice HadSLP2r_lowvar netCDF file is not CF compliant, and they do not 
        provide the baseline HadSLP2r in netCDF format (hence getting it from ESRL).
        
### CFSR
script : cfsr/`get_cfsr_data.py`

authentication : requires http://rda.ucar.edu/ login credentials that must be 
                 manually inserted in the `email` and `passwd` fields in the `.csh` 
                 wget scripts in the cfsr directory.

notes : Remember to manually land mask the uflx data.

### CCMP
script : `get_ccmp_data.py`

authentication : None

notes : data is quite large and takes some time to download. An alternative download
        script via rda specified in the `ccmp` directory requires 
        http://rda.ucar.edu/ login credentials that must be 
        manually inserted in the `email` and `passwd` fields in the `.csh` 
        wget scripts in the ccmp directory.

### MERRA
script : merra/`get_merra_data.py`

authentication : None

notes : This works well since no authentication is needed. Files are large and take 
some time to download and come in individual months. Time joining done afterwards.
Remember to manually land mask the uflx data.

### ERA-Int
script : `get_era_int_data.py`

authentication : requires an authentication file needs to be placed at ` 
                 $HOME/.ecmwfapirc`.

notes :  This ECMWF api works well. Remember to manually land mask the uflx data.

### Marshall
script : marshall_sam/`get_marshall_data.py`

authentication : None

notes : 