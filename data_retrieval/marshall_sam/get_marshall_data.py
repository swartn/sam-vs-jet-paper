""" Create a csv file containing the SLP averaged at the Marshall stations
    at 40 and 65S, and compute the SAM from these.
    
    The SLP data averaged over the six stations at each latitude bands, and in the 
    .dat files, was provided by Gareth Marshall (British Antarctic Survey). This 
    data was the basis for calculating the SAM index in Marshall (2003). See
    
        http://www.nerc-bas.ac.uk/icd/gjma/sam.html
        
.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import pandas as pd
import pandas_tools as pt
import numpy as np
import matplotlib.pyplot as plt
import os

def get_marshall_data(destination='./')
    # data is contained in .dat files here and just needs some processing
    
    #load the data into pandas
    slp40 = pd.read_fwf('l40.1957.2015.monmslp.dat', widths=[5,2,7],
    		        names=['y','m','slp40'], usecols=['slp40'], 
                        na_values=[-999.9])
    slp65 = pd.read_fwf('l65.1957.2015.monmslp.dat', widths=[5,2,7], 
                        names=['y', 'm', 'slp65'], na_values=[-999.9],
                        usecols=['slp65'])

    # join the data from 40 and 65S into a single DF
    df = pd.concat([slp40, slp65], axis=1)
    #df[df<-500] = np.nan

    # setup the dates and purge missing values
    dates = pd.date_range('1957-01-01','2015-12-31', freq='MS')
    df.index = dates
    df = df.dropna()
    # Compute the SAM index (non-normalized)
    df = df.convert_objects(convert_numeric=True)
    df['sam'] = df.slp40 - df.slp65

    # Save the output to destination
    dest = os.path.join(destination, 'marshall_sam.csv') 
    df.to_csv(dest)

if __name__ == '__main__':
    get_marshall_data(destination='../data/')