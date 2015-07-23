import urllib
import os
base_url = 'ftp://podaac-ftp.jpl.nasa.gov/allData/ccmp/L3.5a/monthly/flk/'

for year in range(1987, 2012):

    url = base_url + str( year ) + '/'
    #print url
    for month in range(1,13):
            mnth = str( month ) if month > 9 else '0' + str(month)         
            filen = 'month_' + str( year ) + mnth  + '01_v11l35flk.nc.gz'
            guz = 'gunzip ' + filen

            #print filen
            if year > 1987:
                urllib.urlretrieve( url + filen , filen)
            elif month > 6:
                urllib.urlretrieve( url + filen , filen)
    

os.system( 'gunzip *.gz' )
os.system( 'cdo cat month*.nc ccmp_month_join.nc' )
os.system( 'rm -f month*.nc' )
