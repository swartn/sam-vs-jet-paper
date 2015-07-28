
""" Call scripts that do major data processing and analysis. The input data
is expected to be in ../data_retrieval/data/, or the location specified by 
"datapath". See ../data_retrieval/data/input_data_list.csv for a list of required 
data and download scripts.

The processing here involves:

  - remapping to a 1x1 grid
  - computing the zonal mean
  - computing the SAM index, Marshall SAM index, and jet properties (saved to h5)
  - Computing trend maps over various periods for slp, uas, tauu
  
These steps are performed for the 6 reanalyses, 30 CMIP5 models and relevant 
observations (HadSLP2r, CCMP).  
  
.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import os
import sys
import preprocess_observations
import preprocess_models
import mk_20cr_ens_sam_index
import mk_rean_sam_index
import mk_cmip5_sam_index
import mk_20cr_ens_jetprop
import mk_rean_jetprop
import mk_cmip5_jetprop
import mk_rean_marshall_slp
import mk_cmip5_marshall_slp
import mk_rean_trends
import mk_cmip5_trends
import mk_observed_trends

def run_processing(datapath):
    
    # Preprocess the observational data (remap to a 1x1 grid and make zonal means).
    print 'preprocess_observations \n'
    preprocess_observations.preprocess_observations(datapath=datapath)

    # Preprocess the model data (remap to a 1x1 grid and make zonal means).
    print 'preprocess_models \n'
    preprocess_models.preprocess_models(datapath=datapath)

    #========================
    # Calculate the SAM index
    #========================
    # 20cr ensemble
    print 'mk_20cr_ens_sam_index \n'
    mk_20cr_ens_sam_index.mk_20cr_ens_sam_index(datapath=datapath)

    # Reanalyses
    print 'mk_rean_sam_index \n'
    mk_rean_sam_index.mk_rean_sam_index(datapath=datapath)

    # CMIP5
    print 'mk_cmip5_sam_index \n' 
    mk_cmip5_sam_index.mk_cmip5_sam_index(datapath=datapath)

    #=======================================
    # Calculate the Marshall based SAM index
    #=======================================
    # Reanalyses
    print 'mk_rean_marshall_slp \n'
    mk_rean_marshall_slp.mk_rean_marshall_slp(datapath=datapath)

    #CMIP5
    print 'mk_cmip5_marshall_slp \n' 
    mk_cmip5_marshall_slp.mk_cmip5_marshall_slp(datapath=datapath)

    #=========================
    # Calculate jet properties
    #=========================
    # 20cr ensemble
    print 'mk_20cr_ens_jetprop \n' 
    mk_20cr_ens_jetprop.mk_20cr_ens_jetprop(datapath=datapath)

    # Reanalyses
    print 'mk_rean_jetprop \n'
    mk_rean_jetprop.mk_rean_jetprop(datapath=datapath)

    # CMIP5
    print 'mk_cmip5_jetprop\n'
    mk_cmip5_jetprop.mk_cmip5_jetprop(datapath=datapath)

    #=================
    # Make 2D trends 
    #=================
    
    # Reanalyses, incl. HadSLP2r
    print 'mk_rean_trends\n'
    mk_rean_trends.mk_rean_trends(datapath=datapath)

    # CCMP and 20cr
    print 'mk_observed_trends\n'
    mk_observed_trends.mk_observed_trends(datapath=datapath)

    # CMIP5
    print 'mk_cmip5_trends\n'
    mk_cmip5_trends.mk_cmip5_trends(datapath=datapath)

if __name__ == '__main__':
    # specify the data location
    datapath = os.path.join(os.getcwd(), '../data_retrieval/data/')
    run_processing(datapath=datapath)
    