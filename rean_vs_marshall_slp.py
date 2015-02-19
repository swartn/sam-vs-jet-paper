import cmipdata as cd
import h5py
import numpy as np
import scipy as sp
import pandas as pd
import pandas_tools as pt
import matplotlib.pyplot as plt
import matplotlib as mpl
import brewer2mpl
plt.ion()
plt.close('all')
font = {'size'   : 12}
plt.rc('font', **font)

# load in the Marshall SAM data
df = pd.read_csv('/HOME/ncs/data/marshall_sam/marshall_sam.csv', 
		  index_col=0, parse_dates=True)

# load the reanalysis data
# load in the reanlaysis data
rean = ['R1', 'R2', '20CR', 'ERA-Int', 'CFSR', 'MERRA', 'HadSLP2r']
rlc = [ 'k' , 'y', 'g' , 'b' , 'c' , 'm', 'k']
ls = ['-k', '-y', '-g', '-b', '-c', '-m', '--k']
h5f = pd.HDFStore('/raid/ra40/data/ncs/cmip5/sam/rean_sam.h5', 'a')
dfr = h5f['sam/df']
h5f.close() 

# load in the cmip5 data
h5fc5 = pd.HDFStore('/raid/ra40/data/ncs/cmip5/sam/c5_sam.h5', 'a')
dfc5 = h5fc5['sam/df'] 
h5fc5.close() 
d1 = pd.datetime(1957,1,1)
d2 = pd.datetime(2011,12,31)


si = 60
fig, (axt, axm, axb) = plt.subplots(3,1, sharex=True, figsize=(7,7))
fig.subplots_adjust(right=0.5, hspace=0.05)

pd.rolling_mean(dfr.ix['p40s']/100., si).plot(ax=axt, linewidth=2, 
	        style=ls, legend=False, grid=False)

pd.rolling_mean(pt.time_lim(dfc5.ix['p40s'].mean(axis=1),d1,d2)/100.
		, si).plot(ax=axt, linewidth=3, color='r'
	        , legend=False, grid=False, label='CMIP5')

pd.rolling_mean(df.slp40, si).plot(ax=axt, linewidth=2, color='r'
		,style='--', label='Marshall', grid=False
		, markevery=30, markersize=10, markeredgewidth=2)

pd.rolling_mean(dfr.ix['p65s']/100., si).plot(ax=axm, linewidth=2, style=ls
		, legend=False, grid=False)
pd.rolling_mean(df.slp65, si).plot(ax=axm, linewidth=2, color='r'
		, style='--', label='Marshall', grid=False
		, markevery=30, markersize=10, markeredgewidth=2)

pd.rolling_mean(pt.time_lim(dfc5.ix['p65s'].mean(axis=1),d1,d2)/100.
		, si).plot(ax=axm, linewidth=3, color='r'
	        , legend=False, grid=False, label='CMIP5')

pd.rolling_mean(dfr.ix['sam']/100., si).plot(ax=axb, linewidth=2, style=ls
		, legend=False, grid=False)
pd.rolling_mean(df.sam, si).plot(ax=axb, linewidth=2, color='r'
		, style='--', label='Marshall', grid=False
		, markevery=30, markersize=10, markeredgewidth=2)

pd.rolling_mean(pt.time_lim(dfc5.ix['sam'].mean(axis=1),d1,d2)/100.
		, si).plot(ax=axb, linewidth=3, color='r'
	        , legend=False, grid=False, label='CMIP5')

axb.set_xlabel('Date')
axb.set_xlim([pd.datetime(1957,1,1), pd.datetime(2011,12,31)])

axt.set_ylabel('P at 40$^{\circ}$S (hPa)')
axm.set_ylabel('P at 65$^{\circ}$S (hPa)')
axb.set_ylabel('SAM (hPa)')

axt.set_ylim([1012, 1017])
axm.set_ylim([980, 1000])
axb.set_ylim([15, 35])

axt.legend(bbox_to_anchor=(1.5,1), ncol=1, frameon=False, handletextpad=0.5,
	   numpoints=1, handlelength=1.5, fontsize=12)

for ax in fig.axes:
   ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(5, prune='upper') )
   

plt.savefig('press_and_sam_comparison_all.pdf'
            , bbox_inches = 'tight', dpi=300) 

# Look at some linear trends

# set the date range
ds = pd.datetime(1979,01,01)
ds = pd.datetime(2004,12,31)

# Go and compute some trends for comparison   
df40s = pd.concat([dfr.ix['p40s']/100., df.slp40], axis=1)
df40s = pt.time_lim(df40s, ds, de) 
df40s.columns=[u'R1', u'R2', u'TCR', u'ERA', u'CFSR', 
	       u'MERRA', u'HadSLP2r', u'Marshall']
rtrend40s = pt.ols(df40s, units='decades')
print rtrend40s.ix['slope']*100.

df65s = pd.concat([dfr.ix['p65s']/100., df.slp65], axis=1)
df65s = pt.time_lim(df65s, ds, de) 
df65s.columns=[u'R1', u'R2', u'TCR', u'ERA', u'CFSR', 
	       u'MERRA', u'HadSLP2r', u'Marshall']
rtrend65s = pt.ols(df65s, units='decades')
print rtrend65s.ix['slope']*100.

dfsam = pd.concat([dfr.ix['sam']/100., df.sam], axis=1)
dfsam = pt.time_lim(dfsam, ds, de ) 
dfsam.columns=[u'R1', u'R2', u'TCR', u'ERA', u'CFSR', 
	       u'MERRA', u'HadSLP2r', u'Marshall']
rtrendsam = pt.ols(dfsam, units='decades')
print rtrendsam.ix['slope']*100.

dfsam = pt.time_lim(dfc5.ix['sam']/100., ds, de) 
cn = [n.replace('-','') for n in dfsam.columns]
dfsam.columns = cn
c5trendsam = pt.ols(dfsam, units='decades')
print 'CMIP5 ', c5trendsam.ix['slope'].mean()*100\
              , np.percentile(c5trendsam.ix['slope']*100,2.5)\
              , np.percentile(c5trendsam.ix['slope']*100,97.5)

