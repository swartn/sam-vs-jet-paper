""" Call scripts to fetch and process data

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import os

import get_20cr_data
import get_ccmp_data
import get cfsr_data
import get_cmip5_data
import get_era_int_data
import get_hadslp2r_data
import get_r1_r2_20cr_esrl_data
import get_merra_data

dest = os.path.join(os.getcwd(), 'data/')

#==============================
# Run the data fetching scripts
#==============================

# 20CR
get_20cr_data.get_20cr_data(destination=dest)

# CCMP
get_ccmp_data.get_ccmp_data(destination=dest)

# CFSR
get_cfsr_data.get_cfsr_data(destination=dest)

# ERA-Int
get_era_int_data.get_era_int_data(destination=dest)

# R1, R2 and 20CR ensemble mean data
get_r1_r2_20cr_esrl_data.get_r1_r2_20cr_esrl_data(destination=dest)

# MERRA
get_merra_data.get_merra_data(destination=dest)

# CMIP5


