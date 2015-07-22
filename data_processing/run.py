""" Call scripts to further process data and do analysis

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import os
import sys

# specify the data location
dest = os.path.join(os.getcwd(), '../data_retrieval/data/')

# Preprocess the observational data (remap to a 1x1 grid and make zonal means).
preprocess_observations.preprocess_observations(destination=dest)

#========================
# Calculate the SAM index
#========================
# 20CR ensemble
mk_20cr_sam_index.mk_20cr_sam_index(datapath=dest)

# Reanalyses
mk_rean_sam_index.mk_rean_sam_index(datapath=dest)

# CMIP5
mk_cmip5_sam_index.mk_cmip5_sam_index(datapath=dest)

#=========================
# Calculate jet properties
#=========================
# 20CR ensemble
mk_20cr_jetprop.mk_20cr_jetprop(datapath=dest)

# Reanalyses
mk_rean_jetprop.mk_rean_jetprop(datapath=dest)

# CMIP5
mk_cmip5_jetprop.mk_cmip5_jetprop(datapath=dest)