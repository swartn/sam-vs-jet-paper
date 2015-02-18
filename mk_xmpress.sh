#!/bin/bash

if [0] ;then
    rm mod_list.txt
    for i in `ls -d -1 /rd40/data/CMIP5/historical/psl/**` ; do
	echo $i | cut -d'/' -f7 >> mod_list.txt
	list=`ls $i/r1i1p1/`

	for j in $list; do
	    cdo zonmean $i/r1i1p1/$j ./zonmean_$j
	done
    done
fi

rm -f zonmean_psl_Amon_*_historical_1871_2005.nc

for i in `cat mod_list.txt`; do
mod_time_secs=`ls zonmean_psl_Amon_$i\_historical*.nc`
#echo $mod_time_secs
cdo cat $mod_time_secs tmp1.nc 
cdo -seldate,1871-01-01,2005-12-31 -remapdis,r1x180 -selvar,psl tmp1.nc zonmean_psl_Amon_$i\_historical_1871_2005.nc
rm -f tmp1.nc
echo ' '
echo ' '
mod_time_secs=''
done

cdo -ensmean zonmean_psl_Amon_*_historical_1871_2005.nc  zonmean_psl_Amon_ENSMEAN_historical_1871_2005.nc
cdo ensstd zonmean_psl_Amon_*_historical_1871_2005.nc  zonmean_psl_Amon_ENSSTD_historical_1871_2005.nc

# for i in zonmean_psl_Amon_*_historical_1871_2005.nc; do echo $i ; ncdump -h $i | grep currently; done

