import numpy as np
import matplotlib.pyplot as plt
plt.close('all')
plt.ion()

mod_jet_trend =np.genfromtxt('/ra40/data/ncs/cmip5/sam/c5_sfcWind/mod_jet_trend.txt')
mod_sam_trend =np.genfromtxt('/ra40/data/ncs/cmip5/sam/c5_slp/mod_sam_trend.txt')

rean_jet_trend =np.genfromtxt('rean_jet_trend.txt')
rean_sam_trend =np.genfromtxt('rean_sam_trend.txt')

plt.axes([0.2, 0.5, 0.4, 0.4])
plt.plot( mod_sam_trend , mod_jet_trend ,'ok')
plt.plot( rean_sam_trend , rean_jet_trend ,'or')
plt.xlabel('SAM trend (Pa dec.$^{-1}$)')
plt.ylabel('Wspd trend (ms$^{-1}$ dec.$^{-1}$)')

plt.text( np.min( mod_sam_trend )  , np.mean( mod_jet_trend ) + 0.05 , 'CMIP5' )


rean_names = ['R1', 'R2', '20CR', 'ERA', 'CFSR' ,'MERRA']
for i,n in enumerate( rean_names):
   if n == '20CR':
       plt.text( rean_sam_trend[i] -7 , rean_jet_trend[i]+0.035 , n )
   else:
       plt.text( rean_sam_trend[i] + 4 , rean_jet_trend[i] , n )
       
plt.axis( [ -40, 140, -0.5, 0.5] )
plt.title('Monthly mean trends')
