""" Retrieve slp, uwnd and uflx data for ERA-Int using the ecmwfapi.
    
    NOTE: credentials are required in: 
    
        $HOME/.ecmwfapirc

    See:    

        https://software.ecmwf.int/wiki/display/WEBAPI/Access+ECMWF+Public+Datasets

.. moduleauthor:: Neil Swart <neil.swart@ec.gc.ca>
"""
import os
import glob
import pandas as pd
import cdo; cdo = cdo.Cdo()
from ecmwfapi import ECMWFDataServer
import mv_to_dest

def fetch_era_data(variable_dict):
    """ Download data from ECMWF

        Parameters:
        -----------
        param_dic : dict
          A dictionary defining the download, eg:   
           {"class": "ei",
            "dataset": "interim",
            "date": '19790101/19790201/19790301',
            "grid": "0.75/0.75",
            "levtype": "sfc",
            "param": '165.128',
            "stream": "moda",
            "target": 'ERA-Int_slp.mon.mean.nc',
            "type": "an",
            "format": "netcdf"
            }
            
            See ('https://software.ecmwf.int/wiki/display/WEBAPI/' +
                'Accessing+ECMWF+data+servers+in+batch')

        Returns:
        --------
      
          Downloads files to PWD.
    """
    server = ECMWFDataServer()
    server.retrieve(variable_dict)

def get_era_int_data(destination='.'):
    # Generate the date ranges
    dates = pd.date_range('1979-01-01', '2012-12-01', freq='MS')
    date_string = [str(d.year) + str( "%02d" % d.month) + 
                   str( "%02d" % d.day) for d in dates]
    date_string = '/'.join(date_string)

    outfilename = 'ERA-Int_{var}.mon.mean.nc'
    
    # The names and parameter codes, and other details for variables
    variables = {'uflx' : {'param' : '229.128', 'type' : 'fc'},
                 #'u10m' : {'param' : '165.128'},
                 #'slp' :  {'param' :'151.128'},
                 'land' : {'param' : '172.128', 'date' : '1989-01-01'}
                }
    
    variable_dict = {"class": "ei",
                     "dataset": "interim",
                     "date": '19790101/19790201/19790301',
                     "grid": "0.75/0.75",
                     "levtype": "sfc",
                     "param": '165.128',
                     "stream": "moda",
                     "target": 'ERA-Int_slp.mon.mean.nc',
                     "type": "an",
                     "format": "netcdf"
                     }
    
    # for each variable assign the dates and alter required fields
    for key, pdict in variables.iteritems():
        vdict = variable_dict
        vdict['date'] = date_string
        vdict['target'] = outfilename.format(var=key)
        for key2, val in pdict.iteritems():
            vdict[key2] = val

        # fetch the data
        fetch_era_data(vdict)   
        
        # Change variable names
        old_names = {'uflx' : 'iews', 'u10m' : 'u10', 'slp' : 'msl',
                      'land' : 'lsm'}
        cdo.chname(old_names[key] + ',' + key, input=outfilename.format(var=key),
                   output='tmp.nc')
        os.remove(outfilename.format(var=key))
        os.rename('tmp.nc', outfilename.format(var=key))
        
    # Land mask wind stress
    #instr = ('-selvar,uflx ERA-Int_uflx.mon.mean.nc -setctomiss,2 -addc,1 ERA-Int_land.mon.mean.nc')
    #cdo.mul(input=instr, output='tmp_uflx.nc')
    #os.rename('tmp_uflx.nc', 'ERA-Int_uflx.mon.mean.nc')
    
    # move to destination
    files = glob.glob('ERA-Int*.mon.mean.nc')
    mv_to_dest.mv_to_dest(destination, *files)   

if __name__ == '__main__':
    get_era_int_data(destination='../data/')



