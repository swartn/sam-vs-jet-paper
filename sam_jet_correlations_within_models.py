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

""" Analyze time series in 20CR, CMIP5 and HadSLP2r

Neil Swart, v4, Feb 2015
Neil.Swart@ec.gc.ca

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


ds = pd.datetime(1881,01,01)
de = pd.datetime(2010,12,31)

sam = pt.time_lim(df_20cr_ens_sam, ds, de).values[:,0]
uspd = pt.time_lim(df_20cr_ens_maxspd, ds, de).values[:,0]
loc = pt.time_lim(df_20cr_ens_locmax, ds, de).values[:,0]

print 'maxspd'
slope , conf_int , p_value, yhat, intercept = trend_ts.trend_ts( sam , uspd )
r, p = sp.stats.pearsonr(sam , uspd )
print r, slope, p_value

print 'locmax'
slope , conf_int , p_value, yhat, intercept = trend_ts.trend_ts( sam , loc )
r, p = sp.stats.pearsonr(sam , loc )

print r, slope, p_value
