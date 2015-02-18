import numpy as np
import scipy as sp
import trend_ts
reload(trend_ts)
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from dateutil.parser import parse
import sam_analysis_data as sad
import statsmodels.formula.api as smf
plt.close('all')
plt.ion()
# load the data
press, maxspd, locmax, width, modpress, modmaxspd, modlocmax, modwidth =\
      sad.load_sam_df()

# Period 1
tys = 1951 # start (inclusive)
tye = 2011 # stop (inclusive)

def year_lim( df , ys , ye ):
    """ Limits the dataframe df to between years starting in ys and ending in ye
inclusive"""
    dfo = df[ ( df.index.year >= ys ) & ( df.index.year <= ye ) ]
    if ( df.index.year.min() > ys ):
         print 'WARNING: data record begins after requested trend start.' 
    elif ( df.index.year.max() < ye ):
         print 'WARNING: data record ends before requested trend end.'
    return dfo
    
def gseas(df, s):
    """Extract season, s, and return dataframe where:
         s = 1 : mam
         s = 2 : jja
         s = 3 : son
         s = 4 : djf
         s = 5 : ann
         
    """
    if s == 1:
        df = df[ ( df.index.month >= 3 ) & ( df.index.month <= 5 )]
    elif s == 2:
        df = df[ ( df.index.month >= 6 ) & ( df.index.month <= 8 )]
    elif s == 3:    
        df = df[ ( df.index.month >= 9 ) & ( df.index.month <= 11 )]
    elif s == 4:
        dfsh = df.shift(12)
        df = pd.concat( [ dfsh[dfsh.index.month==12 ] ,\
             df[ ( df.index.month >= 1 ) & ( df.index.month <= 2 )] ],axis=0)
        #df = df.sort(axis=0)
    elif s ==5:
	pass
    
    df = df.resample('A')
    #df = (df - df.mean(axis=0) ) / df.std(axis=0)
    return df
    
press =  year_lim(press, tys, tye) 
maxspd = year_lim(maxspd, tys, tye) 
locmax = year_lim(locmax, tys, tye) 
width =  year_lim(width, tys, tye)     
    
modpress =  year_lim(modpress, tys, tye) 
modmaxspd = year_lim(modmaxspd, tys, tye) 
modlocmax = year_lim(modlocmax, tys, tye) 
modwidth =  year_lim(modwidth, tys, tye) 

cl = ['sam', 'umax', 'pos', 'width']

coeffs = np.zeros((30,4,5))
coeffs_rean = np.zeros((6,4,5))

for m in modpress.columns:
    for s in np.arange(1,6):
        df = pd.concat([ gseas(modpress[m], s), gseas(modmaxspd[m], s) ,
             gseas(modlocmax[m], s), gseas(modwidth[m],s) ], axis=1)
        df.columns = cl
        mod = smf.ols(formula='sam ~ umax + pos + width', data=df)
        res = mod.fit()
        coeffs[int(m-1),:,s-1] = res.params.values
        
for m in press.columns:
    for s in np.arange(1,6):
        df = pd.concat([ gseas(press[m], s), gseas(maxspd[m], s) ,
             gseas(locmax[m], s), gseas(width[m],s) ], axis=1)
        df.columns = cl
        mod = smf.ols(formula='sam ~ umax + pos + width', data=df)
        res = mod.fit()
        coeffs_rean[int(m-1),:,s-1] = res.params.values        

s=4
bpm = plt.boxplot(coeffs[:,1:4,s])
plt.setp(bpm['boxes'], color='black')
plt.setp(bpm['whiskers'], color='black')   
plt.setp(bpm['medians'], color='black')   
plt.setp(bpm['fliers'], color='black')   
plt.setp(bpm['caps'], color='black')   

#bpr = plt.boxplot(coeffs_rean[:,1:4,4])
#plt.setp(bpr['boxes'], color='red')
#plt.setp(bpr['whiskers'], color='red')  
#plt.setp(bpr['medians'], color='red')   
#plt.setp(bpr['fliers'], color='red')   
#plt.setp(bpr['caps'], color='red')   

plt.plot([1,2,3],coeffs_rean[2,1:4,s], 'rx')