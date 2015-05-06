#! /bin/csh -f
#
# c-shell script to download selected files from rda.ucar.edu using Wget
# NOTE: if you want to run under a different shell, make sure you change
#       the 'set' commands according to your shell's syntax
# after you save the file, don't forget to make it executable
#   i.e. - "chmod 755 <name_of_script>"
#
# Experienced Wget Users: add additional command-line flags here
#   Use the -r (--recursive) option with care
#   Do NOT use the -b (--background) option - simultaneous file downloads
#       can cause your data access to be blocked
set opts = "-N"
#
# Replace "xxxxxx" with your password
# IMPORTANT NOTE:  If your password uses a special character that has special
#                  meaning to csh, you should escape it with a backslash
#                  Example:  set passwd = "my\!password"
set passwd = 'xxxxxx'
set num_chars = `echo "$passwd" |awk '{print length($0)}'`
if ($num_chars == 0) then
  echo "You need to set your password before you can continue"
  echo "  see the documentation in the script"
  exit
endif
@ num = 1
set newpass = ""
while ($num <= $num_chars)
  set c = `echo "$passwd" |cut -b{$num}-{$num}`
  if ("$c" == "&") then
    set c = "%26";
  else
    if ("$c" == "?") then
      set c = "%3F"
    else
      if ("$c" == "=") then
        set c = "%3D"
      endif
    endif
  endif
  set newpass = "$newpass$c"
  @ num ++
end
set passwd = "$newpass"
#
set cert_opt = ""
# If you get a certificate verification error (version 1.10 or higher),
# uncomment the following line:
#set cert_opt = "--no-check-certificate"
#
if ("$passwd" == "xxxxxx") then
  echo "You need to set your password before you can continue"
  echo "  see the documentation in the script"
  exit
endif
#
# authenticate - NOTE: You should only execute this command ONE TIME.
# Executing this command for every data file you download may cause
# your download privileges to be suspended.
wget $cert_opt -O auth_status.rda.ucar.edu --save-cookies auth.rda.ucar.edu.$$ --post-data="email=ncswart@uvic.ca&passwd=$passwd&action=login" https://rda.ucar.edu/cgi-bin/login
#
# download the file(s)
# NOTE:  if you get 403 Forbidden errors when downloading the data files, check
#        the contents of the file 'auth_status.rda.ucar.edu'
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19870701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19870801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19870901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19871001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19871101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19871201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19880101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19880201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19880301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19880401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19880501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19880601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19880701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19880801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19880901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19881001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19881101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19881201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19890101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19890201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19890301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19890401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19890501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19890601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19890701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19890801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19890901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19891001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19891101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19891201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19900101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19900201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19900301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19900401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19900501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19900601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19900701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19900801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19900901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19901001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19901101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19901201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19910101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19910201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19910301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19910401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19910501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19910601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19910701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19910801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19910901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19911001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19911101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19911201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19920101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19920201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19920301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19920401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19920501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19920601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19920701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19920801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19920901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19921001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19921101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19921201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19930101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19930201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19930301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19930401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19930501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19930601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19930701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19930801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19930901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19931001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19931101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19931201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19940101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19940201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19940301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19940401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19940501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19940601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19940701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19940801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19940901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19941001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19941101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19941201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19950101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19950201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19950301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19950401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19950501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19950601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19950701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19950801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19950901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19951001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19951101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19951201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19960101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19960201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19960301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19960401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19960501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19960601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19960701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19960801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19960901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19961001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19961101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19961201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19970101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19970201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19970301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19970401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19970501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19970601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19970701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19970801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19970901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19971001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19971101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19971201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19980101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19980201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19980301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19980401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19980501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19980601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19980701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19980801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19980901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19981001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19981101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19981201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19990101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19990201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19990301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19990401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19990501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19990601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19990701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19990801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19990901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19991001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19991101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_19991201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20000101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20000201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20000301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20000401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20000501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20000601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20000701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20000801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20000901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20001001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20001101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20001201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20010101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20010201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20010301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20010401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20010501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20010601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20010701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20010801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20010901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20011001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20011101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20011201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20020101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20020201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20020301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20020401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20020501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20020601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20020701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20020801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20020901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20021001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20021101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20021201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20030101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20030201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20030301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20030401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20030501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20030601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20030701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20030801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20030901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20031001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20031101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20031201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20040101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20040201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20040301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20040401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20040501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20040601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20040701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20040801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20040901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20041001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20041101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20041201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20050101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20050201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20050301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20050401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20050501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20050601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20050701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20050801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20050901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20051001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20051101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20051201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20060101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20060201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20060301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20060401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20060501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20060601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20060701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20060801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20060901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20061001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20061101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20061201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20070101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20070201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20070301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20070401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20070501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20070601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20070701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20070801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20070901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20071001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20071101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20071201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20080101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20080201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20080301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20080401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20080501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20080601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20080701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20080801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20080901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20081001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20081101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20081201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20090101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20090201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20090301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20090401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20090501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20090601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20090701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20090801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20090901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20091001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20091101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20091201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20100101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20100201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20100301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20100401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20100501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20100601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20100701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20100801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20100901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20101001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20101101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20101201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20110101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20110201_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20110301_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20110401_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20110501_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20110601_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20110701_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20110801_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20110901_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20111001_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20111101_v11l35flk.nc.gz
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ http://rda.ucar.edu/data/ds744.9/L35a_Monthly/month_20111201_v11l35flk.nc.gz
#
# clean up
rm auth.rda.ucar.edu.$$ auth_status.rda.ucar.edu

