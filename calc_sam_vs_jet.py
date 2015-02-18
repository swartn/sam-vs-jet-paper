import numpy as np
import scipy as sp
from scipy import stats
import trend_ts
reload(trend_ts)
#import smooth
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from datetime import datetime
from dateutil.relativedelta import relativedelta

plt.close('all')
plt.ion()
font = {'size'   : 16}
plt.rc('font', **font)

rp40 = np.genfromtxt('rean_press40.txt')
rp40 = np.reshape( rp40 , ( 6 , len(rp40) / 6. ) )
rp65 = np.genfromtxt('rean_press40.txt')
rp65 = np.reshape( rp65 , ( 6 , len(rp65) / 6. ) )

date = []
for i in range( rp65.shape[1] ):
    date.append(  datetime(1979,01,01) + relativedelta(months=i) )
 

for i in range(6):
   plt.plot( date, rp40[i,:] )


# import pandas as pd
# test = pd.read_csv('test.txt',names=['date','p40'])
# from dateutil.parser import parse
# test.date = test.date.apply(lambda d: parse(d) )
