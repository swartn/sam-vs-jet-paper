
""" Call scripts to further process data and do analysis

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

# specify the data location
dest = os.path.join(os.getcwd(), '../data_retrieval/data/')

# Preprocess the observational data (remap to a 1x1 grid and make zonal means).
preprocess_observations.preprocess_observations(destination=dest)

# Preprocess the model data (remap to a 1x1 grid and make zonal means).
preprocess_models.preprocess_models(destination=dest)

#========================
# Calculate the SAM index
#========================
# 20CR ensemble
mk_20cr_ens_sam_index.mk_20cr_ens_sam_index(datapath=dest)

# Reanalyses
mk_rean_sam_index.mk_rean_sam_index(datapath=dest)

# CMIP5
mk_cmip5_sam_index.mk_cmip5_sam_index(datapath=dest)

#=======================================
# Calculate the Marshall based SAM index
#=======================================
# Reanalyses
mk_rean_marshall_slp.mk_rean_marshall_sam(datapath=dest)

#CMIP5
mk_cmip5_marshall_psl.mk_cmip5_marshall_sam(datapath=dest)

#=========================
# Calculate jet properties
#=========================
# 20CR ensemble
mk_20cr_ens_jetprop.mk_20cr_ens_jetprop(datapath=dest)

# Reanalyses
mk_rean_jetprop.mk_rean_jetprop(datapath=dest)

# CMIP5
mk_cmip5_jetprop.mk_cmip5_jetprop(datapath=dest)

#=================
# Make 2D trends 
#=================
# Reanalyses, incl. HadSLP2r
mk_rean_trends.mk_rean_trends(datapath=dest)

# CCMP and 20CR
mk_observed_trends.mk_observed_trends(datapath=dest)

# CMIP5
mk_cmip5_trends.mk_cmip5_trends(datapath=dest)
