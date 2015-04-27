"""
Looks for correlations between the SAM and jet properties within CMIP5 models.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import numpy as np
import scipy as sp
from scipy import stats
import trend_ts
reload(trend_ts)
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from dateutil.parser import parse
import sam_analysis_data as sad
import pandas_tools as pt

"""

# set font size
plt.close('all')
plt.ion()
font = {'size'   : 12}
plt.rc('font', **font)

# load in the Marshall SAM data
dfmarshall = pd.read_csv('/HOME/ncs/data/marshall_sam/marshall_sam.csv', 
		  index_col=0, parse_dates=True)

# load the reanalysis data
h5f = pd.HDFStore('/raid/ra40/data/ncs/cmip5/sam/rean_sam.h5', 'r')
dfr = h5f['zonmean_sam/df']
h5f.close()
dfhadslp = dfr['HadSLP2r']/100.

# load in the 20CR ensemble data
h5f_20CR = pd.HDFStore(
    '/raid/ra40/data/ncs/reanalyses/20CR/20cr_ensemble_sam_analysis.h5',
    'r')
df_20cr_ens_sam = h5f_20CR['sam']/100.
df_20cr_ens_locmax = h5f_20CR['locmax']
df_20cr_ens_maxspd = h5f_20CR['maxspd'] 
df_20cr_ens_width = h5f_20CR['width'] 
h5f_20CR.close()

# load in the next set of model data
h5f_c5 = pd.HDFStore('/raid/ra40/data/ncs/cmip5/sam/c5_zonmean_sam-jet_analysis.h5',
                     'r')
df_c5_ens_sam = h5f_c5['sam']/100.
df_c5_ens_locmax = h5f_c5['locmax']
df_c5_ens_maxspd = h5f_c5['maxspd'] 
df_c5_ens_width = h5f_c5['width'] 
h5f_c5.close()


ds = pd.datetime(1900,01,01)
de = pd.datetime(1949,12,31)

mod_sam_uspd_r = np.empty(30)
mod_sam_loc_r = np.empty(30)
mod_sam_width_r = np.empty(30)

for i in range(30):
    sam = pt.time_lim(df_c5_ens_sam, ds, de).values[:,i]
    uspd = pt.time_lim(df_c5_ens_maxspd, ds, de).values[:,i]
    loc = pt.time_lim(df_c5_ens_locmax, ds, de).values[:,i]
    width = pt.time_lim(df_c5_ens_width, ds, de).values[:,i]

    #print 'maxspd'
    #slope , conf_int , p_value, yhat, intercept = trend_ts.trend_ts( sam , uspd )
    mod_sam_uspd_r[i], p = sp.stats.pearsonr(sam , uspd )
    mod_sam_loc_r[i], p = sp.stats.pearsonr(sam , loc )
    mod_sam_width_r[i], p = sp.stats.pearsonr(sam , width)

    #print r #, slope, p_value

#print 'locmax'
#slope , conf_int , p_value, yhat, intercept = trend_ts.trend_ts( sam , loc )
#r, p = sp.stats.pearsonr(sam , loc )

#print r, slope, p_value


print 'model mean SAM-jet correlations'
print 'sam-umax r: ', mod_sam_uspd_r.mean()
print 'sam-loc r: ', mod_sam_loc_r.mean()
print 'sam-loc r: ', mod_sam_width_r.mean()
