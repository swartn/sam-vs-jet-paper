"""
Create cmip5 uas timeseries
===========================

Create CMIP5 uas time-series

The follow steps are needed.
1. Import the uas data for historical and rcp45 experiments
2. Join all time-slices (within and across experiments)
3. Zonal mean
4. remap

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""

import cmipdata as cd
import os

#
# 1. Import the data
# =====================================
os.chdir('/home/ncs/ra40/cmip5/sam/c5_uas2')
os.system('ln -s /rd40/data/CMIP5/historical/uas/*/*/uas* .')
os.system('ln -s /rd40/data/CMIP5/rcp45/uas/*/*/uas* .')

# 2. Join the time-slices
# =====================================

# First build a cmipdata ensemble object
filepattern = 'uas_Amon*'
ens = cd.mkensemble(filepattern)

ens = cd.cat_experiments(ens, 'uas', 'historical', 'rcp45')    # Join slices 


# look at the result.
ens.fulldetails()

# 3. Zonal mean
# =====================================
ens = cd.zonmean(ens,delete=False)

# 4. remap
# =====================================
ens = cd.remap(ens,remap='r1x180',delete=True)






