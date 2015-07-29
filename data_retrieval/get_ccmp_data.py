import urllib
import os

def get_ccmp_data(destination='./'):

    base_url = 'ftp://podaac-ftp.jpl.nasa.gov/allData/ccmp/L3.5a/monthly/flk/'

    for year in range(1987, 2011):
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
        

    # time join the data
    files = glob.glob('month_*_v11l35flk.nc')
    subprocess.Popen(['cdo', 'mergetime', ' '.join(files),
                      'CCMP_198701-201112.nc']).wait()

    # cleanup
    for f in files:
        os.remove(f) 

    # move to destination
    mv_to_dest.mv_to_dest(destination, 'CCMP_198701-201112.nc')

if __name__=='__main__':
    get_ccmp_data('../data/')


