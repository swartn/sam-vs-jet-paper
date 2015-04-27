#!/bin/bash

if [ 1==1 ] ;then
    rm *.nc
    rm mod_list.txt
    for i in `ls -d -1 /rd40/data/CMIP5/historical/psl/**` ; do
	echo $i | cut -d'/' -f7 >> mod_list.txt
	list=`ls $i/r1i1p1/`

	for j in $list; do
	    cdo zonmean $i/r1i1p1/$j ./zonmean_$j
	done
    done

    rm mod_rcp_list.txt
    for i in `ls -d -1 /rd40/data/CMIP5/rcp45/psl/**` ; do
	echo $i | cut -d'/' -f7 >> mod_rcp_list.txt
	list=`ls $i/r1i1p1/`

	for j in $list; do
	    cdo zonmean $i/r1i1p1/$j ./zonmean_$j
	done
    done
# Do some cleaning up
cdo -seldate,1871-01-01,2005-12-31 zonmean_psl_Amon_bcc-csm1-1_historical_r1i1p1_185001-201212.nc zonmean_psl_Amon_bcc-csm1-1_historical_r1i1p1_185001-200512.nc
rm -f zonmean_psl_Amon_bcc-csm1-1_historical_r1i1p1_185001-201212.nc

cdo -seldate,1871-01-01,2005-12-31 zonmean_psl_Amon_bcc-csm1-1-m_historical_r1i1p1_185001-201212.nc zonmean_psl_Amon_bcc-csm1-1-m_historical_r1i1p1_185001-200512.nc
rm -f zonmean_psl_Amon_bcc-csm1-1-m_historical_r1i1p1_185001-201212.nc

cdo -seldate,2001-01-01,2005-12-31 zonmean_psl_Amon_GISS-E2-R-CC_historical_r1i1p1_200101-201012.nc zonmean_psl_Amon_GISS-E2-R-CC_historical_r1i1p1_200101-200512.nc
rm -f zonmean_psl_Amon_GISS-E2-R-CC_historical_r1i1p1_200101-201012.nc

cdo -seldate,1951-01-01,2005-12-31 zonmean_psl_Amon_GISS-E2-H-CC_historical_r1i1p1_195101-201012.nc zonmean_psl_Amon_GISS-E2-H-CC_historical_r1i1p1_195101-200512.nc 
rm -f zonmean_psl_Amon_GISS-E2-H-CC_historical_r1i1p1_195101-201012.nc 

cdo -seldate,1871-01-01,2005-12-31 zonmean_psl_Amon_MIROC5_historical_r1i1p1_185001-201212.nc zonmean_psl_Amon_MIROC5_historical_r1i1p1_185001-200512.nc
rm -f zonmean_psl_Amon_MIROC5_historical_r1i1p1_185001-201212.nc

rm -f zonmean_psl_Amon_HadGEM2-AO_rcp45_r1i1p1_200601-209912.nc

fi


rm -f zonmean_psl_Amon_*_historical_1871_2013.nc

for i in `cat mod_rcp_list.txt`; do
mod_time_secs=`ls zonmean_psl_Amon_$i\_*.nc`
#echo $mod_time_secs
cdo cat $mod_time_secs tmp1.nc 
cdo -seldate,1871-01-01,2013-12-31 -remapdis,r1x180 -selvar,psl tmp1.nc zonmean_psl_Amon_$i\_historical_1871_2013.nc
rm -f tmp1.nc
echo ' '
echo ' '
mod_time_secs=''
done

# clean a bit
rm -f zonmean_psl_Amon_CanCM4_historical_1871_2013.nc
rm -f zonmean_psl_Amon_FGOALS-g2_historical_1871_2013.nc
rm -f zonmean_psl_Amon_MIROC4h_historical_1871_2013.nc
rm -f zonmean_psl_Amon_CESM1-WACCM_historical_1871_2013.nc

# compute ensemble means
rm -f ens*
cdo -ensmean `cat list_match_uas`  ensmean_zonmean_psl_Amon_historical_1871_2013.nc
cdo ensstd `cat list_match_uas`  ensstd_zonmean_psl_Amon_historical_1871_2013.nc

# for i in zonmean_psl_Amon_*_historical_1871_2005.nc; do echo $i ; ncdump -h $i | grep currently; done

