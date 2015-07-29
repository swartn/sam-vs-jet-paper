Data processing and analysis
=============================

Major data processing and analysis. The processing here involves:

  - remapping to a 1x1 grid
  - computing the zonal mean
  - computing the SAM index, Marshall SAM index, and jet properties (saved to h5)
  - Computing trend maps over various periods for slp, uas, tauu
  
These steps are performed for the 6 reanalyses, 30 CMIP5 models and relevant 
observations (HadSLP2r, CCMP). All processing can be run via 
[`run_processing.py`](run_processing.py), which also provides an overview of each 
step. All scripts can also be run individually. 

The processing will fail unless all of the expected data is available
in [../../data_retrieval/data/](../data_retrieval/data/). You must first
[download](../data_retrieval/README.md) all required data.



  



