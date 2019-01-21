#!/bin/bash
#  Description: METEOROLOGIAL MODULE OF the MARCS MODEL 
#  Experiment: SINGLE CATCHMENT
#  17.01.2019
#  Code Owner: FMI, Elena Shevnina
#  ph. +358449185446
#  e-mail:eshevnina@gmail.com

# Define the paths to the Working directory (WD), file with the RCMs historical run (CS) and projections (CSP)
# all input datafile are netCDF, with lat 0..360 and they contain monthly air temperatures and precipitation
# RCMs runs contain a preciputation expressed in kg sec-1m-2  

WD='/home/shevnina/Manuscripts/2019/UnivGeosc/support_data/'
WDU='/home/shevnina/Manuscripts/2019/UnivGeosc/support_data/tst/'

# to set the path to the observed climatology 
RefC='/home/shevnina/DCW/Meteo_history/'
infile_pre_ho=$RefC'precip.mon.total.v401.nc'

#And to calculate the precipitation in [mm] from the precipitation_flux [kg m-2 s-1]and to obtaine the yearly values of precipitation in [mm]
cdo mulc,10 $infile_pre_ho $WDU'pre_mm_ho.nc'
cdo yearsum $WDU'pre_mm_ho.nc' $WDU'pre_year_mm_ho.nc'
cdo selyear,1951,1952,1953,1954,1955,1956,1957,1958,1959,1960,1961,1962,1963,1964,1965,1966,1967,1968,1969,1970,1971,1972,1973,1974,1975,1976,1977,1978,1979,1980,1981,1982,1983,1984,1985,1986,1987,1988,1989,1990 $WDU'pre_year_mm_ho.nc' $WDU'pre5190_mm_ho.nc'
cdo timmean $WDU'pre5190_mm_ho.nc' $WDU'pre5190mean_ho.nc'

rm $WDU'pre_year_mm_ho.nc'
rm $WDU'pre_year_mm_ho.nc'
rm $WDU'pre_mm_ho.nc'

cdo sellonlatbox,21,31,60,71 $WDU'pre5190mean_ho.nc' $WDU'pre_year180_mm_ho.nc'
cdo outputtab,lat,lon,value $WDU'pre_year180_mm_ho.nc' > $WDU'pre_obs5090.txt'

rm $WDU'pre_year_mm_ho.nc' $WDU'pre_year180_mm_ho.nc'

# to set the paths to RCM4 model runs
CS='/home/shevnina/DCW/CORDEX/RCM4_SMHI/europe/hist/'
CP26='/home/shevnina/DCW/CORDEX/RCM4_SMHI/europe/rcp26/'
CP45='/home/shevnina/DCW/CORDEX/RCM4_SMHI/europe/rcp45/'
CP85='/home/shevnina/DCW/CORDEX/RCM4_SMHI/europe/rcp85/'

# To extract annual precipitation amount for the reference period of 1951-1990  
# RCM4 regional model MPI-ESM-LM historical run
cdo mergetime $CS'pr_EUR-44i_MPI-M-MPI-ESM-LR_historical_r1i1p1_SMHI-RCA4_v1_mon_195101-196012.nc' $CS'pr_EUR-44i_MPI-M-MPI-ESM-LR_historical_r1i1p1_SMHI-RCA4_v1_mon_196101-197012.nc' $WDU'tmp_5160.nc'
cdo mergetime $WDU'tmp_5160.nc' $CS'pr_EUR-44i_MPI-M-MPI-ESM-LR_historical_r1i1p1_SMHI-RCA4_v1_mon_197101-198012.nc' $WDU'tmp_5170.nc'
cdo mergetime $WDU'tmp_5170.nc' $CS'pr_EUR-44i_MPI-M-MPI-ESM-LR_historical_r1i1p1_SMHI-RCA4_v1_mon_197101-198012.nc' $WDU'tmp_5180.nc'
cdo mergetime $WDU'tmp_5180.nc' $CS'pr_EUR-44i_MPI-M-MPI-ESM-LR_historical_r1i1p1_SMHI-RCA4_v1_mon_198101-199012.nc' $WDU'pre5190_hm.nc'
cdo mulc,2592000 $WDU'pre5190_hm.nc' $WDU'pre5190_mm_hm.nc'
cdo yearsum $WDU'pre5190_mm_hm.nc' $WDU'pre5190year_hm.nc'
cdo timmean $WDU'pre5190year_hm.nc' $WDU'pre5190mean_hm.nc'
cdo sellonlatbox,21,31,60,71 $WDU'pre5190mean_hm.nc' $WDU'pre_year180_mm_hm.nc'
cdo outputtab,lat,lon,value $WDU'pre_year180_mm_hm.nc' > $WDU'pre_5190hist.txt'
rm $WDU*.nc

# To extract annual precipitation amount for the projected period 2020-2050
# To merge the periods, then to conver precipitation flux to mm
# to calculate yearly values sum of precipitation, and to calculate the mean precipitation over the period 
# to select box covering the territory of Finland
# RCM4 regional model MPI-ESM-LM RCP26 run
cdo mergetime $CP26'pr_EUR-44i_MPI-M-MPI-ESM-LR_rcp26_r1i1p1_SMHI-RCA4_v1_mon_202101-203012.nc' $CP26'pr_EUR-44i_MPI-M-MPI-ESM-LR_rcp26_r1i1p1_SMHI-RCA4_v1_mon_203101-204012.nc' $WDU'tmp2130.nc'
cdo mergetime $WDU'tmp2130.nc' $CP26'pr_EUR-44i_MPI-M-MPI-ESM-LR_rcp26_r1i1p1_SMHI-RCA4_v1_mon_204101-205012.nc' $WDU'pre2150_pr26.nc'
cdo mulc,2592000 $WDU'pre2150_pr26.nc' $WDU'pre_mm_pr26.nc'
cdo yearsum $WDU'pre_mm_pr26.nc' $WDU'pre_year_mm_pr26.nc'
cdo timmean $WDU'pre_year_mm_pr26.nc' $WDU'pre2150mean_pr26.nc'
cdo sellonlatbox,21,31,60,71 $WDU'pre2150mean_pr26.nc' $WDU'pre_year180_mm_pr26.nc'
cdo outputtab,lat,lon,year,value $WDU'pre_year180_mm_pr26.nc' > $WDU'pre_mod26.txt'
rm $WDU*.nc

# RCM4 regional model MPI-ESM-LM RCP45 run
cdo mergetime $CP45'pr_EUR-44i_MPI-M-MPI-ESM-LR_rcp45_r1i1p1_SMHI-RCA4_v1_mon_202101-203012.nc' $CP45'pr_EUR-44i_MPI-M-MPI-ESM-LR_rcp45_r1i1p1_SMHI-RCA4_v1_mon_203101-204012.nc' $WDU'tmp2130.nc'
cdo mergetime $WDU'tmp2130.nc' $CP45'pr_EUR-44i_MPI-M-MPI-ESM-LR_rcp45_r1i1p1_SMHI-RCA4_v1_mon_204101-205012.nc' $WDU'pre2150_pr45.nc'
cdo mulc,2592000 $WDU'pre2150_pr45.nc' $WDU'pre_mm_pr45.nc'
cdo yearsum $WDU'pre_mm_pr45.nc' $WDU'pre_year_mm_pr45.nc'
cdo timmean $WDU'pre_year_mm_pr45.nc' $WDU'pre2150mean_pr45.nc'
cdo sellonlatbox,21,31,60,71 $WDU'pre2150mean_pr45.nc' $WDU'pre_year180_mm_pr45.nc'
cdo outputtab,lat,lon,year,value $WDU'pre_year180_mm_pr45.nc' > $WDU'pre_mod45.txt'
rm $WDU*.nc

# RCM4 regional model MPI-ESM-LM RCP85 run
cdo mergetime $CP85'pr_EUR-44i_MPI-M-MPI-ESM-LR_rcp85_r1i1p1_SMHI-RCA4_v1_mon_202101-203012.nc' $CP85'pr_EUR-44i_MPI-M-MPI-ESM-LR_rcp85_r1i1p1_SMHI-RCA4_v1_mon_203101-204012.nc' $WDU'tmp2130.nc'
cdo mergetime $WDU'tmp2130.nc' $CP85'pr_EUR-44i_MPI-M-MPI-ESM-LR_rcp85_r1i1p1_SMHI-RCA4_v1_mon_204101-205012.nc' $WDU'pre2150_pr85.nc'
cdo mulc,2592000 $WDU'pre2150_pr85.nc' $WDU'pre_mm_pr85.nc'
cdo yearsum $WDU'pre_mm_pr85.nc' $WDU'pre_year_mm_pr85.nc'
cdo timmean $WDU'pre_year_mm_pr85.nc' $WDU'pre2150mean_pr85.nc'
cdo sellonlatbox,21,31,60,71 $WDU'pre2150mean_pr85.nc' $WDU'pre_year180_mm_pr85.nc'
cdo outputtab,lat,lon,year,value $WDU'pre_year180_mm_pr85.nc' > $WDU'pre_mod85.txt'
rm $WDU*.nc
