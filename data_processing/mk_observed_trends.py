"""
Computes trends for the 20CR ensemble slp and u10 and for CCMP.

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import os
import glob
import cdo; cdo = cdo.Cdo()


def save_observed_trends(filen, start_date, end_date, datapath):
    """Compute reanalysis trends and save to HDF5
    """
    cdo_str = ('-seldate,' + start_date + ',' + end_date + ' ' + filen)
    cdo.trend(input=cdo_str, output="int.nc " + "slope_" + filen)        
    os.remove('int.nc')

def mk_observed_trends(datapath='./'):
    # where we are starting from
    cwd = os.getcwd()
    # move to where the data is
    os.chdir(datapath)

        
    # do slp
    save_observed_trends('20CR_ens_slp.mon.mean.nc', start_date='1979-01-01',
                           end_date='2004-12-31', datapath=datapath)
    
    save_observed_trends('20CR_ens_slp.mon.mean.nc', start_date='1951-01-01',
                           end_date='2004-12-31', datapath=datapath)


    # do u10m
    save_observed_trends('20CR_ens_u10m.mon.mean.nc', 
                         start_date='1951-01-01', end_date='2011-12-31', 
                         datapath=datapath)

    save_observed_trends('CCMP_198701-201112.nc', 
                         start_date='1988-01-01', end_date='2011-12-31', 
                         datapath=datapath)

    # move back
    os.chdir(cwd)

if __name__ == '__main__':
    mk_observed_trends(datapath='../data_retrieval/data/')

