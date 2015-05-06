#To get CFSR data from NCAR

# First authenticate
curl -c rda_cookies -d "email=ncswart@uvic.ca&passwd=letneilin&action=login" https://rda.ucar.edu/cgi-bin/login

# try to get the data

# SLP and uflx

curl -b rda_cookies -d "dsid=ds093.2&rtype=S&rinfo=dsnum=093.2;startdate=1979-01-01 00:00;enddate=2010-12-31 00:00;parameters=3%2160-1.2-1:0.3.1,3%217-0.2-1:0.3.1,3%217-0.2-1:0.2.17,3%2160-1.2-1:0.2.17,3%217-4.2-1:0.2.17;product=595;grid_definition=4;ofmt=netCDF" http://rda.ucar.edu/php/dsrqst.php

# uwind
curl -b rda_cookies -d "dsid=ds093.2&rtype=S&rinfo=dsnum=093.2;startdate=1979-01-01 00:00;enddate=2010-12-31 00:00;parameters=3%217-0.2-1:0.2.2,3%2160-1.2-1:0.2.2;grid_definition=4;level=223;product=900;ofmt=netCDF" http://rda.ucar.edu/php/dsrqst.php

