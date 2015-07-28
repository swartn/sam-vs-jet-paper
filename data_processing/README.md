Data processing and analysis
=============================

Major data processing and analysis. The processing here involves:

  - remapping to a 1x1 grid
  - computing the zonal mean
  - computing the SAM index, Marshall SAM index, and jet properties (saved to h5)
  - Computing trend maps over various periods for slp, uas, tauu
  
These steps are performed for the 6 reanalyses, 30 CMIP5 models and relevant 
observations (HadSLP2r, CCMP). All processing can be run via `run_processing.py` 
or scripts can be run individually. See `run_processing.py` for an overview.

The input data is expected to be in `../data_retrieval/data/`, or the location 
specified by "datapath". See `../data_retrieval/input_data_list.csv` for a list 
of required data and potentially helpful download scripts.


  



