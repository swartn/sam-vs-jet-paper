""" Create a csv file containing the SLP averaged at the Marshall stations
    at 40 and 65S, and compute the non-normalized SAM from these and save to csv.
    
    The SLP data averaged over the six stations at each latitude band 
    is provided by Gareth Marshall (British Antarctic Survey). This 
    data was the basis for calculating the SAM index in Marshall (2003). See
    
        http://www.nerc-bas.ac.uk/icd/gjma/sam.html
        
.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def get_marshall_data(destination):
    
    # The data resides at
    base_url = 'http://www.nerc-bas.ac.uk/public/icd/gjma/'

    # Load the 40S data and make into a linear series with datetimeindex
    slp40 = pd.read_csv(base_url + 'l40.1957.2007.txt', sep=' ', skiprows=1, 
                       header=None, index_col=0, skipinitialspace=True)
    slp40 = slp40.stack()
    year = slp40.index.get_level_values(0).values
    month = slp40.index.get_level_values(1).values
    slp40.index = pd.PeriodIndex(year=year, month=month, freq='M')

    # Load the 65s data and make into a linear series with datetimeindex
    slp65 = pd.read_csv(base_url + 'l65.1957.2007.txt', sep=' ', skiprows=1, 
                       header=None, index_col=0, skipinitialspace=True)
    slp65 = slp65.stack()
    year = slp65.index.get_level_values(0).values
    month = slp65.index.get_level_values(1).values
    slp65.index = pd.PeriodIndex(year=year, month=month, freq='M')

    # join the data from 40 and 65S into a single DF
    df = pd.concat([slp40, slp65], axis=1)
    df.columns = ['slp40', 'slp65']
    #df[df<-500] = np.nan

    df = df.dropna()
    # Compute the SAM index (non-normalized)
    df = df.convert_objects(convert_numeric=True)
    df['sam'] = df.slp40 - df.slp65

    # Save the output to destination
    dest = os.path.join(destination, 'marshall_sam.csv') 
    df.to_csv(dest)

if __name__ == '__main__':
    get_marshall_data(destination='./data/')