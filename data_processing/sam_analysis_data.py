"""
Obsolete. 

Save SAM index and jet property data computed in Ferret into Pandas DataFrames in 
HDF5.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""

import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.parser import parse
import os

def save_sam_df():  
	# Create the Pandas dataframes and store them in HDF5
	print "readfiles"
        os.system( 'rm -f sam_analysis.h5')
        store = pd.HDFStore('sam_analysis.h5')

	# Reanalyses
	press = pd.read_csv('rean_press_40_65S.txt',names=['date','ind','rno','p40','p65']) # read in
	press['sam'] = ( press.p40 - press.p65 ) / 100
	press.date = press.date.apply(lambda d: np.datetime64( datetime( parse(d).year, parse(d).month, 1 ) ) )
	press = press.pivot(index='date',columns='rno',values='sam')
	press = press[ press.index.year <= 2013 ]
	store['press'] = press

	maxspd = pd.read_csv('rean_uspd.txt',names=['date','ind','rno','wspd']) # read in
	maxspd.date = maxspd.date.apply(lambda d: np.datetime64( datetime( parse(d).year, parse(d).month, 1 ) ) )
	maxspd = maxspd.pivot(index='date',columns='rno',values='wspd')
	maxspd = maxspd[ maxspd.index.year <= 2013 ]
        store['maxspd'] = maxspd
        
	locmax = pd.read_csv('rean_uloc.txt',names=['date','ind','rno','pos']) # read in
	locmax.date = locmax.date.apply(lambda d: np.datetime64( datetime( parse(d).year, parse(d).month, 1 ) ) )
	locmax = locmax.pivot(index='date',columns='rno',values='pos')
	locmax = locmax[ locmax.index.year <= 2013 ]
        store['locmax'] = locmax

	width = pd.read_csv('rean_uwidth.txt',names=['date','ind','rno','width']) # read in
	width.date = width.date.apply(lambda d: np.datetime64( datetime( parse(d).year, parse(d).month, 1 ) ) )
	# width.date = width.date.apply(lambda d: pd.to_datetime( pd.to_datetime(d).year + pd.to_datetime(d).month + 1,  format='%Y%m%d ))
	width = width.pivot(index='date',columns='rno',values='width')
	width = width[ width.index.year <= 2013 ]
	store['width'] = width


	# Models
	modpress = pd.read_csv('/ra40/data/ncs/cmip5/sam/c5_slp/mod_press_40_65S.txt',\
	names=['date','ind','rno','p40','p65']) # read in
	modpress.rno = modpress.rno - 1 # make the model 'labels' start at 1.
	# parse the dates and set as index. Force set the day to "1" since it varies randomly across models.
	modpress.date = modpress.date.apply(lambda d: np.datetime64( datetime( parse(d).year, parse(d).month, 1 ) ) )
	modpress['sam'] = ( modpress.p40 - modpress.p65 ) / 100
	modpress = modpress.pivot(index='date',columns='rno',values='sam')
	store['modpress'] = modpress

	modmaxspd = pd.read_csv('/ra40/data/ncs/cmip5/sam/c5_uas/mod_umax.txt',\
	names=['date','ind','rno','wspd']) # read in
	modmaxspd.rno = modmaxspd.rno - 1 # make the model 'labels' start at 1.
	modmaxspd.date = modmaxspd.date.apply(lambda d: np.datetime64( datetime( parse(d).year, parse(d).month, 1 ) ) )
	modmaxspd = modmaxspd.pivot(index='date',columns='rno',values='wspd')
        store['modmaxspd'] = modmaxspd


	modlocmax = pd.read_csv('/ra40/data/ncs/cmip5/sam/c5_uas/mod_uloc.txt',\
	names=['date','ind','rno','pos']) # read in
	modlocmax.date = modlocmax.date.apply(lambda d: np.datetime64( datetime( parse(d).year, parse(d).month, 1 ) ) )
	modlocmax.rno = modlocmax.rno - 1 # make the model 'labels' start at 1.
	modlocmax = modlocmax.pivot(index='date',columns='rno',values='pos')
        store['modlocmax'] = modlocmax

	modwidth = pd.read_csv('/ra40/data/ncs/cmip5/sam/c5_uas/mod_uwidth.txt',\
	names=['date','ind','rno','width']) # read in
	modwidth.date = modwidth.date.apply(lambda d: np.datetime64( datetime( parse(d).year, parse(d).month, 1 ) ) )
	modwidth.rno = modwidth.rno - 1 # make the model 'labels' start at 1.
	modwidth = modwidth.pivot(index='date',columns='rno',values='width')
        store['modwidth'] = modwidth
        
        store.close()

	print "finished reading files"
	
def load_sam_df():
        
	# Load Pandas dataframes from HDF5
	print "readfiles"
        store = pd.HDFStore('sam_analysis.h5')

	# Reanalyses
	press  = store['press'] 
        maxspd = store['maxspd']
        locmax = store['locmax']
	width  = store['width'] 


	# Models
	modpress  = store['modpress'] 
        modmaxspd = store['modmaxspd'] 
        modlocmax = store['modlocmax'] 
        modwidth  = store['modwidth']   
        store.close()
	print "finished reading files"

        return press, maxspd, locmax, width, modpress, modmaxspd, modlocmax, modwidth
        
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	